# Unwritten: JSON Data Contracts & Technical Specifications

## Data Contract Philosophy

All game systems communicate through standardized JSON structures. This enables:
- AI agents to generate consistent content
- System interoperability
- Easy data persistence
- Clear technical specifications

**Related Systems:**
- **Character Creation (`20-character-creation.md`):** Starting character JSON output
- **Turn Structure (`21-turn-structure.md`):** Turn state and card resolution data
- **Multi-Lifetime Continuity (`22-multi-lifetime-continuity.md`):** Four-tier context structures
- **Novel Generation (`novel-generation-data-structure.md`):** Chapter generation packets

---

## Card Type Schemas

### Base Card JSON Structure

```json
{
  "id": "card_unique_id",
  "type": "character|activity|location|emotion|resource",
  "base_or_evolved": "base|evolved",
  "level": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "pack": "Base|Premium|DLC_Name",
  "rarity": "common|uncommon|rare|epic|legendary",
  "version": "1.0"
}
```

---

### Character (NPC) Card JSON

```json
{
  "type": "npc",
  "id": "sarah-anderson",
  "display_name": "Sarah Anderson",
  "archetype": "Barista → Bookshop Co-Owner",
  
  "personality": {
    "openness": 4.3,
    "conscientiousness": 4.2,
    "extraversion": 3.4,
    "agreeableness": 4.6,
    "neuroticism": 2.9
  },
  
  "relationship_level": 3,
  "relationship_label": "Friend",
  "trust": 0.75,
  "attraction": 0.45,
  
  "_schema_notes": {
    "relationship_level": "Range 0-5 (0=Not Met, 1=Stranger, 2=Acquaintance, 3=Friend, 4=Close Friend, 5=Soulmate)",
    "display_rule": "Never show 'Level 0' in UI - display 'Not Met' instead",
    "level_up_requires": "Both interaction_count >= threshold AND trust >= threshold"
  },
  
  "memories": [
    {
      "id": "mem_001",
      "timestamp": "Week 2, Day 3",
      "event": "coffee_deep_conversation",
      "location": "cafe_luna",
      "description": "Late night at Café Luna. Sarah's hands wrapped around cold mug, speaking quietly about fear of failure...",
      "emotion": "vulnerable_solidarity",
      "weight": 0.85,
      "tags": ["vulnerability", "shared_fears", "trust_building"],
      "personality_impact": {
        "neuroticism": -0.2,
        "agreeableness": +0.15
      }
    }
  ],
  
  "portrait": {
    "identity_lock": [
      "eye_color:brown",
      "freckles:light",
      "hair:light_brown_wavy"
    ],
    "signature_items": [
      "cerulean_blue_scarf",
      "grandmother_locket"
    ],
    "current_expression": "determined",
    "style_pack": "current-style-pack",
    "evolution_stage": 3
  },
  
  "description": "Sarah trusted you with her deepest fear—and her grandmother's gift. She's been carrying $15k meant for 'something brave.'",
  
  "micro_narrative": "She recommends books you didn't know you needed.",
  
  "fusion_hooks": [
    "bookshop_dreams",
    "mentorship",
    "entrepreneurship",
    "literary_passion"
  ],
  
  "unlocked_activities": [
    "business_planning",
    "grandmother_grave_visit",
    "bookstore_hunting"
  ],
  
  "relationship_history": {
    "first_met": "Week 1, Day 3",
    "total_interactions": 47,
    "last_interaction": "Week 12, Day 5",
    "milestone_moments": [
      "Week 2: First real conversation",
      "Week 5: Shared bookshop dream",
      "Week 12: Late night vulnerability"
    ]
  }
}
```

---

### Activity Card JSON

