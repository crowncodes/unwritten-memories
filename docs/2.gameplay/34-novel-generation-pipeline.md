# Novel Generation Pipeline - Life Bookshelf System

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for generating 12,000-18,000 word novels with emotional authenticity validation and novel-quality scoring

**References:**
- **Multi-Season:** `74-multi-season-continuity-spec.md` (context system)
- **Narrative Arc:** `31-narrative-arc-scaffolding.md` (story structure)
- **Season Flow:** `73-season-flow-implementation.md` (season completion)

---

## Overview

**Every completed season generates a novel** (12k-18k words) that captures the player's unique story. These novels accumulate in the character's "Life Bookshelf"—a permanent record of their 8-10 season journey (120k-180k words total).

**Generation Process:**
1. **Season Complete:** Player finishes season (12/24/36 weeks)
2. **Data Collection:** System gathers all gameplay data
3. **Novel Generation:** AI converts gameplay → narrative (2-3 minutes on-device)
4. **Life Bookshelf:** Novel added to character's permanent collection

**Novel Characteristics:**
- **Length:** 12k-18k words (varies by season length)
- **Structure:** 8-15 chapters mapping to narrative arc
- **Style:** 2nd person, present tense ("You do X")
- **Tone:** Player personality-influenced
- **Continuity:** References past seasons

---

## Novel Generation Pipeline

### Complete Flow

```typescript
interface NovelGenerationPipeline {
  // PHASE 1: Data Collection
  collect_season_data: () => SeasonData;
  
  // PHASE 2: Structural Planning
  generate_chapter_outline: (data: SeasonData) => ChapterOutline;
  
  // PHASE 3: Content Generation
  generate_chapters: (outline: ChapterOutline) => Chapter[];
  
  // PHASE 4: Continuity Integration
  integrate_past_seasons: (chapters: Chapter[]) => EnrichedChapters;
  
  // PHASE 5: Quality & Formatting
  validate_and_format: (enriched: EnrichedChapters) => Novel;
  
  // PHASE 6: Life Bookshelf Storage
  add_to_bookshelf: (novel: Novel) => void;
}
```

---

## PHASE 1: DATA COLLECTION

### Season Data Compilation

```javascript
async function collectSeasonData(seasonNumber, playerState) {
  return {
    // Basic Info
    season_metadata: {
      season_number: seasonNumber,
      season_title: determineSeasonTitle(playerState),
      season_length: playerState.season_length,        // 12/24/36 weeks
      weeks_played: playerState.weeks_played,
      aspiration: playerState.main_aspiration,
      aspiration_result: playerState.aspiration_outcome  // success/partial/failure
    },
    
    // Narrative Structure
    narrative_arc: {
      act_1_weeks: [1, 4],
      act_2_weeks: [5, 20],
      act_3_weeks: [21, 24],
      
      major_beats: playerState.narrative_beats,        // Setup, Midpoint, Crisis, Climax
      decisive_decisions: playerState.major_decisions, // 2-3 per season
      tension_curve: playerState.tension_history,
      hook_points: playerState.hook_points_resolved
    },
    
    // Character Development
    character_arc: {
      personality_start: playerState.personality_season_start,
      personality_end: playerState.personality_current,
      skills_gained: playerState.skills_gained_this_season,
      life_direction_shift: playerState.life_direction_changed,
      
      emotional_journey: playerState.emotional_state_history  // Week-by-week
    },
    
    // Relationships
    relationships: {
      npcs_met: playerState.npcs_met_this_season,
      npcs_deepened: playerState.relationships_leveled_up,
      major_moments: playerState.relationship_defining_moments,
      
      relationship_arcs: playerState.npcs.map(npc => ({
        npc_id: npc.id,
        level_start: npc.level_start,
        level_end: npc.level_end,
        trust_start: npc.trust_start,
        trust_end: npc.trust_end,
        key_moments: npc.major_moments_this_season
      }))
    },
    
    // Events & Activities
    events: {
      major_events: playerState.events_this_season.filter(e => e.significance >= 7),
      phase_transitions: playerState.phase_transitions,
      breakthroughs: playerState.breakthrough_moments,
      crises: playerState.crisis_moments,
      
      aspiration_milestones: playerState.aspiration_progress_moments
    },
    
    // Locations & Rituals
    world: {
      locations_discovered: playerState.new_locations,
      locations_evolved: playerState.location_evolutions,
      rituals_formed: playerState.fusions_this_season,
      
      key_locations: playerState.locations_with_significance
    },
    
    // Memory Highlights
    memories: {
      perfect_moments: playerState.memories.filter(m => m.weight >= 9),
      transformation_moments: playerState.memories.filter(m => m.type === "transformative"),
      relationship_moments: playerState.memories.filter(m => m.type === "relationship"),
      
      top_20_moments: playerState.memories
        .sort((a, b) => b.weight - a.weight)
        .slice(0, 20)
    },
    
    // Past Context (if Season 2+)
    past_seasons: seasonNumber > 1 ? {
      previous_season_summary: await getTier2Context(seasonNumber - 1),
      earlier_seasons: await getTier3Context(),
      character_trajectory: playerState.multi_season_arc,
      recurring_npcs: playerState.npcs.filter(npc => npc.seasons_known > 1)
    } : null
  };
}
```

