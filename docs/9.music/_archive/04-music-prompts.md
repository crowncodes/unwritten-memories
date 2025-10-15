Below is a **definitive, LLM-facing guide** that lets the music adapt to *any* moment by reacting to **one changing gameplay signal at a time** (emotion, event, arc beat, capacity, etc.). It tells the model **what sliders to push/pull** (strong vs. negative drivers), then runs a **conflict check** so the score stays musical and on-brand.

---

# Unwritten Memories — LLM Music Adjustment Policy

## 0) Target: the MSV (Music State Vector)

All sliders live on **0–1** (unless noted). The LLM never hard-sets a “style preset”; it **adds deltas** to sliders, then normalizes and validates.

**MSV groups:** `affect:{valence, arousal, tension, agency}`, `harmony:{brightness, consonance, tonal_certainty, cadential_drive}`, `temporal:{tempo, regularity, syncopation, ostinato, swing}`, `melody:{contour, step_vs_leap, range, register}`, `orchestration:{weights:{piano, strings, woodwinds, guitars, percussion, bells, pads, field_textures}, sparsity(1–5)}`, `texture:{density, intimacy, width, bloom, grain}`, `style:{journal, lofi_jazz, chamber_minimal, indie_folk, ambient_tape, everyday_epic}`, `context:{daypart, weather, privacy}`, `finish:{level 0–3, shimmer 0–1}`, `seed(int)`.

---

## 1) One-signal-at-a-time rule

When the game emits **a single change** (e.g., *state shifts to OVERWHELMED*, *Act switches to 2*, *event = crisis*), apply the **matching driver block** below:

* **Strong drivers** = sliders that should **increase** (or move brighter/faster/denser).
* **Negative drivers** = sliders that should **decrease** (or move darker/slower/sparser).

Then run the **Conflict Check** (Section 4).

---

## 2) Driver blocks by game signal

### A) Emotional State (from the 20-state system)

Use the nearest canonical state the mechanics engine reports.
**Example mappings (representative groups):**

* **ENERGIZING POSITIVE** (e.g., MOTIVATED, INSPIRED, EXCITED, CONFIDENT):

  * **Strong:** `affect.arousal +.20`, `harmony.brightness +.15`, `harmony.cadential_drive +.15`, `temporal.tempo +.15`, `temporal.regularity +.10`, `temporal.ostinato +.10`, `melody.range +.10`, `orchestration.percussion +.10`, `orchestration.strings +.05`, `texture.width +.10`
  * **Negative:** `texture.intimacy −.10` if privacy low, `style.ambient_tape −.10`
  * Rationale: “driven/creative/social lift” moments favor steady pulse, lighter syncopation, and clearer cadences. 
* **CALM POSITIVE** (e.g., CONTENT, PEACEFUL, GRATEFUL, REFLECTIVE):

  * **Strong:** `affect.valence +.15`, `temporal.tempo −.10`, `temporal.regularity +.10`, `temporal.swing +.05` (gentle lilt), `harmony.consonance +.15`, `texture.bloom +.10`, `texture.intimacy +.10`, `style.journal +.10`, `orchestration.piano +.10`, `bells +.05`
  * **Negative:** `orchestration.percussion −.15`, `temporal.ostinato −.10`
  * Rationale: restful maintenance/clarity, small-ensemble warmth. 
* **NEGATIVE HIGH-ENERGY** (e.g., ANXIOUS/WORRIED, STRESSED):

  * **Strong:** `affect.tension +.20`, `temporal.syncopation +.10`, `temporal.ostinato +.15` (motor undercurrent), `temporal.tempo +.10`, `harmony.tonal_certainty −.10` (more ambiguity), `style.ambient_tape +.10`, `texture.width −.05`
  * **Negative:** `harmony.cadential_drive −.10` (fewer tidy cadences), `bells −.10`
  * Rationale: urgency without panic; keep humane, no EDM clichés. 