```json
{
  "type": "activity",
  "id": "coffee-meetup",
  "title": "Coffee Meetup",
  "category": "social",
  "subcategory": "casual_hangout",
  
  "base_or_evolved": "base",
  "evolution_context": null,
  
  "description": "Grab coffee with someone. Standard small talk.",
  "evolved_description": null,
  
  "costs": {
    "energy": 1,
    "time_minutes": 30,
    "money": 5,
    "social_capital": 0
  },
  
  "requirements": [
    "relationship.target>=0.1",
    "time:morning|afternoon|evening",
    "energy>=1"
  ],
  
  "effects": [
    {"meter": "SOCIAL", "delta": 1},
    {"meter": "EMOTIONAL", "delta": 0.5},
    {"relationship": "target", "delta": 0.1}
  ],
  
  "success_chance": 1.0,
  "failure_effects": [],
  
  "unlock_flags": [],
  
  "combinable_with": [
    "character_cards",
    "emotion_cards",
    "location:cafe"
  ],
  
  "visual": {
    "illustration": "generic_cafe_scene",
    "color_scheme": "warm_browns",
    "icon": "coffee_cup"
  },
  
  "micro_narrative": "Small talk over coffee. Nothing special yet."
}
```

---

### Location Card JSON

```json
{
  "type": "location",
  "id": "cafe-luna",
  "display_name": "Café Luna",
  "location_type": "public_social",
  
  "base_or_evolved": "evolved",
  "evolution_level": 3,
  
  "description": "Where you met Sarah. Where Marcus told you about his diagnosis. Where you decided to quit your job. This place holds your story.",
  
  "memories_count": 47,
  "memories_tied": [
    "mem_sarah_001",
    "mem_marcus_015",
    "mem_career_decision_023"
  ],
  
  "available_activities": [
    "work_remotely",
    "meet_friends",
    "read_alone",
    "deep_conversation",
    "people_watch"
  ],
  
  "unlocked_features": [
    "window_seat_reserved",
    "barista_knows_order",
    "nostalgia_triggers"
  ],
  
  "atmosphere": {
    "ambiance": "cozy_intellectual",
    "noise_level": "moderate",
    "typical_crowd": "students_creatives",
    "best_time": "morning_evening"
  },
  
  "visual": {
    "illustration": "evolved_cafe_YOUR_corner",
    "details": [
      "window_seat_with_plant",
      "art_on_wall_you_noticed",
      "familiar_barista"
    ],
    "lighting": "warm_golden_hour"
  },
  
  "special_effects": {
    "when_played_alone": "may_trigger_nostalgic_event",
    "when_with_sarah": "ritual_bonus",
    "memories_display": "timeline_view_available"
  }
}
```

---

### Emotion Card JSON

```json
{
  "type": "emotion",
  "id": "curiosity",
  "display_name": "Curiosity",
  "emotion_category": "positive",
  "intensity": 0.7,
  
  "description": "Feeling interested in something new. Open to possibilities.",
  
  "modifiers": {
    "openness_bonus": 0.2,
    "learning_speed": 1.2,
    "social_outcomes": "positive_boost"
  },
  
  "affects_next_card": true,
  "duration_turns": 1,
  
  "combinable_with": [
    "any_character_card",
    "any_activity_card"
  ],
  
  "dialogue_options_unlocked": [
    "ask_deeper_questions",
    "suggest_new_activity",
    "share_excitement"
  ],
  
  "visual": {
    "color": "bright_yellow",
    "particle_effect": "sparkles",
    "icon": "lightbulb"
  }
}
```

---

## Fusion Card JSON

