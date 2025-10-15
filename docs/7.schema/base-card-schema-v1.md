# Base Card Schema v1

> **Canonical Reference**: Master Truths v1.2  
> **Purpose**: JSON schema for base card definitions  
> **Last Updated**: October 14, 2025

---

## Card JSON Schema

### Complete Card Object

```json
{
  "id": "string (unique identifier, pattern: [type]_[name]_[variant])",
  "type": "string (enum: lifeDirection | aspiration | relationship | activity | routine | place | item)",
  "title": "string (display name, 3-40 characters)",
  "description": "string (2-3 sentences, player-facing)",
  "costs": {
    "energy": "number (0.0-10.0, optional)",
    "time": "number (0.0-3.0, optional)",
    "money": "number (0.0-1000.0, optional)",
    "social_capital": "number (0.0-100.0, optional)"
  },
  "effects": {
    "relationship_gain": "number (-1.0 to +1.0, optional)",
    "trust_gain": "number (-0.5 to +0.5, optional)",
    "energy_gain": "number (-10.0 to +10.0, optional)",
    "money_gain": "number (-1000.0 to +1000.0, optional)",
    "mood_impact": "number (-1.0 to +1.0, optional)"
  },
  "evolution_level": "number (0-5, default: 0)",
  "fusion_compatibility": ["string (card IDs)"],
  "requirements": {
    "relationship_level": "number (0-5, optional)",
    "trust_threshold": "number (0.0-1.0, optional)",
    "energy_minimum": "number (0.0-10.0, optional)",
    "unlocked_by": "string (card ID or event ID, optional)"
  },
  "metadata": {
    "category": "string (optional, for filtering)",
    "intensity": "string (optional: light | moderate | deep)",
    "tags": ["string (optional)"],
    "flavor_text": "string (optional, narrative context)"
  }
}
```

---

## Card Types

### 1. Life Direction Cards
**Purpose**: Define major life paths and values  
**Examples**: Career Focus, Family First, Adventure Seeker, Creative Soul

```json
{
  "id": "dir_career_focus_001",
  "type": "lifeDirection",
  "title": "Career Ambition",
  "description": "You prioritize professional achievement and building a successful career. Work comes first, and you're willing to make sacrifices to reach your goals.",
  "costs": {},
  "effects": {
    "aspiration_progress_multiplier": 1.2,
    "relationship_time_penalty": 0.8
  },
  "evolution_level": 0,
  "fusion_compatibility": ["asp_promotion_001", "asp_start_business_001"],
  "metadata": {
    "category": "life_direction",
    "archetype": "achiever"
  }
}
```

### 2. Aspiration Cards
**Purpose**: Season-long goals that drive the narrative  
**Examples**: Get Promoted, Fall in Love, Learn New Skill, Mend Relationship

```json
{
  "id": "asp_get_promoted_001",
  "type": "aspiration",
  "title": "Chase the Promotion",
  "description": "You're eyeing that corner office. A senior position just opened up, and you're determined to prove you're the right person for it.",
  "costs": {},
  "effects": {
    "season_goal": "reach_manager_role",
    "required_milestones": 5
  },
  "evolution_level": 0,
  "fusion_compatibility": [],
  "requirements": {
    "unlocked_by": "tutorial_complete"
  },
  "metadata": {
    "category": "career",
    "season_length_recommendation": 12,
    "difficulty": "moderate"
  }
}
```

### 3. Relationship Cards
**Purpose**: Represent NPCs and relationship opportunities  
**Examples**: Coffee with Sarah, Deep Talk with Mark, Meet New Friend

```json
{
  "id": "rel_sarah_coffee_001",
  "type": "relationship",
  "title": "Coffee with Sarah",
  "description": "Sarah suggested grabbing coffee this week. She's been your friend since college, and you haven't caught up in a while.",
  "costs": {
    "energy": 1.0,
    "time": 1.0,
    "money": 8.0
  },
  "effects": {
    "relationship_gain": 0.15,
    "trust_gain": 0.03,
    "mood_impact": 0.2
  },
  "evolution_level": 0,
  "fusion_compatibility": ["act_deep_talk_001", "place_cafe_downtown_001"],
  "requirements": {
    "relationship_level": 1
  },
  "metadata": {
    "npc_id": "npc_sarah_001",
    "category": "social",
    "intensity": "light",
    "tags": ["casual", "friendship", "catch_up"]
  }
}
```

### 4. Activity Cards
**Purpose**: Actions players can take (work, hobbies, self-care)  
**Examples**: Morning Jog, Work Late, Practice Guitar, Cook Dinner