---

## PHASE 2: STRUCTURAL PLANNING

### Chapter Outline Generation

```javascript
async function generateChapterOutline(seasonData) {
  const chapterCount = calculateChapterCount(seasonData.season_metadata.season_length);
  
  // 12w season = 8-10 chapters
  // 24w season = 12-14 chapters
  // 36w season = 15-18 chapters
  
  const outline = {
    novel_title: seasonData.season_metadata.season_title,
    total_chapters: chapterCount,
    target_words: calculateTargetWords(seasonData.season_metadata.season_length),
    
    chapters: []
  };
  
  // CHAPTER 1: OPENING (Always)
  outline.chapters.push({
    number: 1,
    title: "The Beginning",
    arc_section: "Act I - Setup",
    weeks_covered: [1, 2],
    
    content_focus: [
      "Season aspiration stated",
      "Starting state (meters, relationships, resources)",
      "Initial motivation/desire",
      "First steps taken"
    ],
    
    target_words: outline.target_words / chapterCount,
    
    key_beats: [
      seasonData.narrative_arc.major_beats.find(b => b.type === "setup")
    ]
  });
  
  // CHAPTER 2-3: RISING ACTION (Act I)
  for (let i = 2; i <= 3; i++) {
    outline.chapters.push({
      number: i,
      title: await generateChapterTitle(i, seasonData),
      arc_section: "Act I - Rising Action",
      weeks_covered: calculateWeeks(i, seasonData.season_length),
      
      content_focus: [
        "Early progress on aspiration",
        "Relationships forming/deepening",
        "Skills developing",
        "Obstacles emerging"
      ],
      
      key_beats: filterBeatsByWeeks(seasonData.narrative_arc.major_beats, weeks)
    });
  }
  
  // CHAPTER 4: ACT I CLIMAX
  outline.chapters.push({
    number: 4,
    title: "The First Challenge",
    arc_section: "Act I - Climax",
    weeks_covered: [4],
    
    content_focus: [
      "First major challenge faced",
      "Decisive Decision #1 (if present)",
      "Success or setback",
      "Transition to Act II"
    ],
    
    key_beats: [
      seasonData.narrative_arc.major_beats.find(b => b.type === "act_1_climax")
    ]
  });
  
  // CHAPTERS 5-N: ACT II (Bulk of story)
  // ... [Detailed middle chapters] ...
  
  // CHAPTER N-2: CRISIS
  outline.chapters.push({
    title: "When Everything Falls Apart",
    arc_section: "Act II - Crisis",
    
    content_focus: [
      "Lowest point",
      "Multiple pressures converge",
      "Support system tested",
      "Decision point"
    ]
  });
  
  // CHAPTER N-1: CLIMAX
  outline.chapters.push({
    title: "The Choice / The Moment",
    arc_section: "Act III - Climax",
    
    content_focus: [
      "Decisive Decision #2 (final)",
      "Aspiration resolved",
      "Character transformation evident",
      "Relationships tested/deepened"
    ]
  });
  
  // CHAPTER N: RESOLUTION
  outline.chapters.push({
    title: "What Changed",
    arc_section: "Act III - Resolution",
    
    content_focus: [
      "Process outcomes",
      "Reflect on growth",
      "Relationship resolutions",
      "Set up next season (if applicable)"
    ]
  });
  
  return outline;
}
```

---

## PHASE 3: CONTENT GENERATION

### Chapter Generation Process

```javascript
async function generateChapter(chapterOutline, seasonData, previousChapters) {
  const prompt = constructChapterPrompt(chapterOutline, seasonData, previousChapters);
  
  // On-device TensorFlow Lite inference
  const chapterText = await ai.generate({
    prompt: prompt,
    max_tokens: calculateTokensNeeded(chapterOutline.target_words),
    temperature: 0.7,
    
    constraints: {
      perspective: "2nd_person",              // "You do X"
      tense: "present",                       // "You walk to café"
      tone: seasonData.player_tone,           // Based on personality
      avoid_contradictions: seasonData.canonical_facts
    }
  });
  
  return {
    number: chapterOutline.number,
    title: chapterOutline.title,
    content: chapterText,
    word_count: countWords(chapterText),
    weeks_covered: chapterOutline.weeks_covered
  };
}

function constructChapterPrompt(outline, data, previous) {
  return `
    Generate Chapter ${outline.number}: "${outline.title}"
    
    CONTEXT:
    Season: ${data.season_metadata.season_number}
    Aspiration: ${data.season_metadata.aspiration}
    Weeks: ${outline.weeks_covered}
    Arc: ${outline.arc_section}
    
    PLAYER CHARACTER:
    Personality: ${data.character_arc.personality_end}
    Life Direction: ${data.season_metadata.life_direction}
    Emotional State (this period): ${getEmotionalStateForWeeks(outline.weeks_covered)}
    
    KEY EVENTS THIS CHAPTER:
    ${outline.key_beats.map(b => `- ${b.description}`).join('\n')}
    
    RELATIONSHIPS:
    ${data.relationships.relationship_arcs.map(r => 
      `- ${r.npc_id}: Level ${r.level_end}, Trust ${r.trust_end}`
    ).join('\n')}
    
    MAJOR MOMENTS TO INCLUDE:
    ${filterMomentsByWeeks(data.memories.top_20_moments, outline.weeks_covered)}
    
    PREVIOUS CHAPTER SUMMARY (for continuity):
    ${previous.length > 0 ? summarize(previous[previous.length - 1]) : "N/A - First chapter"}
    
    REQUIREMENTS:
    - Write in 2nd person present tense ("You walk", not "I walked")
    - Target ${outline.target_words} words
    - Include specific sensory details
    - Show character growth/change
    - Reference relationship development
    - Balance narration and inner monologue
    - Novel-quality prose (not game mechanics)
    - ${outline.content_focus.join(', ')}
    
    TONE: ${determineTone(data.player_tone)}
    
    Generate chapter:
  `;
}
```