```json
{
  "type": "fusion",
  "id": "bookshop-dream-quest",
  "title": "THE BOOKSHOP DREAM",
  "fusion_type": "triple_combination",
  "rarity": "epic",
  
  "parent_cards": [
    "sarah-anderson-lvl3",
    "bookstore-visit",
    "excitement-emotion"
  ],
  
  "description": "After months of talks, Sarah shared her actual business plan. She wants YOU to be part of it. This is real.",
  
  "quest_data": {
    "is_quest": true,
    "quest_type": "life_decision",
    "quest_stages": 5,
    "current_stage": 1
  },
  
  "choices": [
    {
      "id": "invest_savings",
      "label": "Invest Savings",
      "description": "Put your money where your belief is.",
      "risk": "high",
      "cost": {"money": 10000, "career_stability": -0.3},
      "reward": {"sarah_bond": 0.3, "new_career_path": true},
      "consequences": "permanent_relationship_shift"
    },
    {
      "id": "part_time_help",
      "label": "Offer Part-Time Help",
      "description": "Support without full commitment.",
      "risk": "medium",
      "cost": {"time": 10, "energy": 2},
      "reward": {"sarah_bond": 0.15},
      "consequences": "moderate_involvement"
    },
    {
      "id": "encourage_distance",
      "label": "Encourage But Stay Out",
      "description": "Emotionally supportive, practically distant.",
      "risk": "low",
      "cost": {},
      "reward": {"sarah_bond": 0.05},
      "consequences": "safe_but_less_connected"
    }
  ],
  
  "permanent_effects": true,
  "can_be_undone": false,
  
  "visual": {
    "illustration": "sarah_business_plan_custom",
    "border": "purple_epic",
    "effects": "shimmer_glow",
    "background": "bookshop_imagined"
  },
  
  "micro_narrative": "This decision will permanently alter your relationship path.",
  
  "unlock_conditions": {
    "sarah_level": ">=3",
    "trust": ">=0.6",
    "bookstore_visits": ">=5",
    "phase": "establishment|peak"
  }
}
```

---

## Archive Entry JSON

```json
{
  "run_id": "run_20250115_001",
  "run_title": "The Bookshop Dream",
  "user_id": "user_12345",
  
  "dates": {
    "started": "2025-01-15T10:00:00Z",
    "ended": "2025-03-22T18:30:00Z",
    "duration_days": 287
  },
  
  "ending": {
    "ending_type": "moved_to_new_city",
    "ending_description": "Started business with Sarah, left city for new chapter",
    "ending_satisfaction": 0.92
  },
  
  "statistics": {
    "relationships": {
      "total_npcs_met": 42,
      "level_5": 5,
      "level_4": 8,
      "level_3": 15,
      "deepest_bond": {
        "npc": "sarah-anderson",
        "bond_score": 0.98
      }
    },
    
    "activities": {
      "total_activities": 487,
      "coffee_meetups": 87,
      "bookstore_visits": 23,
      "deep_conversations": 34,
      "business_planning": 17,
      "celebrations": 12
    },
    
    "achievements": [
      {"id": "dream_builder", "unlocked": "Week 40"},
      {"id": "best_friend_forever", "count": 5},
      {"id": "entrepreneur", "unlocked": "Week 28"},
      {"id": "community_builder", "unlocked": "Week 45"},
      {"id": "found_family", "unlocked": "Week 35"}
    ],
    
    "fusions": {
      "total_evolutions": 147,
      "legendary_fusions": 3,
      "unique_cards_created": 47
    },
    
    "financial": {
      "starting_money": 5000,
      "ending_money": 23000,
      "business_invested": 15000,
      "total_earned": 45000
    }
  },
  
  "evolved_cards": [
    // Array of full card JSONs
  ],
  
  "story_log": [
    {
      "week": 1,
      "title": "New Beginnings",
      "events": [
        {"day": 1, "description": "Moved to city"},
        {"day": 3, "description": "Met Sarah at coffee shop"},
        {"day": 5, "description": "Explored neighborhood"}
      ]
    }
    // ... continues
  ],
  
  "highlights": [
    {
      "week": 3,
      "title": "That Coffee",
      "description": "Sarah first opened up about her passion for vintage books. You noticed her eyes light up.",
      "weight": 0.8
    },
    {
      "week": 12,
      "title": "Late Night at Luna",
      "description": "'Then we'll both be brave failures together.' The moment everything changed.",
      "weight": 0.95
    }
    // ... more highlights
  ],
  
  "book_generated": {
    "free_book_url": "storage/books/run_001_free.pdf",
    "premium_novel_url": "storage/books/run_001_premium.pdf",
    "word_count_free": 4523,
    "word_count_premium": 14782
  },
  
  "shareable": {
    "public_url": "https://unwritten.game/archive/user123/run1",
    "share_count": 47,
    "views": 892
  }
}
```

