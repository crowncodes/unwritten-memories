Awesome—here’s a production-ready Holo Card JSON spec you can drop into your engine. It includes a strict JSON Schema for validation, an example payload (Sarah “Legacy Gold Holo”), and minimal integration notes (Unity/Unreal).


---

Holo Card JSON — Authoritative Schema (Draft-07)

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://unwritten.game/schemas/holo_card.schema.json",
  "title": "HoloCard",
  "type": "object",
  "required": [
    "version",
    "id",
    "npc",
    "rarity",
    "stylePack",
    "visual",
    "animation",
    "foil",
    "unlock",
    "economy",
    "i18n",
    "telemetry"
  ],
  "properties": {
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },

    "id": { "type": "string", "pattern": "^[a-z0-9-_.]+$" },

    "series": {
      "type": "object",
      "required": ["code", "name"],
      "properties": {
        "code": { "type": "string" },
        "name": { "type": "string" },
        "season": { "type": "string" },
        "event": { "type": "string" } 
      }
    },

    "npc": {
      "type": "object",
      "required": ["npcId", "level", "identityLock"],
      "properties": {
        "npcId": { "type": "string" },
        "level": { "type": "integer", "minimum": 1, "maximum": 5 },
        "identityLock": {
          "type": "object",
          "required": ["eyeColor", "hairColor", "skinTone", "freckles", "signatureItems"],
          "properties": {
            "eyeColor": { "type": "string" },
            "hairColor": { "type": "string" },
            "skinTone": { "type": "string" },
            "freckles": { "type": "string", "enum": ["none","light","visible","heavy"] },
            "signatureItems": { "type": "array", "items": { "type": "string" }, "minItems": 0 }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },

    "rarity": { "type": "string", "enum": ["Epic","Legendary","Mythic"] },

    "stylePack": {
      "type": "object",
      "required": ["id","name"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      }
    },

    "visual": {
      "type": "object",
      "required": ["resolution","base","depth","posterFrame","thumbnails"],
      "properties": {
        "resolution": { "type": "string", "pattern": "^[0-9]+x[0-9]+$" },
        "aspect": { "type": "string", "enum": ["1:1","4:5","9:16"] },
        "base": { "type": "string" },   /* static portrait PNG */
        "depth": { "type": "string" },  /* parallax bg PNG */
        "posterFrame": { "type": "string" },  /* PNG frame for grid */
        "thumbnails": {
          "type": "object",
          "required": ["sm","md","lg"],
          "properties": {
            "sm": { "type": "string" },
            "md": { "type": "string" },
            "lg": { "type": "string" }
          }
        },
        "colorGrade": {
          "type": "object",
          "properties": {
            "lut": { "type": "string" },
            "temperature": { "type": "number", "minimum": -1, "maximum": 1 },
            "tint": { "type": "number", "minimum": -1, "maximum": 1 }
          }
        }
      },
      "additionalProperties": false
    },

    "animation": {
      "type": "object",
      "required": ["duration","fps","loop","video"],
      "properties": {
        "duration": { "type": "number", "minimum": 5, "maximum": 12 },
        "fps": { "type": "integer", "enum": [24,25,30,60] },
        "loop": { "type": "boolean" },
        "camera": {
          "type": "object",
          "properties": {
            "movement": { "type": "string", "enum": ["none","slow_push_in","slow_pan","parallax_only"] },
            "parallaxLayers": { "type": "integer", "minimum": 0, "maximum": 4 },
            "focusDepth": { "type": "string", "enum": ["subject","mid","background"] }
          }
        },
        "emotionCurve": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["t","expression","intensity"],
            "properties": {
              "t": { "type": "number", "minimum": 0, "maximum": 1 },
              "expression": { "type": "string", "enum": ["neutral","warm_smile","confident","serene","reflective","joyful","determined"] },
              "intensity": { "type": "number", "minimum": 0, "maximum": 1 }
            }
          }
        },
        "microMotion": {
          "type": "object",
          "properties": {
            "blinkIntervalSec": { "type": "number", "minimum": 2, "maximum": 8 },
            "breathAmplitude": { "type": "number", "minimum": 0, "maximum": 1 },
            "hairSway": { "type": "number", "minimum": 0, "maximum": 1 },
            "clothSway": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "video": {
          "type": "object",
          "required": ["webm","mp4"],
          "properties": {
            "webm": { "type": "string" },
            "mp4": { "type": "string" },
            "alpha": { "type": "boolean" }
          }
        }
      },
      "additionalProperties": false
    },

    "foil": {
      "type": "object",
      "required": ["enabled","intensity","gradient","particles"],
      "properties": {
        "enabled": { "type": "boolean" },
        "intensity": { "type": "number", "minimum": 0, "maximum": 1 },
        "gradient": {
          "type": "object",
          "required": ["palette","directionDeg","speed"],
          "properties": {
            "palette": {
              "type": "array",
              "items": { "type": "string", "pattern": "^#([0-9a-fA-F]{6})$" },
              "minItems": 2
            },
            "directionDeg": { "type": "number", "minimum": -180, "maximum": 180 },
            "speed": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "particles": {
          "type": "object",
          "properties": {
            "count": { "type": "integer", "minimum": 0, "maximum": 64 },
            "type": { "type": "string", "enum": ["spark","mote","page_glint","dust"] },
            "spawnArea": { "type": "string", "enum": ["full","border","subject","bg"] },
            "lifetimeSec": { "type": "number", "minimum": 0.2, "maximum": 5 },
            "sizePx": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 }
          }
        }
      },
      "additionalProperties": false
    },

    "unlock": {
      "type": "object",
      "required": ["conditions","grants"],
      "properties": {
        "conditions": {
          "type": "array",
          "items": { "type": "string" } 
        },
        "grants": {
          "type": "array",
          "items": { "type": "string" } 
        },
        "limited": {
          "type": "object",
          "properties": {
            "start": { "type": "string", "format": "date-time" },
            "end": { "type": "string", "format": "date-time" },
            "maxMints": { "type": "integer", "minimum": 1 }
          }
        }
      }
    },

    "economy": {
      "type": "object",
      "required": ["isPremium","priceUSD"],
      "properties": {
        "isPremium": { "type": "boolean" },
        "priceUSD": { "type": "number", "minimum": 0 },
        "softCurrency": { "type": "integer", "minimum": 0 },
        "bundleIds": { "type": "array", "items": { "type": "string" } }
      }
    },

    "i18n": {
      "type": "object",
      "required": ["displayName","tagline","description"],
      "properties": {
        "displayName": { "type": "string" },
        "tagline": { "type": "string" },
        "description": { "type": "string" },
        "locale": { "type": "string", "default": "en-US" }
      }
    },

    "telemetry": {
      "type": "object",
      "required": ["createdAt","createdBy","sourcePortraitId"],
      "properties": {
        "createdAt": { "type": "string", "format": "date-time" },
        "createdBy": { "type": "string" },
        "sourcePortraitId": { "type": "string" },
        "generator": { "type": "string" },
        "checksum": { "type": "string" }
      }
    },

    "hooks": {
      "type": "object",
      "properties": {
        "onUnlock": { "type": "string" },
        "onEquip": { "type": "string" },
        "onPlay": { "type": "string" },
        "onInspect": { "type": "string" }
      }
    },

    "cdn": {
      "type": "object",
      "properties": {
        "baseUri": { "type": "string" },
        "cacheKey": { "type": "string" },
        "ttlSec": { "type": "integer", "minimum": 60 }
      }
    }
  },
  "additionalProperties": false
}


---

Example Payload — Sarah “Legacy Gold Holo”

{
  "version": "1.0.0",
  "id": "holo_sarah_legacy_gold_v1",
  "series": { "code": "ARCHIVE-GOLD", "name": "Archive Gold Edition", "season": "S1" },

  "npc": {
    "npcId": "sarah-anderson",
    "level": 5,
    "identityLock": {
      "eyeColor": "brown",
      "hairColor": "light_brown",
      "skinTone": "fair",
      "freckles": "light",
      "signatureItems": ["cerulean_blue_scarf", "golden_locket"]
    }
  },

  "rarity": "Legendary",
  "stylePack": { "id": "french-impressionist", "name": "French Impressionist" },

  "visual": {
    "resolution": "1024x1024",
    "aspect": "1:1",
    "base": "cdn://unwritten/assets/portraits/sarah_l5_base.png",
    "depth": "cdn://unwritten/assets/portraits/sarah_l5_depth.png",
    "posterFrame": "cdn://unwritten/assets/posters/sarah_legacy_gold_poster.png",
    "thumbnails": {
      "sm": "cdn://unwritten/thumbs/sarah_gold_sm.png",
      "md": "cdn://unwritten/thumbs/sarah_gold_md.png",
      "lg": "cdn://unwritten/thumbs/sarah_gold_lg.png"
    },
    "colorGrade": {
      "lut": "cdn://unwritten/luts/golden_hour.cube",
      "temperature": 0.3,
      "tint": 0.05
    }
  },

  "animation": {
    "duration": 7.5,
    "fps": 30,
    "loop": true,
    "camera": { "movement": "slow_push_in", "parallaxLayers": 2, "focusDepth": "subject" },
    "emotionCurve": [
      { "t": 0.0, "expression": "serene", "intensity": 0.2 },
      { "t": 0.5, "expression": "joyful", "intensity": 0.5 },
      { "t": 1.0, "expression": "serene", "intensity": 0.2 }
    ],
    "microMotion": { "blinkIntervalSec": 5, "breathAmplitude": 0.3, "hairSway": 0.25, "clothSway": 0.25 },
    "video": {
      "webm": "cdn://unwritten/video/holo/sarah_legacy_gold_v1.webm",
      "mp4":  "cdn://unwritten/video/holo/sarah_legacy_gold_v1.mp4",
      "alpha": false
    }
  },

  "foil": {
    "enabled": true,
    "intensity": 0.85,
    "gradient": {
      "palette": ["#FFD479","#5FD9E7","#F1B6FF"],
      "directionDeg": -30,
      "speed": 0.35
    },
    "particles": {
      "count": 16,
      "type": "page_glint",
      "spawnArea": "subject",
      "lifetimeSec": 2.4,
      "sizePx": [2, 6]
    }
  },

  "unlock": {
    "conditions": [
      "npc:sarah-anderson.level>=5",
      "account:premium=true"
    ],
    "grants": [
      "gallery:archive_holo_slot+1",
      "achievement:legacy_glow"
    ],
    "limited": null
  },

  "economy": {
    "isPremium": true,
    "priceUSD": 2.99,
    "softCurrency": 0,
    "bundleIds": ["bundle_archive_gold_s1"]
  },

  "i18n": {
    "displayName": "Sarah — Legacy (Gold Holo)",
    "tagline": "Every dream leaves a shimmer in its wake.",
    "description": "A golden-hour loop with parallax bookshelves, soft foil shimmer, and a smile that brightens at midpoint.",
    "locale": "en-US"
  },

  "telemetry": {
    "createdAt": "2025-10-12T14:05:00Z",
    "createdBy": "PortraitPipeline:v3.2",
    "sourcePortraitId": "portrait_sarah_l5_frenchimp_v2",
    "generator": "AnimatedPortraitAgent:2.1",
    "checksum": "sha256:2b1f1b...abcd"
  },

  "hooks": {
    "onUnlock": "event://cards/holo/unlock",
    "onEquip": "event://cards/holo/equip",
    "onPlay": "event://cards/holo/play",
    "onInspect": "event://cards/holo/inspect"
  },

  "cdn": {
    "baseUri": "https://cdn.unwritten.game/",
    "cacheKey": "holo_sarah_legacy_gold_v1",
    "ttlSec": 604800
  }
}


---

Integration Notes (concise)

Unity (C#)

[Serializable]
public class HoloCard {
  public string version, id;
  public Series series;
  public Npc npc;
  public string rarity;
  public StylePack stylePack;
  public Visual visual;
  public AnimationCfg animation;
  public Foil foil;
  public Unlock unlock;
  public Economy economy;
  public I18n i18n;
  public Telemetry telemetry;
  public Hooks hooks;
  public Cdn cdn;
}
// Tip: Addressables for `visual.*` and `animation.video.*`,
// play WebM/MP4 via VideoPlayer, parallax with separate quads.
// Cap decoded bitrate to keep <10MB per loop in memory.

Unreal (DataTable)

Create a UScriptStruct mirroring the schema.

Store asset URIs as soft references; stream via MediaPlayer.

Material instance for foil gradient sweep (direction, speed, intensity as scalar params).

Niagara for particles using foil.particles config.


Performance Budgets

Video: ≤10 MB/loop (WebM VP9), 1024×1024 @30fps, 6–8s.

Decode: single instance ≤12 ms/frame on mid-range mobile GPU; pool decoders.

Thumbnails: eager-load; video lazy-stream on focus/inspect.

Parallax: 2 layers max on mobile; 3–4 on desktop.


Validation

Enforce schema at build time; reject if: missing identity lock, wrong rarity for level <4, or foil.enabled=false for Holo cards.



---

If you want, I can also generate:

a JSON Schema test suite (valid/invalid fixtures), and

a tiny Unity Addressables loader snippet that binds the foil gradient to a shader and Niagara particles to foil.particles.