---

### Example Generated Chapter Opening

```
CHAPTER 1: THE BEGINNING

You stare at your reflection in the bathroom mirror. Twenty-eight. This is the year 
you stop waiting for your life to start.

The photography business. You've been talking about it for two years. Tonight, at 
2 AM, unable to sleep, you finally Googled "how to start photography business." 
Wrote down steps on a Post-it. Stuck it to your laptop.

This is happening.

Your alarm goes off—6:30 AM. Corporate job. Spreadsheets. Conference calls. The 
thing that pays rent but drains your soul. You shower, dress, grab coffee. But 
today feels different. You have a secret now. A plan.

On the bus, you scroll through your old photos. Some of them are... actually good? 
That sunset over the river. The street musician series. Your friend's wedding 
candids—everyone said those were better than the professional shots.

Maybe you can do this.

Café Luna at lunch. Your usual spot. That's when you see her—the woman from the 
bookshop next door. Sarah something. She's at the window seat, writing in a 
notebook, chai latte steaming beside her. You've seen her here before. Tuesdays 
at 3 PM. Creature of habit, like you.

She looks up. Makes eye contact. Small nod of recognition.

You nod back.

That's it. That's the whole interaction. But it feels like something. The beginning 
of something.

You don't know yet that Sarah will become one of the most important people in your 
life. That this café will hold years of your story. That three years from now, 
you'll be opening a bookshop together.

All you know right now is: This is week one. You're starting a photography business. 
And you're terrified.

Good. Terrified means it matters.
```

---

## PHASE 4: CONTINUITY INTEGRATION

### Past Season References