* **NEGATIVE LOW-ENERGY** (e.g., SAD, DISCOURAGED, EXHAUSTED):

  * **Strong:** `temporal.tempo −.15`, `temporal.regularity −.10` (allow rubato), `harmony.brightness −.15`, `harmony.consonance +.10` (simple/add9), `texture.intimacy +.15`, `style.journal +.10`, `style.ambient_tape +.10`, `orchestration.piano +.10`, `pads +.05`
  * **Negative:** `percussion −.20`, `width −.10`, `cadential_drive −.10`
  * Rationale: quiet, close, reflective; conserve energy. 

> If the engine provides a **specific state** (e.g., MOTIVATED vs. INSPIRED), bias instrument families accordingly: *MOTIVATED → strings/pulse*, *INSPIRED → piano/woodwinds/bells subtle*. 

---

### B) Decisive Decision (time pauses)

When a **Decisive Decision** card appears, music should **breathe, clarify, and hold**:

* **Strong:** `texture.intimacy +.20`, `texture.bloom +.10`, `harmony.cadential_drive +.10` (clear but soft cadences), `temporal.regularity −.10` (tiny rubato), `orchestration.percussion −.15`, `style.journal +.10`
* **Negative:** `temporal.syncopation −.10`, `width −.05`
* **Scheduling:** apply at **barline**, keep loop length **8 bars**, tiny crossfade. *No anxiety timers.* 

---

### C) Narrative Arc Beat (Act I / II / III)

* **Act I (Setup):** gentle lift, openness

  * **Strong:** `harmony.tonal_certainty +.10`, `harmony.brightness +.05`, `cadential_drive +.05`, `orchestration.piano +.05`
  * **Negative:** none major
* **Act II (Complications):** escalate effort & uncertainty

  * **Strong:** `affect.tension +.15`, `temporal.ostinato +.10`, `syncopation +.05`, `cadential_drive −.05` (defer some resolutions), `strings +.05`, `pads +.05`
* **Act III (Resolution):** clarity and closure

  * **Strong:** `cadential_drive +.20`, `harmony.tonal_certainty +.15`, `brightness +.10`, `temporal.regularity +.10`, `percussion +.05` (if not private)
  * **Negative:** `tension −.15`
    Rationale and timing come from the season’s 3-act scaffolding. 

---

### D) Event Category (moment-to-moment)

* **SOCIAL / RELATIONSHIP:** `style.journal +.10`, `texture.intimacy +.10`, `width −.05`, `woodwinds +.05`, `piano +.05`, `percussion −.10`
* **ASPIRATION / CAREER (work focus):** `regularity +.10`, `ostinato +.10`, `strings +.05`, `piano +.05`, `bells 0 to +.05 (progress pings)`
* **CRISIS:** `tension +.20`, `brightness −.10`, `cadential_drive −.10`, `ostinato +.10` (low register), `width −.10`, `percussion (hand/brush) +.05`
* **OPPORTUNITY / MILESTONE:** `brightness +.15`, `cadential_drive +.10`, `bells +.10` (tasteful), `width +.05`
  Keep total event frequency musical and non-random; these deltas layer atop the current arc beat. 

---

### E) Tension / Hook Points

When hooks rise (deadline, mystery, threat), **sustain intrigue** without anxiety:

* **Strong:** `affect.tension +.10`, `temporal.ostinato +.10` (subtle motor), `syncopation +.05`, `width −.05`
* **Negative:** avoid big cymbal lifts (`percussion +0` or small), keep `cadential_drive −.05` until reveal
* **On reveal:** briefly flip: `cadential_drive +.15`, `tension −.15`, `bells +.05`
  Always maintain 2–3 unresolved hooks; never flood. 

---

### F) Stakes Escalation (consequence chains)

When stakes escalate (e.g., health neglect → collapse trajectory), **pull toward restraint**:

* **Strong:** `tempo −.10`, `width −.10`, `intimacy +.15`, `percussion −.10`, `ambient_tape +.10`, `pads +.05`
* **Negative:** `bells −.10`, `brightness −.10`
  At *crisis_event*, momentarily **mute ostinati**, highlight solo lead (piano/cello) with longer tail, then rebuild. 

---

### G) Dramatic Irony (player learns what PC/NPC doesn’t)

Use **empathy lens**:

* **Strong:** `intimacy +.15`, `bloom +.10`, `journal +.10`, `woodwinds +.05` (clarinet lines)
* **Negative:** `percussion −.10`, `syncopation −.05`
  POV scenes lean reflective; save cadential resolution for after the reveal lands. 

---

### H) Emotional Memory Echoes

When a **past, similar memory surfaces** during a current beat:

* **Strong:** `style.journal +.10`, `ambient_tape +.05`, `intimacy +.10`, `bloom +.05`, `cadential_drive −.05` (linger)
* **Negative:** `percussion −.10`
  On a “positive echo” (support remembered), allow small shimmer: `bells +.05` at cadence. 

---

### I) Meter & Emotional Capacity (0–10)

Use meters → capacity to respect **privacy & availability**:

* **Capacity ≤ 4 (LOW):** `intimacy +.15`, `width −.10`, `percussion −.10`, `tempo −.10`, `bloom +.05`, favor `piano/pads`, reduce `cadential_drive −.05` (don’t pressure)
* **Capacity 4–6 (MODERATE):** small lifts only; keep pulse gentle
* **Capacity ≥ 6 (HIGH):** it’s safe to **resolve more**, `cadential_drive +.10`, `brightness +.10`, allow `percussion +.05`
* **Specific meter lows:**

  * **Physical low (<3):** `tempo −.10`, `ostinato −.10`, `width −.05`
  * **Mental low (<3):** `syncopation −.10`, `tonal_certainty +.10` (less cognitive load)
  * **Social low (<3):** `privacy +.10` (maps to `intimacy +`, `width −`)
  * **Emotional low (<3):** `tension −.05`, `bloom +.05`, **no harsh dissonance**
    Grounded in capacity thresholds & stacking penalties. 

---

## 3) Day/Weather & Location (context transforms)

These are **additive offsets** (don’t conflict-resolve them away unless critical):

* **Morning:** `brightness +.05`, `bells +.03`, `tempo +.05` (light), `width +.03`
* **Evening/Night:** `bloom +.05`, `intimacy +.05`, `width −.03`
* **Rain:** `ambient_tape +.05`, `pads +.05`, `percussion −.05`, `syncopation +.03` (bus sway)
* **Transit:** subtle motor: `ostinato +.05` low register
  (Use alongside primary drivers above.)

---

## 4) Conflict Check (run every time, after deltas)

1. **Privacy-First Rule** (capacity-aware): if `context.privacy ≥ .7` **or** capacity ≤ 4 → clamp:

   * `percussion ≤ .30`, `width ≤ .40`, `tempo ≤ scene_max − 10%`, ensure `intimacy ≥ .6`. 
2. **Clarity Rule during Decisions:** if Decisive Decision active → `syncopation ≤ .3`, `ostinato ≤ .3`, enforce `8-bar` form, gentle cadence allowed. 
3. **Arc Coherence:**

   * Act II cannot exceed Act III `cadential_drive` by more than `.10`. 
4. **Instrument Top-K:** apply `sparsity` → keep only top-K families (normalize the chosen weights).
5. **Battery & Brand:** avoid long tails if three or more reverbs active; keep **no neon/EDM** (cap percussion brightness).
6. **Tension Hygiene:** if both `tension ≥ .7` and `cadential_drive ≥ .7`, reduce one by `.15` (don’t tug in opposite directions). 
7. **Crisis Courtesy:** if a **crisis_event** is live, mute shimmer (`bells ≤ .05`) and resolve later. 

---

