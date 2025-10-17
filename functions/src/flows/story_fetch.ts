import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';
import { getSeasonStory } from '../db/story_repository';

const GOOGLE_GENAI_API_KEY = defineSecret('GOOGLE_GENAI_API_KEY');

const ai = genkit({ plugins: [googleAI()] });

export const storyFetchFlow = ai.defineFlow(
  {
    name: 'getSeasonStory',
    inputSchema: z.object({ season_id: z.string() }),
    outputSchema: z.any(),
  },
  async (input, runtime) => {
    const uid = (runtime.context as any)?.auth?.uid;
    const story = await getSeasonStory(uid, input.season_id);
    return story || {};
  }
);

export const getSeasonStoryCallable = onCallGenkit({ secrets: [GOOGLE_GENAI_API_KEY] }, storyFetchFlow);




