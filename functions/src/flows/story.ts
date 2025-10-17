import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';
import { LifebondContext } from '../context/contextTypes';
import { StoryInputSchema, StoryOutputSchema } from '../schemas';
import { assembleContextStep, dedupeByPromptHashStep, telemetryStep, evaluateStep } from '../steps/sharedSteps';
import { retrieveSnippets, ingestToNeo4j, ingestToVectorStore } from '../rag';
import { validateArcPlan, validateEventsPlan, validateWorld } from '../validators/story';
import { saveSeasonStory } from '../db/story_repository';
import { writersRoomOrchestrator, WritersRoomInputSchema } from './writers_room_event';

const GOOGLE_GENAI_API_KEY = defineSecret('GOOGLE_GENAI_API_KEY');

const ai = genkit({ plugins: [googleAI()] });

function buildSeedPrompt(seed: typeof StoryInputSchema._type['seed']): string {
  return [
    `Craft a season starting world and story scaffolding with rich but concise context.`,
    `Player chosen aspiration: ${seed.aspiration_id}.`,
    `Starting location: ${seed.start_location_id}.`,
    `Starting career: ${seed.start_career}.`,
    seed.backstory_hint ? `Backstory hint: ${seed.backstory_hint}.` : '',
    `Player OCEAN: O=${seed.player_profile.ocean.openness}, C=${seed.player_profile.ocean.conscientiousness}, E=${seed.player_profile.ocean.extraversion}, A=${seed.player_profile.ocean.agreeableness}, N=${seed.player_profile.ocean.neuroticism}.`,
    `Capacity: ${seed.player_profile.capacity}.`,
    `Season length (weeks): ${typeof seed.season_length_weeks === 'number' ? seed.season_length_weeks : Number(seed.season_length_weeks)}.`,
    `Output must align with: decisive decisions, 3-act scaffolding, base card catalog identities, card generation guidelines, event generation rules, tension hooks, stakes escalation, dramatic irony, and memory tracking.`,
    `Return only JSON with fields: world, arc_plan, events_plan, memory_seeds.`,
  ].filter(Boolean).join(' ');
}

export const storyFlow = ai.defineFlow(
  {
    name: 'buildSeasonStory',
    inputSchema: StoryInputSchema,
    outputSchema: StoryOutputSchema,
  },
  async (input, runtime) => {
    const ctx = (runtime.context || {}) as LifebondContext;
    await assembleContextStep(input, ctx);

    // Retrieve design exemplars to ground consistency (do not bloat prompt)
    const exemplars = await retrieveSnippets({ tags: ['story_specs', input.seed.aspiration_id], topK: 5 });
    ctx.retrieval = { ...(ctx.retrieval || {}), topK: 5, snippets: exemplars };

    const seedPrompt = buildSeedPrompt(input.seed as any);
    const directives = [
      'Follow 3-act arcs (Act1-Act2-Act3) per season length templates.',
      'Schedule at least 1 decisive decision window with foreshadowing weeks before.',
      'Keep world and backstory grounded and specific; no contradictions.',
      'Events plan should include early weeks variety and tension hooks every 2-3 weeks.',
      'Memory seeds should include 1-3 significant callbacks potential.',
      'Return compact JSON; no extra prose; field names must match schema.',
    ].join('\n- ');

    const enableThinking = (ctx.routing?.thinkingEnabled ?? false) || ctx.routing?.tier === 'premium';
    const modelName = enableThinking ? 'gemini-2.0-flash-thinking-exp' : (ctx.routing?.model || 'gemini-2.0-flash-exp');
    const finalPrompt = `${seedPrompt}\n\nConstraints:\n- ${directives}`;

    const { promptHash } = await dedupeByPromptHashStep({ prompt: finalPrompt }, ctx);
    const start = Date.now();

    const gen = await ai.generate({
      model: googleAI.model(modelName),
      prompt: finalPrompt,
      context: ctx,
      config: { responseMimeType: 'application/json' },
    });

    const duration = Date.now() - start;
    let parsed: any;
    try {
      parsed = JSON.parse(gen.text || '{}');
    } catch (e) {
      throw new Error('Story JSON parse failed');
    }

    await telemetryStep({ operation: 'story.build', durationMs: duration, model: modelName, tier: ctx.routing?.tier }, ctx);
    await evaluateStep({ outputText: gen.text || '', prompt: finalPrompt }, ctx);

    // Validate output structure and planning constraints
    const vWorld = validateWorld(parsed.world);
    const vArc = validateArcPlan(parsed.arc_plan);
    const vEvents = validateEventsPlan(parsed.events_plan, (input.seed.season_length_weeks as any) as number);
    const messages = [...vWorld.messages, ...vArc.messages, ...vEvents.messages];
    if (messages.length) {
      throw new Error(`Story validation failed: ${messages.join('; ')}`);
    }

    // Ingest prompts for RAG continuity
    await ingestToVectorStore({ id: `story_${promptHash}`, content: finalPrompt, type: 'other', promptHash, metadata: { aspiration: input.seed.aspiration_id } });
    await ingestToNeo4j({ id: `story_${promptHash}`, content: finalPrompt, type: 'other', promptHash, metadata: { aspiration: input.seed.aspiration_id } });

    const result = {
      world: parsed.world,
      arc_plan: parsed.arc_plan,
      events_plan: parsed.events_plan,
      memory_seeds: parsed.memory_seeds || [],
      model: modelName,
      modelVersion: 'na',
      version: '1.0',
      tier: ctx.routing?.tier || 'free',
      prompt_hash: promptHash,
      generation_time_ms: duration,
    };

    // Premium refinement pass (self-critique + light adjustments request)
    if (enableThinking) {
      const critique = await ai.generate({
        model: googleAI.model('gemini-2.0-flash-thinking-exp'),
        prompt: `Assess this story plan JSON for cohesion with 3-act, decisive decision placement, tension hooks every 2-3 weeks, and memory seeds quality. Reply JSON: {"score": number, "suggestions": string[]}.\n\n${JSON.stringify(result).slice(0, 12000)}`,
        context: ctx,
        config: { responseMimeType: 'application/json' },
      });
      try {
        const parsedCrit = JSON.parse(critique.text || '{}');
        if (parsedCrit?.suggestions?.length) {
          ctx.promptHints = { ...(ctx.promptHints || {}), suggestions: [
            ...(ctx.promptHints?.suggestions || []),
            ...parsedCrit.suggestions,
          ] };
        }
      } catch {}
    }

    // Optional: seed a decisive moment via Writers Room (feature-flagged)
    if (ctx.routing?.enableWritersRoom) {
      const wrInput = WritersRoomInputSchema.parse({
        specialistContext: {
          seasonWeek: 1,
          arcPosition: { currentAct: 1 },
          recentEvents: [],
          player: input.seed.player_profile,
          activeStates: [],
          pacingHistory: [],
          aspirationStatus: { id: input.seed.aspiration_id, progress: 0 },
          retrievalTags: ['story_specs', input.seed.aspiration_id],
        },
      });
      try {
        await writersRoomOrchestrator(wrInput, { context: ctx });
      } catch {}
    }

    // Persist
    const seasonId = `season_${(input.seed.season_length_weeks as any) as number}`;
    await saveSeasonStory(ctx.auth?.uid, seasonId, result as any);

    return result;
  }
);

export const buildSeasonStory = onCallGenkit({ secrets: [GOOGLE_GENAI_API_KEY] }, storyFlow);


