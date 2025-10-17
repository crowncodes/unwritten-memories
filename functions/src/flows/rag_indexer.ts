import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import admin from 'firebase-admin';

const ai = genkit({ plugins: [googleAI()] });

export const IndexerInputSchema = z.object({
  id: z.string().optional(),
  text: z.string(),
  tags: z.array(z.string()).default([]),
});

export const IndexerOutputSchema = z.object({ id: z.string() });

export const indexRagDocumentFlow = ai.defineFlow(
  {
    name: 'indexRagDocument',
    inputSchema: IndexerInputSchema,
    outputSchema: IndexerOutputSchema,
  },
  async (input) => {
    const id = input.id || `rag_${Date.now()}`;
    let vector: number[] | undefined;
    try {
      // Attempt embedding via Genkit Google AI plugin
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const embedder: any = (googleAI as any).embedder ? (googleAI as any).embedder('text-embedding-004') : null;
      if (embedder && (ai as any).embed) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const res: any = await (ai as any).embed({ model: embedder, content: input.text });
        vector = (res && (res.vector || res.embedding || res.output)) as number[] | undefined;
      }
    } catch {
      // Fallback: no embedding available; will store text only
    }

    const db = admin.firestore();
    const doc = {
      id,
      text: input.text,
      tags: input.tags,
      // Firestore Vector Search expects a float array field named consistently with the index
      ...(vector ? { embedding: vector } : {}),
      updatedAt: Date.now(),
    } as Record<string, unknown>;
    await db.collection('rag_docs').doc(id).set(doc, { merge: true });
    return { id };
  }
);


