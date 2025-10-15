import { MSVOutput } from './msvConverter';

export interface LyriaPrompt {
  fullPrompt: string;
  technical: {
    tempo: number;
    key: string;
    mode: string;
    bars: number;
    durationMs: number;
  };
  stems: string[];
}

export function generateLyriaPrompt(msv: MSVOutput): LyriaPrompt {
  // Determine tempo from MSV (0.0-1.0 → 58-100 BPM)
  const tempo = Math.round(58 + (msv.temporal.tempo * 42));
  
  // Determine key and mode from brightness/consonance
  const { key, mode } = selectKeyAndMode(msv);
  
  // Calculate duration for 8 bars
  const bars = 8;
  const durationMs = Math.round(((60 / tempo) * 4 * bars) * 1000);
  
  // Select stems based on sparsity and weights
  const stems = selectStems(msv);
  
  // Build emotional character description
  const emotional = buildEmotionalDescription(msv);
  
  // Build instrumentation description
  const instrumentation = buildInstrumentationDescription(msv, stems);
  
  const fullPrompt = `
${instrumentation}

Tempo: ${tempo} BPM, Time Signature: 4/4, Duration: ${bars} bars (${(durationMs/1000).toFixed(2)}s)
Key: ${key} ${mode}
Emotional Character: ${emotional}

Technical Requirements:
- Loop-safe audio with seamless crossfade at bar boundaries
- Bar-aligned with natural fade tail at loop point
- Opus format @ 48kHz sample rate
- Clean separation between stems (generate each stem individually)
- Intimate journal music aesthetic, battery-friendly
- Privacy-first design: ${msv.texture.intimacy > 0.6 ? 'close-mic\'d, personal sound' : 'moderate space'}

Loop Points: 0ms - ${durationMs}ms

Style References: ${getStyleReferences(msv)}
`.trim();
  
  return {
    fullPrompt,
    technical: { tempo, key, mode, bars, durationMs },
    stems
  };
}

function selectKeyAndMode(msv: MSVOutput): { key: string; mode: string } {
  // Brightness determines mode
  if (msv.harmony.brightness > 0.7) {
    return { key: 'C', mode: 'Ionian' }; // Bright major
  } else if (msv.harmony.brightness > 0.5) {
    return { key: 'C', mode: 'Mixolydian' }; // Warm folk
  } else if (msv.harmony.brightness > 0.35) {
    return { key: 'C', mode: 'Dorian' }; // Bittersweet
  } else {
    return { key: 'C', mode: 'Aeolian' }; // Dark minor
  }
}

function selectStems(msv: MSVOutput): string[] {
  const stems = ['pad', 'piano']; // Always include foundation
  
  if (msv.orchestration.weights.rhythm > 0.3) {
    stems.push('light_rhythm');
  }
  if (msv.orchestration.weights.melody > 0.4) {
    stems.push('melody');
  }
  if (msv.orchestration.weights.texture > 0.3) {
    stems.push('texture');
  }
  
  // Respect sparsity limit
  return stems.slice(0, msv.orchestration.sparsity + 1);
}

function buildEmotionalDescription(msv: MSVOutput): string {
  const descriptors = [];
  
  // Valence
  if (msv.affect.valence > 0.7) {
    descriptors.push('warm', 'hopeful', 'positive');
  } else if (msv.affect.valence < 0.3) {
    descriptors.push('melancholic', 'dark', 'introspective');
  } else {
    descriptors.push('neutral', 'contemplative');
  }
  
  // Arousal
  if (msv.affect.arousal > 0.7) {
    descriptors.push('energetic', 'active');
  } else if (msv.affect.arousal < 0.3) {
    descriptors.push('calm', 'serene', 'peaceful');
  } else {
    descriptors.push('moderate');
  }
  
  // Tension
  if (msv.affect.tension > 0.7) {
    descriptors.push('tense', 'anxious', 'unresolved');
  } else {
    descriptors.push('relaxed', 'comfortable');
  }
  
  // Intimacy
  if (msv.texture.intimacy > 0.7) {
    descriptors.push('intimate', 'close', 'personal');
  }
  
  return descriptors.join(', ');
}

function buildInstrumentationDescription(msv: MSVOutput, stems: string[]): string {
  const descriptions: string[] = [];
  
  if (stems.includes('pad')) {
    if (msv.affect.valence > 0.6) {
      descriptions.push('Warm analog synthesizer pad with gentle movement');
    } else {
      descriptions.push('Dark brooding pad with rich low frequencies');
    }
  }
  
  if (stems.includes('piano')) {
    if (msv.texture.intimacy > 0.7) {
      descriptions.push('Intimate felt piano, soft hammers, close-miked');
    } else {
      descriptions.push('Clear piano with moderate presence');
    }
  }
  
  if (stems.includes('light_rhythm')) {
    descriptions.push('Subtle percussion - brushes or soft shaker, textural not emphatic');
  }
  
  if (stems.includes('melody')) {
    descriptions.push('Melodic line with emotional arc, not overpowering');
  }
  
  if (stems.includes('texture')) {
    descriptions.push('Textural layer adding depth and space');
  }
  
  return descriptions.join('. ');
}

function getStyleReferences(msv: MSVOutput): string {
  if (msv.texture.intimacy > 0.7) {
    return 'Nils Frahm, Ólafur Arnalds, Erik Satie - intimate journal music';
  } else if (msv.affect.valence < 0.3) {
    return 'Jóhann Jóhannsson, A Winged Victory for the Sullen - melancholic soundscapes';
  } else {
    return 'Max Richter, Brian Eno - contemplative ambient';
  }
}


