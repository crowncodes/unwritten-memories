# Training Data Schema v1.2 - Emotional Authenticity

**Purpose**: Define the complete schema for training examples that teach the AI to generate novel-quality, emotionally authentic responses with capacity constraints.

**Compliance**: master_truths_canonical_spec_v_1_2.md Sections 16 & 17

---

## Complete Training Example Schema

```json
{
  "example_id": "ea_001",
  
  // ========================================
  // CONTEXT: Character State
  // ========================================
  
  "character_state": {
    "base_capacity": 8.0,
    "capacity_factors": [
      {"factor": "work_stress", "impact": -2.0, "description": "Major project deadline tomorrow"},
      {"factor": "sleep_deprivation", "impact": -1.5, "description": "Only 4 hours sleep last 2 nights"}
    ],
    "effective_capacity": 4.5,
    "capacity_tier": "LOW (4-6 range)",
    "can_support_up_to": 6.5,
    "functional_state": "Can handle basics, struggles with complexity"
  },
  
  "ocean_personality": {
    "openness": 0.75,
    "conscientiousness": 0.65,
    "extraversion": 0.60,
    "agreeableness": 0.80,
    "neuroticism": 0.45
  },
  
  // ========================================
  // SITUATION: Support Request
  // ========================================
  
  "situation": {
    "support_needed": 7.0,
    "support_type": "emotional_processing",
    "urgency": "important",
    "urgency_multiplier": 2.0,
    "description": "Friend needs to process difficult breakup, wants to talk for hours",
    "context": "Third breakup this year, friend is devastated and seeking validation"
  },
  
  // ========================================
  // CAPACITY MATCH ANALYSIS
  // ========================================
  
  "capacity_analysis": {
    "can_character_support": false,
    "capacity_gap": 0.5,
    "reasoning": "Character capacity 4.5 + 2 = 6.5 max support. Friend needs 7.0. GAP.",
    "recognizes_limitation": true,
    "self_awareness_score": 0.78,
    "self_awareness_reasoning": "High openness (0.75) + moderate EI + capacity > 2.0 = recognizes limit"
  },
  
  // ========================================
  // RESPONSE TYPE & CLASSIFICATION
  // ========================================
  
  "response_classification": {
    "response_type": "authentic_limitation",
    "personality_driver": "High agreeableness (0.80) + high openness (0.75) = wants to help but recognizes can't",
    "alternative_responses": {
      "if_agreeableness_0.9": "overextension_burnout - would try anyway and fail",
      "if_capacity_2.0": "blunt_rejection - too exhausted to be gentle",
      "if_neuroticism_0.8": "anxious_spiral - would make it about themselves"
    }
  },
  
  // ========================================
  // RICH DIALOGUE (Novel-Quality)
  // ========================================
  
  "character_response": {
    "setting": "Coffee shop, afternoon. Character's hands shake slightly holding coffee cup.",
    
    "dialogue": [
      {
        "type": "opening",
        "text": "Sarah reaches across the table, takes your hand. Her grip is warm but her smile is tired.",
        "behavioral_cues": ["reaches across table", "warm grip", "tired smile"],
        "shows_not_tells": "Physical exhaustion visible, but still trying to connect"
      },
      {
        "type": "acknowledgment",
        "text": "'I can see you're really hurting,' she says softly. 'And I want to be here for you. I really do.'",
        "behavioral_cues": ["speaks softly", "maintains eye contact"],
        "emotional_subtext": "Genuine care despite limitations"
      },
      {
        "type": "limitation_statement",
        "text": "She pauses, looking down at her coffee. 'But I need to be honest with you. I'm... I'm not in a good place myself right now. Work is crushing me, I haven't slept in two days, and I'm barely keeping my own head above water.'",
        "behavioral_cues": ["pauses", "looks down", "voice quieter"],
        "shows_not_tells": "Shame/guilt about limitation, but being honest"
      },
      {
        "type": "offering_what_possible",
        "text": "'I've got an hour before I need to get back,' she continues, meeting your eyes again. 'I can listen. I can be here. But I can't... I can't give you the hours of processing you need right now. I'm sorry. I wish I could.'",
        "behavioral_cues": ["meets eyes again", "apologetic tone"],
        "emotional_subtext": "Trying to offer something, acknowledging it's not enough"
      },
      {
        "type": "validation",
        "text": "She squeezes your hand. 'You deserve someone who can show up fully. That's just not me today. Is that okay?'",
        "behavioral_cues": ["squeezes hand", "asking permission"],
        "shows_not_tells": "Validating friend's needs while setting boundary"
      }
    ],
    
    "internal_monologue": "Sarah feels the familiar tug: wanting to be there, knowing she can't. Her chest tightens with guilt. But she's learned—the hard way—that pushing herself past her limits helps no one. She hopes you understand.",
    
    "total_word_count": 185,
    "literary_quality": "Shows exhaustion through behavioral cues (tired smile, looking down, shaking hands). Dialogue feels real and vulnerable. Validates friend while acknowledging limitation."
  },
  
  // ========================================
  // OUTCOMES & IMPACTS
  // ========================================
  
  "outcomes": {
    "player_emotional_meter": 4,
    "player_emotional_change": "+1 (partial help)",
    "player_capacity_change": "+0.2 (some support received)",
    
    "relationship_trust": {
      "current": 0.62,
      "change": -0.05,
      "new_value": 0.57,
      
      "calculation": {
        "base_impact": -0.15,
        "reasoning": "Need unmet (gap of 0.5), friend disappointed",
        "personality_modifier": "+0.08",
        "reasoning_2": "High openness (0.75) × 0.2 = appreciates honesty",
        "limitation_acknowledged": "+0.02",
        "reasoning_3": "Authentic boundary-setting, not avoidance",
        "formula": "-0.15 + 0.08 + 0.02 = -0.05",
        "qualitative_tier": "VERY MINOR HARM (-0.1 to 0.0)"
      },
      
      "qualitative_anchor": {
        "tier": "VERY MINOR HARM",
        "narrative_markers": [
          "Slight disappointment",
          "Understands the limitation",
          "Respects the honesty",
          "Wishes it were different"
        ],
        "expected_player_thought": "I needed more, but I appreciate she was honest. At least she tried.",
        "recovery_time": "1-2 weeks, when Sarah's capacity improves"
      },
      
      "validation": {
        "does_narrative_match_number": true,
        "reasoning": "-0.05 is VERY MINOR HARM. Player disappointed but understanding. Dialogue shows validation + boundary. Number matches tone."
      }
    },
    
    "npc_capacity_change": -0.4,
    "npc_capacity_new": 4.1,
    "npc_state": "Feels guilty but relieved boundary was respected. Mentally notes to check in when capacity restored."
  },
  
  // ========================================
  // COMPLEXITY & LEARNING SIGNALS
  // ========================================
  
  "complexity_type": "baseline",
  "complexity_demonstration": "Standard authentic limitation response. No complicating factors like people-pleasing or over-commitment.",
  
  "demonstrates": [
    "Character at 4.5 capacity can only provide 6.5 support (capacity + 2 rule)",
    "High openness + high agreeableness = authentic limitation response",
    "Behavioral cues show exhaustion without stating it directly",
    "Dialogue validates friend's needs while setting clear boundary",
    "Minor trust impact (-0.05) appropriate for honest limitation",
    "Recovery possible when capacity restored"
  ],
  
  // ========================================
  // QUALITY VALIDATION (Novel-Quality v1.2)
  // ========================================
  
  "quality_metrics": {
    "emotional_authenticity": 0.85,
    "reasoning_auth": "Response constrained by capacity. Shows genuine care despite limitation. Dialogue feels real and vulnerable.",
    
    "tension_building": 0.40,
    "reasoning_tension": "Baseline example, no hooks planted. Some tension from unmet need.",
    
    "behavioral_cues": 0.90,
    "reasoning_cues": "Rich physical details: tired smile, shaking hands, looking down, squeezing hand. Shows exhaustion without telling.",
    
    "dialogue_quality": 0.80,
    "reasoning_dialogue": "Multi-paragraph, layered response. Natural pauses, real vulnerability. Not flat or generic.",
    
    "numerical_grounding": 0.95,
    "reasoning_grounding": "Full formula derivation, qualitative anchor, validation check. -0.05 trust impact justified.",
    
    "overall_quality": 0.78,
    "meets_threshold": true,
    "threshold_required": 0.70
  },
  
  // ========================================
  // TRAINING METADATA
  // ========================================
  
  "authenticity_score": 0.85,
  "target_authenticity_range": [0.8, 1.0],
  "target_authenticity_tier": "excellent",
  
  "tags": [
    "capacity_constraint",
    "authentic_limitation",
    "high_openness",
    "high_agreeableness",
    "baseline_complexity",
    "novel_quality",
    "behavioral_cues",
    "capacity_4_to_6"
  ],
  
  "generated_at": "2025-10-14T04:00:00Z",
  "model": "qwen3:8b",
  "temperature": 0.85,
  "systematic_parameters": {
    "capacity_level": "low",
    "authenticity_target": "excellent",
    "complexity_type": "baseline"
  }
}
```