```javascript
async function integratePastSeasons(chapters, seasonNumber, pastContext) {
  if (seasonNumber === 1) return chapters;  // No past to reference
  
  // Add callbacks to past seasons throughout narrative
  const enrichedChapters = chapters.map(chapter => {
    const callbacks = generateSeasonCallbacks(
      chapter,
      pastContext,
      seasonNumber
    );
    
    return {
      ...chapter,
      content: insertCallbacks(chapter.content, callbacks)
    };
  });
  
  return enrichedChapters;
}

function generateSeasonCallbacks(chapter, pastContext, currentSeason) {
  // Example: Current season's crisis mirrors past season's crisis
  if (chapter.arc_section === "Act II - Crisis") {
    const pastCrisis = pastContext.crisis_moments.find(c => c.similar_to_current);
    
    if (pastCrisis) {
      return [{
        type: "parallel",
        text: `This feels familiar. Different situation, same feeling. Season ${pastCrisis.season}, 
               when ${pastCrisis.description}. You survived that. You'll survive this.`,
        insert_at: "crisis_peak"
      }];
    }
  }
  
  // Example: Recurring NPC reference
  if (chapter.major_npc === "Sarah" && pastContext.sarah_history) {
    return [{
      type: "relationship_depth",
      text: `Sarah. ${currentSeason - pastContext.sarah_first_met_season} years since that 
             first awkward hello at Café Luna. Look at you now.`,
      insert_at: "meaningful_moment"
    }];
  }
  
  return [];
}
```

---

## PHASE 5: QUALITY & FORMATTING

### Novel Validation & Polish

```javascript
async function validateAndFormat(chapters, seasonData) {
  // VALIDATION
  const validation = {
    word_count_check: validateWordCount(chapters),
    continuity_check: validateContinuity(chapters, seasonData.canonical_facts),
    character_consistency: validateCharacterVoice(chapters, seasonData.personality),
    relationship_accuracy: validateRelationships(chapters, seasonData.relationships),
    timeline_coherence: validateTimeline(chapters, seasonData.weeks_played)
  };
  
  if (!validation.all_pass) {
    // Regenerate problematic chapters
    const fixed = await fixValidationIssues(validation, chapters);
    chapters = fixed;
  }
  
  // FORMATTING
  const novel = {
    metadata: {
      title: seasonData.season_title,
      season_number: seasonData.season_number,
      character_name: seasonData.player_name,
      generated_date: new Date(),
      word_count: calculateTotalWords(chapters),
      chapter_count: chapters.length
    },
    
    dedication: generateDedication(seasonData),
    
    table_of_contents: chapters.map(c => ({
      chapter_number: c.number,
      title: c.title,
      page: calculatePageNumber(c, chapters)
    })),
    
    chapters: chapters,
    
    epilogue: generateEpilogue(seasonData),
    
    statistics: {
      weeks_lived: seasonData.weeks_played,
      relationships_formed: seasonData.relationships.npcs_met.length,
      skills_gained: Object.keys(seasonData.character_arc.skills_gained),
      aspiration_result: seasonData.aspiration_result
    }
  };
  
  return novel;
}
```

---

## Master Truths v1.2: Novel-Quality Validation *(NEW)*

### Comprehensive Quality Scoring System

**Purpose:** Ensure generated novels meet Master Truths v1.2 thresholds for emotional authenticity, tension, and dramatic irony.

```javascript
const NOVEL_QUALITY_VALIDATION = {
  required_thresholds: {
    overall_quality: 0.7,           // Master Truths v1.2 Section 17
    emotional_authenticity: 0.7,    // Section 16
    tension_maintenance: 0.6,       // Section 17
    dramatic_irony: 0.6,            // Section 17 (when applicable)
    hook_effectiveness: 0.6         // Section 17
  },
  
  validation_pipeline: {
    phase_1: "Emotional Authenticity Scoring",
    phase_2: "Tension Curve Verification",
    phase_3: "Dramatic Irony Detection",
    phase_4: "Hook Point Effectiveness",
    phase_5: "Overall Quality Calculation",
    phase_6: "Regeneration if Below Threshold"
  }
};
```

---

### Phase 1: Emotional Authenticity Scoring

```javascript
async function scoreEmotionalAuthenticity(novel, seasonData) {
  const scores = {
    capacity_respect: scoreCapacityRespect(novel, seasonData),
    circumstance_awareness: scoreCircumstanceAwareness(novel, seasonData),
    personality_consistency: scorePersonalityConsistency(novel, seasonData),
    emotional_arc_realism: scoreEmotionalArcRealism(novel, seasonData),
    npc_observation: scoreNPCObservation(novel, seasonData)
  };
  
  const overall_authenticity = Object.values(scores).reduce((a, b) => a + b, 0) / Object.keys(scores).length;
  
  return {
    overall_score: overall_authenticity,
    component_scores: scores,
    passes_threshold: overall_authenticity >= 0.7,
    
    details: {
      capacity_respect: {
        score: scores.capacity_respect,
        checks: [
          {
            criterion: "Capacity tracked across arc",
            passed: checkCapacityTracking(novel, seasonData),
            evidence: extractCapacityReferences(novel)
          },
          {
            criterion: "Low capacity moments shown authentically",
            passed: checkLowCapacityAuthenticity(novel, seasonData),
            evidence: extractLowCapacityMoments(novel)
          },
          {
            criterion: "Recovery time shown, not instant bounce-back",
            passed: checkRecoveryRealism(novel, seasonData),
            evidence: extractRecoveryNarrative(novel)
          }
        ]
      },
      
      circumstance_awareness: {
        score: scores.circumstance_awareness,
        checks: [
          {
            criterion: "Multiple stressors shown compounding",
            passed: checkStressorStacking(novel, seasonData),
            evidence: extractStressorStackingMoments(novel)
          },
          {
            criterion: "NPCs aware of player struggles",
            passed: checkNPCAwareness(novel, seasonData),
            evidence: extractNPCObservationDialogue(novel)
          },
          {
            criterion: "Environmental context affects mood",
            passed: checkEnvironmentalContext(novel, seasonData),
            evidence: extractSeasonalWeatherReferences(novel)
          }
        ]
      },
      
      personality_consistency: {
        score: scores.personality_consistency,
        checks: [
          {
            criterion: "OCEAN traits evident in choices",
            passed: checkOCEANConsistency(novel, seasonData),
            evidence: extractPersonalityMoments(novel)
          },
          {
            criterion: "Internal voice matches personality",
            passed: checkInternalVoiceConsistency(novel, seasonData),
            evidence: extractInternalMonologue(novel)
          },
          {
            criterion: "Reactions match trait levels",
            passed: checkReactionConsistency(novel, seasonData),
            evidence: extractReactionMoments(novel)
          }
        ]
      },
      
      emotional_arc_realism: {
        score: scores.emotional_arc_realism,
        checks: [
          {
            criterion: "Emotional journey follows capacity curve",
            passed: checkEmotionalJourneyRealism(novel, seasonData),
            evidence: extractEmotionalArcNarrative(novel)
          },
          {
            criterion: "Breaking point shown at appropriate capacity",
            passed: checkBreakingPointAuthenticity(novel, seasonData),
            evidence: extractCrisisMoments(novel)
          },
          {
            criterion: "Growth shown gradually, not suddenly",
            passed: checkGrowthPacing(novel, seasonData),
            evidence: extractGrowthNarrative(novel)
          }
        ]
      },
      
      npc_observation: {
        score: scores.npc_observation,
        checks: [
          {
            criterion: "Level 2+ NPCs notice physical state",
            passed: checkNPCPhysicalObservation(novel, seasonData),
            evidence: extractPhysicalObservationDialogue(novel)
          },
          {
            criterion: "Level 3+ NPCs notice emotional state",
            passed: checkNPCEmotionalObservation(novel, seasonData),
            evidence: extractEmotionalObservationDialogue(novel)
          },
          {
            criterion: "Level 4+ NPCs intervene when capacity critical",
            passed: checkNPCIntervention(novel, seasonData),
            evidence: extractInterventionMoments(novel)
          }
        ]
      }
    }
  };
}
```

---

### Phase 2: Tension Curve Verification

```javascript
async function verifyTensionMaintenance(novel, seasonData) {
  const tension_analysis = {
    act_1_tension: analyzeTensionInActRange(novel, seasonData.narrative_arc.act_1_weeks),
    act_2_tension: analyzeTensionInActRange(novel, seasonData.narrative_arc.act_2_weeks),
    act_3_tension: analyzeTensionInActRange(novel, seasonData.narrative_arc.act_3_weeks),
    
    hook_effectiveness: analyzeHookPoints(novel, seasonData.narrative_arc.hook_points),
    
    pacing: analyzePacing(novel)
  };
  
  const tension_score = calculateTensionScore(tension_analysis);
  
  return {
    overall_score: tension_score,
    passes_threshold: tension_score >= 0.6,
    
    details: {
      act_1_setup: {
        target_range: "0.3-0.5",
        actual_range: tension_analysis.act_1_tension.range,
        meets_target: tension_analysis.act_1_tension.meets_target,
        
        issues: tension_analysis.act_1_tension.issues || [],
        
        examples: extractTensionMoments(novel, seasonData.narrative_arc.act_1_weeks)
      },
      
      act_2_complications: {
        target_range: "0.5-0.8",
        actual_range: tension_analysis.act_2_tension.range,
        peaks_and_valleys: tension_analysis.act_2_tension.has_variation,
        breathing_room: tension_analysis.act_2_tension.has_breathing_room,
        
        issues: tension_analysis.act_2_tension.issues || [],
        
        examples: extractTensionMoments(novel, seasonData.narrative_arc.act_2_weeks)
      },
      
      act_3_climax: {
        target_pattern: "0.8 → 1.0 → 0.2",
        actual_pattern: tension_analysis.act_3_tension.pattern,
        climax_evident: tension_analysis.act_3_tension.has_climax,
        resolution_release: tension_analysis.act_3_tension.has_release,
        
        issues: tension_analysis.act_3_tension.issues || [],
        
        examples: extractTensionMoments(novel, seasonData.narrative_arc.act_3_weeks)
      },
      
      hook_points: {
        total_hooks: tension_analysis.hook_effectiveness.total,
        resolved_hooks: tension_analysis.hook_effectiveness.resolved,
        unresolved_at_end: tension_analysis.hook_effectiveness.unresolved,
        
        hook_quality: tension_analysis.hook_effectiveness.average_quality,
        
        issues: tension_analysis.hook_effectiveness.issues || []
      },
      
      pacing: {
        chapters_too_fast: tension_analysis.pacing.too_fast_count,
        chapters_too_slow: tension_analysis.pacing.too_slow_count,
        optimal_pacing: tension_analysis.pacing.optimal_count,
        
        overall_pacing_score: tension_analysis.pacing.score
      }
    }
  };
}
```

---

### Phase 3: Dramatic Irony Detection

```javascript
async function detectDramaticIrony(novel, seasonData) {
  // Only score if dramatic irony was present in gameplay
  const dramatic_irony_opportunities = seasonData.narrative_arc.dramatic_irony_moments || [];
  
  if (dramatic_irony_opportunities.length === 0) {
    return {
      applicable: false,
      score: null,
      reason: "No dramatic irony moments in season gameplay"
    };
  }
  
  const irony_analysis = dramatic_irony_opportunities.map(opportunity => {
    return {
      moment: opportunity.title,
      week: opportunity.week,
      
      player_knowledge: opportunity.player_knows,
      npc_knowledge: opportunity.npc_knows,
      knowledge_gap: opportunity.gap_description,
      
      captured_in_novel: checkIronyInNovel(novel, opportunity),
      irony_score: scoreIronyEffectiveness(novel, opportunity),
      
      evidence: extractIronyMoment(novel, opportunity.week)
    };
  });
  
  const overall_irony_score = irony_analysis
    .filter(a => a.captured_in_novel)
    .reduce((sum, a) => sum + a.irony_score, 0) / dramatic_irony_opportunities.length;
  
  return {
    applicable: true,
    overall_score: overall_irony_score,
    passes_threshold: overall_irony_score >= 0.6,
    
    details: {
      total_opportunities: dramatic_irony_opportunities.length,
      captured_count: irony_analysis.filter(a => a.captured_in_novel).length,
      missed_count: irony_analysis.filter(a => !a.captured_in_novel).length,
      
      moments: irony_analysis,
      
      issues: irony_analysis
        .filter(a => !a.captured_in_novel || a.irony_score < 0.6)
        .map(a => ({
          moment: a.moment,
          issue: !a.captured_in_novel ? "Not captured in novel" : "Weak irony execution",
          recommendation: generateIronyImprovement(a)
        }))
    }
  };
}

