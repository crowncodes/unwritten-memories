import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';
import { LifebondContext } from '../context/contextTypes';
import { MSVSchema } from '../schemas';
import { assembleContextStep, dedupeByPromptHashStep, telemetryStep, evaluateStep } from '../steps/sharedSteps';
import { retrieveSnippets, ingestToNeo4j, ingestToVectorStore } from '../rag';
import { uploadDataUrlToStorage, musicAssetPath } from '../storage/assets';
import { writeMusicAsset } from '../db/music_metadata';
import { validateLoopAlignment } from '../validators/audio';

const GOOGLE_GENAI_API_KEY = defineSecret('GOOGLE_GENAI_API_KEY');

const ai = genkit({ plugins: [googleAI()] });

const LyriaInputSchema = z.object({
  msv: MSVSchema,
  cue_id: z.string().optional(),
  duration_bars: z.number().int().min(4).max(64).default(8),
  sample_rate_hz: z.number().int().default(48000),
  format: z.enum(['opus', 'wav']).default('opus'),
  schemaVersion: z.string().default('1.0'),
});

const AudioMediaSchema = z.object({
  url: z.string().describe('Base64 data URL or remote URL'),
  contentType: z.string().describe('audio content type, e.g., audio/ogg'),
});

const LyriaOutputSchema = z.object({
  audio: z.array(AudioMediaSchema).nonempty().describe('One or more stems or full mix'),
  prompt: z.string(),
  model: z.string(),
  modelVersion: z.string().optional(),
  version: z.string().default('1.0'),
  tier: z.string().default('free'),
  prompt_hash: z.string(),
  generation_time_ms: z.number(),
});

function buildLyriaPrompt(msv: z.infer<typeof MSVSchema>, bars: number, sampleRate: number, format: 'opus' | 'wav'): string {
  return [
    `Generate loop-safe instrumental music (${bars} bars, 4/4).`,
    `Target format ${format.toUpperCase()} @ ${sampleRate}Hz.`,
    `Affect: valence ${msv.affect.valence}, arousal ${msv.affect.arousal}, tension ${msv.affect.tension}, agency ${msv.affect.agency}.`,
    `Harmony: brightness ${msv.harmony.brightness}, consonance ${msv.harmony.consonance}, cadence ${msv.harmony.cadentialDrive}.`,
    `Temporal: tempo ${msv.temporal.tempo}, regularity ${msv.temporal.regularity}.`,
    `Orchestration: sparsity ${msv.orchestration.sparsity}.`,
    `Return stems that can mix into a cohesive loop.`,
  ].join(' ');
}

function tryFindMedia(obj: any): Array<{ url: string; contentType?: string }> {
  const results: Array<{ url: string; contentType?: string }> = [];
  const visit = (node: any) => {
    if (!node) return;
    if (node.media && node.media.url) {
      results.push({ url: node.media.url, contentType: node.media.contentType });
    }
    const content = node.message?.content || node.output?.message?.content || node.output?.content || node.content;
    if (Array.isArray(content)) {
      for (const p of content) {
        if (p?.media?.url) results.push({ url: p.media.url, contentType: p.media.contentType });
      }
    }
  };
  visit(obj);
  return results;
}

export const lyriaFlow = ai.defineFlow(
  {
    name: 'generateMusicWithLyria',
    inputSchema: LyriaInputSchema,
    outputSchema: LyriaOutputSchema,
  },
  async (input, runtime) => {
    const ctx = (runtime.context || {}) as LifebondContext;
    await assembleContextStep(input, ctx);

    // RAG exemplars (optional, do not bloat prompt)
    const exemplars = await retrieveSnippets({ tags: ['music', input.cue_id || ''], topK: 3 });
    const exemplarBlock = exemplars.length ? `\nExemplars:\n---\n${exemplars.map((s, i) => `Exemplar ${i + 1}:\n${s.text}`).join('\n\n').slice(0, 3000)}\n---` : '';

    const basePrompt = buildLyriaPrompt(input.msv, input.duration_bars, input.sample_rate_hz, input.format);
    const prompt = `${basePrompt}${exemplarBlock}`;
    const { promptHash } = await dedupeByPromptHashStep({ prompt }, ctx);

    const start = Date.now();
    // Choose Lyria-capable model if present in routing, otherwise a sane default placeholder
    const modelName = ctx.routing?.model || 'lyra-1.0-realtime';

    // Attempt generation; expect audio media in response
    const raw: any = await ai.generate({
      model: googleAI.model(modelName),
      prompt,
      // Some music endpoints may require config for audio; leave minimal and let plugin map
      config: { responseMimeType: input.format === 'opus' ? 'audio/ogg' : 'audio/wav' },
      context: ctx,
    });

    const media = tryFindMedia(raw);
    if (!media.length) {
      console.error('Unexpected Lyria response structure:', JSON.stringify(raw, null, 2));
      throw new Error('No audio media returned by the model');
    }
    const duration = Date.now() - start;

    await telemetryStep({ operation: 'music.lyria', durationMs: duration, model: modelName, tier: ctx.routing?.tier }, ctx);
    await evaluateStep({ outputText: prompt, prompt }, ctx);

    const id = input.cue_id || `msv_${promptHash}`;
    await ingestToVectorStore({ id, content: prompt, type: 'music', promptHash, metadata: { cue_id: input.cue_id, model: modelName } });
    await ingestToNeo4j({ id, content: prompt, type: 'music', promptHash, metadata: { cue_id: input.cue_id, model: modelName } });

    // Optional loop alignment validation when we have measured duration info (not provided by raw here)
    const loopCheck = validateLoopAlignment({ bars: input.duration_bars, tempoBpm: input.msv.temporal.tempo, sampleRateHz: input.sample_rate_hz });

    // Upload media data URLs to Storage when applicable
    const uploaded: Array<{ url: string; contentType: string }> = [];
    for (let i = 0; i < media.length; i++) {
      const m = media[i];
      const contentType = m.contentType || (input.format === 'opus' ? 'audio/ogg' : 'audio/wav');
      if (m.url.startsWith('data:')) {
        const path = musicAssetPath(promptHash, i, input.format);
        const gsUrl = await uploadDataUrlToStorage(path, m.url, contentType);
        uploaded.push({ url: gsUrl, contentType });
      } else {
        uploaded.push({ url: m.url, contentType });
      }
    }

    // Write metadata document
    await writeMusicAsset(ctx.auth?.uid, {
      prompt_hash: promptHash,
      cue_id: input.cue_id,
      model: modelName,
      schemaVersion: '1.0',
      version: '1.0',
      tier: ctx.routing?.tier,
      stems: uploaded.map((u, index) => ({ storage_path: u.url, content_type: u.contentType, index })),
      msv: input.msv as any,
      bars: input.duration_bars,
      tempo: input.msv.temporal.tempo,
      sample_rate_hz: input.sample_rate_hz,
      created_at: Date.now(),
    });

    return {
      audio: uploaded,
      prompt,
      model: modelName,
      modelVersion: 'na',
      version: '1.0',
      tier: ctx.routing?.tier || 'free',
      prompt_hash: promptHash,
      generation_time_ms: duration,
    };
  }
);

export const generateMusicWithLyria = onCallGenkit({ secrets: [GOOGLE_GENAI_API_KEY] }, lyriaFlow);