```json
{
  "id": "act_morning_jog_001",
  "type": "activity",
  "title": "Morning Jog",
  "description": "Start the day with a refreshing run. Clear your head and get your blood pumping.",
  "costs": {
    "energy": 2.0,
    "time": 1.0
  },
  "effects": {
    "energy_gain": 3.0,
    "mood_impact": 0.3
  },
  "evolution_level": 0,
  "fusion_compatibility": ["act_meditation_001", "place_park_001"],
  "requirements": {
    "energy_minimum": 2.0
  },
  "metadata": {
    "category": "self_care",
    "intensity": "moderate",
    "tags": ["exercise", "morning", "health"],
    "can_be_routine": true
  }
}
```

### 5. Routine Cards
**Purpose**: Repeatable activities that can be automated  
**Examples**: Daily Commute, Weekly Groceries, Morning Coffee

```json
{
  "id": "rou_morning_coffee_001",
  "type": "routine",
  "title": "Morning Coffee Ritual",
  "description": "Your essential morning routine. Coffee, news, and a moment of peace before the day begins.",
  "costs": {
    "time": 0.5,
    "money": 3.0
  },
  "effects": {
    "energy_gain": 1.0,
    "mood_impact": 0.1
  },
  "evolution_level": 0,
  "fusion_compatibility": [],
  "requirements": {},
  "metadata": {
    "category": "daily_routine",
    "can_automate": true,
    "automation_cost": 0,
    "tags": ["morning", "coffee", "ritual"]
  }
}
```

### 6. Place Cards
**Purpose**: Locations that enable activities or provide context  
**Examples**: Downtown Cafe, City Park, Home Office, Gym

```json
{
  "id": "place_cafe_downtown_001",
  "type": "place",
  "title": "Downtown Cafe",
  "description": "A cozy cafe with good coffee and better atmosphere. Perfect for meetings, work, or just people-watching.",
  "costs": {},
  "effects": {
    "enables_activities": ["act_coffee_chat_001", "act_work_remote_001"],
    "mood_context": "relaxed"
  },
  "evolution_level": 0,
  "fusion_compatibility": ["rel_sarah_coffee_001", "act_writing_session_001"],
  "requirements": {
    "unlocked_by": "explore_neighborhood"
  },
  "metadata": {
    "category": "social_space",
    "ambiance": "cozy",
    "noise_level": "moderate",
    "tags": ["cafe", "downtown", "wifi"]
  }
}
```

### 7. Item Cards
**Purpose**: Utilities and tools that modify gameplay  
**Examples**: Gym Membership, Meditation App, Recipe Book

```json
{
  "id": "item_gym_membership_001",
  "type": "item",
  "title": "Gym Membership",
  "description": "Monthly gym access. Makes exercise activities cheaper and more effective.",
  "costs": {
    "money": 50.0
  },
  "effects": {
    "modifies_activity": "act_workout_*",
    "energy_cost_reduction": 0.5,
    "energy_gain_boost": 1.0
  },
  "evolution_level": 0,
  "fusion_compatibility": [],
  "requirements": {
    "money_minimum": 50.0
  },
  "metadata": {
    "category": "utility",
    "duration": "season",
    "one_time_purchase": true,
    "tags": ["fitness", "health", "utility"]
  }
}
```

---

## Field Specifications

### ID Pattern
- **Format**: `[type_prefix]_[descriptive_name]_[variant_number]`
- **Type Prefixes**:
  - `dir_` - Life Direction
  - `asp_` - Aspiration
  - `rel_` - Relationship
  - `act_` - Activity
  - `rou_` - Routine
  - `place_` - Place
  - `item_` - Item
- **Examples**:
  - `act_coffee_chat_001`
  - `rel_sarah_deep_talk_002`
  - `place_cafe_downtown_001`

### Costs Object
All costs are **optional**. If not present, assume 0.

| Field | Range | Unit | Notes |
|-------|-------|------|-------|
| `energy` | 0.0-10.0 | Energy points | Daily budget: 10.0 |
| `time` | 0.0-3.0 | Turns | 3 turns per day |
| `money` | 0.0-1000.0 | Dollars | Variable player budget |
| `social_capital` | 0.0-100.0 | SC points | Earned/spent currency |

### Effects Object
All effects are **optional**. Effects are **additive** unless specified.

| Field | Range | Notes |
|-------|-------|-------|
| `relationship_gain` | -1.0 to +1.0 | Applied to relationship meter |
| `trust_gain` | -0.5 to +0.5 | Applied to trust meter |
| `energy_gain` | -10.0 to +10.0 | Can restore or drain energy |
| `money_gain` | -1000.0 to +1000.0 | Positive = income |
| `mood_impact` | -1.0 to +1.0 | Temporary emotional state |

