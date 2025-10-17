import { genkit, z } from "genkit";
import { googleAI } from "@genkit-ai/google-genai";
import { onCallGenkit } from "firebase-functions/https";
import { defineSecret } from "firebase-functions/params";
import admin from "firebase-admin";
import { retrieveSnippets, ingestToNeo4j, ingestToVectorStore } from "./rag";

// Initialize Firebase Admin SDK once per instance
if (!admin.apps.length) {
  admin.initializeApp();
}

// Secret for Google AI (Gemini/Imagen) API key in production
const GOOGLE_GENAI_API_KEY = defineSecret("GOOGLE_GENAI_API_KEY");

// Initialize Genkit with Google AI plugin
export const ai = genkit({
  plugins: [googleAI()],
});

// ============================================================================
// Greeter Flow (example)
// ============================================================================

export const getPersonalizedGreetingFlow = ai.defineFlow(
  {
    name: "getPersonalizedGreeting",
    inputSchema: z.object({ uid: z.string() }),
    outputSchema: z.string(),
  },
  async ({ uid }) => {
    try {
      const snap = await admin.firestore().collection("users").doc(uid).get();
      const data = snap.data() as { name?: string } | undefined;
      const userName = snap.exists && data?.name ? data.name : "friend";

      const result = await ai.generate({
        model: googleAI.model("gemini-2.0-flash-exp"),
        prompt: `Generate a short, friendly greeting for ${userName}.` ,
      });

      return result.text;
    } catch (error) {
      console.error("Error in getPersonalizedGreeting flow:", error);
      throw new Error("Failed to generate greeting.");
    }
  }
);

export const getPersonalizedGreeting = onCallGenkit({
  secrets: [GOOGLE_GENAI_API_KEY],
}, getPersonalizedGreetingFlow);

// ============================================================================
// Location Image Generation Flow
// ============================================================================

const CameraAnchorSchema = z.object({
  angle: z.string().describe('Camera angle, e.g., "45-degree corner view"'),
  distance: z.string().describe('Distance from subject, e.g., "30 feet"'),
  height: z.string().describe('Camera height, e.g., "eye level 5.5 feet"'),
  framing: z.string().describe('Frame composition, e.g., "full building facade with 10% street context"'),
});

const LocationSchema = z.object({
  location_id: z.string(),
  canonical_base_prompt: z.string().describe("The fixed base description of the location"),
  camera_anchor: CameraAnchorSchema,
  consistency_keywords: z.array(z.string()).describe("Keywords that must appear in every generation"),
  signature_elements: z.array(z.string()).describe("Defining features of the location"),
});

const GameContextSchema = z.object({
  turn_time: z.enum(["morning", "afternoon", "evening"]).describe("Time of day"),
  season: z.enum(["spring", "summer", "fall", "winter"]).describe("Current season"),
  player_capacity: z.number().min(0).max(10).describe("Player emotional capacity (0-10)"),
  active_tension: z.enum(["mystery_hook", "partial_reveal", "contradiction", "stakes_escalation", "neutral"]).optional().describe("Current narrative tension type"),
  relationship_level: z.number().min(0).max(5).optional().describe("NPC relationship level (0-5)"),
  associated_npc: z.string().optional().describe("Associated NPC identifier"),
});

const LocationImageInputSchema = z.object({
  location: LocationSchema,
  game_context: GameContextSchema,
});

function getTimeLayer(turnTime: "morning" | "afternoon" | "evening"): string {
  const timeModifiers: Record<string, string> = {
    morning: "Soft golden morning light, long shadows stretching east to west, dew on windows, gentle warm glow, pastel sky tones, low sun angle creating dimensional depth.",
    afternoon: "Bright overhead lighting, shorter shadows, vibrant colors at peak saturation, clear sky or scattered clouds, high-contrast definition, full illumination.",
    evening: "Warm interior lights glowing through windows contrasting with cool blue exterior dusk, amber streetlights beginning to illuminate, gradient sky (orange to deep blue), atmospheric twilight mood, inviting warmth radiating outward.",
  };
  return timeModifiers[turnTime] || "";
}

