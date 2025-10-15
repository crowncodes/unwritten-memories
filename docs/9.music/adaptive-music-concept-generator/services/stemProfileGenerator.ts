import { Settings } from '../types';
import { MSVOutput } from './msvConverter';
import { LyriaPrompt } from './lyriaPromptGenerator';

export interface StemProfile {
  id: string;
  tags: string[];
  msv: MSVOutput;
  gameStateMatch: {
    capacityRange: [number, number];
    valenceRange: [number, number];
    arousalRange: [number, number];
    dayPhases?: string[];
  };
  technical: {
    tempo: number;
    key: string;
    mode: string;
    bars: number;
    durationMs: number;
    loopPoints: [number, number];
  };
  generatedFrom: {
    sixGroupParams: Settings;
    lyriaPrompt: string;
  };
}

export function generateStemProfile(
  sixGroup: Settings,
  msv: MSVOutput,
  lyriaPrompt: LyriaPrompt,
  customName?: string
): StemProfile {
  const id = customName || generateId(msv, lyriaPrompt.technical);
  const tags = generateTags(msv);
  const gameStateMatch = calculateGameStateMatch(msv);
  
  return {
    id,
    tags,
    msv,
    gameStateMatch,
    technical: {
      ...lyriaPrompt.technical,
      loopPoints: [0, lyriaPrompt.technical.durationMs]
    },
    generatedFrom: {
      sixGroupParams: sixGroup,
      lyriaPrompt: lyriaPrompt.fullPrompt
    }
  };
}

function generateId(msv: MSVOutput, technical: any): string {
  const emotional = getEmotionalState(msv);
  const intimacyLevel = msv.texture.intimacy > 0.7 ? 'intimate' : 
                        msv.texture.intimacy < 0.4 ? 'expansive' : 'moderate';
  const key = technical.key.toLowerCase();
  const tempo = technical.tempo;
  
  return `${emotional}_${intimacyLevel}_${key}${tempo}`;
}

function getEmotionalState(msv: MSVOutput): string {
  const { valence, arousal, tension } = msv.affect;
  
  // Map MSV to emotional states defined in Priority Tier 1
  if (valence > 0.6 && arousal < 0.4) return 'calm_positive';
  if (valence < 0.4 && arousal < 0.4) return 'melancholic';
  if (arousal > 0.6 && valence > 0.5) return 'motivated';
  if (tension > 0.7) return 'anxious';
  if (valence > 0.5 && arousal < 0.5 && tension < 0.4) return 'content';
  if (arousal < 0.3 && valence < 0.5) return 'exhausted';
  if (arousal > 0.7 && valence > 0.7) return 'excited';
  if (tension > 0.5 && valence < 0.5) return 'worried';
  if (valence < 0.3) return 'sad';
  
  return 'reflective';
}

function generateTags(msv: MSVOutput): string[] {
  const tags: string[] = [getEmotionalState(msv)];
  
  // Add descriptive tags based on MSV values
  if (msv.affect.valence > 0.6) tags.push('positive');
  if (msv.affect.valence < 0.4) tags.push('negative');
  if (msv.affect.arousal > 0.6) tags.push('energetic');
  if (msv.affect.arousal < 0.4) tags.push('calm');
  if (msv.texture.intimacy > 0.7) tags.push('intimate', 'journal');
  if (msv.texture.privacy > 0.6) tags.push('private');
  if (msv.orchestration.sparsity >= 4) tags.push('minimal', 'sparse');
  
  // Add harmonic tags
  if (msv.harmony.brightness > 0.7) tags.push('bright');
  if (msv.harmony.brightness < 0.4) tags.push('dark');
  if (msv.harmony.consonance > 0.7) tags.push('consonant');
  if (msv.harmony.consonance < 0.4) tags.push('dissonant');
  
  // Add temporal tags
  if (msv.temporal.tempo > 0.7) tags.push('fast');
  if (msv.temporal.tempo < 0.4) tags.push('slow');
  
  return tags;
}

function calculateGameStateMatch(msv: MSVOutput): any {
  // Calculate capacity range from tension and intimacy
  // Low tension = high capacity, high intimacy = low capacity
  const tensionFactor = (1 - msv.affect.tension) * 10;
  const intimacyFactor = msv.texture.intimacy > 0.7 ? 3 : 6;
  const avgCapacity = (tensionFactor + intimacyFactor) / 2;
  
  // Determine appropriate day phases based on intimacy and privacy
  const dayPhases: string[] = [];
  if (msv.texture.intimacy < 0.6 && msv.texture.privacy < 0.5) {
    dayPhases.push('morning', 'afternoon');
  } else if (msv.texture.intimacy > 0.6 || msv.texture.privacy > 0.6) {
    dayPhases.push('evening');
  } else {
    dayPhases.push('morning', 'afternoon', 'evening');
  }
  
  return {
    capacityRange: [
      Math.max(0, avgCapacity - 2),
      Math.min(10, avgCapacity + 2)
    ] as [number, number],
    valenceRange: [
      Math.max(0, msv.affect.valence - 0.15),
      Math.min(1, msv.affect.valence + 0.15)
    ] as [number, number],
    arousalRange: [
      Math.max(0, msv.affect.arousal - 0.15),
      Math.min(1, msv.affect.arousal + 0.15)
    ] as [number, number],
    dayPhases: dayPhases.length > 0 ? dayPhases : undefined
  };
}


