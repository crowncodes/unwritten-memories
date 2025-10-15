
import { Group, ConstraintType, Preset } from './types';

export const GROUPS: Group[] = [
  {
    id: 'emotional',
    title: '1. Emotional Arousal & Valence',
    description: 'The psychological foundation of musical emotion.',
    constraintType: ConstraintType.Independent,
    parameters: [
      { name: 'Energy Level', description: 'From calm/serene to highly energetic/frantic.' },
      { name: 'Valence', description: 'From negative/dark to positive/bright.' },
      { name: 'Tension', description: 'From relaxed to tense/anxious.' },
    ],
  },
  {
    id: 'temporal',
    title: '2. Temporal & Rhythmic Character',
    description: 'Time-based elements that define movement and pace.',
    constraintType: ConstraintType.Independent,
    parameters: [
      { name: 'Tempo Intensity', description: 'From very slow (40 BPM) to very fast (200+ BPM).' },
      { name: 'Rhythmic Complexity', description: 'From simple steady beats to complex polyrhythms.' },
      { name: 'Metric Stability', description: 'From fluid/rubato to strict metronomic time.' },
    ],
  },
  {
    id: 'harmonic',
    title: '3. Harmonic & Tonal Architecture',
    description: 'The structural foundation of musical harmony.',
    constraintType: ConstraintType.SumTo100,
    parameters: [
      { name: 'Consonance Level', description: 'From highly dissonant to perfectly consonant.' },
      { name: 'Modal Character', description: 'From dark modes to bright modes.' },
      { name: 'Harmonic Density', description: 'From simple triads to complex extended chords.' },
    ],
  },
  {
    id: 'textural',
    title: '4. Textural Density & Space',
    description: 'How musical elements are layered and positioned.',
    constraintType: ConstraintType.Independent,
    parameters: [
      { name: 'Instrumental Density', description: 'From solo/sparse to full orchestral.' },
      { name: 'Spatial Width', description: 'From mono/centered to wide stereo field.' },
      { name: 'Dynamic Range', description: 'From compressed/flat to highly dynamic.' },
    ],
  },
  {
    id: 'cultural',
    title: '5. Cultural & Stylistic Identity',
    description: 'Genre and cultural signifiers that provide contextual meaning.',
    constraintType: ConstraintType.SumTo100,
    parameters: [
      { name: 'Western Classical', description: 'Traditional orchestral and chamber music elements.' },
      { name: 'Popular/Contemporary', description: 'Rock, pop, electronic, hip-hop elements.' },
      { name: 'World/Ethnic', description: 'Non-western scales, instruments, and traditions.' },
    ],
  },
  {
    id: 'functional',
    title: '6. Narrative & Contextual Function',
    description: 'The role music plays in supporting story or environment.',
    constraintType: ConstraintType.Independent,
    parameters: [
      { name: 'Foreground Presence', description: 'From ambient background to attention-grabbing.' },
      { name: 'Narrative Support', description: 'From abstract/atmospheric to story-driven.' },
      { name: 'Emotional Directness', description: 'From subtle suggestion to obvious emotional manipulation.' },
    ],
  },
];

export const INITIAL_SETTINGS = GROUPS.reduce((acc, group) => {
  if (group.constraintType === ConstraintType.SumTo100) {
    acc[group.id] = [34, 33, 33];
  } else {
    acc[group.id] = [50, 50, 50];
  }
  return acc;
}, {} as { [key: string]: number[] });


export const PRESETS: Preset[] = [
  {
    name: 'Tense Boss Battle',
    settings: {
      emotional: [95, 20, 95],
      temporal: [85, 75, 90],
      harmonic: [30, 20, 50],
      textural: [85, 90, 95],
      cultural: [40, 60, 0],
      functional: [95, 85, 90],
    },
  },
  {
    name: 'Peaceful Village',
    settings: {
      emotional: [25, 80, 15],
      temporal: [30, 35, 50],
      harmonic: [70, 75, -45], // Note: Doc has weird values, will normalize to sum-100
      textural: [35, 60, 40],
      cultural: [20, 0, 80],
      functional: [30, 40, 45],
    },
  },
  {
    name: 'Mysterious Exploration',
    settings: {
      emotional: [45, 40, 60],
      temporal: [40, 65, 35],
      harmonic: [40, 35, 25],
      textural: [50, 85, 70],
      cultural: [60, 30, 10],
      functional: [50, 70, 40],
    },
  },
  {
    name: 'Romantic Dialogue',
    settings: {
      emotional: [30, 85, 25],
      temporal: [35, 25, 60],
      harmonic: [85, 80, -65], // Normalize
      textural: [25, 45, 60],
      cultural: [85, 15, 0],
      functional: [40, 90, 75],
    },
  },
  {
    name: 'High-Speed Chase',
    settings: {
      emotional: [98, 60, 85],
      temporal: [95, 80, 95],
      harmonic: [50, 60, -10], // Normalize
      textural: [80, 90, 85],
      cultural: [20, 80, 0],
      functional: [100, 75, 85],
    },
  },
];

// Normalize presets with sum-to-100 constraints
PRESETS.forEach(preset => {
    GROUPS.forEach(group => {
        if (group.constraintType === ConstraintType.SumTo100) {
            const values = preset.settings[group.id];
            // Treat negative values as zero for sum calculation
            const positiveValues = values.map(v => Math.max(0, v));
            const total = positiveValues.reduce((sum, v) => sum + v, 0);
            if (total !== 100 && total > 0) {
                preset.settings[group.id] = positiveValues.map(v => Math.round((v / total) * 100));
                // Adjust for rounding errors
                const finalTotal = preset.settings[group.id].reduce((sum, v) => sum + v, 0);
                if (finalTotal !== 100) {
                    preset.settings[group.id][0] += 100 - finalTotal;
                }
            } else if (total === 0) {
                preset.settings[group.id] = [34, 33, 33];
            }
        }
    });
});