function getSeasonLayer(season: "spring" | "summer" | "fall" | "winter"): string {
  const seasonModifiers: Record<string, string> = {
    spring: "Fresh green foliage emerging, flower boxes with early blooms, rain-cleaned surfaces, soft diffused light through clouds, puddles reflecting sky, renewed textures.",
    summer: "Lush full foliage, vibrant saturated colors, strong sunlight, outdoor seating populated, heat shimmer on pavement, long days extending golden hour, doors open to interior.",
    fall: "Warm amber and rust foliage, fallen leaves scattered on pavement, rich golden light, slightly overcast skies, cozy atmosphere, transition toward shorter days.",
    winter: "Bare tree branches, frost on windows, warm interior glow contrasting cold exterior, muted color palette, possible snow accumulation on ledges, condensation on glass, inviting warmth emphasized.",
  };
  return seasonModifiers[season] || "";
}

function getEmotionalLayer(playerCapacity: number): string {
  if (playerCapacity >= 8) {
    return "Crisp details, vibrant colors, inviting warmth, clear atmospheric perspective, welcoming ambiance, emphasize positive architectural features, slight glow to warm lights, optimistic color grading.";
  } else if (playerCapacity >= 5) {
    return "Balanced neutral tone, realistic color saturation, even lighting distribution, comfortable but not idealized, authentic texture representation, grounded atmosphere.";
  } else if (playerCapacity >= 2) {
    return "Slightly muted colors, cooler color temperature shift, emphasized shadows, more contrast between light/dark areas, subtle desaturation, heavier atmospheric weight, details remain clear but mood shifts toward melancholy.";
  } else {
    return "Desaturated palette, heavy shadows dominating, cool blue-gray tones, oppressive atmosphere, windows appear less inviting, emphasize isolation, stark contrast, location feels distant or unreachable, foreboding mood.";
  }
}

function getTensionLayer(activeTension?: "mystery_hook" | "partial_reveal" | "contradiction" | "stakes_escalation" | "neutral"): string {
  const tensionModifiers: Record<string, string> = {
    mystery_hook: "Partially obscured details (figure in window, unfamiliar car parked outside), something slightly off in the scene (door ajar when usually closed), atmospheric fog or rain obscuring clarity, sense of anticipation, one element that raises questions.",
    partial_reveal: "Visual evidence of unseen events (new sign, missing familiar element, unexpected change), hint of activity but no clear explanation, viewer positioned as observer discovering clues, subtle before/after markers.",
    contradiction: "Unexpected visual state (closed when usually open, crowded when usually empty), lighting or atmosphere counter to expected time/season, visual dissonance creating intrigue, something fundamental has shifted.",
    stakes_escalation: "Heightened dramatic lighting (storm clouds gathering, urgent golden hour), visual time pressure cues (moving van, closing soon sign), intensity in atmospheric rendering, sense of impending change or decision, dynamic weather elements.",
    neutral: "Clean, authentic representation, no narrative cues added, location exists in natural state, focus on beauty and welcoming atmosphere, daily life rhythm visible.",
  };
  return (activeTension && tensionModifiers[activeTension]) || tensionModifiers.neutral;
}

function getRelationshipLayer(relationshipLevel?: number): string {
  if (relationshipLevel === undefined || relationshipLevel === null) return "";
  const relationshipModifiers: Record<number, string> = {
    0: "Exterior view only or public interior spaces, observed from distance, no personal details visible, generic welcoming atmosphere, professional/public presentation.",
    1: "Exterior view only or public interior spaces, observed from distance, no personal details visible, generic welcoming atmosphere, professional/public presentation.",
    2: "Interior glimpse showing general layout, some personality hints (decor style, color choices), inviting but not intimate, comfortable viewing angle, public spaces emphasized.",
    3: "Familiar angles, personal touches visible (photos on wall, specific furniture choices), warm lighting emphasizing comfort, viewer positioned as welcome guest, details that suggest repeated visits.",
    4: "Intimate details visible (personal items, lived-in authenticity), viewer positioned as regular presence, imperfections showing comfort (coffee mug left out, book open on table), warm emotional atmosphere, private spaces partially visible.",
    5: "Deeply personal perspective, full interior access, cherished details emphasized (photo of you and NPC, gift you gave them displayed), maximum emotional warmth, location rendered as sanctuary, your presence felt in the space.",
  };
  return relationshipModifiers[relationshipLevel] || "";
}

