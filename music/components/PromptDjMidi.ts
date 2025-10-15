/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import { css, html, LitElement } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { styleMap } from 'lit/directives/style-map.js';

import { throttle } from '../utils/throttle';

import './PlayPauseButton';
import './ConceptGroup';
import type { PlaybackState } from '../types';

const GROUP_CONFIG = [
  {
    title: '1. Emotional Arousal & Valence',
    type: 'independent',
    key: 'group1',
    params: [
      { key: 'energy', label: 'Energy Level' },
      { key: 'valence', label: 'Valence' },
      { key: 'tension', label: 'Tension' },
    ],
  },
  {
    title: '2. Temporal & Rhythmic Character',
    type: 'independent',
    key: 'group2',
    params: [
      { key: 'tempo', label: 'Tempo Intensity' },
      { key: 'complexity', label: 'Rhythmic Complexity' },
      { key: 'stability', label: 'Metric Stability' },
    ],
  },
  {
    title: '3. Harmonic & Tonal Architecture',
    type: 'sum-to-100',
    key: 'group3',
    params: [
      { key: 'consonance', label: 'Consonance Level' },
      { key: 'modal', label: 'Modal Character' },
      { key: 'density', label: 'Harmonic Density' },
    ],
  },
  {
    title: '4. Textural Density & Space',
    type: 'independent',
    key: 'group4',
    params: [
      { key: 'density', label: 'Instrumental Density' },
      { key: 'width', label: 'Spatial Width' },
      { key: 'range', label: 'Dynamic Range' },
    ],
  },
  {
    title: '5. Cultural & Stylistic Identity',
    type: 'sum-to-100',
    key: 'group5',
    params: [
      { key: 'classical', label: 'Western Classical' },
      { key: 'pop', label: 'Popular/Contemporary' },
      { key: 'world', label: 'World/Ethnic' },
    ],
  },
  {
    title: '6. Narrative & Contextual Function',
    type: 'independent',
    key: 'group6',
    params: [
      { key: 'presence', label: 'Foreground Presence' },
      { key: 'narrative', label: 'Narrative Support' },
      { key: 'directness', label: 'Emotional Directness' },
    ],
  },
];

/** The main music control board. */
@customElement('prompt-dj-midi')
export class PromptDjMidi extends LitElement {
  static override styles = css`
    :host {
      height: 100%;
      width: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      box-sizing: border-box;
      position: relative;
      padding: 2vmin;
    }
    #background {
      position: absolute;
      height: 100%;
      width: 100%;
      z-index: -1;
      background: #111;
      transition: background 0.5s ease-out;
    }
    #grid {
      width: 100%;
      max-width: 1600px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2vmin;
      margin-bottom: 3vmin;
    }
    play-pause-button {
      position: relative;
      width: 15vmin;
      max-width: 140px;
    }
  `;

  @property({ type: String }) public playbackState: PlaybackState = 'stopped';
  @state() public audioLevel = 0;

  @state()
  private parameters = {
    group1: { energy: 25, valence: 80, tension: 15 },
    group2: { tempo: 30, complexity: 35, stability: 50 },
    group3: { consonance: 70, modal: 20, density: 10 },
    group4: { density: 35, width: 60, range: 40 },
    group5: { classical: 20, pop: 0, world: 80 },
    group6: { presence: 30, narrative: 40, directness: 45 },
  };

  override firstUpdated() {
    this.dispatchPromptChange();
  }
  
  private handleValuesChanged(groupKey: string, e: CustomEvent<number[]>) {
    const paramKeys = GROUP_CONFIG.find(g => g.key === groupKey)!.params.map(p => p.key);
    const newValues: { [key: string]: number } = {};
    paramKeys.forEach((key, i) => {
        newValues[key] = e.detail[i];
    });

    this.parameters = {
        ...this.parameters,
        [groupKey as keyof typeof this.parameters]: newValues,
    };
    this.dispatchPromptChange();
  }

  private dispatchPromptChange = throttle(() => {
    const prompt = this.generatePrompt();
    this.dispatchEvent(
      new CustomEvent('prompt-changed', { detail: prompt, bubbles: true, composed: true }),
    );
  }, 200, {leading: false, trailing: true});