function checkIronyInNovel(novel, opportunity) {
  // Check if novel narrative includes:
  // 1. Player's limited knowledge shown
  // 2. Reader has hints/context player lacks
  // 3. Tension created by knowledge gap
  
  const narrative_text = novel.chapters
    .filter(c => c.weeks_covered.includes(opportunity.week))
    .map(c => c.content)
    .join('\n');
  
  const has_player_perspective = checkPlayerPerspective(narrative_text, opportunity);
  const has_reader_context = checkReaderContext(narrative_text, opportunity);
  const has_tension_from_gap = checkIronyTension(narrative_text, opportunity);
  
  return has_player_perspective && has_reader_context && has_tension_from_gap;
}
```

---

### Phase 4: Hook Point Effectiveness

```javascript
async function analyzeHookEffectiveness(novel, seasonData) {
  const hooks = seasonData.narrative_arc.hook_points || [];
  
  const hook_analysis = hooks.map(hook => {
    return {
      hook_title: hook.title,
      hook_type: hook.type,
      
      introduction: {
        week: hook.introduced_week,
        captured: checkHookIntroInNovel(novel, hook),
        quality: scoreHookIntroQuality(novel, hook)
      },
      
      development: {
        development_moments: hook.development_cards?.length || 0,
        captured_count: countDevelopmentInNovel(novel, hook),
        tension_maintained: checkTensionMaintained(novel, hook)
      },
      
      resolution: {
        week: hook.target_resolution_week,
        captured: checkHookResolutionInNovel(novel, hook),
        satisfying: scoreResolutionSatisfaction(novel, hook)
      },
      
      overall_effectiveness: calculateHookEffectiveness(novel, hook)
    };
  });
  
  const overall_hook_score = hook_analysis.reduce((sum, h) => sum + h.overall_effectiveness, 0) / hooks.length;
  
  return {
    overall_score: overall_hook_score,
    passes_threshold: overall_hook_score >= 0.6,
    
    details: {
      total_hooks: hooks.length,
      well_executed: hook_analysis.filter(h => h.overall_effectiveness >= 0.7).length,
      adequate: hook_analysis.filter(h => h.overall_effectiveness >= 0.5 && h.overall_effectiveness < 0.7).length,
      weak: hook_analysis.filter(h => h.overall_effectiveness < 0.5).length,
      
      hooks: hook_analysis,
      
      issues: hook_analysis
        .filter(h => h.overall_effectiveness < 0.6)
        .map(h => ({
          hook: h.hook_title,
          issue: identifyHookIssue(h),
          recommendation: generateHookImprovement(h)
        }))
    }
  };
}
```

---

### Phase 5: Overall Quality Calculation

```javascript
async function calculateOverallNovelQuality(novel, seasonData) {
  // Run all validation phases
  const authenticity = await scoreEmotionalAuthenticity(novel, seasonData);
  const tension = await verifyTensionMaintenance(novel, seasonData);
  const irony = await detectDramaticIrony(novel, seasonData);
  const hooks = await analyzeHookEffectiveness(novel, seasonData);
  
  // Calculate weighted overall score
  const weights = {
    authenticity: 0.35,
    tension: 0.30,
    hooks: 0.25,
    irony: 0.10  // Lower weight, only applicable sometimes
  };
  
  let overall_score = 
    (authenticity.overall_score * weights.authenticity) +
    (tension.overall_score * weights.tension) +
    (hooks.overall_score * weights.hooks);
  
  // Add irony if applicable
  if (irony.applicable) {
    overall_score += (irony.overall_score * weights.irony);
  } else {
    // Redistribute irony weight to other components
    const redistribute = weights.irony / 3;
    overall_score += 
      (authenticity.overall_score * redistribute) +
      (tension.overall_score * redistribute) +
      (hooks.overall_score * redistribute);
  }
  
  const passes = overall_score >= 0.7 &&
                 authenticity.passes_threshold &&
                 tension.passes_threshold &&
                 hooks.passes_threshold &&
                 (!irony.applicable || irony.passes_threshold);
  
  return {
    overall_quality_score: overall_score,
    passes_master_truths_v1_2: passes,
    
    component_scores: {
      emotional_authenticity: authenticity.overall_score,
      tension_maintenance: tension.overall_score,
      hook_effectiveness: hooks.overall_score,
      dramatic_irony: irony.applicable ? irony.overall_score : "N/A"
    },
    
    component_details: {
      authenticity,
      tension,
      irony,
      hooks
    },
    
    issues: [
      ...(!authenticity.passes_threshold ? ["Emotional authenticity below 0.7 threshold"] : []),
      ...(!tension.passes_threshold ? ["Tension maintenance below 0.6 threshold"] : []),
      ...(!hooks.passes_threshold ? ["Hook effectiveness below 0.6 threshold"] : []),
      ...(irony.applicable && !irony.passes_threshold ? ["Dramatic irony below 0.6 threshold"] : [])
    ],
    
    recommendations: generateImprovementRecommendations({
      authenticity,
      tension,
      irony,
      hooks
    })
  };
}
```

---

### Phase 6: Regeneration if Below Threshold

```javascript
async function validateAndRegenerateIfNeeded(novel, seasonData, maxAttempts = 3) {
  let attempt = 1;
  let current_novel = novel;
  let quality_report = await calculateOverallNovelQuality(current_novel, seasonData);
  
  while (!quality_report.passes_master_truths_v1_2 && attempt <= maxAttempts) {
    console.log(`Novel quality: ${quality_report.overall_quality_score.toFixed(2)} - Below 0.7 threshold`);
    console.log(`Issues: ${quality_report.issues.join(', ')}`);
    console.log(`Regenerating (Attempt ${attempt}/${maxAttempts})...`);
    
    // Identify weakest components
    const weak_chapters = identifyWeakChapters(quality_report);
    
    // Regenerate specific chapters with improved prompts
    current_novel = await regenerateChapters(
      current_novel,
      weak_chapters,
      seasonData,
      quality_report.recommendations
    );
    
    // Re-validate
    quality_report = await calculateOverallNovelQuality(current_novel, seasonData);
    attempt++;
  }
  
  if (!quality_report.passes_master_truths_v1_2) {
    console.warn(`Novel quality still below threshold after ${maxAttempts} attempts`);
    console.warn(`Final score: ${quality_report.overall_quality_score.toFixed(2)}`);
    console.warn(`Consider manual review or additional regeneration`);
  } else {
    console.log(`✅ Novel passes Master Truths v1.2 quality standards`);
    console.log(`Final score: ${quality_report.overall_quality_score.toFixed(2)}`);
  }
  
  return {
    novel: current_novel,
    quality_report,
    attempts_needed: attempt - 1,
    passed: quality_report.passes_master_truths_v1_2
  };
}
```

---

## PHASE 6: LIFE BOOKSHELF STORAGE

### Adding to Character's Collection

```javascript
async function addToUnwrittenshelf(novel, playerState) {
  const bookshelf = {
    character_id: playerState.character_id,
    character_name: playerState.character_name,
    total_seasons: playerState.seasons_completed,
    
    novels: [
      ...playerState.bookshelf.novels,
      {
        season: novel.metadata.season_number,
        title: novel.metadata.title,
        word_count: novel.metadata.word_count,
        generated: novel.metadata.generated_date,
        
        novel_file: await saveNovelFile(novel),
        
        cover_art: await generateCoverArt(novel.metadata),
        
        reading_time: calculateReadingTime(novel.metadata.word_count),
        
        highlight_moments: novel.chapters
          .flatMap(c => c.key_moments)
          .sort((a, b) => b.emotional_weight - a.emotional_weight)
          .slice(0, 10)
      }
    ],
    
    total_word_count: playerState.bookshelf.total_words + novel.metadata.word_count,
    
    life_trajectory: updateTrajectory(playerState.bookshelf.trajectory, novel)
  };
  
  await saveBookshelf(bookshelf);
  
  return bookshelf;
}
```

---

## Life Bookshelf UI

### Player View

```
┌──────────────────────────────────────────────────┐
│ LIFE BOOKSHELF - Alex Chen                       │
├──────────────────────────────────────────────────┤
│ 8 Seasons • 115,000 words • 5 years lived       │
└──────────────────────────────────────────────────┘