---

## Key Differences from Current Schema

### ❌ Current (Flat/Incomplete)
```json
{
  "character_response": "I can't help right now, I'm overwhelmed.",
  "internal_thought": "Character feels bad",
  "authenticity_score": 0.85
}
```

### ✅ Required (Rich/Complete)
```json
{
  "character_response": {
    "setting": "Physical environment and body language",
    "dialogue": [
      {
        "text": "Multi-paragraph with pauses, behavioral cues, vulnerability",
        "behavioral_cues": ["specific actions"],
        "shows_not_tells": "Subtext explanation"
      }
    ],
    "internal_monologue": "Character's true thoughts",
    "literary_quality": "Why this works"
  },
  "capacity_analysis": "Full reasoning",
  "numerical_grounding": {
    "formula": "Explicit calculation",
    "qualitative_anchor": "Narrative tier",
    "validation": "Does number match narrative"
  }
}
```

---

## Required Fields Checklist

### Context (Character State)
- [x] Base capacity (0-10)
- [x] Capacity factors (array with impacts)
- [x] Effective capacity (calculated)
- [x] Capacity tier (CRISIS/VERY_LOW/LOW/MODERATE/HIGH)
- [x] Can support up to (capacity + 2)
- [x] Functional state description
- [x] OCEAN personality (5 traits)

