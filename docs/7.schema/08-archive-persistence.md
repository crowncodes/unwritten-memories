# Archive & Persistence Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`, `02-card-system.md`, `03-character-system.md`, `05-narrative-system.md`

---

## Overview

Defines season archives, save/load systems, progression persistence, cross-lifetime continuity, and data storage structures.

---

## 1. Season Archive System

### Season Archive

```typescript
/**
 * Complete season archive
 */
interface SeasonArchive {
  archive_id: string;
  season_id: SeasonID;
  player_id: PlayerID;
  lifetime_number: number;
  
  // Basic info
  season_number: number;
  season_title: string;
  start_week: Week;
  end_week: Week;
  total_weeks: number;
  
  // Tier
  tier: "free" | "premium";
  free_tier_slots_used?: number;   // If free tier
  
  // Archived content
  archived_cards: ArchiveCard[];
  archived_memories: ArchiveMemory[];
  archived_relationships: ArchivedRelationship[];
  
  // State snapshots
  final_personality: PersonalitySnapshot;
  final_meters: Meters;
  final_resources: PlayerResources;
  
  // Narrative
  story_arcs_completed: StoryArcArchive[];
  story_arcs_failed: StoryArcArchive[];
  decisive_decisions: DecisiveDecisionArchive[];
  
  // Achievements
  aspirations_completed: AspirationArchive[];
  fusion_cards_created: FusionArchive[];
  skills_mastered: SkillArchive[];
  
  // Quality metrics
  season_quality_score: Percentage;
  dramatic_density: Percentage;
  emotional_resonance: Percentage;
  character_growth: Percentage;
  
  // Book
  book_generated: boolean;
  book_metadata?: BookMetadata;
  
  // Metadata
  archived_at: ISO8601String;
  last_accessed: ISO8601String;
  access_count: number;
  
  // Persistence
  persist_to_next_lifetime: boolean;
  schema_version: SemanticVersion;
}
```

### Archive Card

```typescript
/**
 * Archived card (preserved from season)
 */
interface ArchiveCard {
  card_id: CardID;
  original_card: BaseCard;
  
  // Evolution
  final_evolution_level: number;
  evolution_history: EvolutionEvent[];
  
  // Usage
  times_played: number;
  first_played: GameTime;
  last_played: GameTime;
  
  // Significance
  archive_significance: ArchiveSignificance;
  selection_reason: string;
  
  // Context
  associated_npcs: NPCID[];
  associated_arcs: StoryArcID[];
  memorable_uses: CardUsageMemory[];
  
  // Fusion
  is_fusion: boolean;
  fusion_id?: FusionID;
  
  // Player choice
  player_selected: boolean;
  auto_selected: boolean;
}

interface CardUsageMemory {
  week: Week;
  context: string;
  outcome: OutcomeType;
  emotional_weight: Intensity;
  memory_id?: MemoryID;
}
```

### Archive Memory

```typescript
/**
 * Archived narrative memory
 */
interface ArchiveMemory {
  memory_id: MemoryID;
  original_memory: NarrativeMemory;
  
  // Significance
  archive_significance: ArchiveSignificance;
  emotional_weight: Intensity;
  narrative_importance: Intensity;
  
  // Context
  week: Week;
  season_act: 1 | 2 | 3;
  arc_phase?: number;
  
  // Characters
  characters_involved: NPCID[];
  primary_pov: string;
  
  // Book chapter
  becomes_chapter: boolean;
  chapter_number?: number;
  estimated_word_count?: number;
  
  // Player selection
  player_selected: boolean;
  auto_selected: boolean;
  selection_reason: string;
}
```

### Archive Limits