---

## AI Generation Prompt Contract

### Input Context JSON

```json
{
  "generation_type": "character_evolution|dialogue|fusion|memory",
  "target_card_id": "sarah-anderson",
  
  "immediate_context": {
    "event": "coffee_deep_conversation",
    "player_choice": "supportive_listening",
    "emotion_active": "empathy",
    "location": "cafe_luna"
  },
  
  "relationship_context": {
    "current_level": 2,
    "trust": 0.55,
    "attraction": 0.35,
    "total_interactions": 12,
    "last_interaction": "3_days_ago"
  },
  
  "memory_context": [
    {
      "event": "bookstore_visit",
      "weight": 0.7,
      "recency": "1_week_ago"
    },
    {
      "event": "helped_move",
      "weight": 0.75,
      "recency": "2_weeks_ago"
    }
  ],
  
  "personality_current": {
    "openness": 3.7,
    "conscientiousness": 4.0,
    "extraversion": 3.0,
    "agreeableness": 4.1,
    "neuroticism": 3.5
  },
  
  "player_tendencies": {
    "conversation_style": "supportive, curious, not pushy",
    "activity_preferences": ["cultural", "quiet", "intellectual"],
    "relationship_pace": "slow-burn"
  },
  
  "life_context": {
    "player_career": "software_developer",
    "player_stress": 6.5,
    "recent_events": ["promotion", "apartment_move"],
    "current_phase": "establishment"
  },
  
  "generation_constraints": {
    "personality_shift_max": 0.3,
    "memory_weight_target": "0.7-0.9",
    "description_max_words": 100,
    "micro_narrative_max_words": 20,
    "must_reference_previous": true,
    "maintain_consistency": true
  }
}
```

---

### AI Output JSON

```json
{
  "generation_id": "gen_20250115_123456",
  "generation_type": "character_evolution",
  "target_card_id": "sarah-anderson",
  "timestamp": "2025-01-15T14:30:00Z",
  
  "new_memory": {
    "id": "mem_sarah_012",
    "description": "Late night at Café Luna. Sarah's hands wrapped around a cold mug, speaking quietly about the fear of trying and failing. 'What if I open the shop and no one comes?' she said. You told her about your own fear of the promotion. She smiled and said, 'Then we'll both be brave failures together.'",
    "emotion": "vulnerable_solidarity",
    "weight": 0.85,
    "setting": "cafe_luna_after_closing",
    "key_quote": "Then we'll both be brave failures together.",
    "tags": ["vulnerability", "shared_fears", "trust", "mutual_support"]
  },
  
  "personality_shifts": {
    "openness": 0.1,
    "agreeableness": 0.15,
    "neuroticism": -0.2,
    "reasoning": "Sharing fear and receiving support reduces anxiety, builds trust"
  },
  
  "new_detail": {
    "revelation": "Her grandmother left her $15,000 specifically for 'something brave.' Sarah's been too scared to use it. Until maybe now.",
    "significance": "sacred_money",
    "emotional_weight": "high",
    "story_implications": "adds stakes to bookshop decision"
  },
  
  "unlocked_combinations": [
    {
      "fusion_id": "business_planning_sarah",
      "required_cards": ["sarah", "cafe_luna", "notebook"],
      "description": "Help Sarah actually plan the bookshop",
      "unlock_phase": "current"
    },
    {
      "fusion_id": "grandmother_grave",
      "required_cards": ["sarah", "cemetery", "flowers"],
      "description": "Visit grandmother's grave together",
      "unlock_phase": "current"
    }
  ],
  
  "portrait_update": {
    "add_element": "small_notebook_in_bag",
    "description": "Business plan notebook visible",
    "expression_change": "more_determined_less_uncertain",
    "visual_evolution_stage": 3
  },
  
  "updated_description": "Sarah trusted you with her deepest fear—and her grandmother's gift. She's been carrying $15k meant for 'something brave.' The question isn't if she'll do it anymore, it's when.",
  
  "micro_narrative": "'Then we'll both be brave failures together.' Your shared vulnerability changed something.",
  
  "relationship_progression": {
    "level_up": false,
    "level_up_progress": 0.73,
    "next_milestone": "level_3_close_friend",
    "trust_change": 0.08,
    "attraction_change": 0.05
  }
}
```