[SEASON 1] Finding My Footing
12 weeks • 12,500 words • Read: 50 min
★ "The week I met Sarah and Marcus"

[SEASON 2] The Photography Dream  
24 weeks • 16,800 words • Read: 67 min
★★★ "When I collapsed. When everything changed."

[SEASON 3] Rebuilding
24 weeks • 15,200 words • Read: 61 min
★ "Learning to slow down"

[SEASON 4-5] Corporate Life Unraveling
12w + 24w • 28,000 words combined • Read: 112 min
★★ "The burnout that broke me"

[SEASON 6] Starting Over
24 weeks • 14,500 words • Read: 58 min
★★★ "Quitting. Discovering design. Sarah's idea."

[SEASON 7] Building the Foundation
24 weeks • 13,900 words • Read: 56 min
★★ "Freelance success. Making it real."

[SEASON 8] The Bookshop Opening  ⬅ You Are Here
36 weeks (in progress) • Novel generates at season end
"Opening a bookshop with Sarah. The dream realized."

───────────────────────────────────────────────────
YOUR STORY SO FAR:
• Started: Corporate designer, unfulfilled
• Discovered: Photography passion
• Crisis: Health collapse, burnout
• Pivoted: Design freelance
• Now: Co-owner of bookshop with best friend Sarah
• Relationships: Sarah (Level 5), Marcus (Level 5)
• Skills Mastered: Design (7), Photography (8)
• Life Direction: Seek Deep Relationships
───────────────────────────────────────────────────