function getTechnicalSpecs(cameraAnchor: z.infer<typeof CameraAnchorSchema>): string {
  return `Painterly digital art style with photorealistic foundation. ${cameraAnchor.angle} from street level, ${cameraAnchor.distance} from entrance, ${cameraAnchor.height} height, ${cameraAnchor.framing}. 16:9 aspect ratio. Rule of thirds composition with primary architectural feature as focal point. 3-layer depth: foreground (street pavement detail), mid-ground (location building), background (adjacent buildings and sky). Single primary light source with soft ambient fill. High detail, consistent quality, optimized for 512x512 or 768x768 resolution.`;
}

function assembleLocationPrompt(
  location: z.infer<typeof LocationSchema>,
  gameContext: z.infer<typeof GameContextSchema>
): string {
  const parts = [
    location.canonical_base_prompt,
    getTimeLayer(gameContext.turn_time),
    getSeasonLayer(gameContext.season),
    getEmotionalLayer(gameContext.player_capacity),
    getTensionLayer(gameContext.active_tension as any),
    getRelationshipLayer(gameContext.relationship_level),
    getTechnicalSpecs(location.camera_anchor),
  ];
  return parts.filter(Boolean).join("\n\n");
}

export const generateLocationImageFlow = ai.defineFlow(
  {
    name: "generateLocationImage",
    inputSchema: LocationImageInputSchema,
    outputSchema: z.object({
      prompt: z.string().describe("The assembled prompt for image generation"),
      metadata: z.object({
        location_id: z.string(),
        turn_time: z.string(),
        season: z.string(),
        player_capacity: z.number(),
        active_tension: z.string().optional(),
        relationship_level: z.number().optional(),
      }),
    }),
  },
  async ({ location, game_context }) => {
    try {
      const prompt = assembleLocationPrompt(location, game_context);
      console.log(`Generating prompt for location: ${location.location_id}`);
      return {
        prompt,
        metadata: {
          location_id: location.location_id,
          turn_time: game_context.turn_time,
          season: game_context.season,
          player_capacity: game_context.player_capacity,
          active_tension: game_context.active_tension,
          relationship_level: game_context.relationship_level,
        },
      };
    } catch (error) {
      console.error("Error in generateLocationImage flow:", error);
      throw new Error("Failed to generate location image prompt.");
    }
  }
);

export const generateLocationImage = onCallGenkit({
  secrets: [GOOGLE_GENAI_API_KEY],
}, generateLocationImageFlow);

// ============================================================================
// Generate Location Image with Imagen/Gemini
// ============================================================================