---

## Game State JSON

```json
{
  "user_id": "user_12345",
  "current_run_id": "run_20250115_001",
  
  "run_meta": {
    "started": "2025-01-15T10:00:00Z",
    "current_day": 87,
    "current_week": 12,
    "current_phase": "establishment",
    "life_direction": "creative_fulfillment"
  },
  
  "player_state": {
    "meters": {
      "physical": 7.2,
      "mental": 6.8,
      "social": 8.1,
      "emotional": 7.5
    },
    
    "resources": {
      "energy_current": 5,
      "energy_max": 8,
      "money": 12500,
      "social_capital": 7
    },
    
    "career": {
      "job": "software_developer",
      "level": 3,
      "salary_monthly": 6500,
      "satisfaction": 0.72
    },
    
    "skills": {
      "cooking": 5,
      "programming": 8,
      "social": 6,
      "creative_writing": 4
    }
  },
  
  "active_cards": {
    "deck_size": 127,
    "characters": 15,
    "activities": 45,
    "locations": 12,
    "resources": 8,
    "evolutions": 47
  },
  
  "active_relationships": [
    {
      "npc_id": "sarah-anderson",
      "level": 3,
      "trust": 0.75,
      "attraction": 0.45,
      "last_interaction": "2_hours_ago"
    },
    {
      "npc_id": "marcus-rivera",
      "level": 4,
      "trust": 0.82,
      "attraction": 0.15,
      "last_interaction": "1_day_ago"
    }
  ],
  
  "active_aspirations": [
    {
      "id": "master_programming",
      "progress": 0.68,
      "deadline": "week_24"
    },
    {
      "id": "deep_friendship_5x",
      "progress": 0.60,
      "deadline": "week_52"
    }
  ],
  
  "unlocks": {
    "total_base_cards_unlocked": 347,
    "legendary_fusions_available": 2,
    "special_events_unlocked": 5
  }
}
```

---

## Technical Specifications

### API Endpoints

```
POST /api/v1/card/evolve
Body: {context: {...}, target_card: "id"}
Response: {evolved_card: {...}, ai_output: {...}}

POST /api/v1/fusion/attempt
Body: {cards: ["id1", "id2", "id3"], context: {...}}
Response: {fusion_result: {...}, success: true}

GET /api/v1/archive/run/{run_id}
Response: {archive_data: {...}}

POST /api/v1/ai/generate
Body: {prompt_context: {...}, generation_type: "..."}
Response: {ai_output: {...}}
```

---

### Performance Targets

```json
{
  "local_ai_generation": "< 750ms",
  "cloud_ai_generation": "< 200ms",
  "card_render": "< 100ms",
  "fusion_detection": "< 50ms",
  "save_operation": "< 200ms",
  "archive_load": "< 500ms"
}
```

---

### Storage Requirements

```json
{
  "base_card_db": "~10MB",
  "evolved_cards_per_run": "~5MB",
  "archive_per_run": "~8MB",
  "portrait_cache": "~50MB",
  "total_app_size": "< 200MB"
}
```

---

## Version Control

```json
{
  "schema_version": "1.0",
  "breaking_changes": false,
  "migration_path": "v0.9_to_v1.0.json",
  "deprecation_warnings": [],
  "new_fields": [
    "character.fusion_hooks",
    "archive.shareable.views"
  ]
}
```

---

## Design Principles

### 1. Consistent Structure
All card types follow similar JSON patterns.

### 2. Forward Compatible
New fields can be added without breaking old saves.

### 3. Human Readable
JSON is formatted for debugging and understanding.

### 4. Validation Ready
Clear types and constraints for validation.

### 5. AI Friendly
Structure optimized for AI generation and parsing.

