# Context & Memory Systems

**Purpose:** Context injection strategies and memory management for AI generations  
**Audience:** AI engineers, backend developers, system architects  
**Status:** ✅ Complete  
**Related:** ← 33-prompt-templates-library.md | → 35-consistency-coherence.md for validation

---

## What This Document Covers

This document details the **context and memory architecture** for Unwritten's AI system. You'll learn:
- How to build comprehensive context for AI generations
- Memory tier system and persistence rules
- Context optimization for token efficiency
- Memory recall prioritization
- Context compression techniques
- Memory fade and consolidation systems

**Why This Matters:**
- AI quality depends on context quality
- Token costs scale with context size
- Memory systems create character continuity
- Poor context = inconsistent generations

---

## Table of Contents

1. [Context Layer Architecture](#context-layer-architecture)
2. [Building Comprehensive Context](#building-comprehensive-context)
3. [Context Injection Templates](#context-injection-templates)
4. [Memory Tier System](#memory-tier-system)
5. [Memory Recall & Prioritization](#memory-recall--prioritization)
6. [Context Optimization](#context-optimization)
7. [Memory Persistence & Fade](#memory-persistence--fade)
8. [Memory Consolidation](#memory-consolidation)
9. [Token Budget Management](#token-budget-management)
10. [Implementation Examples](#implementation-examples)

---

## Context Layer Architecture

### The Seven-Layer Context Model

Every AI generation should include these seven layers of context, prioritized by importance:

```javascript
const buildContext = (character, player, interaction) => {
  return {
    // Layer 1: Character State (CRITICAL - always include)
    character: {
      name: character.name,
      level: character.relationshipLevel,
      personalityScores: character.ocean,
      currentDescription: character.description,
      memories: character.memories.slice(-10), // Last 10 memories
      traits: character.traits,
      currentMood: character.emotionalState,
      emotionalCapacity: character.emotionalCapacity || 5.0 // NEW: 0-10 scale
    },
    
    // Layer 2: Relationship History (CRITICAL - always include)
    relationship: {
      durationWeeks: calculateWeeks(character.firstMet),
      totalInteractions: character.interactions.length,
      interactionTypes: categorizeInteractions(character.interactions),
      trustLevel: character.trust,
      conflictsResolved: character.conflictsHistory.length,
      significantMoments: character.milestones
    },
    
    // Layer 3: Current Interaction (CRITICAL - always include)
    interaction: {
      activity: interaction.activity,
      location: interaction.location,
      playerChoice: interaction.playerDialogueChoice,
      playerEmotion: player.currentEmotion,
      duration: interaction.duration,
      otherPresent: interaction.otherCharacters,
      
      // Master Truths v1.2: NPC Response Framework
      urgencyAssessment: {
        level: assessUrgency(interaction).level,        // routine/important/urgent/crisis
        multiplier: assessUrgency(interaction).multiplier, // 1x-5x
        score: assessUrgency(interaction).score,        // 0.0-1.0
        reasoning: "Brief explanation of why this urgency level applies"
      }
    },
    
    // Layer 4: Player State (IMPORTANT - include when relevant)
    player: {
      emotionalState: player.emotion,
      stressLevel: player.stress,
      recentEvents: player.recentLifeEvents.slice(-5),
      career: player.career,
      reputation: player.reputation,
      playStyle: analyzePlayStyle(player.history)
    },
    
    // Layer 5: World Context (OPTIONAL - include for flavor)
    world: {
      timeOfDay: getCurrentTimeOfDay(),
      season: getCurrentSeason(),
      weather: getCurrentWeather(),
      recentWorldEvents: getRecentEvents(),
      dayOfWeek: getDayOfWeek()
    },
    
    // Layer 6: Dramatic Irony Context (NEW - for novel-quality tension)
    dramaticIrony: buildDramaticIronyContext(character, player, interaction),
    
    // Layer 7: Meta Context (IMPORTANT - include for quality)
    meta: {
      characterEvolutionRate: calculateEvolutionSpeed(character),
      narrativePacing: assessStoryPacing(player.playthrough),
      emotionalTone: determineDesiredTone(interaction),
      previousAIGenerations: character.aiGenerationHistory.slice(-3)
    }
  };
};

/**
 * Context for Training Data Generation (Differs from Runtime)
 * 
 * When generating training data (not game runtime), context focuses on:
 * - Character capacity constraints
 * - Target authenticity ranges
 * - Systematic parameter coverage
 * - Novel-quality dialogue requirements
 */
function buildTrainingDataContext(scenario) {
  return {
    character_state: {
      base_capacity: 6.0,  # Before stress factors
      capacity_factors: [
        {"factor": "work_stress", "impact": -2.0},
        {"factor": "sleep_deprivation", "impact": -1.5}
      ],
      effective_capacity: 2.5,  # After factors applied
      can_support_up_to: 4.5  # effective_capacity + buffer
    },
    situation: {
      support_level_needed: 7.0,  # What the situation requires
      urgency: 4.0,  # 1-5 scale (5 = life/death)
      relationship_type: "close_friend"
    },
    target_authenticity: {
      range: (0.4, 0.6),  # Struggling response
      demonstrates: "Character wants to help but capacity insufficient"
    },
    complexity_type: "people_pleasing",  # Type of messy human behavior to show
    novel_quality_requirements: {
      min_word_count: 150,
      behavioral_cues_required: 3,
      show_vs_tell_ratio: 0.8,
      ocean_influence_visible: True
    }
  };
}

/**
 * See: src/unwritten/training/systematic_generator.py for complete implementation
 */

/**
 * Build Dramatic Irony Context Layer (NEW)
 * 
 * Purpose: Identify knowledge gaps between player and character
 * to create tension, dramatic irony, and "yelling at screen" moments.
 */
function buildDramaticIronyContext(character, player, interaction) {
  // 1. Identify what player knows that character doesn't
  const playerKnowledge = {
    npc_secrets: player.knownNPCSecrets.filter(secret => 
      secret.aboutCharacter === character.name && !secret.characterKnows
    ),
    witnessed_events: player.witnessedEvents.filter(event =>
      event.involvesCharacter === character.name && !event.characterPresent
    ),
    overheard_conversations: player.overheardConversations.filter(conv =>
      conv.aboutCharacter === character.name
    ),
    hidden_information: player.hiddenInformation.filter(info =>
      info.relevantToCharacter === character.name
    )
  };
  
  // 2. Identify what character knows that player doesn't
  const characterKnowledge = {
    internal_struggles: character.hiddenStruggles.filter(s => !s.revealed),
    secret_information: character.secrets.filter(s => !s.shared),
    true_feelings: character.hiddenFeelings.filter(f => !f.expressed),
    off_screen_events: character.recentEvents.filter(e => !e.playerKnows)
  };
  
  // 3. Calculate knowledge gap and tension potential
  const knowledgeGap = calculateKnowledgeGap(playerKnowledge, characterKnowledge);
  const tensionPotential = assessTensionPotential(knowledgeGap, interaction);
  
  // 4. Retrieve previous dramatic irony moments for continuity
  const previousIronyMoments = character.dramaticIronyHistory
    .filter(moment => !moment.resolved)
    .slice(-3);
  
  return {
    player_knows: summarizePlayerKnowledge(playerKnowledge),
    character_knows: summarizeCharacterKnowledge(characterKnowledge),
    knowledge_gap: knowledgeGap,
    tension_opportunity: tensionPotential,
    previous_irony_moments: previousIronyMoments,
    
    // Should this interaction include dramatic irony?
    should_use_dramatic_irony: tensionPotential.score >= 0.6,
    
    // What type of dramatic irony is most appropriate?
    recommended_irony_type: tensionPotential.recommendedType,
    
    // Emotional capacity constraint (affects how character interprets situation)
    capacity_limitation: {
      current_capacity: character.emotionalCapacity,
      affects_perception: character.emotionalCapacity < 5.0,
      likely_misreads: character.emotionalCapacity < 3.0
    }
  };
}

/**
 * Calculate knowledge gap magnitude and type
 */
function calculateKnowledgeGap(playerKnowledge, characterKnowledge) {
  const playerKnowsCount = Object.values(playerKnowledge)
    .reduce((sum, arr) => sum + arr.length, 0);
  
  const characterKnowsCount = Object.values(characterKnowledge)
    .reduce((sum, arr) => sum + arr.length, 0);
  
  return {
    player_has_advantage: playerKnowsCount > characterKnowsCount,
    character_has_advantage: characterKnowsCount > playerKnowsCount,
    gap_size: Math.abs(playerKnowsCount - characterKnowsCount),
    gap_type: determineGapType(playerKnowledge, characterKnowledge)
  };
}

/**
 * Assess tension potential from knowledge gap
 */
function assessTensionPotential(knowledgeGap, interaction) {
  let score = 0;
  
  // More knowledge gap = more tension potential
  score += Math.min(1.0, knowledgeGap.gap_size / 5) * 0.4;
  
  // Player knowing character secret = high tension
  if (knowledgeGap.player_has_advantage) {
    score += 0.3;
  }
  
  // Current interaction involves the secret topic
  if (interaction.topicsInvolved && hasTopicOverlap(interaction.topicsInvolved, knowledgeGap)) {
    score += 0.3;
  }
  
  // Determine recommended type
  let recommendedType = 'none';
  if (score >= 0.6) {
    if (knowledgeGap.gap_type === 'secret_about_npc') {
      recommendedType = 'character_oblivious_to_npc_truth';
    } else if (knowledgeGap.gap_type === 'witnessed_event') {
      recommendedType = 'character_misinterprets_situation';
    } else if (knowledgeGap.gap_type === 'emotional_misread') {
      recommendedType = 'capacity_limited_perception';
    }
  }
  
  return {
    score: Math.min(1.0, score),
    recommendedType
  };
}

/**
 * Summarize what player knows for prompt context
 */
function summarizePlayerKnowledge(playerKnowledge) {
  const summaries = [];
  
  if (playerKnowledge.npc_secrets.length > 0) {
    summaries.push(...playerKnowledge.npc_secrets.map(s => 
      `Player knows: ${s.description}`
    ));
  }
  
  if (playerKnowledge.witnessed_events.length > 0) {
    summaries.push(...playerKnowledge.witnessed_events.map(e =>
      `Player witnessed: ${e.description}`
    ));
  }
  
  if (playerKnowledge.overheard_conversations.length > 0) {
    summaries.push(...playerKnowledge.overheard_conversations.map(c =>
      `Player overheard: ${c.summary}`
    ));
  }
  
  return summaries;
}

/**
 * Summarize what character knows (but player doesn't)
 */
function summarizeCharacterKnowledge(characterKnowledge) {
  const summaries = [];
  
  if (characterKnowledge.internal_struggles.length > 0) {
    summaries.push(...characterKnowledge.internal_struggles.map(s =>
      `Character struggling with: ${s.description}`
    ));
  }
  
  if (characterKnowledge.true_feelings.length > 0) {
    summaries.push(...characterKnowledge.true_feelings.map(f =>
      `Character truly feels: ${f.description}`
    ));
  }
  
  return summaries;
}

/**
 * Determine the type of knowledge gap
 */
function determineGapType(playerKnowledge, characterKnowledge) {
  if (playerKnowledge.npc_secrets.length > 0) return 'secret_about_npc';
  if (playerKnowledge.witnessed_events.length > 0) return 'witnessed_event';
  if (characterKnowledge.internal_struggles.length > 0) return 'internal_struggle';
  if (characterKnowledge.true_feelings.length > 0) return 'hidden_feelings';
  return 'emotional_misread';
}

/**
 * Check if interaction topics overlap with knowledge gap
 */
function hasTopicOverlap(topics, knowledgeGap) {
  // Implementation would check if current conversation touches on
  // the area where knowledge gap exists
  return topics.some(topic => 
    knowledgeGap.gap_type.includes(topic.toLowerCase())
  );
}
```

### Layer Priority Matrix

| Layer | Priority | Token Budget | Can Omit If | Impact on Quality |
|-------|----------|-------------|-------------|-------------------|
| Character State | **CRITICAL** | 300-500 tokens | Never | Massive |
| Relationship History | **CRITICAL** | 200-400 tokens | Never | Massive |
| Current Interaction | **CRITICAL** | 150-300 tokens | Never | Massive |
| Player State | **IMPORTANT** | 100-200 tokens | Low-priority gens | Moderate |
| World Context | **OPTIONAL** | 50-100 tokens | Budget tight | Minor |
| Dramatic Irony Context | **IMPORTANT** | 150-250 tokens | No tension opportunity | High (for novel-quality) |
| Meta Context | **IMPORTANT** | 100-200 tokens | Template gens | Moderate |

**Total Token Budget:**
- **Full Context:** 1050-1950 tokens
- **Optimized Context:** 800-1350 tokens
- **Minimal Context:** 600-1050 tokens

---

## Building Comprehensive Context

### Layer 1: Character State (Critical)

```javascript
function buildCharacterContext(character) {
  return {
    // Basic Identity
    name: character.name,
    age: character.age,
    occupation: character.occupation,
    relationshipLevel: character.level,
    
    // Personality (OCEAN)
    personality: {
      openness: {
        score: character.ocean.openness,
        description: getOCEANDescription(character.ocean.openness, 'openness')
      },
      conscientiousness: {
        score: character.ocean.conscientiousness,
        description: getOCEANDescription(character.ocean.conscientiousness, 'conscientiousness')
      },
      extraversion: {
        score: character.ocean.extraversion,
        description: getOCEANDescription(character.ocean.extraversion, 'extraversion')
      },
      agreeableness: {
        score: character.ocean.agreeableness,
        description: getOCEANDescription(character.ocean.agreeableness, 'agreeableness')
      },
      neuroticism: {
        score: character.ocean.neuroticism,
        description: getOCEANDescription(character.ocean.neuroticism, 'neuroticism')
      }
    },
    
    // Current State
    currentDescription: character.description,
    emotionalState: character.currentEmotion,
    
    // Recent Memories (prioritized)
    recentMemories: prioritizeMemories(character.memories, 10),
    
    // Established Facts (canonical)
    establishedFacts: character.canonicalFacts,
    
    // Visual Details
    appearance: character.visualDetails
  };
}

function getOCEANDescription(score, trait) {
  const descriptions = {
    openness: {
      low: "Practical, prefers routine, concrete thinking",
      medium: "Balanced, open to new ideas occasionally",
      high: "Creative, curious, loves new experiences"
    },
    conscientiousness: {
      low: "Spontaneous, flexible, goes with flow",
      medium: "Generally organized but adaptable",
      high: "Organized, disciplined, reliable"
    },
    extraversion: {
      low: "Introverted, energized by alone time",
      medium: "Ambivert, context-dependent",
      high: "Extraverted, energized by social interaction"
    },
    agreeableness: {
      low: "Direct, competitive, values honesty",
      medium: "Balanced, diplomatic but authentic",
      high: "Warm, empathetic, cooperative"
    },
    neuroticism: {
      low: "Emotionally stable, calm under pressure",
      medium: "Normal emotional range",
      high: "Sensitive, prone to worry"
    }
  };
  
  if (score < 2.5) return descriptions[trait].low;
  if (score < 3.5) return descriptions[trait].medium;
  return descriptions[trait].high;
}
```

### Layer 2: Relationship History

```javascript
function buildRelationshipContext(character, player) {
  const firstMet = character.firstMetTimestamp;
  const now = Date.now();
  const durationWeeks = Math.floor((now - firstMet) / (7 * 24 * 60 * 60 * 1000));
  
  return {
    // Timeline
    durationWeeks: durationWeeks,
    firstMetDate: new Date(firstMet).toLocaleDateString(),
    totalInteractions: character.interactions.length,
    
    // Interaction Breakdown
    interactionTypes: categorizeInteractions(character.interactions),
    
    // Relationship Metrics
    trustLevel: character.trust,
    respectLevel: character.respect,
    attractionLevel: character.attraction || 0,
    relationshipQuality: calculateQuality(character),
    
    // History
    significantMoments: character.milestones.map(m => ({
      week: m.week,
      type: m.type,
      description: m.description
    })),
    
    conflictHistory: character.conflicts.map(c => ({
      type: c.type,
      resolved: c.resolved,
      week: c.week
    })),
    
    // Growth Trajectory
    personalityEvolution: character.personalityHistory.map((snapshot, index) => ({
      week: snapshot.week,
      changes: describePersonalityChanges(
        index > 0 ? character.personalityHistory[index - 1] : null,
        snapshot
      )
    }))
  };
}

function categorizeInteractions(interactions) {
  const categories = {
    casual: 0,        // Coffee, walks, casual meetups
    deep: 0,          // Meaningful conversations
    activity: 0,      // Shared activities
    conflict: 0,      // Disagreements
    crisis: 0,        // Emergency support
    romantic: 0       // Romantic interactions
  };
  
  interactions.forEach(interaction => {
    categories[interaction.category]++;
  });
  
  return categories;
}
```

### Layer 3: Current Interaction

```javascript
function buildInteractionContext(interaction, player) {
  return {
    // Activity Details
    activity: {
      name: interaction.activity.name,
      type: interaction.activity.type,
      location: interaction.location.name,
      locationDetails: interaction.location.description
    },
    
    // Timing
    timing: {
      timeOfDay: interaction.timeOfDay,
      dayOfWeek: interaction.dayOfWeek,
      duration: interaction.estimatedDuration
    },
    
    // Player Actions
    playerActions: {
      dialogueChoice: interaction.playerChoice.text,
      choiceType: interaction.playerChoice.type,
      emotionalApproach: interaction.playerChoice.emotion,
      resourcesCommitted: interaction.playerChoice.resources || null
    },
    
    // Player State During Interaction
    playerState: {
      emotion: player.currentEmotion,
      stress: player.stress,
      energy: player.energy
    },
    
    // Context
    interactionContext: {
      isFirstTime: interaction.isFirstTimeActivity,
      wasPlanned: interaction.wasPlanned,
      otherCharactersPresent: interaction.otherCharacters || [],
      specialCircumstances: interaction.specialContext || null
    }
  };
}
```

### Layer 4: Player State

```javascript
function buildPlayerContext(player) {
  return {
    // Current Emotional State
    emotionalState: {
      primary: player.currentEmotion,
      intensity: player.emotionIntensity,
      recent: player.recentEmotions.slice(-3)
    },
    
    // Life Context
    lifeContext: {
      career: player.career,
      careerSatisfaction: player.careerSatisfaction,
      stress: player.stress,
      recentLifeEvents: player.recentEvents.slice(-5).map(e => ({
        type: e.type,
        description: e.description,
        weeksAgo: calculateWeeksAgo(e.timestamp)
      }))
    },
    
    // Social Context
    socialContext: {
      reputation: player.reputation,
      activeRelationships: player.activeRelationshipCount,
      friendCount: player.friends.length,
      recentSocialPatterns: analyzeRecentSocialActivity(player)
    },
    
    // Play Style
    playStyle: {
      preferredInteractions: player.interactionPreferences,
      averageSessionLength: player.avgSessionLength,
      pacing: player.preferredPacing,
      riskTaking: player.riskProfile
    }
  };
}

function analyzeRecentSocialActivity(player) {
  const recent = player.interactions.slice(-20);
  return {
    mostFrequentActivity: getMostCommon(recent.map(i => i.activity)),
    averageInteractionsPerWeek: calculateAvgPerWeek(recent),
    diversityScore: calculateDiversityScore(recent)
  };
}
```

### Layer 5: World Context

```javascript
function buildWorldContext() {
  return {
    // Time
    time: {
      timeOfDay: getCurrentTimeOfDay(),
      dayOfWeek: getDayOfWeek(),
      season: getCurrentSeason(),
      month: getCurrentMonth()
    },
    
    // Environment
    environment: {
      weather: getCurrentWeather(),
      temperature: getCurrentTemperature(),
      ambience: getSeasonalAmbience()
    },
    
    // World Events (optional flavor)
    worldEvents: {
      recentEvents: getRecentWorldEvents().slice(-3),
      holidays: getUpcomingHolidays()
    }
  };
}

function getSeasonalAmbience() {
  const season = getCurrentSeason();
  const ambiences = {
    spring: "Fresh blooms, warming days, sense of renewal",
    summer: "Long days, warm nights, vibrant energy",
    fall: "Crisp air, falling leaves, cozy atmosphere",
    winter: "Cold nights, early darkness, intimate gatherings"
  };
  return ambiences[season];
}
```

### Layer 6: Meta Context

```javascript
function buildMetaContext(character, player, interaction) {
  return {
    // Evolution Guidance
    evolution: {
      currentLevel: character.level,
      targetLevel: determineTargetLevel(character, interaction),
      evolutionRate: calculateEvolutionRate(character),
      shouldEvolvThisInteraction: shouldEvolve(character, interaction)
    },
    
    // Narrative Pacing
    pacing: {
      overall: assessNarrativePacing(player.playthrough),
      thisCharacter: assessCharacterPacing(character),
      desiredTone: determineDesiredTone(interaction),
      tensions: identifyNarrativeTensions(character, player)
    },
    
    // Quality Control
    qualityContext: {
      previousGenerations: character.aiGenerationHistory.slice(-3),
      consistencyRequirements: character.canonicalFacts,
      avoidancePatterns: identifyOverusedPatterns(character)
    },
    
    // Generation Settings
    generationSettings: {
      importance: assessInteractionImportance(interaction),
      requiredQuality: determineRequiredQuality(interaction),
      suggestedModel: routeToModel(interaction),
      tokenBudget: calculateTokenBudget(interaction)
    }
  };
}

function determineDesiredTone(interaction) {
  if (interaction.type === 'crisis') return 'intense_emotional';
  if (interaction.type === 'romantic') return 'intimate_warm';
  if (interaction.type === 'conflict') return 'tense_authentic';
  if (interaction.isFirstTime) return 'curious_exploring';
  return 'comfortable_friendly';
}
```

---

## Context Injection Templates

### Full Context Template (High Priority)

```markdown
COMPREHENSIVE CONTEXT FOR AI:

=== CHARACTER CURRENT STATE ===
Name: {name}
Level: {level} ({level_name})
Age: {age}
Occupation: {occupation}

Personality Profile (OCEAN):
- Openness: {O}/5 - {O_description}
- Conscientiousness: {C}/5 - {C_description}
- Extraversion: {E}/5 - {E_description}
- Agreeableness: {A}/5 - {A_description}
- Neuroticism: {N}/5 - {N_description}

Current Emotional State: {emotion} (intensity: {intensity}/10)
Current Description: "{description}"

Physical Details Established:
{visual_details}

=== RELATIONSHIP HISTORY ===
Duration: {weeks} weeks ({interactions} interactions)
First Met: {first_met_date}

Relationship Metrics:
- Quality: {quality}/10
- Trust: {trust}/10
- Respect: {respect}/10
- Attraction: {attraction}/10 (if applicable)

Interaction Breakdown:
- Coffee/Casual: {casual_count}
- Deep Conversations: {deep_count}
- Activities Together: {activity_count}
- Conflicts: {conflict_count} (resolved: {resolved_count})
- Crisis Support: {crisis_count}

Significant Past Moments:
{list_significant_memories}

Personality Evolution:
{personality_changes_summary}

=== CURRENT INTERACTION ===
Activity: {activity}
Location: {location}
Time: {time_of_day}, {day_of_week}
Weather: {weather}
Duration: {duration} minutes

Player's Approach: {player_dialogue_choice}
Player's Emotional State: {player_emotion}
Player's Stress Level: {player_stress}/10

Other Context:
{additional_context}

=== PLAYER INFORMATION ===
The player character has:
- Career: {player_career} (satisfaction: {career_satisfaction}/10)
- Recent Life Events: {player_recent_events}
- Current Stress: {player_stress}/10
- Energy Level: {player_energy}/10

Player's Interaction Style with {name}:
{player_style_analysis}

=== WORLD CONTEXT ===
Season: {season}
Time of Day: {time_of_day}
Ambience: {seasonal_ambience}

=== META GUIDANCE ===
Narrative Pacing: {pacing} (slow-burn/moderate/fast)
Evolution Target: Level {current} → {target}
Desired Emotional Tone: {tone}
Interaction Importance: {importance}/10

This interaction should:
{specific_guidance_for_this_evolution}

Previous AI Generations for Consistency:
Generation 1: {prev_gen_1_summary}
Generation 2: {prev_gen_2_summary}
Generation 3: {prev_gen_3_summary}

Avoid These Patterns (already used):
{overused_patterns}

=== YOUR TASK ===
{specific_task_instructions}
```

### Optimized Context Template (Medium Priority)

```markdown
CONTEXT FOR AI:

=== CHARACTER ===
{name}, Level {level}, {occupation}
OCEAN: O:{O} C:{C} E:{E} A:{A} N:{N}
Current Mood: {emotion}
Description: "{description}"

=== RELATIONSHIP ===
{weeks} weeks, {interactions} interactions
Trust: {trust}/10, Quality: {quality}/10
Key Memories: {top_3_memories}
Evolution: {personality_changes}

=== INTERACTION ===
Activity: {activity} at {location}
Player Choice: {player_choice}
Context: {interaction_context}

=== GUIDANCE ===
Target: Level {current} → {target}
Tone: {tone}
Importance: {importance}/10

Previous Generations: {prev_summary}

=== TASK ===
{task}
```

### Minimal Context Template (Low Priority)

```markdown
CHARACTER: {name} (Level {level})
OCEAN: O:{O} C:{C} E:{E} A:{A} N:{N}
RELATIONSHIP: {weeks} weeks, Trust {trust}/10
INTERACTION: {activity}
TASK: {task}
```

---

## Memory Tier System

### Memory Hierarchy

```javascript
const MEMORY_TIERS = {
  TRIVIAL: {
    weight: [0.1, 0.3],
    fadeTime: '2-4 weeks',
    personalityImpact: 'none',
    storage: 'summarized',
    description: 'Routine interactions, small talk'
  },
  
  NOTABLE: {
    weight: [0.3, 0.6],
    fadeTime: 'weeks to months',
    personalityImpact: 'minimal (0.1-0.2 shifts)',
    storage: 'discrete',
    description: 'Enjoyable interactions, learning about each other'
  },
  
  SIGNIFICANT: {
    weight: [0.6, 0.8],
    fadeTime: 'months to years',
    personalityImpact: 'moderate (0.2-0.4 shifts)',
    storage: 'permanent',
    description: 'Vulnerability shared, important revelations'
  },
  
  DEFINING: {
    weight: [0.8, 1.0],
    fadeTime: 'never',
    personalityImpact: 'significant (0.3-0.5+ shifts)',
    storage: 'permanent + frequently recalled',
    description: 'Relationship turning points, crisis support'
  }
};

function classifyMemory(interaction, relationshipContext) {
  // Trivial if routine and low emotional weight
  if (interaction.isRoutine && interaction.emotionalWeight < 0.3) {
    return MEMORY_TIERS.TRIVIAL;
  }
  
  // Significant if vulnerability or crisis
  if (interaction.vulnerabilityShared || interaction.type === 'crisis') {
    return interaction.emotionalWeight > 0.7 
      ? MEMORY_TIERS.DEFINING 
      : MEMORY_TIERS.SIGNIFICANT;
  }
  
  // Defining if level change or major milestone
  if (interaction.causedLevelChange || interaction.isMilestone) {
    return MEMORY_TIERS.DEFINING;
  }
  
  // Otherwise notable
  return MEMORY_TIERS.NOTABLE;
}
```

### Memory Structure

```javascript
class Memory {
  constructor(data) {
    this.id = generateUUID();
    this.tier = data.tier;
    this.weight = data.weight;
    this.timestamp = Date.now();
    
    // Core Content
    this.description = data.description;
    this.sensoryDetails = data.sensoryDetails;
    this.emotionalTone = data.emotionalTone;
    this.dialogueContent = data.dialogueContent;
    
    // Context
    this.activity = data.activity;
    this.location = data.location;
    this.weekNumber = data.weekNumber;
    this.relationshipLevel = data.relationshipLevel;
    
    // Impact
    this.personalityImpact = data.personalityImpact;
    this.futureImplications = data.futureImplications;
    this.unlockedTopics = data.unlockedTopics;
    
    // Metadata
    this.recallCount = 0;
    this.lastRecalled = null;
    this.fadeStatus = 'fresh';
  }
  
  recall() {
    this.recallCount++;
    this.lastRecalled = Date.now();
    
    // Strengthen memory through recall
    if (this.tier !== MEMORY_TIERS.DEFINING) {
      this.weight = Math.min(1.0, this.weight + 0.05);
    }
  }
  
  fade(weeksPassed) {
    if (this.tier === MEMORY_TIERS.DEFINING) {
      return; // Never fade
    }
    
    const fadeRate = {
      TRIVIAL: 0.1,    // 10% per week
      NOTABLE: 0.03,   // 3% per week
      SIGNIFICANT: 0.01 // 1% per week
    };
    
    this.weight -= fadeRate[this.tier.name] * weeksPassed;
    
    if (this.weight < 0.1) {
      this.fadeStatus = 'faded';
    } else if (this.weight < 0.3) {
      this.fadeStatus = 'fading';
    }
  }
  
  shouldIncludeInContext(priority) {
    // Always include defining memories
    if (this.tier === MEMORY_TIERS.DEFINING) return true;
    
    // Include significant if medium+ priority
    if (this.tier === MEMORY_TIERS.SIGNIFICANT && priority >= 2) return true;
    
    // Include notable if high priority and not faded
    if (this.tier === MEMORY_TIERS.NOTABLE && priority >= 3 && this.fadeStatus !== 'faded') return true;
    
    // Skip trivial unless explicitly requested
    return false;
  }
}
```

---

## Memory Recall & Prioritization

### Recall Priority Algorithm

```javascript
function prioritizeMemories(character, currentInteraction, count = 10) {
  const memories = character.memories;
  
  // Score each memory for relevance
  const scoredMemories = memories.map(memory => ({
    memory,
    score: calculateRelevanceScore(memory, currentInteraction, character)
  }));
  
  // Sort by score
  scoredMemories.sort((a, b) => b.score - a.score);
  
  // Take top N
  return scoredMemories.slice(0, count).map(sm => sm.memory);
}

function calculateRelevanceScore(memory, currentInteraction, character) {
  let score = 0;
  
  // 1. Tier weight (40% of score)
  score += memory.weight * 0.4;
  
  // 2. Recency (20% of score)
  const weeksSince = calculateWeeksSince(memory.timestamp);
  const recencyScore = Math.max(0, 1 - (weeksSince / 52)); // Full score if within year
  score += recencyScore * 0.2;
  
  // 3. Contextual relevance (20% of score)
  const contextScore = assessContextualRelevance(memory, currentInteraction);
  score += contextScore * 0.2;
  
  // 4. Memory Resonance (Master Truths v1.2) (20% of score)
  const resonanceScore = assessMemoryResonance(memory, currentInteraction, character);
  score += resonanceScore * 0.2;
  
  // 5. Recall frequency (10% of score)
  const recallScore = Math.min(1.0, memory.recallCount / 10);
  score += recallScore * 0.1;
  
  return score;
}

// Master Truths v1.2: Memory Resonance Scoring
function assessMemoryResonance(memory, currentInteraction, character) {
  let resonance = 0;
  
  // Past trauma triggers: 0.95 weight
  if (memory.isTraumaticEvent && isTriggeringSituation(currentInteraction, memory)) {
    resonance = Math.max(resonance, 0.95);
  }
  
  // Opposite emotion growth: 0.9 weight
  // (e.g., past betrayal memory recalled during trust-building moment)
  if (isOppositeEmotionalContext(memory.emotionalTone, currentInteraction.emotionalTone)) {
    resonance = Math.max(resonance, 0.9);
  }
  
  // Same emotion pattern: 0.8 weight
  // (e.g., past joy recalled during joyful moment)
  if (memory.emotionalTone === currentInteraction.emotionalTone) {
    resonance = Math.max(resonance, 0.8);
  }
  
  // Contextual dampening: 0.7 weight
  // (e.g., past memories that provide context but aren't emotionally charged)
  if (memory.providesContext && !memory.isEmotionallyCharged) {
    resonance = Math.max(resonance, 0.7);
  }
  
  return resonance;
}

function isTriggeringSituation(current, traumaMemory) {
  // Check if current situation resembles traumatic memory
  return (
    current.activity === traumaMemory.activity ||
    current.emotionalStakes > 7.0 && traumaMemory.emotionalStakes > 7.0 ||
    current.themeOverlap.some(theme => traumaMemory.themes.includes(theme))
  );
}

function isOppositeEmotionalContext(pastEmotion, currentEmotion) {
  const opposites = {
    'betrayal': 'trust',
    'isolation': 'connection',
    'grief': 'joy',
    'anger': 'peace',
    'fear': 'safety'
  };
  return opposites[pastEmotion] === currentEmotion;
}

function assessContextualRelevance(memory, currentInteraction) {
  let relevance = 0;
  
  // Same activity type?
  if (memory.activity === currentInteraction.activity) {
    relevance += 0.3;
  }
  
  // Same location?
  if (memory.location === currentInteraction.location) {
    relevance += 0.2;
  }
  
  // Similar emotional context?
  if (memory.emotionalTone === currentInteraction.predictedTone) {
    relevance += 0.2;
  }
  
  // References something player just mentioned?
  if (currentInteraction.topicsReferenced.some(topic => 
    memory.unlockedTopics.includes(topic)
  )) {
    relevance += 0.3;
  }
  
  // NEW: Enhanced Emotional Resonance (see novel-quality enhancements)
  const emotionalResonance = calculateEmotionalResonance(memory, currentInteraction);
  relevance += emotionalResonance * 0.4;
  
  return Math.min(1.0, relevance);
}

/**
 * Enhanced Memory Retrieval with Emotional Resonance (NEW)
 * 
 * Purpose: Prioritize memories that create emotional callbacks,
 * dramatic tension, and novel-quality storytelling moments.
 */
function calculateEmotionalResonance(memory, context) {
  let resonance = 0;
  
  const memoryEmotion = memory.emotionalTone;
  const currentEmotion = context.predictedTone || context.playerEmotion;
  
  // 1. SAME EMOTION, DIFFERENT CONTEXT (0.8 weight)
  //    Example: Both memories involve joy, but first was achievement, now is connection
  if (memoryEmotion === currentEmotion && 
      memory.activity !== context.activity) {
    resonance += 0.8;
  }
  
  // 2. OPPOSITE EMOTION, GROWTH OPPORTUNITY (0.9 weight)
  //    Example: Memory of sadness, current situation is joy - shows character growth
  const emotionPairs = {
    'joy': 'sadness',
    'sadness': 'joy',
    'calm': 'anxiety',
    'anxiety': 'calm',
    'anger': 'contentment',
    'contentment': 'anger'
  };
  
  if (emotionPairs[memoryEmotion] === currentEmotion) {
    resonance += 0.9;
  }
  
  // 3. PAST TRAUMA, CURRENT TRIGGER (0.95 weight)
  //    Example: Memory of breakup, current situation involves romantic risk
  if (memory.tier === 'Crisis' || memory.tier === 'Defining') {
    if (memoryEmotion === 'sadness' || memoryEmotion === 'anxiety' || memoryEmotion === 'anger') {
      // Check for situational similarity that could trigger memory
      if (hasSituationalOverlap(memory, context)) {
        resonance += 0.95;
      }
    }
  }
  
  // 4. PAST JOY, CURRENT SADNESS (0.85 weight)
  //    Example: Memory of happy time with friend, friend now distant - creates poignancy
  if (memoryEmotion === 'joy' && (currentEmotion === 'sadness' || currentEmotion === 'anxiety')) {
    // Especially powerful if involves same character/relationship
    if (memory.involvedCharacters && 
        memory.involvedCharacters.some(char => context.characterNames?.includes(char))) {
      resonance += 0.85;
    }
  }
  
  // 5. EMOTIONAL GROWTH CALLBACK (0.7 weight)
  //    Example: Memory of struggling with emotion, now handling it better
  if (memory.personalityImpact && context.character?.recentGrowth) {
    const growthAreas = context.character.recentGrowth.map(g => g.area);
    if (memory.personalityImpact.traits.some(trait => growthAreas.includes(trait))) {
      resonance += 0.7;
    }
  }
  
  return Math.min(1.0, resonance);
}

/**
 * Check if memory and current context have situational overlap
 * that could make memory emotionally resonant
 */
function hasSituationalOverlap(memory, context) {
  // Same emotional stakes
  if (memory.tags && context.tags) {
    const sharedTags = memory.tags.filter(tag => context.tags.includes(tag));
    if (sharedTags.length > 0) return true;
  }
  
  // Same social context (e.g., both involve romantic relationships)
  if (memory.relationshipContext && context.relationshipContext) {
    if (memory.relationshipContext === context.relationshipContext) return true;
  }
  
  // Same life domain (career, family, friendship, romance)
  if (memory.lifeDomain && context.lifeDomain) {
    if (memory.lifeDomain === context.lifeDomain) return true;
  }
  
  return false;
}
```

### Memory Consolidation

```javascript
class MemoryManager {
  constructor(character) {
    this.character = character;
  }
  
  // Weekly memory maintenance
  weeklyConsolidation() {
    this.fadeOldMemories();
    this.summarizeTrivialMemories();
    this.strengthenDefiningMemories();
    this.pruneExcessMemories();
  }
  
  fadeOldMemories() {
    this.character.memories.forEach(memory => {
      const weeksSince = calculateWeeksSince(memory.timestamp);
      memory.fade(weeksSince);
    });
  }
  
  summarizeTrivialMemories() {
    // Group trivial memories by activity type
    const trivialByActivity = this.character.memories
      .filter(m => m.tier === MEMORY_TIERS.TRIVIAL && m.fadeStatus !== 'faded')
      .reduce((groups, memory) => {
        const key = memory.activity;
        if (!groups[key]) groups[key] = [];
        groups[key].push(memory);
        return groups;
      }, {});
    
    // Summarize groups with 5+ memories
    Object.entries(trivialByActivity).forEach(([activity, memories]) => {
      if (memories.length >= 5) {
        const summary = this.createSummaryMemory(activity, memories);
        this.character.memories.push(summary);
        
        // Remove individual trivial memories
        this.character.memories = this.character.memories.filter(m => 
          !memories.includes(m)
        );
      }
    });
  }
  
  createSummaryMemory(activity, memories) {
    return new Memory({
      tier: MEMORY_TIERS.NOTABLE,
      weight: 0.4,
      description: `We often ${activity} together. It's become a comfortable routine.`,
      sensoryDetails: [],
      emotionalTone: 'comfortable',
      activity: activity,
      location: memories[0].location,
      weekNumber: memories[memories.length - 1].weekNumber,
      relationshipLevel: this.character.level,
      personalityImpact: null,
      futureImplications: ['Established routine', 'Comfortable pattern'],
      unlockedTopics: []
    });
  }
  
  strengthenDefiningMemories() {
    // Defining memories should be easily recalled
    this.character.memories
      .filter(m => m.tier === MEMORY_TIERS.DEFINING)
      .forEach(memory => {
        if (memory.weight < 0.95) {
          memory.weight = Math.min(1.0, memory.weight + 0.05);
        }
      });
  }
  
  pruneExcessMemories() {
    // Keep max 100 discrete memories
    const MAX_MEMORIES = 100;
    
    if (this.character.memories.length > MAX_MEMORIES) {
      // Sort by relevance score
      const scored = this.character.memories.map(m => ({
        memory: m,
        score: this.calculatePruneScore(m)
      }));
      
      scored.sort((a, b) => b.score - a.score);
      
      // Keep top MAX_MEMORIES
      this.character.memories = scored.slice(0, MAX_MEMORIES).map(s => s.memory);
    }
  }
  
  calculatePruneScore(memory) {
    // Never prune defining
    if (memory.tier === MEMORY_TIERS.DEFINING) return Infinity;
    
    // Score based on weight, recency, and recall count
    let score = memory.weight * 0.5;
    
    const weeksSince = calculateWeeksSince(memory.timestamp);
    score += Math.max(0, 1 - (weeksSince / 52)) * 0.3;
    
    score += Math.min(1.0, memory.recallCount / 10) * 0.2;
    
    return score;
  }
}
```

---

## Context Optimization

### Token Budget Management

```javascript
class ContextBuilder {
  constructor(tokenBudget = 1500) {
    this.tokenBudget = tokenBudget;
    this.tokenCount = 0;
  }
  
  buildOptimizedContext(character, player, interaction, priority) {
    const context = {};
    
    // Layer 1: Character (always include, ~400 tokens)
    context.character = this.buildCharacterLayer(character);
    this.tokenCount += this.estimateTokens(context.character);
    
    // Layer 2: Relationship (always include, ~300 tokens)
    context.relationship = this.buildRelationshipLayer(character, player);
    this.tokenCount += this.estimateTokens(context.relationship);
    
    // Layer 3: Interaction (always include, ~200 tokens)
    context.interaction = this.buildInteractionLayer(interaction, player);
    this.tokenCount += this.estimateTokens(context.interaction);
    
    // Remaining budget for optional layers
    const remainingBudget = this.tokenBudget - this.tokenCount;
    
    // Layer 4: Player (if budget allows, ~150 tokens)
    if (remainingBudget > 150 && priority >= 2) {
      context.player = this.buildPlayerLayer(player);
      this.tokenCount += this.estimateTokens(context.player);
    }
    
    // Layer 5: World (if budget allows, ~75 tokens)
    if (remainingBudget > 75 && priority >= 3) {
      context.world = this.buildWorldLayer();
      this.tokenCount += this.estimateTokens(context.world);
    }
    
    // Layer 6: Meta (if budget allows, ~150 tokens)
    if (remainingBudget > 150 && priority >= 2) {
      context.meta = this.buildMetaLayer(character, player, interaction);
      this.tokenCount += this.estimateTokens(context.meta);
    }
    
    return context;
  }
  
  estimateTokens(obj) {
    // Rough estimation: 1 token ~= 4 characters
    const json = JSON.stringify(obj);
    return Math.ceil(json.length / 4);
  }
  
  buildCharacterLayer(character) {
    // Core character info, optimized for tokens
    return {
      name: character.name,
      level: character.level,
      ocean: character.ocean,
      description: this.truncate(character.description, 300),
      memories: prioritizeMemories(character, null, 5).map(m => ({
        description: this.truncate(m.description, 150),
        week: m.weekNumber
      }))
    };
  }
  
  truncate(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
  }
}
```

### Context Compression Techniques

```javascript
// Technique 1: Summary instead of full history
function compressRelationshipHistory(character) {
  const interactions = character.interactions;
  
  return {
    summary: `${character.name} and player have known each other for ${character.durationWeeks} weeks ` +
             `with ${interactions.length} interactions. Their relationship has evolved from ` +
             `${getLevelName(character.startLevel)} to ${getLevelName(character.level)}.`,
    
    keyMoments: character.milestones.map(m => ({
      week: m.week,
      summary: this.summarize(m.description, 50)
    })).slice(-3), // Last 3 only
    
    metrics: {
      trust: character.trust,
      quality: character.quality
    }
  };
}

// Technique 2: Memory clustering
function clusterMemories(memories) {
  // Group similar memories together
  const clusters = {};
  
  memories.forEach(memory => {
    const key = `${memory.activity}_${memory.emotionalTone}`;
    if (!clusters[key]) {
      clusters[key] = [];
    }
    clusters[key].push(memory);
  });
  
  // For each cluster, keep the best example
  return Object.values(clusters).map(cluster => {
    // Sort by weight
    cluster.sort((a, b) => b.weight - a.weight);
    return cluster[0]; // Return highest weight memory
  });
}

// Technique 3: Progressive detail reduction
function adaptiveContextCompression(context, targetTokens, currentTokens) {
  if (currentTokens <= targetTokens) return context;
  
  const compressionSteps = [
    // Step 1: Remove world context
    () => delete context.world,
    
    // Step 2: Reduce memories to top 5
    () => context.character.memories = context.character.memories.slice(0, 5),
    
    // Step 3: Truncate descriptions
    () => {
      context.character.description = truncate(context.character.description, 200);
      context.character.memories.forEach(m => {
        m.description = truncate(m.description, 100);
      });
    },
    
    // Step 4: Remove player context
    () => delete context.player,
    
    // Step 5: Further reduce memories to top 3
    () => context.character.memories = context.character.memories.slice(0, 3),
    
    // Step 6: Minimal relationship history
    () => {
      context.relationship = {
        duration: context.relationship.durationWeeks,
        trust: context.relationship.trustLevel,
        level: context.relationship.level
      };
    }
  ];
  
  for (const step of compressionSteps) {
    step();
    currentTokens = estimateTokens(context);
    if (currentTokens <= targetTokens) break;
  }
  
  return context;
}
```

---

## Memory Persistence & Fade

### Fade Algorithm

```javascript
class MemoryFadeSystem {
  constructor() {
    this.fadeRates = {
      TRIVIAL: 0.10,      // 10% per week
      NOTABLE: 0.03,      // 3% per week
      SIGNIFICANT: 0.01,  // 1% per week
      DEFINING: 0         // Never fades
    };
  }
  
  weeklyFade(character) {
    const now = Date.now();
    
    character.memories.forEach(memory => {
      const weeksSinceCreated = calculateWeeksSince(memory.timestamp);
      const weeksSinceRecalled = memory.lastRecalled 
        ? calculateWeeksSince(memory.lastRecalled)
        : weeksSinceCreated;
      
      // Fade based on tier
      const fadeRate = this.fadeRates[memory.tier.name];
      
      // Modified by recall - recently recalled memories fade slower
      const recallModifier = Math.max(0.2, 1 - (memory.recallCount / 20));
      const adjustedFadeRate = fadeRate * recallModifier;
      
      // Apply fade
      memory.weight -= adjustedFadeRate * weeksSinceRecalled;
      memory.weight = Math.max(0, memory.weight);
      
      // Update fade status
      if (memory.weight < 0.1) {
        memory.fadeStatus = 'faded';
      } else if (memory.weight < 0.3) {
        memory.fadeStatus = 'fading';
      } else {
        memory.fadeStatus = 'fresh';
      }
    });
    
    // Remove completely faded non-defining memories
    character.memories = character.memories.filter(m => 
      m.tier === MEMORY_TIERS.DEFINING || m.weight > 0
    );
  }
  
  recallStrengthening(memory) {
    // Recalling a memory strengthens it
    if (memory.tier !== MEMORY_TIERS.DEFINING) {
      const strengthenAmount = 0.05 * (1 + memory.recallCount * 0.01);
      memory.weight = Math.min(1.0, memory.weight + strengthenAmount);
    }
    
    memory.recall();
  }
}
```

---

## Implementation Examples

### Example 1: Full Context Build

```javascript
async function generateEvolution(character, player, interaction) {
  // 1. Build context
  const contextBuilder = new ContextBuilder(1500);
  const context = contextBuilder.buildOptimizedContext(
    character, 
    player, 
    interaction, 
    3 // High priority
  );
  
  // 2. Select appropriate template
  const template = selectTemplate(character.level, interaction.type);
  
  // 3. Fill template with context
  const prompt = fillTemplate(template, context);
  
  // 4. Estimate tokens
  const estimatedTokens = estimateTokens(prompt);
  console.log(`Prompt tokens: ${estimatedTokens}`);
  
  // 5. Call AI
  const response = await callAI(prompt);
  
  // 6. Mark memories as recalled (for fade system)
  context.character.memories.forEach(memory => {
    memoryFadeSystem.recallStrengthening(memory);
  });
  
  return response;
}
```

### Example 2: Context Optimization

```javascript
function optimizeContextForBudget(context, targetTokens) {
  let currentTokens = estimateTokens(context);
  
  if (currentTokens <= targetTokens) {
    return context;
  }
  
  console.log(`Over budget: ${currentTokens} / ${targetTokens}`);
  
  // Apply compression
  context = adaptiveContextCompression(context, targetTokens, currentTokens);
  
  currentTokens = estimateTokens(context);
  console.log(`After compression: ${currentTokens} / ${targetTokens}`);
  
  return context;
}
```

### Example 3: Memory Prioritization

```javascript
function getMemoriesForContext(character, interaction, count = 10) {
  // Get all non-faded memories
  const activeMemories = character.memories.filter(m => 
    m.fadeStatus !== 'faded'
  );
  
  // Prioritize memories
  const prioritized = prioritizeMemories(character, interaction, count * 2);
  
  // Ensure we always include defining memories
  const definingMemories = prioritized.filter(m => 
    m.tier === MEMORY_TIERS.DEFINING
  );
  
  // Fill remaining slots with highest scoring memories
  const nonDefining = prioritized.filter(m => 
    m.tier !== MEMORY_TIERS.DEFINING
  );
  
  const selectedMemories = [
    ...definingMemories,
    ...nonDefining.slice(0, count - definingMemories.length)
  ];
  
  return selectedMemories;
}
```

---

## Summary

### Key Takeaways

**Context Architecture:**
- Use 6-layer model for comprehensive context
- Prioritize: Character > Relationship > Interaction
- Budget tokens carefully (900-1700 range)

**Memory Management:**
- 4-tier memory system (Trivial → Defining)
- Memories fade over time (except Defining)
- Recall strengthens memories
- Consolidate trivial memories into summaries

**Optimization:**
- Estimate tokens before generation
- Compress context adaptively
- Cluster similar memories
- Remove faded memories weekly

**Best Practices:**
- Always include character, relationship, and interaction layers
- Prioritize memories by relevance, not just recency
- Run weekly consolidation to manage memory count
- Track recall to strengthen important memories

---

## Next Steps

**You now understand:**
- ✅ How to build comprehensive context
- ✅ Memory tier system and management
- ✅ Context optimization techniques
- ✅ Memory fade and consolidation

**Continue to:**
- → 35-consistency-coherence.md for quality validation
- → 39-cost-performance-targets.md for token budgeting
- ← 33-prompt-templates-library.md for template usage

**Remember:**
- Context quality = generation quality
- Memory persistence creates character continuity
- Token budgets must be respected
- Weekly maintenance prevents memory bloat

**This system ensures characters remember what matters, forget what doesn't, and always have rich context for authentic evolution. 🧠**

---

## Compliance Checklist (Master Truths v1.2)

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0)
- [x] **Urgency assessment added to Layer 3 context (level, multiplier, score, reasoning)**
- [x] **Memory resonance scoring implemented (weights: 0.7-0.95 based on emotional context)**
- [x] **Trauma triggers prioritized at 0.95 weight in memory recall**
- [x] **Opposite emotion growth memories weighted at 0.9**
- [x] **Same emotion pattern memories weighted at 0.8**
- [x] Emotional capacity included in Layer 1 character state
- [x] 4-tier memory system maintained (Trivial → Defining)
- [x] This doc implements **Truths v1.2** context and memory systems

