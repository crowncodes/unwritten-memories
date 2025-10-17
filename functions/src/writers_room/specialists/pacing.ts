import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { LifebondContext } from '../../context/contextTypes';
import { SpecialistInputSchema, PacingRecSchema, TensionLevelSchema } from '../schemas';

const ai = genkit({ plugins: [googleAI()] });

function buildPrompt(input: typeof SpecialistInputSchema._type): string {
  const levels = TensionLevelSchema.options.join(' | ');
  return [
    `You are the Pacing Specialist (Dramaturg). Output ONLY JSON matching schema {recommendation, targetTension, rationale}.`,
    `Tension scale: ${levels}.`,
    `Recent events: ${JSON.stringify(input.recentEvents).slice(0, 2000)}.`,
    `Pacing history: ${JSON.stringify(input.pacingHistory)}.`,
    `Active states: ${JSON.stringify(input.activeStates)}.`,
    `Player capacity: ${input.player.capacity}.`,
    `If tension has been high for days, recommend PROVIDE_RESPITE; if flat, INJECT_INTRIGUE; if building toward climax, MAINTAIN_ESCALATION.`,
    `Return compact JSON.`,
  ].join(' ');
}

export const pacingSpecialist = ai.defineFlow(
  {
    name: 'pacingSpecialist',
    inputSchema: SpecialistInputSchema,
    outputSchema: PacingRecSchema,
  },
  async (input, runtime) => {
    const ctx = (runtime.context || {}) as LifebondContext;
    const model = (ctx.routing?.tier === 'premium') ? 'gemini-2.0-flash-thinking-exp' : (ctx.routing?.model || 'gemini-2.0-flash-exp');
    const gen = await ai.generate({
      model: googleAI.model(model),
      prompt: buildPrompt(input),
      context: ctx,
      config: { responseMimeType: 'application/json' },
    });
    const parsed = JSON.parse(gen.text || '{}');
    return PacingRecSchema.parse(parsed);
  }
);