  private generatePrompt(): string {
    const p = this.parameters;
    const desc = (val: number, map: {[key: number]: string}) => {
        if (val <= 33) return map[0];
        if (val <= 66) return map[33];
        return map[67];
    };

    const emotional = `Emotional state: ${desc(p.group1.energy, {0: 'calm', 33: 'moderate energy', 67: 'highly energetic'})}, valence is ${desc(p.group1.valence, {0: 'dark/negative', 33: 'neutral', 67: 'bright/positive'})}, and tension is ${desc(p.group1.tension, {0: 'relaxed', 33: 'anticipatory', 67: 'tense/anxious'})}.`;
    
    const temporal = `Temporal character: ${desc(p.group2.tempo, {0: 'very slow', 33: 'moderate tempo', 67: 'very fast'})}, with ${desc(p.group2.complexity, {0: 'simple rhythms', 33: 'moderately complex rhythms', 67: 'highly complex polyrhythms'})}, and ${desc(p.group2.stability, {0: 'fluid/rubato timing', 33: 'a natural human feel', 67: 'strict, metronomic timing'})}.`;
    
    const harmonic = `Harmonic architecture: primarily ${Math.round(p.group3.consonance)}% consonant, with a ${desc(p.group3.modal, {0: 'dark modal character (Phrygian/Aeolian)', 33: 'neutral modal character (Dorian/Mixolydian)', 67: 'bright modal character (Ionian/Lydian)'})}, and ${desc(p.group3.density, {0: 'sparse harmony (triads)', 33: 'medium harmonic density (7th chords)', 67: 'dense harmony (9th, 11th, 13th chords)'})}.`;

    const textural = `Texture: ${desc(p.group4.density, {0: 'sparse instrumentation (solo/duo)', 33: 'small ensemble', 67: 'large, dense ensemble'})}, a ${desc(p.group4.width, {0: 'narrow, centered stereo field', 33: 'standard stereo width', 67: 'wide, immersive stereo field'})}, and a ${desc(p.group4.range, {0: 'compressed, flat dynamic range', 33: 'moderate dynamic range', 67: 'highly expressive and wide dynamic range'})}.`;

    const cultural = `Stylistic identity: a blend of ${Math.round(p.group5.classical)}% Western Classical, ${Math.round(p.group5.pop)}% Popular/Contemporary, and ${Math.round(p.group5.world)}% World/Ethnic influences.`;
    
    const narrative = `Narrative function: ${desc(p.group6.presence, {0: 'subtle, atmospheric background music', 33: 'present but not dominant', 67: 'prominent, attention-grabbing foreground music'})}, with ${desc(p.group6.narrative, {0: 'abstract, non-narrative mood', 33: 'environmental storytelling support', 67: 'direct narrative support with leitmotifs'})}, and ${desc(p.group6.directness, {0: 'subtle, ambiguous emotional guidance', 33: 'clear emotional guidance', 67: 'direct, cinematic emotional cueing'})}.`;

    return [emotional, temporal, harmonic, textural, cultural, narrative].join(' ');
  }

  private playPause() {
    this.dispatchEvent(new CustomEvent('play-pause'));
  }

  private makeBackground() {
    const { energy, valence, tension } = this.parameters.group1;
    // Valence (0-100) maps to hue (e.g., 240 for blue to 60 for yellow)
    const hue = 240 - (valence / 100) * 180;
    // Energy (0-100) maps to circle size (e.g., 50% to 150%)
    const size = 50 + energy;
    // Tension (0-100) maps to opacity of a noise layer
    const noiseOpacity = tension / 200;

    return `
      radial-gradient(circle at center, hsl(${hue}, 60%, 40%) 0%, #111 ${size}%),
      url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="f"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%" height="100%" filter="url(%23f)"/%3E%3C/svg%3E')
    `;
  }

  override render() {
    const bg = styleMap({
      backgroundImage: this.makeBackground(),
    });

    return html`
      <div id="background" style=${bg}></div>
      <div id="grid">
        ${GROUP_CONFIG.map(group => {
          const values = Object.values(this.parameters[group.key as keyof typeof this.parameters]);
          const labels = group.params.map(p => p.label);
          return html`
            <concept-group
              .title=${group.title}
              .type=${group.type}
              .labels=${labels}
              .values=${values}
              @values-changed=${(e: CustomEvent<number[]>) => this.handleValuesChanged(group.key, e)}
            ></concept-group>
          `;
        })}
      </div>
      <play-pause-button
        .playbackState=${this.playbackState}
        @click=${this.playPause}
      ></play-pause-button>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'prompt-dj-midi': PromptDjMidi
  }
}