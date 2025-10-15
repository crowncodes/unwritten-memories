Here’s a concise **reference doc** for every control in your Music State Vector (MSV) UI, what it represents musically, and how the engine uses it.

# Unwritten Memories — Music Controls Reference

## Presets & Transport

* **Presets**: loads a saved MSV (all groups) via the dropdown. 
* **Play/Pause**: starts/stops realtime generation. 
* **Slider ranges**: most sliders are 0.00–1.00, step 0.01. 

---

## Affect

Emotional coordinates (continuous). These steer “feel” before orchestration.

* **Valence**: sad/dark → warm/hopeful. Raises major/color tones at higher values. 
* **Arousal**: calm → urgent. Lifts BPM, rhythm activity, drum velocity. 
* **Tension**: relaxed → on-edge. Increases dissonance, pedal tones, unresolved chords. 
* **Agency**: powerless → in-control. Pushes clearer melodies, confident cadences. 

---

## Harmony

Controls chord color and how strongly the music “finds home.”

* **Brightness**: minor/Dorian ↔ Lydian/Ionian sheen. Higher = brighter modes/voicings. 
* **Consonance**: roughness ↔ purity. Higher = triads/add9; lower = clustered/extended. 
* **Tonal Certainty**: modal blur ↔ clear key center. Affects modulation drift. 
* **Cadential Drive**: drift ↔ resolve. Probability of strong cadences. 

---

## Temporal

Time & groove.

* **Tempo**: maps to BPM per scene. Higher = faster. 
* **Regularity**: rubato ↔ steady grid. Humanization vs quantization. 
* **Syncopation**: on-beat ↔ off-beat accents. 
* **Ostinato**: none ↔ motor pattern density. 
* **Swing**: straight ↔ swing/compound feel. 

---

## Melody

Shape and presence of the top line.

* **Contour**: static ↔ evolving arcs. 
* **Step vs Leap**: scalar motion ↔ bigger intervals. 
* **Range**: narrow ↔ wide span. 
* **Register**: low ↔ high center. 

---

## Orchestration

What plays, and how many things play at once.

* **Sparsity (1–5)**: caps simultaneous instrument families (top-k). Lower = more solo/duo; higher = fuller ensemble. UI uses a number input.  
* **Weights** (0–1 each): **piano, strings, woodwinds, guitars, percussion, bells, pads**. Higher = more of that family in the mix.  

**Tip:** keep 2–3 families prominent (use Sparsity≈2–3) for clarity; raise **percussion** mainly when Arousal/Tempo are high.

---

## Texture

Space and recording character (brand “journal” feel).

* **Density**: solo ↔ ensemble bed. 
* **Intimacy**: close-mic ↔ distant. Narrows stereo when high. 
* **Width**: mono-ish ↔ wide image. 
* **Bloom**: reverb length/tail. Keep moderate for battery. 
* **Grain**: clean ↔ tape/vinyl texture. 

---

## Style (Blends)

Soft “genre” nudges; they bend mappings rather than hard-switching instruments.

* **journal, lofi_jazz, chamber_minimal, indie_folk, ambient_tape, everyday_epic** — combine any (0–1 each). 

---

## Context

Scene transforms that apply offsets, not replacements.

* **Daypart**: Morning / Afternoon / Evening / Night.  
* **Weather**: Clear / Rain / Wind / Snow / Transit.  
* **Privacy**: public ↔ private. Higher = narrower width, closer mic, softer percussion. 

---

## Finish

Progression sparkle & reproducibility.

* **Level (0–3)**: Plain / Copper / Gold / Iridescent—drives “foil” shimmer accents.  
* **Shimmer (0–1)**: how much high-partial sparkle/bells. 
* **Seed (int)**: repeatable randomness for the generator. 

---

## How the engine consumes these settings

* The UI emits an **MSV** object with all groups; transport hooks wire it to the realtime session. 
* The current implementation sends a *weighted prompt* built from the **entire MSV JSON** to the live model (one prompt entry). (You can evolve this to multi-prompt “score cards” later.) 

---

## Quick recipes (sanity checks)

* **Romantic, private**: Valence .75, Arousal .30, Tension .20; Brightness .70; Tempo .35; Sparsity 2; Piano .45 / Strings .30; Intimacy .70; Bloom .45; Style journal .6. 
* **Tense transit**: Valence .20, Arousal .74, Tension .86; Tempo .70; Ostinato .65; Strings .55 / Pads .25; Context Night+Transit; Privacy .40. 

---

### Notes & best practices

* Move a few sliders at a time; extreme, contradictory combos (e.g., **Privacy 1.0** with **Percussion 1.0 & Width 1.0**) can sound confused.
* Prefer **Sparsity 2–3** for musical clarity; raise density via **Texture.Density** instead of activating all families.
* Save strong moments as **Presets** to reuse across scenes. 

If you want this as a printable page, I can export it to a one-pager PDF or inject it into your app as an in-UI “?” panel.
