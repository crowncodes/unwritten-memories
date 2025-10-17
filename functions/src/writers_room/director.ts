import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { LifebondContext } from '../context/contextTypes';
import { ArcRecSchema, CharacterRecSchema, CriticRecSchema, DirectorBriefSchema, PacingRecSchema } from './schemas';

const ai = genkit({ plugins: [googleAI()] });

export interface DirectorInput {
  pacing: typeof PacingRecSchema._type;
  arc: typeof ArcRecSchema._type;
  character: typeof CharacterRecSchema._type;
  critic: typeof CriticRecSchema._type;
}

function buildDirectorPrompt(input: DirectorInput): string {
  return [
    `You are the Narrative Director (Showrunner). Synthesize all four notes into ONE creative brief JSON matching schema DirectorBriefSchema.`,
    `Do not compromise—resolve conflicts creatively as per Writers Room docs.`,
    `Notes:`,
    `PACING: ${JSON.stringify(input.pacing)}`,
    `ARC: ${JSON.stringify(input.arc)}`,
    `CHARACTER: ${JSON.stringify(input.character)}`,
    `CRITIC: ${JSON.stringify(input.critic)}`,
    `Constraints:`,
    `- event_type must be a short classifier (e.g., ASPIRATION_MILESTONE_WITH_TWIST)`,
    `- choices_framework must present tradeoffs; no right answer`,
    `- capacity_impact should include immediate and net if applicable`,
    `Output only compact JSON.`,
  ].join('\n');
}

export async function synthesizeDirectorBrief(input: DirectorInput, ctx: LifebondContext) {
  const model = (ctx.routing?.tier === 'premium') ? 'gemini-2.0-flash-thinking-exp' : (ctx.routing?.model || 'gemini-2.0-flash-exp');
  const gen = await ai.generate({
    model: googleAI.model(model),
    prompt: buildDirectorPrompt(input),
    context: ctx,
    config: { responseMimeType: 'application/json' },
  });
  return DirectorBriefSchema.parse(JSON.parse(gen.text || '{}'));
}


