# Unwritten Schema Documentation

**Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Status**: ✅ Complete

---

## Overview

This directory contains the **complete, unified data schema** for the entire Unwritten game system. All schemas are designed to be:

- **Comprehensive**: Every data structure is fully specified
- **Consistent**: Cross-references validated across all schemas
- **Analyzable**: Easily parsed by LLMs for inconsistency detection
- **Implementable**: Direct TypeScript interfaces ready for development

---

## Quick Start

### For Developers

1. **Read**: Start with `00-INDEX.md` for organization overview
2. **Reference**: Use `01-core-types.md` for foundational types
3. **Implement**: Each schema is a standalone reference for that system
4. **Validate**: Use `11-validation-rules.md` to ensure data integrity

### For LLMs (Consistency Analysis)

1. **Load**: Ingest all 11 schema files into context
2. **Cross-Reference**: Check entity IDs across schemas
3. **Validate**: Apply rules from `11-validation-rules.md`
4. **Report**: Flag inconsistencies with specific schema references

### For Designers

1. **Explore**: Schemas show what data is available
2. **Design**: Use schemas to understand system capabilities
3. **Validate**: Check designs against schema constraints
4. **Communicate**: Reference schemas when discussing features

---

## Schema Files

### Core & Foundation

| File | Purpose | Key Contents |
|------|---------|--------------|
| **00-INDEX.md** | Master index & navigation | Organization, dependencies, patterns |
| **01-core-types.md** | Foundational types | IDs, time, enums, utilities |

### Game Systems

| File | Purpose | Key Contents |
|------|---------|--------------|
| **02-card-system.md** | Card taxonomy & mechanics | 7 tiers, evolution, fusion, hand management |
| **03-character-system.md** | NPCs & personality | OCEAN model, relationships, memory, voice |
| **04-gameplay-mechanics.md** | Resources & turns | Energy, meters, time, success calculations |
| **05-narrative-system.md** | Story & arcs | Multi-phase arcs, decisions, timeline, continuity |
| **06-emotional-system.md** | Emotional states | 20 states, transitions, mood filtering |

### Technical Systems

| File | Purpose | Key Contents |
|------|---------|--------------|
| **07-ai-integration.md** | AI inference & generation | TensorFlow Lite, personality modeling, dialogue |
| **08-archive-persistence.md** | Saving & seasons | Archive system, save/load, cross-lifetime |
| **09-monetization-schema.md** | Tiers & pricing | Essence tokens, subscriptions, packs |

### Content Generation

| File | Purpose | Key Contents |
|------|---------|--------------|
| **10-novel-generation.md** | Premium book generation | Master context, chapter packets, literary techniques |

### Quality Assurance

| File | Purpose | Key Contents |
|------|---------|--------------|
| **11-validation-rules.md** | Consistency checks | Cross-schema validation, automated QA |

---

## Schema Statistics

- **Total Schema Files**: 12 (including index and README)
- **Core Interfaces**: 200+
- **Enum Definitions**: 50+
- **Validation Rules**: 100+
- **Cross-Schema References**: Validated
- **Lines of Documentation**: ~12,000+

---

## Key Design Principles

### 1. **Unique Identifiers**

All entities use consistent ID formats:
```typescript
type CardID = string;           // "card_12847"
type NPCID = string;            // "npc_sarah_anderson"
type PlayerID = string;         // "player_uuid_xyz789"
```

### 2. **Temporal Consistency**

Game time and real-world time are clearly separated:
```typescript
// Game time
interface GameTime {
  week: Week;
  day: DayOfWeek;
  turn: TurnOfDay;
}

// Real-world time
type ISO8601String = string;    // "2025-10-13T14:30:00Z"
```

### 3. **Range Validation**

All numeric values have explicit ranges:
```typescript
type Meter = RangedInt<0, 10>;
type Personality = RangedFloat<1, 5>;
type Trust = RangedFloat<0, 1>;
```

### 4. **Cross-Schema References**

All references are validated:
```typescript
// Card references NPC
interface SocialActivityCard {
  participants: NPCID[];         // Must exist in character-system
}

// Memory references Card
interface NarrativeMemory {
  cards_played: CardID[];        // Must exist in card-system
}
```

### 5. **Versioning**

All persistent data includes version tracking:
```typescript
interface Versioned {
  schema_version: SemanticVersion;
  created_at: ISO8601String;
  updated_at: ISO8601String;
}
```

---

## Dependency Graph

```
                 core-types
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    card-system  character    gameplay
                    ↓            ↓
                emotional    narrative
                    ↓            ↓
                    └──→ ai-integration
                         ↓
                    archive-persistence
                         ↓
                    ┌────┴────┐
                    ↓         ↓
              monetization  novel-generation
                    ↓
              validation-rules
```

---

## Usage Examples

### Validating a Card

```typescript
// From 02-card-system.md
const card: BaseCard = {
  card_id: "card_00123",           // Valid format (01-core-types)
  tier: CardTier.Activity,         // Valid enum (02-card-system)
  costs: {
    energy: 2,                     // Valid range 0-8 (04-gameplay-mechanics)
    time_hours: 1.5               // Valid range (04-gameplay-mechanics)
  },
  effects: [
    {
      type: CardEffectType.ModifyMeter,
      target: { type: "player" },
      value: { physical: 1 }       // Valid meter range 0-10
    }
  ]
};
```

### Validating a Relationship

