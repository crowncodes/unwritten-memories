import admin from 'firebase-admin';

export interface MusicAssetDoc {
  prompt_hash: string;
  cue_id?: string;
  model: string;
  schemaVersion: string;
  version: string;
  tier?: string;
  stems: Array<{
    storage_path: string;
    content_type: string;
    index: number;
  }>;
  msv?: Record<string, unknown>;
  bars?: number;
  tempo?: number;
  sample_rate_hz?: number;
  created_at: number;
}

export async function writeMusicAsset(uid: string | undefined, doc: MusicAssetDoc): Promise<string> {
  const db = admin.firestore();
  const col = uid ? db.collection('users').doc(uid).collection('ai_outputs').doc('music').collection('assets') : db.collection('ai_public_assets');
  const ref = await col.add(doc);
  return ref.id;
}




