import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { LifebondContext } from '../../context/contextTypes';
import { SpecialistInputSchema, CharacterRecSchema } from '../schemas';

const ai = genkit({ plugins: [googleAI()] });

function buildPrompt(input: typeof SpecialistInputSchema._type): string {
  return [
    `You are the Character State Specialist (Character Advocate). Output ONLY JSON {recommendation, constraints, rationale}.`,
    `Player capacity: ${input.player.capacity}. Active states: ${JSON.stringify(input.activeStates)}.`,
    `Rules: Capacity >= 7.0 → READY_FOR_CHALLENGE; 3.0-5.0 → PROTECT_FROM_CRISIS; < 3.0 → NEEDS_INTERVENTION; steady decline → NEEDS_A_WIN.`,
    `Add constraints like maxIntensity and lockTypes if relevant (e.g., lock high-stakes when fragile).`,
  ].join(' ');
}

export const characterStateSpecialist = ai.defineFlow(
  {
    name: 'characterStateSpecialist',
    inputSchema: SpecialistInputSchema,
    outputSchema: CharacterRecSchema,
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
    return CharacterRecSchema.parse(JSON.parse(gen.text || '{}'));
  }
);