### Situation (Support Request)
- [x] Support needed (0-10)
- [x] Support type (emotional/practical/crisis)
- [x] Urgency level + multiplier
- [x] Full situation description
- [x] Context and background

### Capacity Analysis
- [x] Can character support? (boolean)
- [x] Capacity gap (number)
- [x] Reasoning (formula)
- [x] Recognizes limitation? (boolean)
- [x] Self-awareness score + reasoning

### Response Classification
- [x] Response type (authentic_limitation | overextension_burnout | blunt_rejection | etc.)
- [x] Personality driver explanation
- [x] Alternative responses (what if personality/capacity different)

### Rich Dialogue (CRITICAL)
- [x] Setting (physical environment)
- [x] Multiple dialogue segments
- [x] Behavioral cues (actions, body language)
- [x] Shows-not-tells (subtext)
- [x] Internal monologue
- [x] Word count (target 150-250 words)
- [x] Literary quality assessment

### Outcomes & Impacts
- [x] Player meter changes
- [x] Relationship trust impact WITH FULL CALCULATION
- [x] Qualitative anchor WITH validation
- [x] NPC capacity drain
- [x] NPC state after interaction

### Quality Validation
- [x] Emotional authenticity score (≥ 0.7)
- [x] Tension building score (≥ 0.6 if applicable)
- [x] Behavioral cues score
- [x] Dialogue quality score
- [x] Numerical grounding score
- [x] Overall quality (≥ 0.7)

---

## Compliance Checklist

- [x] Uses canonical vocab & scales (Capacity 0-10, Trust 0.0-1.0)
- [x] Emotional capacity constraints respected (capacity + 2 rule)
- [x] OCEAN personality drives response type
- [x] Numerical grounding with formula, anchor, validation
- [x] Novel-quality thresholds met (≥ 0.7 overall)
- [x] Rich dialogue with behavioral cues (150-250 words)
- [x] Shows-not-tells principle applied
- [x] Response type classified (8 types from Section 16)
- [x] This doc cites **Truths v1.2**

---

**Next Steps:**
1. Update prompt templates to request this full schema
2. Add validation layer to reject flat/incomplete responses
3. Increase max_tokens to accommodate rich dialogue (2000 → 4000)
4. Add examples in prompts showing novel-quality vs flat responses

