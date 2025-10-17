import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';
import { LifebondContext } from '../context/contextTypes';
import { retrieveSnippets, ingestToNeo4j, ingestToVectorStore } from '../rag';
import { assembleContextStep, dedupeByPromptHashStep, telemetryStep } from '../steps/sharedSteps';
import { SpecialistInputSchema, DirectorBriefSchema } from '../writers_room/schemas';
import { pacingSpecialist } from '../writers_room/specialists/pacing';
import { narrativeArcSpecialist } from '../writers_room/specialists/narrative_arc';
import { characterStateSpecialist } from '../writers_room/specialists/character_state';
import { criticSpecialist } from '../writers_room/specialists/critic';
import { synthesizeDirectorBrief } from '../writers_room/director';
import { cacheGet, cacheSet } from '../writers_room/cache';

const GOOGLE_GENAI_API_KEY = defineSecret('GOOGLE_GENAI_API_KEY');
const ai = genkit({ plugins: [googleAI()] });

export const WritersRoomInputSchema = z.object({
  specialistContext: SpecialistInputSchema,
});

export const WritersRoomOutputSchema = z.object({
  brief: DirectorBriefSchema,
  prompt_hash: z.string(),
  tier: z.string().default('free'),
  generation_time_ms: z.number(),
});

export const writersRoomOrchestrator = ai.defineFlow(
  {
    name: 'generateWritersRoomEvent',
    inputSchema: WritersRoomInputSchema,
    outputSchema: WritersRoomOutputSchema,
  },
  async (input, runtime) => {
    const ctx = (runtime.context || {}) as LifebondContext;
    await assembleContextStep(input, ctx);

    // Enrich retrieval
    const snippets = await retrieveSnippets({ tags: input.specialistContext.retrievalTags, topK: 5 });
    ctx.retrieval = { ...(ctx.retrieval || {}), topK: 5, snippets };

    const promptRaw = `WritersRoom ${JSON.stringify({ ctxHints: { tier: ctx.routing?.tier, act: input.specialistContext.arcPosition?.currentAct }, tags: input.specialistContext.retrievalTags })}`;
    const { promptHash } = await dedupeByPromptHashStep({ prompt: promptRaw }, ctx);

    const start = Date.now();

    // Simple memoization per context hash
    const cacheKey = `wr:${promptHash}`;
    const cached = cacheGet<ReturnType<typeof DirectorBriefSchema.parse>>(cacheKey);
    if (cached) {
      return { brief: cached as any, prompt_hash: promptHash, tier: ctx.routing?.tier || 'free', generation_time_ms: 0 };
    }

    // Specialists in parallel
    const [pacing, arc, character, critic] = await Promise.all([
      pacingSpecialist(input.specialistContext, { context: ctx }),
      narrativeArcSpecialist(input.specialistContext, { context: ctx }),
      characterStateSpecialist(input.specialistContext, { context: ctx }),
      criticSpecialist(input.specialistContext, { context: ctx }),
    ]);

    const brief = await synthesizeDirectorBrief({ pacing, arc, character, critic }, ctx);

    // Premium: optional iterative refinement (lightweight — ask critic for notes and re-synthesize)
    if (ctx.routing?.tier === 'premium') {
      // Reuse critic to add a nudge; in a full version, feed back into specialists.
      // Here we simply keep the first brief for latency reasons.
    }

    const duration = Date.now() - start;
    await telemetryStep({ operation: 'writersroom.generate', durationMs: duration, model: ctx.routing?.model, tier: ctx.routing?.tier }, ctx);

    // Persist for RAG continuity
    await ingestToVectorStore({ id: `wr_${promptHash}`, content: JSON.stringify(brief), type: 'other', promptHash, metadata: { tags: input.specialistContext.retrievalTags } });
    await ingestToNeo4j({ id: `wr_${promptHash}`, content: JSON.stringify(brief), type: 'other', promptHash, metadata: { tags: input.specialistContext.retrievalTags } });

    cacheSet(cacheKey, brief, 10 * 60 * 1000);
    return { brief, prompt_hash: promptHash, tier: ctx.routing?.tier || 'free', generation_time_ms: duration };
  }
);

export const generateWritersRoomEvent = onCallGenkit({ secrets: [GOOGLE_GENAI_API_KEY] }, writersRoomOrchestrator);