## 5) Scheduling & Smoothing

* **Apply at barlines** with **80–120 ms crossfade**; never mid-beat during decisions. 
* **EMA smoothing** on scalar groups (α≈0.2) to avoid lurching.
* **Normalize** style/orchestration blends; enforce `sparsity` top-K.

---

## 6) Minimal algorithm (LLM pseudocode)

```pseudo
onSignal(signal):
  deltas = empty map<slider, float>

  switch signal.type:

    case EMOTIONAL_STATE(s):
      deltas += lookupDriverBlock("emotional", s)      // Section 2A

    case DECISIVE_DECISION(enter|exit):
      deltas += (enter ? decisionBlock : inverse(decisionBlock))   // 2B

    case ARC_BEAT(act):
      deltas += arcBlock(act)                          // 2C

    case EVENT(category):
      deltas += eventBlock(category)                   // 2D

    case TENSION_HOOK(level|reveal):
      deltas += tensionBlock(level or reveal)          // 2E

    case STAKES_ESCALATION(stage):
      deltas += stakesBlock(stage)                     // 2F

    case DRAMATIC_IRONY(active|resolved):
      deltas += ironyBlock(active|resolved)            // 2G

    case MEMORY_ECHO(type):
      deltas += echoBlock(type)                        // 2H

    case CAPACITY(value) or METERS(m):
      deltas += capacityBlock(value, m)                // 2I

    case CONTEXT(daypart|weather|location):
      deltas += contextOffsets(daypart, weather)       // 3

  // Apply deltas
  msv' = clamp(msv + deltas, 0..1)

  // Conflict checks
  msv'' = runConflictCheck(msv', signal, capacity, arcState)       // Section 4

  // Schedule
  scheduleAtBarline(msv'')  // xfade 100ms, hold 8-bar during decisions
```

---

## 7) Examples (single-signal adjustments)

* **State → OVERWHELMED (capacity likely low):**
  Apply 2A NEGATIVE HIGH-ENERGY but cap per Conflict Check #1 (privacy-first). Result: lower tempo/width, subtle motor, fewer cadences.  

* **Event → CRISIS (no decision yet):**
  Raise tension/ostinato a touch, dim brightness, defer resolution; keep percussion human (no aggression). 

* **Arc switches to Act III:**
  Increase cadential drive & tonal certainty; allow a little shimmer at the final push. 

* **Memory Echo surfaces during success:**
  Increase intimacy/bloom briefly, then restore cadential resolution; tasteful bell at cadence. 

* **Decisive Decision opens:**
  Pause-time vibe: reduce groove/syncopation, bump intimacy, allow clear but gentle cadence. Apply at barline. 

---

## 8) What not to do (guardrails the LLM must follow)

* Don’t activate >`sparsity` families; always top-K then normalize.
* Don’t raise **tension** *and* **cadential_drive** high at once (they conflict). 
* Don’t use bright, aggressive percussion during **private** or **decision** beats. 
* Don’t ignore **capacity**—it governs privacy/width/tempo ceilings. 

---

## 9) Output format (from LLM to engine)

Return **only deltas** and **reasoning tag** for logging:

```json
{
  "deltas": {
    "affect.tension": +0.20,
    "temporal.ostinato": +0.10,
    "harmony.cadential_drive": -0.10,
    "texture.width": -0.05,
    "orchestration.percussion": -0.10
  },
  "constraints_applied": ["privacy_first", "arc_coherence"],
  "schedule": "at_barline_xfade_100ms",
  "why": "Crisis event while tension hook active; sustain intrigue without anxiety."
}
```

---

This policy gives you **infinite coverage**: any new moment is just “one signal → apply driver block → validate,” so music **evolves naturally with gameplay** while staying consistent with your mechanics for emotions, decisions, arcs, events, tension, stakes, irony, memories, and capacity.         

If you want, I can also package this as a JSON/YAML rule file the LLM can load and apply directly.