```typescript
// From 03-character-system.md
const relationship: Relationship = {
  from_character_id: "player_001",  // Valid PlayerID
  to_character_id: "npc_sarah",     // Valid NPCID (must exist)
  trust: 0.75,                      // Valid range 0.0-1.0
  relationship_level: RelationshipLevel.CloseFriend,
  // Level matches trust (0.6-0.8 = CloseFriend) ✓
};
```

### Validating Novel Data

```typescript
// From 10-novel-generation.md
const chapterPacket: ChapterGenerationPacket = {
  chapter_metadata: {
    chapter_number: 5,
    primary_pov: "npc_sarah",      // Must exist in character_registry
    target_word_count: 3000        // Valid for premium tier
  },
  master_context: {
    established_facts: [
      {
        fact: "Sarah owns Luna Brew coffee shop",
        week_established: 4,
        immutable: true             // Cannot be contradicted
      }
    ],
    character_registry: [/* All characters */]
  }
};
```

---

## Consistency Checks

### Automated Validation

Run these checks on all data:

1. **ID Format**: All IDs match regex patterns from `01-core-types.md`
2. **Range Validation**: All numeric values within defined ranges
3. **Entity Existence**: All referenced IDs exist in source schemas
4. **Timeline Coherence**: Events in chronological order
5. **State Validity**: All state transitions valid
6. **Enum Values**: All enum references defined
7. **Cross-References**: Bidirectional relationships consistent
8. **No Contradictions**: Established facts never contradicted

### Manual Review

For complex systems:

- **Narrative Continuity**: Story arcs make sense
- **Character Consistency**: Personalities evolve logically
- **Emotional Journey**: State transitions feel authentic
- **Relationship Evolution**: Trust changes are earned
- **Quality Metrics**: Scores reflect actual quality

---

## Integration with Codebase

### Flutter/Dart Implementation

These TypeScript schemas can be directly translated to Dart:

```dart
// From 01-core-types.md
class GameTime {
  final int week;
  final int day;  // 1-7
  final int turn; // 1-3
  
  const GameTime({
    required this.week,
    required this.day,
    required this.turn,
  });
}

// From 03-character-system.md
class PersonalityTraits {
  final double openness;           // 1.0-5.0
  final double conscientiousness;
  final double extraversion;
  final double agreeableness;
  final double neuroticism;
  
  const PersonalityTraits({
    required this.openness,
    required this.conscientiousness,
    required this.extraversion,
    required this.agreeableness,
    required this.neuroticism,
  });
}
```

---

## Common Patterns

### 1. Entity Pattern

```typescript
interface Entity {
  id: string;                      // Unique identifier
  created_at: ISO8601String;       // Creation timestamp
  updated_at: ISO8601String;       // Last update
  schema_version: SemanticVersion; // Schema version
}
```

### 2. State Pattern

```typescript
interface StatefulEntity extends Entity {
  current_state: EntityState;
  state_history: StateSnapshot[];
  transitions: StateTransition[];
}
```

### 3. Snapshot Pattern

```typescript
interface Snapshot {
  week: Week;
  data: any;
  notable_change?: string;
  trigger?: string;
}
```

### 4. Range Pattern

```typescript
type RangedValue = number & {
  __min: number;
  __max: number;
};
```

---

## Error Patterns

### Common Issues

1. **Invalid ID Format**
   ```
   ERROR: card_id "Card_001" doesn't match pattern /^card_[a-z0-9_]+$/
   FIX: Use lowercase: "card_001"
   ```

2. **Out of Range**
   ```
   ERROR: meter value 12 exceeds max of 10
   FIX: Clamp to valid range [0, 10]
   ```

3. **Missing Reference**
   ```
   ERROR: npc_id "npc_john" not found in character_registry
   FIX: Ensure NPC exists before referencing
   ```

4. **Timeline Violation**
   ```
   ERROR: Event at week 10 before event at week 12
   FIX: Sort events chronologically
   ```

---

## Future Extensions

This schema system is designed for extension:

- ✅ **Add New Card Tiers**: Extend `CardTier` enum
- ✅ **Add New Emotional States**: Update emotional-system
- ✅ **Add New Expansion Packs**: Add to monetization-schema
- ✅ **Add New Literary Techniques**: Extend novel-generation
- ✅ **Add New Validation Rules**: Update validation-rules

All extensions should:
1. Follow existing patterns
2. Add validation rules
3. Document cross-schema impacts
4. Update dependency graph
5. Increment schema version

---

## Contributing

When modifying schemas:

1. **Update Version**: Increment `schema_version` in affected files
2. **Document Changes**: Add to file header changelog
3. **Update Dependencies**: Check cross-schema impacts
4. **Add Validation**: Include validation rules for new data
5. **Test**: Validate against existing data
6. **Review**: LLM analysis for consistency

---

## Support

For questions or issues:

1. **Read**: Check relevant schema file first
2. **Search**: Use `00-INDEX.md` for quick reference
3. **Validate**: Run consistency checks
4. **Document**: File issues with schema references

---

## Summary

This schema documentation provides:

- ✅ **Complete Coverage**: All Unwritten systems documented
- ✅ **Consistency**: Cross-validated references
- ✅ **Clarity**: Clear, implementable interfaces
- ✅ **Quality**: Automated validation rules
- ✅ **Extensibility**: Designed for future growth

**Total Coverage**: 100% of game systems
**Status**: Production-ready
**Last Validation**: 2025-10-13

---

*This schema system is the single source of truth for Unwritten data structures.*

