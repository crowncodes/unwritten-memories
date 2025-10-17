import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';
import { LifebondContext } from '../context/contextTypes';
import { assembleContextStep, dedupeByPromptHashStep, evaluateStep, telemetryStep, validateStep } from '../steps/sharedSteps';
import { validateDialogueContent } from '../validators/content';
import { DialogueInputSchema, DialogueOutputSchema } from '../schemas';
import { retrieveSnippets, ingestToNeo4j, ingestToVectorStore } from '../rag';

const GOOGLE_GENAI_API_KEY = defineSecret('GOOGLE_GENAI_API_KEY');

const ai = genkit({ plugins: [googleAI()] });

export const dialogueFlow = ai.defineFlow(
  {
    name: 'generateDialogue',
    inputSchema: DialogueInputSchema,
    outputSchema: DialogueOutputSchema,
  },
  async (input, runtime) => {
    const ctx = (runtime.context || {}) as LifebondContext;

    await assembleContextStep(input, ctx);
    const snippets = await retrieveSnippets({ cardId: input.card_id, topK: 5 });
    ctx.retrieval = { ...(ctx.retrieval || {}), topK: 5, snippets };
    const { prompt, promptHash } = await dedupeByPromptHashStep({ prompt: input.prompt }, ctx);

    const isPremium = (ctx.routing?.thinkingEnabled ?? false) || ctx.routing?.tier === 'premium';
    const modelName = isPremium ? 'gemini-2.0-flash-thinking-exp' : (ctx.routing?.model || 'gemini-2.0-flash-exp');

    // Build many-shot exemplars block for premium without leaking metadata
    let finalPrompt = prompt;
    if (isPremium && ctx.retrieval?.snippets?.length) {
      const exemplars = ctx.retrieval.snippets
        .map((s, i) => `Example ${i + 1}:\n${s.text}`)
        .join('\n\n')
        .slice(0, 6000); // guard size
      const directives = [
        'Think through how this line impacts the character emotions and capacity.',
        'Internally self-verify continuity and avoid contradictions; do not reveal your reasoning.',
        'Return only the final in-character dialogue (no analysis).',
      ].join('\n- ');
      finalPrompt = `You are writing a single in-character response.\n\nExemplars:\n---\n${exemplars}\n---\n\nTask:\n${prompt}\n\nConstraints:\n- ${directives}`;
    }

    const start = Date.now();
    const gen = await ai.generate({
      model: googleAI.model(modelName),
      prompt: finalPrompt,
      // Telemetry attributes can be attached via context side-channel
      context: ctx,
    });
    const text = gen.text;
    const duration = Date.now() - start;

    await validateStep(z.string().min(1))(text, ctx);
    const quality = validateDialogueContent(text);
    if (!quality.ok) {
      // Non-blocking: record messages; future policy could reject
      console.warn('dialogue_quality', quality);
    }
    await telemetryStep({ operation: 'dialogue.generate', durationMs: duration, model: ctx.routing?.model, tier: ctx.routing?.tier }, ctx);
    const evalFeedback = await evaluateStep({ outputText: text, prompt }, ctx);
    if (evalFeedback.suggestions?.length) {
      ctx.promptHints = { ...(ctx.promptHints || {}), suggestions: evalFeedback.suggestions };
    }

    // Optional self-critique (premium): ask for a compact assessment to improve future prompts
    if (isPremium) {
      const critique = await ai.generate({
        model: googleAI.model('gemini-2.0-flash-thinking-exp'),
        prompt: `Rate (0.0-1.0) how well this reply fits capacity/emotion continuity and list up to 2 targeted improvements.\nReply JSON: {"score": number, "suggestions": string[]}\n\nReply: ${JSON.stringify(text).slice(0, 6000)}`,
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
      } catch {
        // ignore parse errors
      }
    }

    await ingestToVectorStore({
      id: `${input.card_id}_${input.interaction_id}`,
      content: text,
      type: 'dialogue',
      promptHash,
      metadata: { card_id: input.card_id, interaction_id: input.interaction_id },
    });
    await ingestToNeo4j({
      id: `${input.card_id}_${input.interaction_id}`,
      content: text,
      type: 'dialogue',
      promptHash,
      metadata: { card_id: input.card_id, interaction_id: input.interaction_id },
    });

    return {
      text,
      model: ctx.routing?.model || 'gemini-2.0-flash-exp',
      modelVersion: 'na',
      version: '1.0',
      tier: isPremium ? 'premium' : (ctx.routing?.tier || 'free'),
      prompt_hash: promptHash,
      generation_time_ms: duration,
    };
  }
);

export const generateDialogue = onCallGenkit({ secrets: [GOOGLE_GENAI_API_KEY] }, dialogueFlow);