[EXPORT OPTIONS]
📄 Download All (PDF) - 115,000 words
📚 Order Physical Book - $45 + shipping
🌐 Publish to Unwritten Stories - Share your journey
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Novel Generation (v1.1 Foundation)
- [x] One novel per season (8-10 total per character)
- [x] Multi-season continuity (references past seasons)
- [x] On-device generation (TensorFlow Lite, 2-3 minutes)
- [x] Respects canonical facts (no contradictions)
- [x] Personality-influenced tone
- [x] 12k-18k words per novel (varies by season length)
- [x] 2nd person present tense ("You walk", not "I walked")
- [x] 8-15 chapters mapping to narrative arc

### ✅ Master Truths v1.2: Novel-Quality Validation *(NEW)*
- [x] **Overall Quality Threshold:** ≥ 0.7 (Master Truths v1.2 Section 17)
- [x] **Emotional Authenticity Scoring:** ≥ 0.7 threshold
  - Capacity respect tracked
  - Circumstance awareness shown
  - Personality consistency maintained
  - Emotional arc realism verified
  - NPC observation captured
- [x] **Tension Maintenance Verification:** ≥ 0.6 threshold
  - Act 1: 0.3-0.5 gentle rise
  - Act 2: 0.5-0.8 peaks and valleys
  - Act 3: 0.8 → 1.0 → 0.2 climax and release
  - Hook effectiveness scored
  - Pacing validated
