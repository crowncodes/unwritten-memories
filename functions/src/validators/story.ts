import { z } from 'genkit';
import { ArcPlanSchema, EventsPlanSchema, StoryWorldSchema } from '../schemas';

export function validateArcPlan(arcPlan: z.infer<typeof ArcPlanSchema>): { ok: boolean; messages: string[] } {
  const messages: string[] = [];
  const { season_length_weeks, three_act, decisive_decisions } = arcPlan;
  const [a1s, a1e] = three_act.act1_weeks;
  const [a2s, a2e] = three_act.act2_weeks;
  const [a3s, a3e] = three_act.act3_weeks;
  const ordered = a1s <= a1e && a1e < a2s && a2s <= a2e && a2e < a3s && a3s <= a3e;
  if (!ordered) messages.push('three_act week ranges must be ordered and non-overlapping');
  const withinBounds = [a1s, a1e, a2s, a2e, a3s, a3e].every((w) => w >= 1 && w <= season_length_weeks);
  if (!withinBounds) messages.push('act week ranges must be within season length');
  if (!Array.isArray(decisive_decisions) || decisive_decisions.length < 1) messages.push('at least one decisive decision required');
  for (const dd of decisive_decisions) {
    const [ws, we] = dd.window_weeks;
    if (!(ws >= 1 && we <= season_length_weeks && ws <= we)) messages.push(`decisive decision ${dd.id} window invalid`);
    if (!dd.foreshadowing_weeks_before?.length) messages.push(`decisive decision ${dd.id} needs foreshadowing weeks`);
  }
  return { ok: messages.length === 0, messages };
}

export function validateEventsPlan(eventsPlan: z.infer<typeof EventsPlanSchema>, seasonLength: number): { ok: boolean; messages: string[] } {
  const messages: string[] = [];
  for (const w of eventsPlan.initial_weeks || []) {
    if (!(w.week >= 1 && w.week <= seasonLength)) messages.push(`event week ${w.week} out of bounds`);
    if (!Array.isArray(w.event_types) || w.event_types.length === 0) messages.push(`week ${w.week} missing event_types`);
  }
  return { ok: messages.length === 0, messages };
}

export function validateWorld(world: z.infer<typeof StoryWorldSchema>): { ok: boolean; messages: string[] } {
  const messages: string[] = [];
  if (!world.starting_location?.enriched_description) messages.push('starting_location.enriched_description required');
  if (!world.starting_location?.image_prompt) messages.push('starting_location.image_prompt required');
  if (!world.starting_career?.description) messages.push('starting_career.description required');
  if (!world.backstory?.summary) messages.push('backstory.summary required');
  return { ok: messages.length === 0, messages };
}




