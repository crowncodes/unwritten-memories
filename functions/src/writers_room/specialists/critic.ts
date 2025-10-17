import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { LifebondContext } from '../../context/contextTypes';
import { SpecialistInputSchema, CriticRecSchema } from '../schemas';

const ai = genkit({ plugins: [googleAI()] });

function buildPrompt(input: typeof SpecialistInputSchema._type): string {
  return [
    `You are The Critic (Audience Voice). Output ONLY JSON {recommendation, notes}.`,
    `Assess repetitiveness, underused NPCs, surprise factor, emotional variety based on recentEvents and retrievalTags.`,
    `Choose one recommendation: INJECT_SURPRISE | ESCALATE_PERSONAL_STAKES | INTRODUCE_CONTRAST | ACTIVATE_DORMANT_RELATIONSHIP.`,
    `Keep notes concise (1-3 bullets).`,
    `Context: ${JSON.stringify({ recentEvents: input.recentEvents.slice(-5), retrievalTags: input.retrievalTags }).slice(0, 2000)}`,
  ].join(' ');
}

export const criticSpecialist = ai.defineFlow(
  {
    name: 'criticSpecialist',
    inputSchema: SpecialistInputSchema,
    outputSchema: CriticRecSchema,
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
    return CriticRecSchema.parse(JSON.parse(gen.text || '{}'));
  }
);


