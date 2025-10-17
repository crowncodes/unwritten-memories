import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';
import { LifebondContext } from '../context/contextTypes';
import { assembleContextStep, dedupeByPromptHashStep, evaluateStep, telemetryStep } from '../steps/sharedSteps';
import { validateNumericalGrounding } from '../validators/grounding';
import { MSVSchema, MusicInputSchema, MusicOutputSchema } from '../schemas';
import { retrieveSnippets, ingestToNeo4j, ingestToVectorStore } from '../rag';

const GOOGLE_GENAI_API_KEY = defineSecret('GOOGLE_GENAI_API_KEY');

const ai = genkit({ plugins: [googleAI()] });


function buildMusicPrompt(msv: z.infer<typeof MSVSchema>): string {
  // Keep MSV in context; build concise generation text
  return `Generate loop-safe stems (8 bars, 4/4), Opus@48kHz. Describe instrumentation and roles matching: ` +
    `valence ${msv.affect.valence}, arousal ${msv.affect.arousal}, tension ${msv.affect.tension}, agency ${msv.affect.agency}; ` +
    `brightness ${msv.harmony.brightness}, consonance ${msv.harmony.consonance}; tempo ${msv.temporal.tempo}.`;
}

export const musicFlow = ai.defineFlow(
  {
    name: 'generateMusicStems',
    inputSchema: MusicInputSchema,
    outputSchema: MusicOutputSchema,
  },
  async (input, runtime) => {
    const ctx = (runtime.context || {}) as LifebondContext;
    await assembleContextStep(input, ctx);

    const basePrompt = buildMusicPrompt(input.msv);
    // Example grounding check hook (non-blocking)
    const grounding = validateNumericalGrounding({
      value: input.msv.affect.tension,
      base: 0.5,
      factors: [
        { name: 'consonanceModifier', value: Math.max(0.5, 1 - input.msv.harmony.consonance) },
        { name: 'regularityModifier', value: Math.max(0.5, 1 - input.msv.temporal.regularity) },
      ],
    });
    if (!grounding.ok) {
      runtime.log?.warn?.('music_grounding_mismatch', grounding);
    }
    const isPremium = ctx.routing?.tier === 'premium';
    let prompt = basePrompt;
    if (isPremium && ctx.retrieval?.snippets?.length) {
      const exemplars = ctx.retrieval.snippets
        .map((s, i) => `Exemplar ${i + 1}:\n${s.text}`)
        .join('\n\n')
        .slice(0, 6000);
      const constraints = [
        'Ensure 8-bar loop, bar-aligned loop points.',
        'Match MSV affect/harmony/temporal parameters; keep stems mixable.',
        'Return only the final, concise generation prompt (no analysis).',
      ].join('\n- ');
      prompt = `Design a single high-quality music generation prompt for stems.\n\nMSV summary:\n${JSON.stringify(input.msv)}\n\nExemplars:\n---\n${exemplars}\n---\n\nTask:\n${basePrompt}\n\nConstraints:\n- ${constraints}`;
    }
    const { promptHash } = await dedupeByPromptHashStep({ prompt }, ctx);

    // Pre-gen retrieval
    const snippets = await retrieveSnippets({ tags: ['music', input.cue_id || ''], topK: 5 });
    ctx.retrieval = { ...(ctx.retrieval || {}), topK: 5, snippets };
    const start = Date.now();
    // Prompting strategies: concise generation text, MSV details in context
    const gen = await ai.generate({
      model: googleAI.model(isPremium ? 'gemini-2.0-flash-thinking-exp' : (ctx.routing?.model || 'gemini-2.0-flash-exp')),
      prompt,
      context: { ...ctx, retrieval: { ...(ctx.retrieval || {}), snippets: [] } },
    });
    gen.text; // ensure resolved
    const duration = Date.now() - start;

    await telemetryStep({ operation: 'music.prompt', durationMs: duration, model: ctx.routing?.model, tier: ctx.routing?.tier }, ctx);
    await evaluateStep({ outputText: prompt, prompt }, ctx);
    if (isPremium) {
      const critique = await ai.generate({
        model: googleAI.model('gemini-2.0-flash-thinking-exp'),
        prompt: `Rate (0.0-1.0) how well this prompt reflects MSV and list up to 2 targeted improvements.\nReply JSON: {"score": number, "suggestions": string[]}\n\nPrompt: ${JSON.stringify(prompt).slice(0, 6000)}`,
        context: ctx,
      });
      try {
        const parsed = JSON.parse(critique.text || '{}');
        if (parsed?.suggestions?.length) {
          ctx.promptHints = { ...(ctx.promptHints || {}), suggestions: [
            ...(ctx.promptHints?.suggestions || []),
            ...parsed.suggestions,
          ] };
        }
      } catch {}
    }

    // Post-gen ingestion
    const id = input.cue_id || `msv_${promptHash}`;
    await ingestToVectorStore({ id, content: prompt, type: 'music', promptHash, metadata: { cue_id: input.cue_id } });
    await ingestToNeo4j({ id, content: prompt, type: 'music', promptHash, metadata: { cue_id: input.cue_id } });

    return {
      prompt,
      model: ctx.routing?.model || 'gemini-2.0-flash-exp',
      version: '1.0',
      tier: isPremium ? 'premium' : (ctx.routing?.tier || 'free'),
      prompt_hash: promptHash,
      generation_time_ms: duration,
    };
  }
);

export const generateMusicStems = onCallGenkit({ secrets: [GOOGLE_GENAI_API_KEY] }, musicFlow);