```typescript
/**
 * Archive limits by tier
 */
interface ArchiveLimits {
  tier: "free" | "premium";
  
  // Free tier limits
  free_tier: {
    max_cards_per_season: 3;
    max_memories_per_season: 10;
    max_archived_seasons: Infinity; // All seasons saved
    book_quality: "free_tier";
  };
  
  // Premium tier (unlimited)
  premium_tier: {
    max_cards_per_season: Infinity;
    max_memories_per_season: Infinity;
    max_archived_seasons: Infinity;
    book_quality: "premium_tier";
  };
}

/**
 * Archive selection system
 */
interface ArchiveSelection {
  season_id: SeasonID;
  tier: "free" | "premium";
  
  // Auto-selection (AI-driven)
  auto_selected_cards: CardID[];
  auto_selected_memories: MemoryID[];
  auto_selection_criteria: SelectionCriteria;
  
  // Player overrides
  player_selected_cards: CardID[];
  player_selected_memories: MemoryID[];
  
  // Final
  final_cards: CardID[];
  final_memories: MemoryID[];
  
  // Status
  selection_complete: boolean;
  within_limits: boolean;
}

interface SelectionCriteria {
  prioritize: "significance" | "emotional_weight" | "variety" | "narrative_importance";
  min_significance: ArchiveSignificance;
  ensure_arc_coverage: boolean;
  ensure_character_coverage: boolean;
  balance_positive_negative: boolean;
}
```

---

## 2. Save System

### Save Game Structure

```typescript
/**
 * Complete save game
 */
interface SaveGame {
  save_id: string;
  player_id: PlayerID;
  save_type: "auto" | "manual" | "checkpoint";
  
  // Timestamp
  saved_at: ISO8601String;
  save_name?: string;               // For manual saves
  
  // Game state
  game_state: GameState;
  
  // Player
  player_character: PlayerCharacter;
  
  // World
  world_state: WorldState;
  
  // NPCs
  npcs: Record<NPCID, NPCCharacter>;
  
  // Cards
  card_states: Record<CardID, CardState>;
  player_hand: CardID[];
  player_deck: CardID[];
  
  // Story
  active_arcs: Record<StoryArcID, StoryArc>;
  timeline: GameTimeline;
  memory_bank: Record<MemoryID, NarrativeMemory>;
  
  // Archive
  completed_seasons: SeasonArchive[];
  
  // Metadata
  play_time_hours: number;
  last_auto_save: ISO8601String;
  save_version: SemanticVersion;
  game_version: SemanticVersion;
  
  // Compression
  compressed: boolean;
  compression_method?: string;
  compressed_size_mb?: number;
  uncompressed_size_mb?: number;
}

interface GameState {
  // Time
  current_time: GameTime;
  total_weeks_played: number;
  current_season: number;
  lifetime_number: number;
  
  // Turn
  current_turn_state: TurnState;
  turn_phase: TurnPhase;
  
  // Flags
  game_paused: boolean;
  tutorial_complete: boolean;
  unlocked_features: string[];
}

interface CardState {
  card_id: CardID;
  current_state: CardState;
  evolution_level: number;
  times_played: number;
  last_played?: GameTime;
  on_cooldown: boolean;
  cooldown_until?: GameTime;
}
```

### Save Management

```typescript
/**
 * Save file metadata
 */
interface SaveFileMetadata {
  save_id: string;
  file_path: string;
  
  // Basic info
  player_name: string;
  current_week: Week;
  season_number: number;
  lifetime_number: number;
  
  // Preview
  thumbnail?: URL;
  preview_text: string;
  
  // Stats
  total_weeks: number;
  play_time_hours: number;
  
  // Technical
  file_size_mb: number;
  save_version: SemanticVersion;
  game_version: SemanticVersion;
  
  // Metadata
  saved_at: ISO8601String;
  last_played: ISO8601String;
  
  // Validation
  corrupted: boolean;
  migration_required: boolean;
}

/**
 * Auto-save configuration
 */
interface AutoSaveConfig {
  enabled: boolean;
  
  // Frequency
  save_every_n_turns: number;       // Save every 5 turns
  save_before_major_decisions: boolean;
  save_at_season_end: boolean;
  
  // Slots
  max_auto_save_slots: number;      // Keep last 5 auto-saves
  rotate_oldest: boolean;
  
  // Performance
  background_save: boolean;
  compress_saves: boolean;
}
```

---

## 3. Cross-Lifetime Continuity

### Lifetime Archive

