export interface RAGSnippet {
  id: string;
  text: string;
  score?: number;
  tags?: string[];
}

export interface RAGIngestRecord {
  id: string;
  content: string;
  type: 'dialogue' | 'image' | 'music' | 'other';
  promptHash?: string;
  metadata?: Record<string, unknown>;
}

export async function ingestToVectorStore(record: RAGIngestRecord): Promise<void> {
  const { indexRagDocumentFlow, IndexerInputSchema } = await import('../flows/rag_indexer.js');
  const input = IndexerInputSchema.parse({ id: record.id, text: record.content, tags: (record.metadata as any)?.tags || [] });
  await indexRagDocumentFlow(input);
}

export async function ingestToNeo4j(record: RAGIngestRecord): Promise<void> {
  // Minimal Event schema; extend with characters/locations/themes as needed
  const { runCypher } = await import('../writers_room/neo4j_client.js');
  const tags = Array.isArray((record.metadata as any)?.tags) ? (record.metadata as any).tags : [];
  const ts = Date.now();
  const query = `
    MERGE (e:Event {id: $id})
    ON CREATE SET e.createdAt = timestamp()
    SET e.type = $type, e.text = $text, e.promptHash = $promptHash, e.updatedAt = $updatedAt
    WITH e
    UNWIND $tags AS t
    MERGE (th:Theme {name: t})
    MERGE (e)-[:THEME]->(th)
    RETURN e.id as id
  `;
  await runCypher(query, { id: record.id, type: record.type, text: record.content, promptHash: record.promptHash || null, updatedAt: ts, tags });
}

export async function retrieveSnippets(query: { cardId?: string; locationId?: string; tags?: string[]; topK?: number; textQuery?: string }): Promise<RAGSnippet[]> {
  // TODO: Implement Firestore vector search. For now, try Neo4j theme filter when tags provided.
  if (query.tags && query.tags.length) {
    const { runCypher } = await import('../writers_room/neo4j_client.js');
    const res = await runCypher(
      `MATCH (e:Event)-[:THEME]->(th:Theme)
       WHERE th.name IN $tags
       RETURN e.id as id, e.text as text
       LIMIT $limit`,
      { tags: query.tags, limit: query.topK || 5 }
    );
    return (res as any[]).map((r: any) => ({ id: r.id, text: r.text }));
  }
  if (query.textQuery) {
    const { retrieveRagSnippetsFlow, RetrieverInputSchema } = await import('../flows/rag_retriever.js');
    const res = await retrieveRagSnippetsFlow(RetrieverInputSchema.parse({ query: query.textQuery, topK: query.topK || 5, tags: query.tags }));
    return res.items.map((i: any) => ({ id: i.id, text: i.text, score: i.score, tags: i.tags }));
  }
  return [];
}