export const generateLocationImageWithImagenFlow = ai.defineFlow(
  {
    name: "generateLocationImageWithImagen",
    inputSchema: z.object({
      prompt: z.string().optional().describe("Pre-assembled prompt for image generation"),
      location: LocationSchema.optional(),
      game_context: GameContextSchema.optional(),
      tier: z.enum(["free", "premium"]).default("free").describe('Generation tier: "free" uses Gemini 2.x image, "premium" uses Imagen 3.x'),
    }),
    outputSchema: z.object({
      image: z.object({
        url: z.string().describe("Base64-encoded image data URL or remote URL"),
        contentType: z.string().describe("MIME type of the image"),
      }),
      prompt: z.string().describe("The prompt used for generation"),
      metadata: z.object({
        schemaVersion: z.string().default('1.0'),
        version: z.string().default('1.0'),
        prompt_hash: z.string(),
        location_id: z.string().optional(),
        turn_time: z.string().optional(),
        season: z.string().optional(),
        player_capacity: z.number().optional(),
        active_tension: z.string().optional(),
        relationship_level: z.number().optional(),
        generation_time_ms: z.number(),
        tier: z.string(),
        model: z.string(),
      }),
    }),
  },
  async ({ prompt, location, game_context, tier = "free" }) => {
    try {
      const start = Date.now();
      let finalPrompt = prompt;
      let meta: any = {};

      if (!finalPrompt && location && game_context) {
        const res = await generateLocationImageFlow({ location, game_context });
        finalPrompt = res.prompt;
        meta = res.metadata;
      } else if (!finalPrompt) {
        throw new Error("Either prompt or (location + game_context) must be provided");
      }

      const modelName = tier === "premium" ? "imagen-3.0-generate-002" : "gemini-2.5-flash-image";

      // Premium: add many-shot exemplars to strengthen consistency
      if (tier === 'premium') {
        const exemplars = await retrieveSnippets({ locationId: meta?.location_id, topK: 5 });
        if (exemplars.length) {
          const block = exemplars.map((s, i) => `Exemplar ${i + 1}:\n${s.text}`).join('\n\n').slice(0, 4000);
          finalPrompt = `Exemplars:\n---\n${block}\n---\n\nTask:\n${finalPrompt}`;
        }
      }

      // Configs are model-specific; keep minimal for compatibility
      const config: Record<string, unknown> = tier === "premium"
        ? { numberOfImages: 1, aspectRatio: "16:9" }
        : {};

      const raw: any = await ai.generate({
        model: googleAI.model(modelName),
        prompt: finalPrompt!,
        config,
      });

      // Try to find media in several plausible locations
      const tryFindMedia = (obj: any): any | null => {
        if (!obj) return null;
        const content = obj.message?.content || obj.output?.message?.content || obj.output?.content || obj.content;
        if (Array.isArray(content)) {
          const mediaPart = content.find((p: any) => p?.media);
          if (mediaPart?.media) return mediaPart.media;
        }
        if (obj.media) return obj.media;
        return null;
      };

      const media = tryFindMedia(raw);
      if (!media) {
        console.error("Unexpected image response structure:", JSON.stringify(raw, null, 2));
        throw new Error("No image media returned by the model");
      }

      const end = Date.now();
      const promptHash = require('node:crypto').createHash('sha256').update(finalPrompt!).digest('hex').slice(0, 16);
      // Premium: quick post-check to suggest missing signature elements
      if (tier === 'premium' && location) {
        const checklist = location.signature_elements || [];
        const checkPrompt = `Given the image prompt below and this checklist, list any missing items.\nReply JSON: {"missing": string[]}\n\nChecklist: ${JSON.stringify(checklist)}\n\nPrompt: ${JSON.stringify(finalPrompt).slice(0, 4000)}`;
        try {
          const critique = await ai.generate({ model: googleAI.model('gemini-2.0-flash-thinking-exp'), prompt: checkPrompt });
          // Suggestions can be stored via evaluators/promptHints as needed
          critique.text;
        } catch {}
      }

      // Post-ingestion for RAG/graph
      await ingestToVectorStore({ id: meta?.location_id ? `loc_${meta.location_id}_${promptHash}` : `loc_${promptHash}` , content: finalPrompt!, type: 'image', promptHash, metadata: { location_id: meta?.location_id } });
      await ingestToNeo4j({ id: meta?.location_id ? `loc_${meta.location_id}_${promptHash}` : `loc_${promptHash}` , content: finalPrompt!, type: 'image', promptHash, metadata: { location_id: meta?.location_id } });
      return {
        image: {
          url: media.url,
          contentType: media.contentType || "image/png",
        },
        prompt: finalPrompt!,
        metadata: {
          schemaVersion: '1.0',
          version: '1.0',
          prompt_hash: promptHash,
          ...meta,
          generation_time_ms: end - start,
          tier,
          model: modelName,
        },
      };
    } catch (error: any) {
      console.error("Error in generateLocationImageWithImagen flow:", error);
      throw new Error(`Failed to generate image: ${error?.message || String(error)}`);
    }
  }
);

export const generateLocationImageWithImagen = onCallGenkit({
  secrets: [GOOGLE_GENAI_API_KEY],
}, generateLocationImageWithImagenFlow);


