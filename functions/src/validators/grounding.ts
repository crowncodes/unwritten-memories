export interface NumericalGroundingFactor {
  name: string;
  value: number;
}

export interface NumericalGroundingInput {
  value: number;
  base: number;
  factors: NumericalGroundingFactor[];
  qualitativeTier?: string;
}

export interface NumericalGroundingResult {
  ok: boolean;
  normalizedValue: number;
  messages: string[];
}

export function validateNumericalGrounding(input: NumericalGroundingInput): NumericalGroundingResult {
  const messages: string[] = [];
  if (!Number.isFinite(input.value)) messages.push('value must be finite');
  if (!Number.isFinite(input.base)) messages.push('base must be finite');
  const product = input.factors.reduce((acc, f) => acc * (Number.isFinite(f.value) ? f.value : 1), input.base);
  const normalizedValue = Math.round(product * 100) / 100;
  if (Math.abs(normalizedValue - input.value) > 0.2) {
    messages.push(`value ${input.value} does not match computed ${normalizedValue}`);
  }
  return { ok: messages.length === 0, normalizedValue, messages };
}




