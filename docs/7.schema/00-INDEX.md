# Unwritten Schema Documentation - Master Index

## Overview

This directory contains the complete, unified data schema for the entire Unwritten game. Each document is focused on a specific system and designed to be:
- **Comprehensive**: Contains all data structures for that system
- **Digestible**: Organized logically with clear sections
- **Consistent**: Cross-referenced with other schemas
- **Analyzable**: Easily parsed by LLMs for inconsistency detection

---

## Schema Documents

### Core & Foundational

1. **[01-core-types.md](./01-core-types.md)**
   - Fundamental types used across all systems
   - Common interfaces, enums, utilities
   - ID formats and conventions
   - Timestamps and versioning

### Game Systems

2. **[02-card-system.md](./02-card-system.md)**
   - All 7 card tiers (Foundation, Aspiration, Structure, Quest, Activity, Event, System)
   - Card states, evolution, fusion
   - Hand management, deck composition
   - Rarity and unlock systems

3. **[03-character-system.md](./03-character-system.md)**
   - NPC data structures (personality, memory, relationships)
   - Player character schema
   - Character evolution and growth
   - Voice profiles and behavioral patterns

4. **[04-gameplay-mechanics.md](./04-gameplay-mechanics.md)**
   - Resource types (Energy, Time, Money, Social Capital, Comfort, Success)
   - Turn structure (daily/weekly/seasonal)
   - Meter systems (Physical, Mental, Social, Emotional)
   - Decision weight tiers

5. **[05-narrative-system.md](./05-narrative-system.md)**
   - Story arc structures (multi-phase arcs)
   - Decisive decision points
   - Crisis and breakthrough events
   - Timeline and continuity tracking

6. **[06-emotional-system.md](./06-emotional-system.md)**
   - All 20 emotional states
   - State detection and transitions
   - Emotional influence on gameplay
   - Mood filtering algorithms

### AI & Technical Systems

7. **[07-ai-integration.md](./07-ai-integration.md)**
   - Personality modeling (Big 5 OCEAN)
   - AI inference requests/responses
   - Dialogue generation schemas
   - Sentiment analysis structures

8. **[08-archive-persistence.md](./08-archive-persistence.md)**
   - Season archive structures
   - Lifetime progression data
   - Memory storage and retrieval
   - Save/load game states

### Monetization & Content

9. **[09-monetization-schema.md](./09-monetization-schema.md)**
   - Free vs Premium tier structures
   - Expansion pack schemas
   - Purchase and entitlement tracking
   - Content unlock conditions

10. **[10-novel-generation.md](./10-novel-generation.md)**
    - Master story context
    - Chapter generation packets
    - POV perspective structures
    - Literary technique guidance schemas

### Validation & Quality

11. **[11-validation-rules.md](./11-validation-rules.md)**
    - Cross-schema validation rules
    - Consistency checks
    - Data integrity constraints
    - Type compatibility matrix

---

## Schema Organization Principles

### 1. **Unique Identifiers**

All entities use consistent ID formats:
```typescript
// Format: {type}_{uuid} or {type}_{incrementing_number}
card_id: string;           // "card_12847" or "card_uuid_abc123"
npc_id: string;            // "npc_sarah_anderson" or "npc_001"
season_id: string;         // "season_3" or "season_uuid_def456"
arc_id: string;            // "arc_photography_dream" or "arc_012"
```

### 2. **Timestamps**

All time-based data uses consistent formats:
```typescript
// Game time
week: number;              // 1-based week number
day: number;               // 1-7 (Mon-Sun)
turn: number;              // 1-3 per day (morning, afternoon, evening)

// Real-world time
created_at: ISO8601String; // "2025-10-13T14:30:00Z"
updated_at: ISO8601String;
```

### 3. **Relationships**

All entity relationships use consistent patterns:
```typescript
// One-to-many: Array of IDs
npc_ids: string[];

// Many-to-many: Junction objects
relationships: Array<{
  from_id: string;
  to_id: string;
  type: RelationshipType;
  metadata: any;
}>;

// Parent-child: Explicit parent_id
parent_card_id?: string;
```

