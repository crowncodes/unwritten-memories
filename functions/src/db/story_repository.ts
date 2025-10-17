import admin from 'firebase-admin';
import { StoryOutput } from '../schemas';

export async function saveSeasonStory(uid: string | undefined, seasonId: string, story: StoryOutput): Promise<string> {
  const db = admin.firestore();
  const base = uid ? db.collection('users').doc(uid).collection('story') : db.collection('public_story');
  const ref = base.doc(seasonId);
  await ref.set({ ...story, saved_at: Date.now() }, { merge: true });
  return ref.id;
}

export async function getSeasonStory(uid: string | undefined, seasonId: string): Promise<StoryOutput | null> {
  const db = admin.firestore();
  const base = uid ? db.collection('users').doc(uid).collection('story') : db.collection('public_story');
  const snap = await base.doc(seasonId).get();
  return (snap.exists ? (snap.data() as unknown as StoryOutput) : null);
}




