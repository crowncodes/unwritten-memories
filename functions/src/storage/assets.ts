import admin from 'firebase-admin';

export function musicAssetPath(promptHash: string, index: number, format: 'opus' | 'wav'): string {
  const ext = format === 'opus' ? 'ogg' : 'wav';
  return `music/${promptHash}/stem_${index}.${ext}`;
}

export async function uploadDataUrlToStorage(path: string, dataUrl: string, contentType?: string): Promise<string> {
  const match = dataUrl.match(/^data:(.*?);base64,(.*)$/);
  if (!match) throw new Error('Invalid data URL');
  const [, mime, b64] = match;
  const buffer = Buffer.from(b64, 'base64');
  const bucket = admin.storage().bucket();
  const file = bucket.file(path);
  await file.save(buffer, { contentType: contentType || mime, resumable: false, public: false });
  return `gs://${bucket.name}/${path}`;
}