```typescript
/**
 * Archive of completed lifetime
 */
interface LifetimeArchive {
  lifetime_id: string;
  player_id: PlayerID;
  lifetime_number: number;
  
  // Character
  character_name: string;
  final_age: number;
  total_weeks_lived: number;
  
  // Seasons
  seasons: SeasonArchive[];
  total_seasons: number;
  
  // Overall narrative
  lifetime_summary: LifetimeSummary;
  
  // Achievements
  total_aspirations_completed: number;
  total_fusion_cards: number;
  mastered_skills: SkillID[];
  
  // Relationships
  final_relationships: ArchivedRelationship[];
  deep_connections: number;
  
  // Books
  books_generated: BookMetadata[];
  
  // Ending
  ending_type: string;
  ending_description: string;
  player_satisfaction: Percentage;
  
  // Metadata
  completed_at: ISO8601String;
  total_play_time_hours: number;
  
  // Next lifetime
  carries_forward: LifetimeCarryForward;
}

interface LifetimeSummary {
  one_sentence_summary: string;
  key_moments: string[];
  defining_relationships: NPCID[];
  primary_theme: string;
  emotional_journey: string;
  
  // Character arc
  starting_personality: PersonalityTraits;
  ending_personality: PersonalityTraits;
  personality_evolution: string;
  
  // Quality
  overall_quality: Percentage;
  most_memorable_season: number;
  most_meaningful_arc: StoryArcID;
}

interface LifetimeCarryForward {
  // What persists to next lifetime
  carried_themes: string[];
  carried_lessons: string[];
  unlocked_content: string[];
  
  // Meta-progression
  player_skill_level: number;
  content_packs_owned: PackID[];
  premium_tier: boolean;
}
```

### Multi-Lifetime Progression

```typescript
/**
 * Player progression across multiple lifetimes
 */
interface MultiLifetimeProgression {
  player_id: PlayerID;
  
  // Lifetimes
  total_lifetimes: number;
  completed_lifetimes: LifetimeArchive[];
  current_lifetime: number;
  
  // Aggregate stats
  total_weeks_played: number;
  total_play_time_hours: number;
  total_seasons: number;
  
  // Content
  total_cards_collected: number;
  unique_fusion_cards: number;
  unique_npcs_met: number;
  total_memories: number;
  
  // Books
  total_books_generated: number;
  total_book_word_count: number;
  
  // Unlocks
  unlocked_content: UnlockedContent;
  
  // Achievements
  lifetime_achievements: Achievement[];
  
  // Preferences learned
  content_preferences: ContentPreferences;
  difficulty_adjustments: any;
}

interface UnlockedContent {
  expansion_packs: PackID[];
  special_cards: CardID[];
  special_npcs: NPCID[];
  special_locations: LocationID[];
  special_arcs: StoryArcID[];
}

interface Achievement {
  achievement_id: string;
  achievement_name: string;
  description: string;
  earned_at: ISO8601String;
  lifetime_earned: number;
  rarity: "common" | "uncommon" | "rare" | "legendary";
}
```

---

## 4. Data Migration

### Migration System

```typescript
/**
 * Save data migration
 */
interface SaveMigration {
  migration_id: string;
  from_version: SemanticVersion;
  to_version: SemanticVersion;
  
  // Changes
  breaking_changes: BreakingChange[];
  data_transformations: DataTransformation[];
  
  // Process
  migration_steps: MigrationStep[];
  
  // Validation
  validation_tests: ValidationTest[];
  
  // Status
  status: "pending" | "in_progress" | "complete" | "failed";
  error?: GameError;
}

interface BreakingChange {
  change_type: "schema_change" | "data_removal" | "field_rename" | "type_change";
  affected_data: string;
  description: string;
  requires_manual_intervention: boolean;
}

interface DataTransformation {
  transformation_id: string;
  source_field: string;
  target_field: string;
  transformation_function: string;
  reversible: boolean;
}

interface MigrationStep {
  step_id: string;
  step_order: number;
  description: string;
  critical: boolean;
  executed: boolean;
  result?: any;
}

interface ValidationTest {
  test_id: string;
  test_name: string;
  passed: boolean;
  error?: string;
}
```

---

## 5. Cloud Sync (Future)

### Cloud Save Structure

