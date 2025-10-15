import { Settings } from '../types';

export interface MSVOutput {
  affect: {
    valence: number;
    arousal: number;
    tension: number;
    agency: number;
  };
  harmony: {
    brightness: number;
    consonance: number;
    cadentialDrive: number;
  };
  temporal: {
    tempo: number;
    regularity: number;
  };
  orchestration: {
    sparsity: number;
    weights: Record<string, number>;
  };
  texture: {
    intimacy: number;
    privacy: number;
  };
}

export function convertToMSV(sixGroup: Settings): MSVOutput {
  const e = sixGroup.emotional;
  const t = sixGroup.temporal;
  const h = sixGroup.harmonic;
  const tex = sixGroup.textural;
  const c = sixGroup.cultural;
  const f = sixGroup.functional;
  
  // Affect calculations
  const modalCharacterModifier = h[1] < 35 ? 0.7 : h[1] > 70 ? 1.15 : 1.0;
  const valence = clamp((e[1] / 100) * modalCharacterModifier);
  
  const tempoBoost = t[0] > 75 ? 0.1 : 0;
  const rhythmicBoost = t[1] > 70 ? 0.05 : 0;
  const arousal = clamp((e[0] / 100) + tempoBoost + rhythmicBoost);
  
  const dissonanceBoost = h[0] < 35 ? 0.15 : 0;
  const metricsBoost = t[2] < 40 ? 0.1 : 0;
  const tension = clamp((e[2] / 100) + dissonanceBoost + metricsBoost);
  
  const agency = clamp((e[0] * 0.4 + f[1] * 0.3 + t[0] * 0.3) / 100);
  
  // Harmony calculations
  const valenceBoost = e[1] > 70 ? 0.1 : 0;
  const rangeBoost = tex[2] > 70 ? 0.05 : 0;
  const brightness = clamp((h[1] / 100) + valenceBoost + rangeBoost);
  
  const tensionModifier = e[2] > 70 ? 0.8 : 1.0;
  const culturalModifier = c[0] > 60 ? 1.1 : 1.0;
  const consonance = clamp((h[0] / 100) * tensionModifier * culturalModifier);
  
  const cadentialDrive = clamp((h[2] * 0.5 + f[1] * 0.5) / 100);
  
  // Temporal calculations
  const energyModifier = e[0] < 30 ? 0.85 : 1.0;
  const arousalModifier = arousal > 0.8 ? 1.15 : 1.0;
  const tempo = clamp((t[0] / 100) * energyModifier * arousalModifier);
  
  const complexityModifier = t[1] > 75 ? 0.85 : 1.0;
  const tensionModifierTemporal = e[2] > 70 ? 0.9 : 1.0;
  const regularity = clamp((t[2] / 100) * complexityModifier * tensionModifierTemporal);
  
  // Orchestration calculations
  const presenceBonus = f[0] < 40 ? 0.15 : 0;
  const dynamicBonus = tex[2] < 35 ? 0.1 : 0;
  const intimacy = clamp(
    1.0 - ((tex[1] * 0.6 + tex[0] * 0.4) / 100) + presenceBonus + dynamicBonus
  );
  
  const spatialBonus = tex[1] < 35 ? 1 : 0;
  const sparsity = Math.max(1, Math.min(5, 
    Math.round(5 - (tex[0] / 25)) + spatialBonus
  ));
  
  const weights = calculateWeights(arousal, tempo, agency, f[1], e[0], 
    tex[0], intimacy, sparsity, c[0], c[1], c[2]);
  
  // Privacy calculation
  const minPrivacy = intimacy > 0.7 ? 0.6 : 0.0;
  const privacy = clamp(
    1.0 - ((f[0] * 0.5 + tex[1] * 0.3 + f[2] * 0.2) / 100),
    minPrivacy
  );
  
  return {
    affect: { valence, arousal, tension, agency },
    harmony: { brightness, consonance, cadentialDrive },
    temporal: { tempo, regularity },
    orchestration: { sparsity, weights },
    texture: { intimacy, privacy }
  };
}

function clamp(value: number, min: number = 0, max: number = 1): number {
  return Math.max(min, Math.min(max, value));
}

function calculateWeights(
  arousal: number, 
  tempo: number, 
  agency: number, 
  narrative: number,
  energy: number, 
  density: number, 
  intimacy: number, 
  sparsity: number,
  classical: number, 
  contemporary: number, 
  world: number
): Record<string, number> {
  const weights: Record<string, number> = {
    pad: 1.0, // Always present
    piano: 0.8, // Always present
    rhythm: (arousal + tempo) / 2 * (sparsity >= 4 ? 0.5 : 1.0),
    melody: (agency + narrative / 100) / 2 * (sparsity >= 4 ? 0.6 : 1.0),
    bass: sparsity >= 4 ? 0 : (energy / 100 + (1 - density / 100)) / 2,
    texture: (intimacy + clamp(1.0 - density / 100)) / 2,
    orchestral: classical / 100,
    electronic: contemporary / 100,
    world: world / 100
  };
  
  return weights;
}