- [x] **Dramatic Irony Detection:** ≥ 0.6 threshold (when applicable)
  - Player perspective shown
  - Reader context provided
  - Tension from knowledge gap
- [x] **Hook Point Effectiveness:** ≥ 0.6 threshold
  - Introduction quality
  - Development captured
  - Resolution satisfaction

### ✅ Master Truths v1.2: Validation Components

**Emotional Authenticity (5 Components):**
1. **Capacity Respect:** Tracks capacity across arc, shows low capacity authentically, depicts realistic recovery
2. **Circumstance Awareness:** Shows stressor stacking, NPCs aware of struggles, environmental context affects mood
3. **Personality Consistency:** OCEAN traits evident, internal voice matches personality, reactions consistent
4. **Emotional Arc Realism:** Journey follows capacity curve, breaking point at appropriate level, gradual growth
5. **NPC Observation:** Level 2+ notice physical state, Level 3+ notice emotional state, Level 4+ intervene

**Tension Maintenance (5 Components):**
1. **Act 1 Tension:** Gentle rise (0.3-0.5), establishes intrigue
2. **Act 2 Tension:** Rising action with breathing room (0.5-0.8), peaks and valleys
3. **Act 3 Tension:** Climax spike then release (0.8 → 1.0 → 0.2)
4. **Hook Points:** Total hooks, resolved hooks, unresolved at end, average quality
5. **Pacing:** Chapters neither too fast nor too slow

**Dramatic Irony (when applicable):**
- Total opportunities vs captured count
- Player knowledge shown, reader context provided
- Tension created by knowledge gap
- Irony effectiveness scored per moment

**Hook Effectiveness:**
- Introduction captured and quality scored
- Development moments tracked
- Resolution captured and satisfaction scored
- Overall effectiveness per hook

### ✅ Regeneration System
- [x] Validates novel quality automatically
- [x] Identifies weak chapters if below threshold
- [x] Regenerates specific chapters with improved prompts
- [x] Re-validates after regeneration
- [x] Max 3 attempts before warning
- [x] Logs quality score and issues

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~510 lines** of new v1.2 quality validation systems
2. **5-component emotional authenticity scoring** with detailed checks
3. **3-act tension curve verification** with target ranges
4. **Dramatic irony detection** for knowledge gap moments
5. **Hook point effectiveness analysis** across lifecycle
6. **Weighted overall quality calculation** (0.7 threshold)
7. **Automatic regeneration system** for below-threshold novels

**Quality Weights:**
- Emotional Authenticity: 35%
- Tension Maintenance: 30%
- Hook Effectiveness: 25%
- Dramatic Irony: 10% (when applicable, redistributed if not)

**Design Principles:**
- Novels must pass v1.2 standards before storage
- Emotional authenticity is highest weighted component
- Capacity respect and circumstance awareness central to quality
- Tension curves validated against 3-act structure
- Regeneration automatic if quality below threshold
- Maximum 3 regeneration attempts before manual review

**References:**
- See `01-emotional-authenticity.md` for cross-system integration
- See `31-narrative-arc-scaffolding.md` for story structure and emotional journey mapping
- See `33-dialogue-generation-templates.md` for NPC observation systems
- See `35-tension-maintenance-system.md` for hook point and tension curve specifications
- See `74-multi-season-continuity-spec.md` for memory/context system
- See `73-season-flow-implementation.md` for season completion triggers

---

**This specification enables AI engineers to implement the complete novel generation pipeline with Master Truths v1.2 quality validation, transforming gameplay data into emotionally authentic, tension-balanced, 12k-18k word narrative novels that pass strict quality thresholds before storage in the Life Bookshelf.**

