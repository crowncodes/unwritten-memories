/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
export type PlaybackState = 'stopped' | 'playing' | 'loading' | 'paused';

// Fix: Add Prompt type definition.
export interface Prompt {
  promptId: string;
  text: string;
  weight: number;
  cc: number;
  color: string;
}

// Fix: Add ControlChange type definition.
export interface ControlChange {
  channel: number;
  cc: number;
  value: number;
}