### Requirements Object
All requirements are **optional**. All specified requirements must be met.

| Field | Type | Notes |
|-------|------|-------|
| `relationship_level` | 0-5 | Minimum relationship level with NPC |
| `trust_threshold` | 0.0-1.0 | Minimum trust with NPC |
| `energy_minimum` | 0.0-10.0 | Minimum energy to play card |
| `unlocked_by` | string | Card/event ID that unlocks this |

### Metadata Object
**All fields optional**. Used for filtering, evolution context, and UI.

Common fields:
- `category`: Filtering/grouping (e.g., "social", "self_care", "work")
- `intensity`: "light" | "moderate" | "deep"
- `tags`: Array of strings for search/filtering
- `flavor_text`: Additional narrative context (not gameplay-affecting)
- `npc_id`: For relationship cards, links to NPC definition
- `can_be_routine`: Boolean, if activity can become routine
- `can_automate`: Boolean, if routine can be automated

---

## Evolution Levels

Cards evolve through use, gaining personalized descriptions and effects.

| Level | Name | Description |
|-------|------|-------------|
| 0 | Base | Initial card state |
| 1 | Familiar | After 5+ uses, personalized to player story |
| 2 | Developed | After 10+ uses, enhanced effects |
| 3 | Mastered | After 20+ uses, significant bonuses |
| 4 | Legendary | Rare, story-defining moments |
| 5 | Mythic | Ultimate card state (very rare) |

**Evolution Changes**:
- Title may be personalized (e.g., "Coffee with Sarah" → "Your Thursday Tradition with Sarah")
- Description updated with story context
- Effects may increase (e.g., +0.15 relationship gain → +0.20)
- New fusion compatibility unlocked
- Metadata updated with evolution narrative

---

## Fusion Compatibility

`fusion_compatibility` array lists card IDs that can combine with this card.

**Rules**:
1. Both cards must list each other in compatibility array
2. Both cards must be in player's hand simultaneously
3. Fusion creates new card, removes originals
4. Fusion cards preserve narrative context

**Example**:
```json
// Card A
{
  "id": "act_coffee_chat_001",
  "fusion_compatibility": ["place_cafe_downtown_001"]
}

// Card B
{
  "id": "place_cafe_downtown_001",
  "fusion_compatibility": ["act_coffee_chat_001"]
}

// Fusion Result
{
  "id": "fus_cafe_meetup_tradition_001",
  "title": "Your Cafe Tradition",
  "description": "Every week, you meet here. This cafe isn't just a place anymore—it's where your friendship lives.",
  "evolution_level": 1
}
```

---

## Validation Rules

### Required Fields
- ✅ `id` (must be unique)
- ✅ `type` (must be valid enum)
- ✅ `title` (3-40 characters)
- ✅ `description` (10-200 characters)
- ✅ `evolution_level` (0-5)

### Optional But Recommended
- 🟡 `costs` (at least one cost for activity/relationship cards)
- 🟡 `effects` (at least one effect for activity/relationship cards)
- 🟡 `metadata.category` (for filtering)

### Consistency Checks
- ❗ If `type: "relationship"`, must have `metadata.npc_id`
- ❗ If `type: "routine"`, should have `metadata.can_automate`
- ❗ If `type: "place"`, should have `effects.enables_activities`
- ❗ `fusion_compatibility` must reference existing card IDs
- ❗ `requirements.unlocked_by` must reference existing card/event ID

---

## Example: Complete Base Card Set (Starter 10)

