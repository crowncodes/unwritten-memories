Awesome — here’s a self-contained JSON rulebook your LLM can use to nudge sliders from **one changing input at a time**, auto-resolve conflicts, and keep the music evolving with play. It’s grounded in your v1.2 systems for emotional capacity, decisive decisions, arc beats, tension/stakes, dramatic irony, and emotional memory/echoes.      

```json
{
  "metadata": {
    "name": "Unwritten Memories — Music Rulebook v1.0",
    "description": "Deterministic rules for mapping game signals → music slider deltas; conflict checks ensure privacy-first, calm UI audio aesthetic; evolves continuously as single parameters change.",
    "updated": "2025-10-14",
    "scales": {
      "intensity": "0.0–1.0",
      "capacity": "0.0–10.0",
      "trust": "0.0–1.0",
      "meters": "0–10"
    }
  },

  "msv_schema": {
    "transport": {
      "tempo_bpm": { "min": 48, "max": 128, "default": 74 },
      "swing": { "min": 0.0, "max": 0.5, "default": 0.08 },
      "pulse_stability": { "min": 0.0, "max": 1.0, "default": 0.7 }
    },
    "rhythm": {
      "rhythm_density": { "min": 0.0, "max": 1.0, "default": 0.35 },
      "syncopation": { "min": 0.0, "max": 1.0, "default": 0.25 },
      "percussive_focus": { "min": 0.0, "max": 1.0, "default": 0.2 }
    },
    "harmony": {
      "harmonic_tension": { "min": 0.0, "max": 1.0, "default": 0.3 },
      "cadence_stability": { "min": 0.0, "max": 1.0, "default": 0.6 },
      "mode_blend": {
        "ionian": 0.25,
        "dorian": 0.12,
        "aeolian": 0.22,
        "mixolydian": 0.14,
        "lydian": 0.12,
        "phrygian": 0.05,
        "locrian": 0.0
      },
      "transpose_semitones": { "min": -5, "max": 5, "default": 0 }
    },
    "melody": {
      "melodic_activity": { "min": 0.0, "max": 1.0, "default": 0.4 },
      "interval_leap_bias": { "min": -1.0, "max": 1.0, "default": -0.2 },
      "leitmotif_intensity": { "min": 0.0, "max": 1.0, "default": 0.35 },
      "memory_variation": { "min": 0.0, "max": 1.0, "default": 0.25 }
    },
    "orchestration": {
      "layer_count": { "min": 1, "max": 6, "default": 3 },
      "register_bias": { "min": -1.0, "max": 1.0, "default": 0.0 },
      "instrument_max_active": 4,
      "mix_top_k_instruments": 3,
      "instruments": {
        "felt_piano": 0.5,
        "nylon_guitar": 0.2,
        "warm_strings": 0.35,
        "soft_woodwinds": 0.15,
        "brush_kit": 0.2,
        "rim_clicks": 0.1,
        "shaker": 0.1,
        "warm_pad": 0.2,
        "soft_pluck": 0.15,
        "glass_bells": 0.08,
        "tape_choir": 0.1,
        "field_cafe": 0.0,
        "field_rain": 0.0
      }
    },
    "fx": {
      "reverb_wet": { "min": 0.0, "max": 0.5, "default": 0.18 },
      "delay_wet": { "min": 0.0, "max": 0.35, "default": 0.1 },
      "tape_saturation": { "min": 0.0, "max": 0.5, "default": 0.12 },
      "noise_film_grain": { "min": 0.0, "max": 0.25, "default": 0.08 }
    },
    "brand_safety": {
      "brightness_ceiling": 0.65,
      "no_slot_machine_shine": true,
      "battery_friendly": true
    }
  },

  "algorithm": {
    "update_order": [
      "ingest_signal",
      "select_rule_block",
      "compute_raw_deltas",
      "apply_conflict_checks",
      "normalize_groups",
      "smooth_and_schedule",
      "emit_msv"
    ],
    "smoothing": {
      "ema_alpha": 0.22,
      "bar_quantize": "apply_at_next_bar",
      "crossfade_ms": 750
    },
    "normalization": {
      "instrument_weights_top_k": 3,
      "instrument_min_weight": 0.05,
      "group_sum_caps": {
        "instruments": 1.0,
        "mode_blend": 1.0
      }
    }
  },

  "taxonomies": {
    "emotional_states": {
      "energizing_positive": ["MOTIVATED", "INSPIRED", "EXCITED", "CONFIDENT"],
      "calm_positive": ["CONTENT", "PEACEFUL", "GRATEFUL", "REFLECTIVE"],
      "tense_negative": ["ANXIOUS", "WORRIED", "STRESSED"],
      "low_negative": ["SAD", "DISCOURAGED", "EXHAUSTED", "OVERWHELMED"]
    },
    "event_categories": [
      "SOCIAL",
      "RELATIONSHIP",
      "ASPIRATION",
      "CAREER",
      "ROUTINE",
      "CRISIS",
      "OPPORTUNITY",
      "MYSTERY_HOOK"
    ],
    "arc_beats": ["ACT_I_SETUP", "ACT_II_COMPLICATION", "ACT_III_RESOLUTION"],
    "tension_hooks": ["MYSTERY_PLANTED", "REVEAL_PARTIAL", "OPPORTUNITY_THREATENED", "RELATIONSHIP_SHIFT", "EXTERNAL_PRESSURE"],
    "stakes_levels": ["LOW", "MODERATE", "HIGH", "VERY_HIGH", "MAX"]
  },

  "rules": {
    "by_emotional_state": [
      {
        "match": { "state_in": ["MOTIVATED"] },
        "deltas": {
          "transport": { "tempo_bpm": +6, "pulse_stability": +0.1 },
          "rhythm": { "rhythm_density": +0.15, "syncopation": +0.05 },
          "harmony": { "harmonic_tension": +0.05, "mode_blend.mixolydian": +0.06, "cadence_stability": +0.05 },
          "melody": { "melodic_activity": +0.1, "leitmotif_intensity": +0.08, "interval_leap_bias": +0.1 },
          "orchestration": { "layer_count": +1, "register_bias": +0.15, "instruments.felt_piano": +0.1, "instruments.warm_strings": +0.08, "instruments.brush_kit": +0.06 },
          "fx": { "reverb_wet": -0.02, "delay_wet": -0.02 }
        },
        "notes": "Productive energy; stay grounded and humane."
      },
      {
        "match": { "state_in": ["INSPIRED", "REFLECTIVE"] },
        "deltas": {
          "transport": { "tempo_bpm": +0 },
          "rhythm": { "rhythm_density": +0.05, "syncopation": +0.08 },
          "harmony": { "mode_blend.lydian": +0.06, "harmonic_tension": +0.08 },
          "melody": { "melodic_activity": +0.12, "memory_variation": +0.15, "leitmotif_intensity": +0.1 },
          "orchestration": { "instruments.warm_pad": +0.12, "instruments.glass_bells": +0.06, "register_bias": +0.1 },
          "fx": { "reverb_wet": +0.05, "delay_wet": +0.04, "tape_saturation": +0.02 }
        }
      },
      {
        "match": { "state_in": ["CONTENT", "PEACEFUL", "GRATEFUL"] },
        "deltas": {
          "transport": { "tempo_bpm": -2, "pulse_stability": +0.12, "swing": -0.03 },
          "rhythm": { "rhythm_density": -0.08, "syncopation": -0.05 },
          "harmony": { "cadence_stability": +0.12, "mode_blend.ionian": +0.1, "harmonic_tension": -0.06 },
          "melody": { "melodic_activity": -0.05, "interval_leap_bias": -0.1, "leitmotif_intensity": +0.06 },
          "orchestration": { "layer_count": -1, "register_bias": -0.05, "instruments.felt_piano": +0.08, "instruments.soft_woodwinds": +0.06, "instruments.warm_strings": +0.06 },
          "fx": { "reverb_wet": +0.03 }
        }
      },
      {
        "match": { "state_in": ["ANXIOUS", "STRESSED", "WORRIED"] },
        "deltas": {
          "transport": { "tempo_bpm": +4, "pulse_stability": -0.15 },
          "rhythm": { "rhythm_density": +0.12, "syncopation": +0.12, "percussive_focus": +0.15 },
          "harmony": { "harmonic_tension": +0.2, "mode_blend.phrygian": +0.05, "mode_blend.aeolian": +0.06, "cadence_stability": -0.1 },
          "melody": { "melodic_activity": +0.08, "interval_leap_bias": +0.1, "leitmotif_intensity": -0.06 },
          "orchestration": { "layer_count": +1, "register_bias": +0.05, "instruments.rim_clicks": +0.12, "instruments.shaker": +0.08, "instruments.warm_pad": -0.05 },
          "fx": { "reverb_wet": -0.05, "delay_wet": +0.02, "tape_saturation": +0.05 }
        }
      },
      {
        "match": { "state_in": ["SAD", "DISCOURAGED"] },
        "deltas": {
          "transport": { "tempo_bpm": -4 },
          "rhythm": { "rhythm_density": -0.12, "syncopation": -0.04 },
          "harmony": { "mode_blend.aeolian": +0.12, "harmonic_tension": +0.06, "cadence_stability": -0.05 },
          "melody": { "melodic_activity": -0.08, "interval_leap_bias": -0.15, "leitmotif_intensity": +0.12 },
          "orchestration": { "layer_count": -1, "register_bias": -0.15, "instruments.nylon_guitar": +0.08, "instruments.tape_choir": +0.06 },
          "fx": { "reverb_wet": +0.04, "delay_wet": +0.03 }
        }
      },
      {
        "match": { "state_in": ["EXHAUSTED", "OVERWHELMED"] },
        "deltas": {
          "transport": { "tempo_bpm": -6, "pulse_stability": -0.1 },
          "rhythm": { "rhythm_density": -0.2, "syncopation": -0.08, "percussive_focus": -0.1 },
          "harmony": { "harmonic_tension": +0.08, "cadence_stability": -0.08, "mode_blend.dorian": +0.04 },
          "melody": { "melodic_activity": -0.15, "leitmotif_intensity": -0.1 },
          "orchestration": { "layer_count": -2, "register_bias": -0.2, "instruments.felt_piano": +0.06, "instruments.warm_strings": -0.05, "instruments.field_rain": +0.08 },
          "fx": { "reverb_wet": +0.02, "tape_saturation": -0.04, "noise_film_grain": +0.02 }
        }
      }
    ],

    "by_emotional_capacity": [
      { "if_capacity_gte": 8.0,
        "deltas": {
          "orchestration": { "layer_count": +1, "register_bias": +0.1, "instruments.warm_strings": +0.08, "instruments.soft_woodwinds": +0.06 },
          "melody": { "leitmotif_intensity": +0.12 },
          "fx": { "reverb_wet": -0.02 }
        },
        "notes": "Perceptive, present; allow empathetic color. Capacity gates empathy moments in narrative."
      },
      { "if_capacity_between": [5.0, 7.0],
        "deltas": { "transport": { "tempo_bpm": +0 }, "orchestration": { "layer_count": +0 }, "melody": { "leitmotif_intensity": -0.04 } }
      },
      { "if_capacity_lte": 3.0,
        "deltas": {
          "transport": { "tempo_bpm": -3, "pulse_stability": -0.08 },
          "rhythm": { "rhythm_density": -0.1 },
          "orchestration": { "layer_count": -1, "instruments.felt_piano": +0.05, "instruments.field_rain": +0.06, "instruments.warm_pad": -0.08 },
          "melody": { "leitmotif_intensity": -0.12 },
          "fx": { "reverb_wet": +0.02, "delay_wet": -0.02 }
        },
        "notes": "Low capacity = diminished social perception; avoid bright textures."
      }
    ],

    "by_event_category": [
      { "match": { "category": "SOCIAL" },
        "deltas": { "rhythm": { "rhythm_density": +0.08, "swing": +0.03 }, "orchestration": { "instruments.brush_kit": +0.08, "instruments.soft_woodwinds": +0.05 } }
      },
      { "match": { "category": "RELATIONSHIP" },
        "deltas": { "melody": { "leitmotif_intensity": +0.1 }, "harmony": { "cadence_stability": +0.08 }, "orchestration": { "instruments.felt_piano": +0.1, "instruments.warm_strings": +0.1 } }
      },
      { "match": { "category": "ASPIRATION" },
        "deltas": { "transport": { "tempo_bpm": +3 }, "melody": { "melodic_activity": +0.08 }, "harmony": { "mode_blend.mixolydian": +0.05 } }
      },
      { "match": { "category": "CAREER" },
        "deltas": { "rhythm": { "percussive_focus": +0.1, "syncopation": +0.04 }, "harmony": { "harmonic_tension": +0.06 } }
      },
      { "match": { "category": "ROUTINE" },
        "deltas": { "rhythm": { "rhythm_density": -0.06 }, "melody": { "melodic_activity": -0.05 }, "orchestration": { "layer_count": -1 } }
      },
      { "match": { "category": "CRISIS" },
        "deltas": { "transport": { "tempo_bpm": +6 }, "rhythm": { "syncopation": +0.15, "percussive_focus": +0.18 }, "harmony": { "harmonic_tension": +0.25, "cadence_stability": -0.15 }, "fx": { "reverb_wet": -0.08 } }
      },
      { "match": { "category": "OPPORTUNITY" },
        "deltas": { "harmony": { "mode_blend.lydian": +0.05, "harmonic_tension": +0.06 }, "melody": { "leitmotif_intensity": +0.08 } }
      },
      { "match": { "category": "MYSTERY_HOOK" },
        "deltas": { "harmony": { "mode_blend.dorian": +0.06, "mode_blend.phrygian": +0.03 }, "fx": { "delay_wet": +0.05 }, "melody": { "memory_variation": +0.12 } }
      }
    ],

    "by_arc_beat": [
      { "match": { "act": "ACT_I_SETUP" },
        "deltas": { "orchestration": { "layer_count": -1 }, "melody": { "leitmotif_intensity": +0.06 }, "harmony": { "cadence_stability": +0.08 } }
      },
      { "match": { "act": "ACT_II_COMPLICATION" },
        "deltas": { "harmony": { "harmonic_tension": +0.12 }, "rhythm": { "syncopation": +0.08 }, "fx": { "delay_wet": +0.03 } }
      },
      { "match": { "act": "ACT_III_RESOLUTION" },
        "deltas": { "harmony": { "cadence_stability": +0.18, "harmonic_tension": -0.12 }, "melody": { "leitmotif_intensity": +0.14 }, "orchestration": { "register_bias": +0.1 } }
      }
    ],

    "tension_and_stakes": [
      { "match": { "tension_hook": "MYSTERY_PLANTED" },
        "deltas": { "fx": { "delay_wet": +0.04 }, "harmony": { "harmonic_tension": +0.08 }, "melody": { "memory_variation": +0.08 } }
      },
      { "match": { "tension_hook": "REVEAL_PARTIAL" },
        "deltas": { "harmony": { "harmonic_tension": -0.06 }, "melody": { "leitmotif_intensity": +0.08 } }
      },
      { "match": { "stakes_level": "LOW" }, "deltas": { "harmony": { "harmonic_tension": +0.02 } } },
      { "match": { "stakes_level": "MODERATE" }, "deltas": { "harmony": { "harmonic_tension": +0.08 }, "rhythm": { "rhythm_density": +0.06 } } },
      { "match": { "stakes_level": "HIGH" }, "deltas": { "transport": { "tempo_bpm": +4 }, "harmony": { "harmonic_tension": +0.16 }, "rhythm": { "syncopation": +0.1 } } },
      { "match": { "stakes_level": "VERY_HIGH" }, "deltas": { "transport": { "tempo_bpm": +6 }, "harmony": { "harmonic_tension": +0.22 }, "fx": { "reverb_wet": -0.06 } } },
      { "match": { "stakes_level": "MAX" }, "deltas": { "transport": { "tempo_bpm": +8 }, "harmony": { "harmonic_tension": +0.28, "cadence_stability": -0.18 }, "rhythm": { "percussive_focus": +0.2 } } }
    ],

    "decisive_decision": {
      "match": { "is_decisive_decision": true },
      "pre_roll": { "bar_hold": 2, "fade_out_ms": 400 },
      "deltas": {
        "transport": { "tempo_bpm": -2, "pulse_stability": +0.2 },
        "rhythm": { "rhythm_density": -0.12, "syncopation": -0.08 },
        "harmony": { "cadence_stability": +0.2, "harmonic_tension": -0.1 },
        "melody": { "leitmotif_intensity": +0.16 },
        "fx": { "reverb_wet": -0.04, "delay_wet": -0.03 }
      },
      "post_confirm": {
        "success": { "harmony": { "cadence_stability": +0.12 }, "melody": { "leitmotif_intensity": +0.12 } },
        "costly": { "harmony": { "harmonic_tension": +0.1 }, "transport": { "tempo_bpm": -1 } }
      }
    },

    "dramatic_irony": {
      "enabled": true,
      "gate": { "knowledge_gap_score_min": 0.6 },
      "capacity_effects": {
        "if_capacity_gte_8": { "melody": { "leitmotif_intensity": +0.12 }, "orchestration": { "instruments.soft_woodwinds": +0.08 } },
        "if_capacity_lte_3": { "melody": { "leitmotif_intensity": -0.1 }, "orchestration": { "instruments.felt_piano": +0.06, "instruments.warm_strings": -0.06 } }
      }
    },

    "emotional_memory_echo": {
      "on_echo_surface": {
        "deltas": {
          "melody": { "memory_variation": +0.2, "leitmotif_intensity": +0.08 },
          "fx": { "tape_saturation": +0.02, "delay_wet": +0.03 }
        },
        "cooldown_bars": 16,
        "max_per_scene": 2
      }
    }
  },

  "conflict_checks": [
    {
      "id": "privacy_first_and_battery",
      "if": { "fx.reverb_wet": ">0.45" },
      "then": [ { "set": { "fx.reverb_wet": 0.45 } }, { "note": "Respect calm/battery-friendly visuals in audio domain." } ]
    },
    {
      "id": "decision_clarity",
      "if_scene_flag": "is_decisive_decision",
      "then": [
        { "mul": { "fx.reverb_wet": 0.85, "fx.delay_wet": 0.75 } },
        { "set_min": { "pulse_stability": 0.65 } }
      ]
    },
    {
      "id": "arc_coherence",
      "if": { "arc": "ACT_III_RESOLUTION", "and_harmonic_tension_over": 0.5 },
      "then": [ { "lerp_to": { "harmony.harmonic_tension": 0.3, "amount": 0.6 } }, { "add": { "harmony.cadence_stability": 0.12 } } ]
    },
    {
      "id": "instrument_top_k",
      "apply": "keep_top_k",
      "args": { "group": "orchestration.instruments", "k": 3, "min_weight": 0.05 }
    },
    {
      "id": "capacity_filter_for_empathy",
      "if": { "capacity_lt": 4.0 },
      "then": [ { "add": { "melody.leitmotif_intensity": -0.06 } }, { "add": { "orchestration.instruments.warm_strings": -0.06 } } ]
    },
    {
      "id": "tension_hygiene",
      "if": { "stakes": "MAX", "and": { "act_not": "ACT_III_RESOLUTION" } },
      "then": [ { "cap": { "fx.reverb_wet": 0.15 } }, { "add": { "rhythm.percussive_focus": +0.06 } } ]
    }
  ],

  "scheduler": {
    "apply_at": "next_bar",
    "hold_bars_on_decision": 2,
    "loop_forms": {
      "low_tension": "A A' B A'",
      "high_tension": "A B A'' C",
      "resolution": "A B A"
    }
  },

  "output_contract": {
    "type": "msv_delta",
    "fields": [
      "transport.tempo_bpm", "transport.swing", "transport.pulse_stability",
      "rhythm.rhythm_density", "rhythm.syncopation", "rhythm.percussive_focus",
      "harmony.harmonic_tension", "harmony.cadence_stability", "harmony.mode_blend.*", "harmony.transpose_semitones",
      "melody.melodic_activity", "melody.interval_leap_bias", "melody.leitmotif_intensity", "melody.memory_variation",
      "orchestration.layer_count", "orchestration.register_bias", "orchestration.instruments.*",
      "fx.reverb_wet", "fx.delay_wet", "fx.tape_saturation", "fx.noise_film_grain"
    ],
    "postconditions": [
      "mode_blend weights sum to ≤ 1.0; renormalize if > 1.0",
      "orchestration.instruments obey top_k & min_weight",
      "respect brightness_ceiling and battery_friendly constraints"
    ]
  }
}
```

### Why this matches your systems

* **Capacity-aware:** low capacity reduces perceptual/empathetic colors; high capacity opens them up — exactly how your dramatic-irony & stakes specs behave (knowledge-gap ≥ 0.6 gate; capacity 8 vs 2 perception).  
* **Decisions pause time, calm UI:** the “decisive_decision” block clamps ambience and quantizes changes at barlines to keep things clear and humane. 
* **Arc-aware tension:** Act II raises tension/syncopation; Act III restores cadence stability for closure — mirroring your 3-act scaffolding and consequence chains. 
* **Echoes & memory:** surfacing an Emotional Echo boosts leitmotif variation briefly, with a cooldown to avoid fatigue, matching your resonance/priority rules. 
* **Stakes escalation:** stakes levels push harmonic tension/tempo and trim reverb to avoid mush during intensity. 
