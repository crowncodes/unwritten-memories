import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { LifebondContext } from '../../context/contextTypes';
import { SpecialistInputSchema, ArcRecSchema } from '../schemas';

const ai = genkit({ plugins: [googleAI()] });

function buildPrompt(input: typeof SpecialistInputSchema._type): string {
  return [
    `You are the Narrative Arc Specialist (Plot Keeper). Output ONLY JSON {recommendation, beatsNeeded, rationale}.`,
    `Follow 3-act structure. Current act: ${input.arcPosition?.currentAct ?? 'unknown'}.`,
    `Season week: ${input.seasonWeek ?? 'n/a'}.`,
    `Recent events: ${JSON.stringify(input.recentEvents).slice(0, 2000)}.`,
    `Choose one recommendation: ESTABLISH_STAKES | GENERATE_COMPLICATION | TRIGGER_DECISIVE_MOMENT | RESOLVE_AND_REFLECT.`,
    `List concise beatsNeeded (e.g., setback, breakthrough).`,
  ].join(' ');
}

export const narrativeArcSpecialist = ai.defineFlow(
  {
    name: 'narrativeArcSpecialist',
    inputSchema: SpecialistInputSchema,
    outputSchema: ArcRecSchema,
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
    return ArcRecSchema.parse(JSON.parse(gen.text || '{}'));
  }
);


