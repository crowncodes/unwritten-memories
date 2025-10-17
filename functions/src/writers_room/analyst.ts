import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { LifebondContext } from '../context/contextTypes';
import { AnalystMetadataSchema, DirectorBriefSchema } from './schemas';

const ai = genkit({ plugins: [googleAI()] });

export interface AnalystInput {
  brief: typeof DirectorBriefSchema._type;
  outcome?: { choice?: string; resultText?: string };
}

function buildPrompt(input: AnalystInput): string {
  return [
    `You are the Narrative Analyst (Post-Mortem). Output ONLY JSON matching AnalystMetadataSchema.`,
    `Attach themes, character arc notes, symbolic elements, relationship dynamics, callbacks, future_query_tags.`,
    `Brief: ${JSON.stringify(input.brief).slice(0, 8000)}`,
    input.outcome?.resultText ? `Outcome: ${input.outcome.resultText.slice(0, 2000)}` : '',
  ].filter(Boolean).join('\n');
}

export async function annotateEvent(input: AnalystInput, ctx: LifebondContext) {
  const model = (ctx.routing?.tier === 'premium') ? 'gemini-2.0-flash-thinking-exp' : (ctx.routing?.model || 'gemini-2.0-flash-exp');
  const gen = await ai.generate({
    model: googleAI.model(model),
    prompt: buildPrompt(input),
    context: ctx,
    config: { responseMimeType: 'application/json' },
  });
  return AnalystMetadataSchema.parse(JSON.parse(gen.text || '{}'));
}