```json
{
  "cards": [
    {
      "id": "act_coffee_chat_001",
      "type": "activity",
      "title": "Coffee Chat",
      "description": "Casual conversation over coffee. Light, easy, comfortable.",
      "costs": {"energy": 1.0, "time": 1.0, "money": 5.0},
      "effects": {"relationship_gain": 0.1, "mood_impact": 0.2},
      "evolution_level": 0,
      "fusion_compatibility": ["act_deep_talk_001", "place_cafe_001"],
      "metadata": {"category": "social", "intensity": "light", "tags": ["casual", "friendship"]}
    },
    {
      "id": "act_deep_talk_001",
      "type": "activity",
      "title": "Deep Conversation",
      "description": "Meaningful heart-to-heart. The kind of talk that matters.",
      "costs": {"energy": 3.0, "time": 2.0},
      "effects": {"relationship_gain": 0.3, "trust_gain": 0.05, "mood_impact": 0.4},
      "evolution_level": 0,
      "fusion_compatibility": ["act_coffee_chat_001"],
      "requirements": {"relationship_level": 2, "trust_threshold": 0.3},
      "metadata": {"category": "social", "intensity": "deep", "tags": ["meaningful", "trust"]}
    },
    {
      "id": "act_work_focused_001",
      "type": "activity",
      "title": "Focused Work Session",
      "description": "Head down, distractions off. Time to get things done.",
      "costs": {"energy": 2.0, "time": 1.0},
      "effects": {"money_gain": 25.0, "aspiration_progress": 0.1},
      "evolution_level": 0,
      "fusion_compatibility": ["place_home_office_001", "item_noise_canceling_001"],
      "metadata": {"category": "work", "intensity": "moderate", "tags": ["productivity", "career"]}
    },
    {
      "id": "act_morning_jog_001",
      "type": "activity",
      "title": "Morning Jog",
      "description": "Start the day right. Fresh air, movement, clarity.",
      "costs": {"energy": 2.0, "time": 1.0},
      "effects": {"energy_gain": 3.0, "mood_impact": 0.3},
      "evolution_level": 0,
      "fusion_compatibility": ["place_park_001"],
      "requirements": {"energy_minimum": 2.0},
      "metadata": {"category": "self_care", "intensity": "moderate", "tags": ["exercise", "morning"], "can_be_routine": true}
    },
    {
      "id": "act_rest_evening_001",
      "type": "activity",
      "title": "Evening Rest",
      "description": "Give yourself permission to do nothing. Recharge.",
      "costs": {"time": 1.0},
      "effects": {"energy_gain": 4.0, "mood_impact": 0.2},
      "evolution_level": 0,
      "fusion_compatibility": [],
      "metadata": {"category": "self_care", "intensity": "light", "tags": ["rest", "recovery"]}
    },
    {
      "id": "rel_sarah_001",
      "type": "relationship",
      "title": "Catch Up with Sarah",
      "description": "Your college friend. You've known each other for years, but life gets busy.",
      "costs": {"energy": 1.0, "time": 1.0},
      "effects": {"relationship_gain": 0.15, "trust_gain": 0.02, "mood_impact": 0.3},
      "evolution_level": 0,
      "fusion_compatibility": ["act_coffee_chat_001", "place_cafe_001"],
      "requirements": {"relationship_level": 1},
      "metadata": {"npc_id": "npc_sarah_001", "category": "friendship", "intensity": "light"}
    },
    {
      "id": "place_cafe_001",
      "type": "place",
      "title": "Local Cafe",
      "description": "Your neighborhood spot. Good coffee, familiar faces, comfortable couches.",
      "costs": {},
      "effects": {"enables_activities": ["act_coffee_chat_001"], "mood_context": "relaxed"},
      "evolution_level": 0,
      "fusion_compatibility": ["act_coffee_chat_001", "rel_sarah_001"],
      "metadata": {"category": "social_space", "ambiance": "cozy", "tags": ["cafe", "neighborhood"]}
    },
    {
      "id": "place_park_001",
      "type": "place",
      "title": "City Park",
      "description": "Green space in the middle of the city. Trees, trails, benches.",
      "costs": {},
      "effects": {"enables_activities": ["act_morning_jog_001"], "mood_context": "peaceful"},
      "evolution_level": 0,
      "fusion_compatibility": ["act_morning_jog_001"],
      "metadata": {"category": "outdoor", "ambiance": "natural", "tags": ["park", "exercise", "nature"]}
    },
    {
      "id": "rou_morning_coffee_001",
      "type": "routine",
      "title": "Morning Coffee",
      "description": "First thing every morning. Non-negotiable.",
      "costs": {"time": 0.5, "money": 3.0},
      "effects": {"energy_gain": 1.0, "mood_impact": 0.1},
      "evolution_level": 0,
      "fusion_compatibility": [],
      "metadata": {"category": "daily_routine", "can_automate": true, "tags": ["morning", "coffee"]}
    },
    {
      "id": "asp_promotion_001",
      "type": "aspiration",
      "title": "Get the Promotion",
      "description": "Senior position just opened. You want it. You've earned it.",
      "costs": {},
      "effects": {"season_goal": "achieve_promotion"},
      "evolution_level": 0,
      "fusion_compatibility": [],
      "metadata": {"category": "career", "season_length_recommendation": 12, "difficulty": "moderate"}
    }
  ]
}
```

---

## Compliance Checklist

- [x] Uses canonical vocab & scales (Trust 0.0–1.0, Relationship 0-5, Energy 0-10)
- [x] Costs limited to Time/Energy/Money/Social Capital
- [x] Evolution levels 0-5
- [x] Fusion compatibility explicitly defined
- [x] Requirements use canonical thresholds
- [x] This doc cites **Truths v1.2**

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Status**: Ready for implementation

