import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import admin from 'firebase-admin';

const ai = genkit({ plugins: [googleAI()] });

export const RetrieverInputSchema = z.object({
  query: z.string(),
  topK: z.number().int().min(1).max(20).default(5),
  tags: z.array(z.string()).optional(),
});

export const RetrieverOutputSchema = z.object({
  items: z.array(z.object({ id: z.string(), text: z.string(), score: z.number().optional(), tags: z.array(z.string()).optional() })),
});

export const retrieveRagSnippetsFlow = ai.defineFlow(
  {
    name: 'retrieveRagSnippets',
    inputSchema: RetrieverInputSchema,
    outputSchema: RetrieverOutputSchema,
  },
  async (input) => {
    let queryVector: number[] | undefined;
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const embedder: any = (googleAI as any).embedder ? (googleAI as any).embedder('text-embedding-004') : null;
      if (embedder && (ai as any).embed) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const res: any = await (ai as any).embed({ model: embedder, content: input.query });
        queryVector = (res && (res.vector || res.embedding || res.output)) as number[] | undefined;
      }
    } catch {}

    const db = admin.firestore();
    if (!queryVector) {
      // Fallback: simple keyword search by tag/text (non-vector)
      let q = db.collection('rag_docs') as FirebaseFirestore.Query;
      if (input.tags && input.tags.length) {
        q = q.where('tags', 'array-contains-any', input.tags);
      }
      const snap = await q.limit(input.topK).get();
      return { items: snap.docs.map((d) => ({ id: d.id, text: (d.data() as any).text, tags: (d.data() as any).tags })) };
    }

    // Vector Search (requires Firestore vector search enabled & index configured)
    // @ts-expect-error Experimental vector query API placeholder
    const results = await (db as any).collection('rag_docs')
      .findNearest('embedding', queryVector, { limit: input.topK });

    const items = (results?.docs || []).map((d: any) => ({ id: d.id, text: d.data().text, score: d.distance, tags: d.data().tags }));
    return { items };
  }
);