```typescript
/**
 * Cloud save metadata (for future cloud sync)
 */
interface CloudSave {
  cloud_save_id: string;
  player_id: PlayerID;
  
  // Local reference
  local_save_id: string;
  
  // Cloud storage
  cloud_provider: "gcp" | "aws" | "azure";
  cloud_path: string;
  
  // Sync
  last_sync: ISO8601String;
  sync_status: "synced" | "pending" | "conflict" | "error";
  
  // Conflict resolution
  conflicts?: SaveConflict[];
  
  // Metadata
  cloud_file_size_mb: number;
  checksum: string;
}

interface SaveConflict {
  conflict_id: string;
  conflict_type: "version_mismatch" | "data_divergence" | "timestamp_conflict";
  local_version: any;
  cloud_version: any;
  resolution: "keep_local" | "keep_cloud" | "merge" | "manual";
}
```

---

## 6. Storage Optimization

### Compression Strategy

```typescript
/**
 * Data compression configuration
 */
interface CompressionStrategy {
  enabled: boolean;
  compression_level: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
  
  // What to compress
  compress_card_data: boolean;
  compress_memory_data: boolean;
  compress_npc_data: boolean;
  compress_timeline_data: boolean;
  
  // Thresholds
  compress_if_over_mb: number;
  
  // Performance
  background_compression: boolean;
  decompress_on_load: boolean;
}

/**
 * Storage usage tracking
 */
interface StorageUsage {
  player_id: PlayerID;
  
  // Total usage
  total_storage_mb: number;
  
  // Breakdown
  save_files_mb: number;
  archive_data_mb: number;
  book_data_mb: number;
  cache_mb: number;
  ai_models_mb: number;
  assets_mb: number;
  
  // Limits
  storage_limit_mb?: number;
  storage_warning_threshold: Percentage;
  
  // Cleanup
  last_cleanup: ISO8601String;
  eligible_for_cleanup_mb: number;
}
```

---

## 7. Backup & Recovery

### Backup System

```typescript
/**
 * Backup configuration
 */
interface BackupSystem {
  enabled: boolean;
  
  // Frequency
  backup_frequency: Duration;
  max_backups: number;
  
  // Location
  backup_location: "local" | "cloud" | "both";
  local_backup_path?: string;
  
  // What to backup
  backup_saves: boolean;
  backup_archives: boolean;
  backup_books: boolean;
  backup_settings: boolean;
  
  // Retention
  retention_policy: RetentionPolicy;
}

interface RetentionPolicy {
  keep_daily_backups: number;       // Last 7 days
  keep_weekly_backups: number;      // Last 4 weeks
  keep_monthly_backups: number;     // Last 12 months
  keep_season_end_backups: boolean; // All season end backups
}

/**
 * Recovery operation
 */
interface RecoveryOperation {
  recovery_id: string;
  
  // Source
  backup_id: string;
  backup_timestamp: ISO8601String;
  
  // Target
  restore_to_save_slot?: number;
  overwrite_current: boolean;
  
  // Process
  recovery_steps: MigrationStep[];
  
  // Status
  status: "pending" | "in_progress" | "complete" | "failed";
  progress_percentage: Percentage;
  
  // Result
  success: boolean;
  error?: GameError;
  recovered_data_summary: string;
}
```

---

## Notes for LLM Analysis

When validating archive & persistence schemas:

1. **Archive Limits**: Free tier = 3 cards, premium = unlimited
2. **Season Archives**: All seasons saved regardless of tier
3. **Save Versioning**: Track schema versions for migration
4. **Data Integrity**: All IDs reference existing entities
5. **Compression**: Optional, configurable by performance needs
6. **Migration**: Support backward compatibility for 2 major versions
7. **Backup Frequency**: Configurable, recommend daily auto-backup
8. **Storage Limits**: Monitor and warn at 80% capacity

**Cross-schema dependencies**:
- CardID from card-system (all archived cards must exist)
- NPCID from character-system (all NPCs must be defined)
- MemoryID from narrative-system (all memories must exist)
- StoryArcID from narrative-system (all arcs must exist)
- PersonalityTraits from character-system (in valid ranges)
- All archived data must pass validation-rules consistency checks
- Book metadata references novel-generation schema
- Quality scores use consistent Percentage type from core-types