### 4. **Versioning**

All schemas include version information:
```typescript
schema_version: string;    // "1.0.0"
last_updated: ISO8601String;
breaking_changes_from?: string; // Previous version if breaking
```

### 5. **Enums vs Union Types**

Clear distinction:
```typescript
// Enums: Fixed, never changes
enum CardTier {
  Foundation = 1,
  Aspiration = 2,
  // ... etc
}

// Union types: Extensible
type EmotionalState = 
  | "MOTIVATED" 
  | "ANXIOUS" 
  | "CONTENT"
  | string; // Allow custom states in future
```

---

## Cross-Schema Dependencies

### Dependency Graph

```
core-types (foundation for all)
    ↓
┌───┴───┬───────┬──────────┬────────────┐
↓       ↓       ↓          ↓            ↓
card    character gameplay narrative   emotional
        ↓       ↓          ↓            ↓
        └───────┴──────────┴────────────┘
                    ↓
            ┌───────┴────────┐
            ↓                ↓
        ai-integration   archive
            ↓                ↓
            └────────┬───────┘
                     ↓
            ┌────────┴────────┐
            ↓                 ↓
        monetization    novel-generation
```

### Key Dependencies

- **Everyone depends on**: `core-types`
- **AI integration depends on**: `character-system`, `emotional-system`, `gameplay-mechanics`
- **Archive depends on**: All game systems
- **Novel generation depends on**: `archive`, `character-system`, `narrative-system`

---

## Using This Documentation

### For Developers

1. Start with `01-core-types.md` to understand foundational types
2. Read schemas relevant to your feature area
3. Check `11-validation-rules.md` for constraints
4. Use TypeScript interfaces directly in code

### For LLM Analysis

1. Load all schemas into context
2. Use `11-validation-rules.md` to identify inconsistencies
3. Cross-reference ID fields across schemas
4. Verify enum values match across references

### For Game Designers

1. Schemas show exact data structures available
2. Use to understand what data drives gameplay
3. Reference when designing new content
4. Validate designs against schema constraints

---

## Schema Maintenance

### When to Update

- ✅ **New features**: Add to appropriate schema
- ✅ **Changed mechanics**: Update relevant schema + validation rules
- ✅ **Removed features**: Mark as `@deprecated` with migration path
- ✅ **Breaking changes**: Bump schema version, document migration

### Update Process

1. Modify schema file
2. Update `schema_version` and `last_updated`
3. Check `11-validation-rules.md` for affected rules
4. Update cross-references in other schemas
5. Run validation suite
6. Document changes in schema file header

---

## Quick Reference

### Most Used Schemas

| Task | Schema |
|------|--------|
| Working with cards | `02-card-system.md` |
| Character/NPC logic | `03-character-system.md` |
| Turn/resource management | `04-gameplay-mechanics.md` |
| Story progression | `05-narrative-system.md` |
| Emotional states | `06-emotional-system.md` |
| Saving/loading | `08-archive-persistence.md` |

### Common Patterns

| Pattern | Location |
|---------|----------|
| ID formats | `01-core-types.md` → Identifiers |
| Personality traits | `03-character-system.md` → OCEAN Model |
| Resource costs | `04-gameplay-mechanics.md` → Resource Types |
| Decision structures | `05-narrative-system.md` → Decisive Decisions |
| State transitions | `06-emotional-system.md` → State Changes |

---

## Version History

- **1.0.0** (2025-10-13): Initial unified schema documentation
  - Consolidated from gameplay, narrative, monetization docs
  - Added comprehensive novel generation schemas
  - Established validation rules framework

---

## Next Steps

After reading this index:

1. **If new to the project**: Read schemas in order (01→11)
2. **If working on specific feature**: Jump to relevant schema
3. **If analyzing consistency**: Load all + validation rules
4. **If designing content**: Focus on card/character/narrative schemas

All schemas use TypeScript notation for clarity and IDE support, but are language-agnostic in their design.

