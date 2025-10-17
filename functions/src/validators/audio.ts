export interface LoopValidationInput {
  bars: number;
  tempoBpm: number;
  sampleRateHz: number;
  // optional: measured sample length if known
  measuredSamples?: number;
}

export interface LoopValidationResult {
  ok: boolean;
  expectedSamples: number;
  toleranceSamples: number;
  message?: string;
}

export function validateLoopAlignment(input: LoopValidationInput): LoopValidationResult {
  const secondsPerBeat = 60 / input.tempoBpm;
  const beatsPerBar = 4; // fixed 4/4 for now
  const durationSec = input.bars * beatsPerBar * secondsPerBeat;
  const expectedSamples = Math.round(durationSec * input.sampleRateHz);
  const toleranceSamples = Math.round(input.sampleRateHz * 0.02); // 20ms tolerance
  if (typeof input.measuredSamples === 'number') {
    const delta = Math.abs(input.measuredSamples - expectedSamples);
    return {
      ok: delta <= toleranceSamples,
      expectedSamples,
      toleranceSamples,
      message: delta <= toleranceSamples ? undefined : `Loop length off by ${delta} samples`,
    };
  }
  return { ok: true, expectedSamples, toleranceSamples };
}




