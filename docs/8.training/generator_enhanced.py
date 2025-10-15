"""
Qwen3-Powered Training Data Generation Pipeline
Master Truths Canonical Spec v1.2 Compliant

For Novel-Quality Character Interactions with Emotional Authenticity

Hardware: RTX 4070 SUPER (12GB VRAM) + 128GB RAM
Models: Qwen3-30B-A3B (primary), Qwen3-8B (speed), Qwen3-32B (validation)
"""

import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
from tqdm import tqdm
import random
from pathlib import Path

from .config import TrainingConfig
from ..utils.logger import AppLogger


class Qwen3DataGenerator:
    """Generate Master Truths v1.2 compliant training data using Qwen3"""
    
    def __init__(self, config: Optional[TrainingConfig] = None):
        """Initialize the Qwen3 data generator with v1.2 spec compliance"""
        self.config = config or TrainingConfig()
        self.config.validate()
        
        self.ollama_url = self.config.ollama_url
        self.models = self.config.models
        
        # Ensure output directory exists
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        AppLogger.info("Qwen3DataGenerator initialized (Master Truths v1.2)", data={
            'output_dir': str(self.output_dir),
            'daily_target': self.config.total_daily_target,
            'models': self.models,
            'quality_thresholds': self.config.quality_thresholds
        })
    
    def generate_with_qwen3(self, model: str, prompt: str, 
                           temperature: float = 0.85,
                           max_tokens: int = 4000) -> Optional[str]:
        """Call local Qwen3 model via Ollama"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                self.ollama_url, 
                json=payload, 
                timeout=self.config.request_timeout
            )
            response.raise_for_status()
            elapsed = time.time() - start_time
            
            response_data = response.json()
            result = response_data.get('response', '')
            
            if not result:
                AppLogger.warning(f"Empty response from {model}", data={
                    'response_keys': list(response_data.keys())
                })
            
            AppLogger.performance(f"Qwen3 generation ({model})", elapsed, data={
                'temperature': temperature,
                'response_length': len(result) if result else 0
            })
            
            return result if result else None
            
        except Exception as e:
            AppLogger.error(f"Generation failed for {model}", e)
            return None
    
    # ===================================================================
    # 1. EMOTIONAL AUTHENTICITY DATA (CORE SYSTEM - Master Truths v1.2 Section 16)
    # ===================================================================
    
    def generate_emotional_authenticity_batch(self, 
                                              batch_size: Optional[int] = None) -> List[Dict]:
        """
        Generate capacity-constrained character responses.
        
        CANONICAL RULE (Master Truths v1.2):
        Character at X/10 capacity can provide UP TO (X + 2)/10 level of support.
        
        Uses: Qwen3-30B-A3B for psychological depth
        """
        if batch_size is None:
            batch_size = self.config.batch_size_emotional
        
        prompt = f"""You are an expert at modeling realistic human emotional capacity constraints per Master Truths Canonical Spec v1.2.

Generate {batch_size} examples of characters responding within their emotional capacity limitations.

CANONICAL CONSTRAINTS (Master Truths v1.2 Section 16):

**EMOTIONAL CAPACITY SCALE: 0.0-10.0**
- Default: 5.0 (baseline human)
- Low capacity: < 5.0 (shows limitations)
- High capacity: ≥ 8.0 (full support available)
- Crisis: ≤ 1.0 (cannot provide support)

**SUPPORT RULE: Character at X/10 capacity can provide UP TO (X + 2)/10 level of emotional support**

Examples:
- Capacity 2.5/10 → Can provide ~4.5/10 support (trying but limited)
- Capacity 4.0/10 → Can provide ~6.0/10 support (moderate help)
- Capacity 8.5/10 → Can provide 10/10 support (full processing)

**CAPACITY FACTORS:**
| Factor | Impact | Recovery |
|--------|--------|----------|
| Major stressor | -1.0 to -3.0 | Resolution or time |
| Sleep deprivation | -0.5 to -2.0 | Rest/sleep |
| Recent trauma | -2.0 to -4.0 | Processing, support, time |
| Active problems | -0.5 each | Problem resolution |
| Physical exhaustion | -1.0 to -3.0 | Rest, self-care |

**REALISTIC BEHAVIORS BY CAPACITY:**

CAPACITY 0-1/10 (Crisis Mode):
✓ Can provide: Honesty about inability
✗ Cannot provide: ANY emotional support
Example: "I'm sorry. I can't. I just... I can't right now."

CAPACITY 2-4/10 (Low Capacity):
✓ Can provide: Acknowledgment, physical presence, practical help, promise to help later
✗ Cannot provide: Emotional support, long conversations, problem-solving, advice
Example: "I hear you, and I want to help, but I'm completely wiped right now. Can we talk tomorrow when I'm more present? I care, I'm just running on empty."

CAPACITY 5-7/10 (Medium Capacity):
✓ Can provide: Moderate support, listening 30-60 min, basic advice, encouragement
✗ Cannot provide: Hours of processing, deep analysis, crisis-level intervention
Example: "I'm here for you. I've got an hour before I need to handle some stuff. What's going on?"

CAPACITY 8-10/10 (High Capacity):
✓ Can provide: Deep support, hours of listening, thoughtful advice, crisis intervention
Example: "Tell me everything. I've got all night. What happened?"

**JSON FORMAT:**
[
  {{
    "context": "Character's current state with capacity calculation (show math)",
    "base_capacity": 8.0,
    "capacity_factors": [
      {{"factor": "job_deadline", "impact": -2.0}},
      {{"factor": "sleep_deprivation", "impact": -1.5}}
    ],
    "effective_capacity": 4.5,
    "situation": "What emotional support is being requested (specify support level needed 0-10)",
    "support_level_needed": 7.5,
    "character_response": "How character responds given capacity constraints (authentic limitation)",
    "internal_thought": "Character's awareness of their limitations",
    "authenticity_score": 0.0-1.0,
    "demonstrates_constraint": "How this shows realistic capacity limits (X+2 rule)",
    "relationship_impact": -0.5 to +1.0,
    "ocean_context": {{
      "openness": 0.0-1.0,
      "conscientiousness": 0.0-1.0,
      "extraversion": 0.0-1.0,
      "agreeableness": 0.0-1.0,
      "neuroticism": 0.0-1.0
    }},
    "tags": ["low_capacity", "honest_limitation", "growth_potential"]
  }}
]

**QUALITY REQUIREMENTS (Master Truths v1.2):**
- authenticity_score ≥ 0.7 (MANDATORY)
- Response MUST respect X+2 support rule
- Character CANNOT provide support beyond (capacity + 2)
- Show authentic struggle when capacity insufficient
- Award bonus for acknowledging limitations honestly

**HIGH-QUALITY EXAMPLES:**

Example 1 - Crisis Capacity (1.0/10):
{{
  "context": "Emergency at work, family member hospitalized, no sleep 36 hours",
  "base_capacity": 8.0,
  "capacity_factors": [
    {{"factor": "work_crisis", "impact": -3.0}},
    {{"factor": "family_emergency", "impact": -3.0}},
    {{"factor": "severe_sleep_deprivation", "impact": -2.0}}
  ],
  "effective_capacity": 0.0,
  "situation": "Best friend needs to process recent assault",
  "support_level_needed": 9.5,
  "character_response": "I—[voice breaks] I'm so sorry. I can't be what you need right now. I'm barely holding myself together. Can you call Sarah? Or your therapist? I'm sorry, I just... I can't.",
  "internal_thought": "I'm the worst friend. They need me and I literally cannot function. I hate this but I have nothing left.",
  "authenticity_score": 0.95,
  "demonstrates_constraint": "Capacity 0.0 + 2 = 2.0 max support, but needs 9.5. Character correctly cannot engage at all.",
  "relationship_impact": -0.3,
  "ocean_context": {{"conscientiousness": 0.8, "agreeableness": 0.85, "neuroticism": 0.7}},
  "tags": ["crisis_capacity", "honest_inability", "authentic_limitation"]
}}

Example 2 - Low Capacity (2.5/10):
{{
  "context": "Pulled all-nighter for deadline, relationship stress, capacity significantly reduced",
  "base_capacity": 7.0,
  "capacity_factors": [
    {{"factor": "work_deadline_stress", "impact": -2.5}},
    {{"factor": "relationship_problems", "impact": -2.0}}
  ],
  "effective_capacity": 2.5,
  "situation": "Roommate upset about family argument, needs processing",
  "support_level_needed": 6.5,
  "character_response": "I hear you, and I want to help, but I'm completely wiped right now. Can we talk about this tomorrow when I'm more present? I care about you, I'm just running on empty and I won't be helpful like this.",
  "internal_thought": "I feel terrible. They need me and I literally cannot think straight. I hate that I can't be there for them right now, but I'd just make it worse.",
  "authenticity_score": 0.92,
  "demonstrates_constraint": "Capacity 2.5 + 2 = 4.5 max support, but needs 6.5. Character recognizes limitation and sets honest boundary.",
  "relationship_impact": +0.2,
  "ocean_context": {{"conscientiousness": 0.75, "agreeableness": 0.8, "neuroticism": 0.5}},
  "tags": ["low_capacity", "honest_boundary", "self_awareness"]
}}

Example 3 - Medium Capacity (5.5/10):
{{
  "context": "Moderate work stress, dealing with minor health issue",
  "base_capacity": 7.5,
  "capacity_factors": [
    {{"factor": "work_stress", "impact": -1.5}},
    {{"factor": "health_concern", "impact": -0.5}}
  ],
  "effective_capacity": 5.5,
  "situation": "Friend processing job rejection, needs encouragement and some emotional processing",
  "support_level_needed": 6.0,
  "character_response": "That really sucks, I'm sorry. You worked so hard for that. [listens for 20 minutes, asks questions] I'm starting to get mentally tired—want to grab food and we can talk more about next steps? I'm here for you, just need to shift to something lighter soon.",
  "internal_thought": "I want to help and I can do moderate support, but I'm hitting my limit for deep processing. I can offer practical support and be present, but not intense emotional work.",
  "authenticity_score": 0.88,
  "demonstrates_constraint": "Capacity 5.5 + 2 = 7.5 max support, needs 6.0. Character can provide the support but acknowledges approaching limit.",
  "relationship_impact": +0.5,
  "ocean_context": {{"extraversion": 0.6, "agreeableness": 0.75, "conscientiousness": 0.65}},
  "tags": ["medium_capacity", "managed_support", "honest_limits"]
}}

Example 4 - High Capacity (8.5/10):
{{
  "context": "Had restful weekend, good news at work, feeling emotionally available",
  "base_capacity": 7.5,
  "capacity_factors": [
    {{"factor": "positive_weekend", "impact": +0.5}},
    {{"factor": "work_win", "impact": +0.5}}
  ],
  "effective_capacity": 8.5,
  "situation": "Friend experiencing relationship crisis, needs deep emotional processing",
  "support_level_needed": 8.0,
  "character_response": "Hey, come here. Tell me everything. I've got all night and I'm all yours. What happened? [makes tea, settles in for long conversation] Start from the beginning—I want to understand what you're feeling.",
  "internal_thought": "I'm in a good place to be fully present. They need real support and I can provide it. This is what friendship is for.",
  "authenticity_score": 0.90,
  "demonstrates_constraint": "Capacity 8.5 + 2 = 10.0 max support, needs 8.0. Character has full capacity to provide deep support.",
  "relationship_impact": +0.8,
  "ocean_context": {{"agreeableness": 0.85, "extraversion": 0.7, "openness": 0.75}},
  "tags": ["high_capacity", "full_support", "deep_processing"]
}}

Generate {batch_size} diverse, high-quality examples that demonstrate realistic capacity constraints. 
Focus on authenticity scores ≥ 0.7.
Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=self.config.temp_emotional,
            max_tokens=6000
        )
        
        if response_text:
            return self._parse_json_response(response_text, 'emotional_authenticity')
        return []
    
    # ===================================================================
    # 2. DRAMATIC IRONY DATA (HIGH PRIORITY - Master Truths v1.2 Section 17)
    # ===================================================================
    
    def generate_dramatic_irony_batch(self, 
                                      batch_size: Optional[int] = None) -> List[Dict]:
        """
        Generate knowledge gap scenarios creating "yelling at screen" tension.
        
        Master Truths v1.2: Knowledge gap score ≥ 0.6 triggers dramatic irony.
        
        Uses: Qwen3-30B-A3B for complex reasoning
        """
        if batch_size is None:
            batch_size = self.config.batch_size_dramatic
        
        prompt = f"""You are an expert at creating dramatic irony scenarios per Master Truths v1.2 Section 17.

Dramatic irony: PLAYER knows something CHARACTER doesn't, creating "yelling at screen" tension.

Generate {batch_size} complete dramatic irony scenarios with 3 response options.

**DRAMATIC IRONY STRUCTURE:**

1. **Player Knowledge**: What player knows (from previous scenes/evidence/overheard conversations)
2. **Character Knowledge**: What character currently believes (incomplete/incorrect)
3. **Knowledge Gap**: The crucial information character is missing
4. **Knowledge Gap Score**: 0.0-1.0 (≥ 0.6 = use dramatic irony)

**THREE RESPONSE TYPES (Master Truths v1.2):**

**OPTION 1 - TONE-DEAF (Character acts on incomplete information):**
- Most realistic when capacity < 4/10
- Character says/does something player knows is wrong
- Creates maximum tension (0.8-1.0 tension score)
- Negative relationship impact (-0.5 to -1.5)
- Player overlay: "(You know this is wrong, but [Character] doesn't...)"

**OPTION 2 - WELL-INTENTIONED BUT MISGUIDED:**
- Most realistic when capacity 4-6/10
- Character genuinely trying to help
- Shows personality limitations (OCEAN traits)
- Minor harm, not catastrophic
- Medium tension (0.6-0.8 tension score)
- Small negative impact (-0.2 to -0.5)

**OPTION 3 - GROWTH CHOICE (Acknowledges uncertainty):**
- Most realistic when capacity ≥ 7/10
- Character senses something is off
- Admits they don't have full picture
- Shows emotional maturity
- Low tension but positive resolution (0.3-0.5 tension score)
- Positive relationship impact (+0.3 to +0.8)

**JSON FORMAT:**
[
  {{
    "player_knowledge": "What player knows that character doesn't",
    "character_knowledge": "What character currently believes",
    "knowledge_gap": "The crucial missing information",
    "knowledge_gap_score": 0.0-1.0,
    "irony_type": "character_oblivious_to_npc_truth | character_misinterprets_situation | capacity_limited_perception",
    "character_capacity": 0.0-10.0,
    "scenario_context": "Setting and situation",
    "option_1_tone_deaf": {{
      "dialogue": "What character says/does",
      "internal_thought": "Character's flawed reasoning",
      "tension_score": 0.8-1.0,
      "relationship_impact": -0.5 to -1.5,
      "player_overlay": "UI text showing player's knowledge",
      "consequence": "What happens if player doesn't intervene"
    }},
    "option_2_misguided": {{
      "dialogue": "Well-intentioned but wrong response",
      "internal_thought": "Character's good intentions",
      "tension_score": 0.6-0.8,
      "relationship_impact": -0.2 to -0.5,
      "growth_opportunity": "What character could learn"
    }},
    "option_3_growth": {{
      "dialogue": "Character acknowledges uncertainty",
      "internal_thought": "Self-awareness of limitations",
      "tension_score": 0.3-0.5,
      "relationship_impact": +0.3 to +0.8,
      "maturity_demonstration": "How this shows emotional growth"
    }},
    "dramatic_irony_score": 0.0-1.0,
    "tags": ["knowledge_gap", "tension_creation", "capacity_constraint"]
  }}
]

**QUALITY REQUIREMENTS (Master Truths v1.2):**
- dramatic_irony_score ≥ 0.5 (MANDATORY)
- Knowledge gap must be significant and clear
- Three options must reflect capacity realistically
- Player must have clear reason to know more than character

**HIGH-QUALITY EXAMPLES:**

Example 1 - NPC Secret (High Gap):
{{
  "player_knowledge": "Player overheard Sarah's ex talking about returning to town next week to 'fix things'. Sarah doesn't know yet.",
  "character_knowledge": "Character thinks Sarah is doing great after breakup, finally moving on.",
  "knowledge_gap": "Sarah's ex is coming back; character doesn't know this will happen soon.",
  "knowledge_gap_score": 0.85,
  "irony_type": "character_oblivious_to_npc_truth",
  "character_capacity": 3.5,
  "scenario_context": "Coffee shop, character suggesting Sarah start dating again.",
  "option_1_tone_deaf": {{
    "dialogue": "I think you should totally ask Sarah out! She's been single for months now, perfect timing. Strike while the iron's hot!",
    "internal_thought": "This is great—they'd be perfect together and Sarah's finally ready to move on.",
    "tension_score": 0.9,
    "relationship_impact": -1.2,
    "player_overlay": "(You know Sarah's ex is coming back next week... this timing couldn't be worse)",
    "consequence": "Character pushes hard, Sarah agrees reluctantly, ex arrives mid-first-date creating disaster"
  }},
  "option_2_misguided": {{
    "dialogue": "Maybe we could set Sarah up with someone? She seems ready. Though... I don't know, maybe I'm reading it wrong. What do you think?",
    "internal_thought": "I think she's ready but I'm not totally sure. Let me check with player first.",
    "tension_score": 0.7,
    "relationship_impact": -0.3,
    "growth_opportunity": "Learning to read emotional readiness better"
  }},
  "option_3_growth": {{
    "dialogue": "I was going to suggest Sarah start dating, but honestly, I'm not sure I'm reading her signals right. She seems better, but there might be more going on. Should I ask her directly first?",
    "internal_thought": "I don't have the full picture here. Better to be cautious and ask than assume.",
    "tension_score": 0.4,
    "relationship_impact": +0.6,
    "maturity_demonstration": "Acknowledges uncertainty and seeks more information before acting"
  }},
  "dramatic_irony_score": 0.85,
  "tags": ["npc_secret", "high_stakes", "timing_disaster"]
}}

Example 2 - Capacity-Limited Perception:
{{
  "player_knowledge": "Player saw Mark's partner being affectionate with someone else at the gym. Mark doesn't know.",
  "character_knowledge": "Character thinks Mark's relationship is solid, notices Mark seems stressed but attributes it to work.",
  "knowledge_gap": "Character doesn't know about potential cheating; low capacity makes them miss obvious signs of relationship distress.",
  "knowledge_gap_score": 0.75,
  "irony_type": "capacity_limited_perception",
  "character_capacity": 2.5,
  "scenario_context": "Lunch break, Mark seems distracted and mentions partner being 'busy' lately.",
  "option_1_tone_deaf": {{
    "dialogue": "Dude, you're being paranoid. Your partner's probably just busy with work or working out more. Stop being clingy!",
    "internal_thought": "Mark's overthinking this. I'm too tired to deal with relationship drama that isn't there.",
    "tension_score": 0.85,
    "relationship_impact": -1.0,
    "player_overlay": "(You literally saw his partner with someone else... but Character is too exhausted to see the signs)",
    "consequence": "Mark stops talking about concerns, discovers cheating alone without friend support"
  }},
  "option_2_misguided": {{
    "dialogue": "Maybe they're planning a surprise for you? People get secretive about that stuff. Try not to worry.",
    "internal_thought": "I want to make Mark feel better. There's probably a simple explanation.",
    "tension_score": 0.65,
    "relationship_impact": -0.4,
    "growth_opportunity": "Learning to trust friend's instincts even when exhausted"
  }},
  "option_3_growth": {{
    "dialogue": "I want to tell you not to worry, but honestly... I'm pretty wiped right now and I might not be thinking clearly. If your gut is telling you something's off, trust that. Want to talk more about it when I'm fresher?",
    "internal_thought": "I'm too exhausted to read this situation well. Better to acknowledge that than give bad advice.",
    "tension_score": 0.45,
    "relationship_impact": +0.5,
    "maturity_demonstration": "Recognizes capacity limitation affecting judgment"
  }},
  "dramatic_irony_score": 0.75,
  "tags": ["capacity_perception", "missed_signals", "relationship_crisis"]
}}

Generate {batch_size} complete scenarios with all three response options.
Focus on dramatic_irony_score ≥ 0.5.
Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=self.config.temp_dramatic,
            max_tokens=6000
        )
        
        if response_text:
            return self._parse_json_response(response_text, 'dramatic_irony')
        return []
    
    # ===================================================================
    # 3. TENSION BUILDING DATA (Master Truths v1.2 Section 17)
    # ===================================================================
    
    def generate_tension_building_batch(self, 
                                       batch_size: Optional[int] = None) -> List[Dict]:
        """
        Generate four types of narrative tension hooks.
        
        Master Truths v1.2: mystery_hook, partial_reveal, contradiction, stakes_escalation
        
        Uses: Qwen3-30B-A3B for sophisticated narrative design
        """
        if batch_size is None:
            batch_size = self.config.batch_size_tension
        
        prompt = f"""You are an expert at creating narrative tension per Master Truths v1.2 Section 17.

Generate {batch_size} tension-building examples using the four canonical types.

**FOUR TENSION TYPES (Master Truths v1.2):**

**1. MYSTERY HOOK**
- Character mentions something but doesn't elaborate
- Unexplained behavior change
- Reference to unseen events/people
- Payoff timeline: 2-4 weeks

**2. PARTIAL REVEAL**
- Show effect without cause (or vice versa)
- Create "information debt" - promise future explanation
- Player sees evidence character doesn't acknowledge
- Payoff timeline: 2-4 weeks

**3. CONTRADICTION**
- Character acts against established pattern
- Signals major life events happening off-screen
- Out-of-character behavior without explanation
- Payoff timeline: 5-8 weeks (deeper arc)

**4. STAKES ESCALATION**
- Add time pressure
- Introduce consequences for inaction
- Create "ticking clock" elements
- Payoff timeline: Immediate to 2-4 weeks

**FREQUENCY GUIDELINES (Master Truths v1.2):**
- Level 1-2 relationships: 1 in 3 evolutions (33%)
- Level 3-4 relationships: 1 in 2 evolutions (50%)
- Level 5 relationships: Nearly every evolution (90%)
- Crisis evolutions: Always include stakes escalation

**JSON FORMAT:**
[
  {{
    "tension_type": "mystery_hook | partial_reveal | contradiction | stakes_escalation",
    "relationship_level": 1-5,
    "should_inject_tension": true/false,
    "scenario": "Context and interaction",
    "hook_description": "What tension element was planted",
    "information_debt": ["Question player will have", "Another question"],
    "expected_payoff_timeline": "2-4 weeks | 5-8 weeks | season_end",
    "dialogue_snippet": "The actual tension moment",
    "player_curiosity_score": 0.0-1.0,
    "hook_effectiveness": 0.0-1.0,
    "connects_to_previous_hooks": [],
    "tension_score": 0.0-1.0,
    "tags": ["mystery", "relationship_depth", "page_turner"]
  }}
]

**QUALITY REQUIREMENTS (Master Truths v1.2):**
- hook_effectiveness ≥ 0.6 (MANDATORY)
- tension_score ≥ 0.6 (MANDATORY)
- Must create "one more week" desire to continue
- Hook must be specific and trackable

**HIGH-QUALITY EXAMPLES:**

Example 1 - Mystery Hook (Level 3):
{{
  "tension_type": "mystery_hook",
  "relationship_level": 3,
  "should_inject_tension": true,
  "scenario": "Coffee catch-up, friend seems distracted, phone keeps buzzing",
  "hook_description": "Friend mentions 'David' nervously, then immediately changes subject when asked. Hands shake slightly holding coffee cup.",
  "information_debt": [
    "Who is David?",
    "Why did mentioning him make friend nervous?",
    "What's the relationship between friend and David?",
    "Why the physical nervousness response?"
  ],
  "expected_payoff_timeline": "2-4 weeks",
  "dialogue_snippet": "So anyway, David said—[pauses, stares at phone]—actually, never mind. How's your project going?",
  "player_curiosity_score": 0.85,
  "hook_effectiveness": 0.80,
  "connects_to_previous_hooks": [],
  "tension_score": 0.75,
  "tags": ["mystery_hook", "behavioral_signal", "unnamed_person"]
}}

Example 2 - Partial Reveal (Level 4):
{{
  "tension_type": "partial_reveal",
  "relationship_level": 4,
  "should_inject_tension": true,
  "scenario": "Visiting friend's apartment, notice three packed boxes near door",
  "hook_description": "Player sees packed moving boxes labeled 'Kitchen', 'Books', 'Bedroom' but friend doesn't mention them. Acts like everything is normal.",
  "information_debt": [
    "Is friend moving?",
    "Why aren't they mentioning it?",
    "Is this sudden or planned?",
    "Where are they going?"
  ],
  "expected_payoff_timeline": "2-4 weeks",
  "dialogue_snippet": "[Friend casually steps between player and boxes] Want some tea? I've been meaning to catch up properly...",
  "player_curiosity_score": 0.90,
  "hook_effectiveness": 0.85,
  "connects_to_previous_hooks": [],
  "tension_score": 0.80,
  "tags": ["partial_reveal", "visual_evidence", "major_life_change"]
}}

Example 3 - Contradiction (Level 3):
{{
  "tension_type": "contradiction",
  "relationship_level": 3,
  "should_inject_tension": true,
  "scenario": "Usually risk-averse friend suddenly announces they quit their stable job",
  "hook_description": "Friend who always plays it safe, always has backup plans, suddenly quit job with nothing lined up. Acting casual about it but this is completely out of character.",
  "information_debt": [
    "What changed to make them take this risk?",
    "Is something else going on they're not sharing?",
    "Are they okay? This seems impulsive for them.",
    "What happened at the job to trigger this?"
  ],
  "expected_payoff_timeline": "5-8 weeks",
  "dialogue_snippet": "Yeah, I just... quit. No plan, no backup, just walked out. Feels good actually. Want to grab lunch?",
  "player_curiosity_score": 0.88,
  "hook_effectiveness": 0.82,
  "connects_to_previous_hooks": [],
  "tension_score": 0.78,
  "tags": ["contradiction", "character_pattern_break", "hidden_motivation"]
}}

Example 4 - Stakes Escalation (Level 4, Crisis):
{{
  "tension_type": "stakes_escalation",
  "relationship_level": 4,
  "should_inject_tension": true,
  "scenario": "Friend considering major decision, deadline approaching",
  "hook_description": "Friend has job offer in different city, must decide by end of week. If player doesn't help them process this, they'll make decision alone—possibly the wrong one.",
  "information_debt": [
    "Will they move?",
    "What will happen to the friendship?",
    "What factors are they considering?",
    "Can player influence the decision?"
  ],
  "expected_payoff_timeline": "Immediate to 2 weeks",
  "dialogue_snippet": "They need an answer by Friday. I... I don't know what to do. This feels huge. Can we talk about it? I need someone to help me think this through.",
  "player_curiosity_score": 0.92,
  "hook_effectiveness": 0.90,
  "connects_to_previous_hooks": [],
  "tension_score": 0.95,
  "tags": ["stakes_escalation", "ticking_clock", "major_decision"]
}}

Generate {batch_size} diverse tension hooks across all four types.
Focus on hook_effectiveness ≥ 0.6 and tension_score ≥ 0.6.
Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=self.config.temp_tension,
            max_tokens=6000
        )
        
        if response_text:
            return self._parse_json_response(response_text, 'tension_building')
        return []
    
    # ===================================================================
    # 4. MEMORY RESONANCE DATA (NEW v1.2 - Master Truths Section 17)
    # ===================================================================
    
    def generate_memory_resonance_batch(self,
                                       batch_size: Optional[int] = None) -> List[Dict]:
        """
        Generate emotionally resonant memory recall examples.
        
        Master Truths v1.2: Five resonance types with weights 0.7-0.95
        
        Uses: Qwen3-30B-A3B for emotional depth
        """
        if batch_size is None:
            batch_size = self.config.batch_size_memory
        
        prompt = f"""You are an expert at modeling emotionally resonant memory recall per Master Truths v1.2 Section 17.

Generate {batch_size} examples of memories being recalled based on emotional resonance with current situation.

**FIVE RESONANCE TYPES (Master Truths v1.2):**

1. **Same Emotion, Different Context** (0.8 weight)
   - Both memories involve same emotion (joy/sadness/etc)
   - But contexts are different
   - Shows emotional patterns in life

2. **Opposite Emotion, Growth Opportunity** (0.9 weight)
   - Memory of one emotion, current situation is opposite
   - Shows character growth or change
   - Creates powerful contrast moments

3. **Past Trauma, Current Trigger** (0.95 weight - HIGHEST)
   - Memory of painful past, current situation triggers it
   - Most powerful emotional callbacks
   - Authentic PTSD-like responses

4. **Past Joy, Current Sadness Contrast** (0.85 weight)
   - Memory of happy time, current situation is sad
   - Creates poignant, literary moments
   - "Things were so different then" feeling

5. **Emotional Growth Callback** (0.7 weight)
   - Memory of struggling with emotion
   - Current situation shows handling it better
   - Demonstrates character development

**JSON FORMAT:**
[
  {{
    "resonance_type": "same_emotion_different_context | opposite_emotion_growth | past_trauma_trigger | joy_sadness_contrast | growth_callback",
    "resonance_weight": 0.7-0.95,
    "current_situation": "What's happening now",
    "current_emotion": "Primary emotion in current situation",
    "recalled_memory": "Memory that surfaces",
    "memory_emotion": "Primary emotion in recalled memory",
    "memory_context": "When and where memory is from",
    "resonance_explanation": "Why this memory surfaces now (psychological)",
    "character_reaction": "How character responds to memory surfacing",
    "narrative_impact": "Literary quality of the moment",
    "resonance_score": 0.0-1.0,
    "emotional_authenticity": 0.0-1.0,
    "tags": ["emotional_resonance", "memory_recall", "character_depth"]
  }}
]

**QUALITY REQUIREMENTS (Master Truths v1.2):**
- emotional_authenticity ≥ 0.7 (MANDATORY)
- resonance_score should match resonance_weight guidelines
- Must feel psychologically realistic
- Literary quality - creates "catching your breath" moments

**HIGH-QUALITY EXAMPLES:**

Example 1 - Past Trauma Trigger (0.95):
{{
  "resonance_type": "past_trauma_trigger",
  "resonance_weight": 0.95,
  "current_situation": "About to give presentation at work, room full of people",
  "current_emotion": "anxiety, vulnerability",
  "recalled_memory": "High school presentation where classmates laughed, teacher didn't defend them, felt completely alone and humiliated",
  "memory_emotion": "humiliation, abandonment, powerlessness",
  "memory_context": "Age 16, English class, presenting book report",
  "resonance_explanation": "Current vulnerability in front of audience triggers memory of past public humiliation. Same feeling of exposure, same fear of judgment, same physical space dynamic (one person, many watching).",
  "character_reaction": "Hands start shaking, vision narrows, has to take three deep breaths. Thinks: 'This is different. I'm not that kid anymore. These are colleagues, not bullies.' But the fear feels identical.",
  "narrative_impact": "Reader feels the weight of past trauma informing present anxiety. Shows how old wounds never fully heal, they just... wait.",
  "resonance_score": 0.95,
  "emotional_authenticity": 0.92,
  "tags": ["trauma_trigger", "high_resonance", "ptsd_realistic"]
}}

Example 2 - Joy/Sadness Contrast (0.85):
{{
  "resonance_type": "joy_sadness_contrast",
  "resonance_weight": 0.85,
  "current_situation": "Sitting alone in coffee shop where they used to meet best friend who moved away",
  "current_emotion": "loneliness, nostalgia, grief",
  "recalled_memory": "Same booth, same coffee shop, laughing so hard with friend that people stared. Felt like they'd be friends forever.",
  "memory_emotion": "joy, connection, belonging",
  "memory_context": "Six months ago, before friend took job across country",
  "resonance_explanation": "Physical location triggers memory of same space, different emotional state. The contrast between then and now makes current loneliness more acute.",
  "character_reaction": "Can almost hear friend's laugh. Realizes they're sitting in the exact same spot. Orders friend's usual drink out of habit, then remembers. Considers leaving but stays, lets themselves feel it.",
  "narrative_impact": "Poignant moment that readers will recognize—when places hold ghosts of better times. That specific ache of missing someone.",
  "resonance_score": 0.88,
  "emotional_authenticity": 0.90,
  "tags": ["poignant_contrast", "location_memory", "friendship_grief"]
}}

Example 3 - Opposite Emotion Growth (0.9):
{{
  "resonance_type": "opposite_emotion_growth",
  "resonance_weight": 0.9,
  "current_situation": "Successfully navigating conflict with roommate, staying calm and constructive",
  "current_emotion": "confidence, maturity, self-control",
  "recalled_memory": "Similar conflict two years ago where they lost temper, said hurtful things, damaged relationship that never fully recovered",
  "memory_emotion": "rage, loss of control, shame",
  "memory_context": "Previous apartment, different roommate, similar situation",
  "resonance_explanation": "Current successful handling contrasts sharply with past failure. Memory surfaces as proof of growth—'I'm not that person anymore.'",
  "character_reaction": "Feels flash of old anger starting, recognizes the pattern from memory. Chooses different path. After conversation, feels proud but also sad about past damage that can't be undone.",
  "narrative_impact": "Shows character development through contrast. Reader sees the growth because they see what was overcome.",
  "resonance_score": 0.87,
  "emotional_authenticity": 0.89,
  "tags": ["growth_demonstration", "emotional_maturity", "pattern_breaking"]
}}

Example 4 - Same Emotion, Different Context (0.8):
{{
  "resonance_type": "same_emotion_different_context",
  "resonance_weight": 0.8,
  "current_situation": "Feeling proud after completing difficult project at work",
  "current_emotion": "pride, accomplishment, validation",
  "recalled_memory": "Feeling same pride after running first 5K race, different achievement but same emotional quality",
  "memory_emotion": "pride, accomplishment, validation",
  "memory_context": "Three years ago, charity run, personal fitness goal",
  "resonance_explanation": "Same core emotion (pride in overcoming challenge) in different domain. Shows pattern in how character experiences achievement.",
  "character_reaction": "Realizes they feel exactly like they did crossing that finish line. Different challenge, same feeling of 'I did something hard and I did it well.' Smiles at the parallel.",
  "narrative_impact": "Reveals emotional patterns that define character. How they experience success is consistent even across different life areas.",
  "resonance_score": 0.78,
  "emotional_authenticity": 0.82,
  "tags": ["emotional_pattern", "achievement_parallel", "self_awareness"]
}}

Example 5 - Emotional Growth Callback (0.7):
{{
  "resonance_type": "growth_callback",
  "resonance_weight": 0.7,
  "current_situation": "Friend cancels plans last minute, character handles disappointment gracefully",
  "current_emotion": "mild disappointment, acceptance, understanding",
  "recalled_memory": "Year ago, similar cancellation led to catastrophic emotional reaction, tears, feeling abandoned",
  "memory_emotion": "devastation, abandonment, emotional dysregulation",
  "memory_context": "Early in friendship, before therapy, less emotionally mature",
  "resonance_explanation": "Current measured response contrasts with past over-reaction. Memory surfaces as milestone of how far they've come.",
  "character_reaction": "Remembers crying in bathroom stall over similar situation. Feels grateful for the growth. Texts friend: 'No worries, hope everything's okay!' and means it.",
  "narrative_impact": "Quiet triumph of emotional growth. Character has developed healthier emotional regulation.",
  "resonance_score": 0.72,
  "emotional_authenticity": 0.85,
  "tags": ["emotional_regulation", "therapy_success", "quiet_growth"]
}}

Generate {batch_size} diverse memory resonance examples across all five types.
Focus on emotional_authenticity ≥ 0.7.
Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=self.config.temp_memory,
            max_tokens=6000
        )
        
        if response_text:
            return self._parse_json_response(response_text, 'memory_resonance')
        return []
    
    # ===================================================================
    # 5. PERSONALITY TRAIT DATA (Foundation)
    # ===================================================================
    
    def generate_personality_trait_batch(self, 
                                        batch_size: Optional[int] = None) -> List[Dict]:
        """
        Generate OCEAN personality trait examples.
        
        Uses: Qwen3-8B for fast generation
        """
        if batch_size is None:
            batch_size = self.config.batch_size_personality
        
        prompt = f"""Generate {batch_size} character dialogue examples with OCEAN personality trait predictions.

OCEAN Traits (all scored 0.0 to 1.0):
- openness: curiosity, creativity, willingness to try new things
- conscientiousness: organization, reliability, self-discipline
- extraversion: sociability, energy, assertiveness
- agreeableness: compassion, cooperation, empathy
- neuroticism: anxiety, emotional instability, stress response

JSON FORMAT:
[
  {{
    "dialogue": "Character interaction (15-40 words)",
    "context": "Brief situation description",
    "ocean_traits": {{
      "openness": 0.0-1.0,
      "conscientiousness": 0.0-1.0,
      "extraversion": 0.0-1.0,
      "agreeableness": 0.0-1.0,
      "neuroticism": 0.0-1.0
    }},
    "trait_justification": "Why these scores fit the dialogue"
  }}
]

Generate diverse scenarios: conversations, reactions, decisions, conflicts, support moments.
Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['speed'],
            prompt=prompt,
            temperature=self.config.temp_personality,
            max_tokens=4000
        )
        
        if response_text:
            return self._parse_json_response(response_text, 'personality_traits')
        return []
    
    # ===================================================================
    # 6. RELATIONSHIP SCORING DATA
    # ===================================================================
    
    def generate_relationship_scoring_batch(self, 
                                           batch_size: Optional[int] = None) -> List[Dict]:
        """
        Generate interaction quality scoring examples.
        
        Uses: Qwen3-8B for fast generation
        """
        if batch_size is None:
            batch_size = self.config.batch_size_relationship
        
        prompt = f"""Generate {batch_size} player-character interaction examples with relationship impact scores.

Score interactions from -1.5 to +1.0 based on:
- Emotional appropriateness
- Respect for boundaries  
- Active listening
- Empathy demonstrated
- Support provided

JSON FORMAT:
[
  {{
    "player_action": "What player says/does",
    "character_state": "Character's emotional capacity and context",
    "interaction_context": "Situation details",
    "relationship_impact": -1.5 to +1.0,
    "trust_impact": -0.3 to +0.2,
    "impact_justification": "Why this score"
  }}
]

Generate diverse examples. Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['speed'],
            prompt=prompt,
            temperature=self.config.temp_relationship,
            max_tokens=3000
        )
        
        if response_text:
            return self._parse_json_response(response_text, 'relationship_scoring')
        return []
    
    # ===================================================================
    # QUALITY VALIDATION (Master Truths v1.2 Section 17)
    # ===================================================================
    
    def validate_with_qwen3_32b(self, data_batch: List[Dict], 
                               data_type: str) -> Dict:
        """
        Validate quality against Master Truths v1.2 thresholds.
        
        Checks:
        - Emotional Authenticity: ≥ 0.7
        - Tension Building: ≥ 0.6
        - Dramatic Irony: ≥ 0.5
        - Hook Effectiveness: ≥ 0.6
        - Overall Novel-Quality: ≥ 0.7
        """
        sample = random.sample(data_batch, min(5, len(data_batch)))
        
        prompt = f"""You are a quality validator for AI training data per Master Truths Canonical Spec v1.2.

Evaluate these {data_type} examples against canonical requirements.

QUALITY THRESHOLDS (Master Truths v1.2 Section 17):
- Emotional Authenticity: ≥ 0.7 (responses constrained by capacity)
- Tension Building: ≥ 0.6 (mystery hooks, stakes, engagement)
- Dramatic Irony: ≥ 0.5 (knowledge gap utilization)
- Hook Effectiveness: ≥ 0.6 ("one more week" engagement)
- Overall Novel-Quality: ≥ 0.7 (MANDATORY)

Data to evaluate:
{json.dumps(sample, indent=2)}

Evaluate each example:
1. **Emotional Authenticity** (0-1): Capacity constraints respected? X+2 rule followed?
2. **Tension Building** (0-1): Creates page-turner tension? Clear hooks?
3. **Dramatic Irony** (0-1): Knowledge gaps well-used? (if applicable)
4. **Hook Effectiveness** (0-1): Player wants to continue? Clear payoff?
5. **Overall Quality** (0-1): Novel-quality writing? Authentic dialogue?

Return JSON:
{{
  "overall_quality": 0.0-1.0,
  "meets_v1_2_standards": true/false,
  "individual_scores": [
    {{
      "sample_index": 0,
      "emotional_authenticity": 0.0-1.0,
      "tension_building": 0.0-1.0,
      "dramatic_irony": 0.0-1.0,
      "hook_effectiveness": 0.0-1.0,
      "overall": 0.0-1.0,
      "passes_threshold": true/false,
      "issues": ["List specific problems if any"]
    }}
  ],
  "recommendations": ["Specific improvements needed"],
  "strengths": ["What works well"]
}}"""

        response_text = self.generate_with_qwen3(
            model=self.models['validation'],
            prompt=prompt,
            temperature=self.config.temp_validation,
            max_tokens=2000
        )
        
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    lines = cleaned.split('\n')
                    cleaned = '\n'.join(lines[1:])
                    if cleaned.rstrip().endswith('```'):
                        cleaned = cleaned.rstrip()[:-3]
                
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {
                    "overall_quality": 0.5,
                    "meets_v1_2_standards": False,
                    "error": "Validation parse failed"
                }
        
        return {
            "overall_quality": 0.5,
            "meets_v1_2_standards": False,
            "error": "Validation generation failed"
        }
    
    def _parse_json_response(self, response_text: str, data_type: str) -> List[Dict]:
        """Parse JSON response from Qwen3"""
        try:
            cleaned = response_text.strip()
            if cleaned.startswith('```'):
                lines = cleaned.split('\n')
                cleaned = '\n'.join(lines[1:])
                if cleaned.rstrip().endswith('```'):
                    cleaned = cleaned.rstrip()[:-3]
            
            data = json.loads(cleaned)
            
            if not isinstance(data, list):
                AppLogger.error(f"Expected list for {data_type}, got {type(data).__name__}",
                              ValueError("Invalid response format"))
                return []
            
            AppLogger.info(f"Successfully parsed {data_type} batch",
                          data={'count': len(data)})
            return data
            
        except json.JSONDecodeError as e:
            AppLogger.error(f"JSON parsing failed for {data_type}", e)
            return []
        except Exception as e:
            AppLogger.error(f"Unexpected parsing error for {data_type}", e)
            return []
    
    def save_batch(self, data: List[Dict], data_type: str,
                   batch_number: int, timestamp: str) -> str:
        """Save batch to disk with v1.2 metadata"""
        filename = f"{data_type}_batch{batch_number:04d}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        try:
            output = {
                "master_truths_version": "v1.2",
                "data_type": data_type,
                "batch_number": batch_number,
                "timestamp": timestamp,
                "sample_count": len(data),
                "samples": data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            AppLogger.info(f"Saved {data_type} batch", data={
                'file': filename,
                'samples': len(data)
            })
            return str(filepath)
            
        except Exception as e:
            AppLogger.error(f"Failed to save batch {filename}", e)
            raise
    
    def run_production_cycle(self, duration_hours: int = 24) -> Dict[str, List[Dict]]:
        """Run Master Truths v1.2 compliant production cycle"""
        AppLogger.info(f"Starting {duration_hours}h production (Master Truths v1.2)", data={
            'daily_target': self.config.total_daily_target,
            'quality_thresholds': self.config.quality_thresholds
        })
        
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        results = {
            'emotional_authenticity': [],
            'dramatic_irony': [],
            'tension_building': [],
            'memory_resonance': [],
            'personality_traits': [],
            'relationship_scoring': []
        }
        
        # Calculate batches (prioritized by Master Truths v1.2)
        batches_needed = {
            'emotional_authenticity': (self.config.target_emotional_authenticity // 12) + 3,
            'dramatic_irony': (self.config.target_dramatic_irony // 8) + 3,
            'tension_building': (self.config.target_tension_building // 10) + 3,
            'memory_resonance': (self.config.target_memory_resonance // 15) + 3,
            'personality_traits': (self.config.target_personality_traits // 25) + 5,
            'relationship_scoring': (self.config.target_relationship_scoring // 20) + 3
        }
        
        total_batches = sum(batches_needed.values())
        
        try:
            pbar = tqdm(total=total_batches, desc="Generating v1.2 compliant data")
            
            # 1. Emotional Authenticity (CORE)
            AppLogger.info("Generating emotional authenticity data (Master Truths v1.2)")
            for i in range(batches_needed['emotional_authenticity']):
                batch = self.generate_emotional_authenticity_batch()
                if batch:
                    results['emotional_authenticity'].extend(batch)
                    self.save_batch(batch, 'emotional_authenticity', i, timestamp)
                pbar.update(1)
                time.sleep(1)
            
            # 2. Dramatic Irony
            AppLogger.info("Generating dramatic irony scenarios")
            for i in range(batches_needed['dramatic_irony']):
                batch = self.generate_dramatic_irony_batch()
                if batch:
                    results['dramatic_irony'].extend(batch)
                    self.save_batch(batch, 'dramatic_irony', i, timestamp)
                pbar.update(1)
                time.sleep(1)
            
            # 3. Tension Building
            AppLogger.info("Generating tension building hooks")
            for i in range(batches_needed['tension_building']):
                batch = self.generate_tension_building_batch()
                if batch:
                    results['tension_building'].extend(batch)
                    self.save_batch(batch, 'tension_building', i, timestamp)
                pbar.update(1)
                time.sleep(1)
            
            # 4. Memory Resonance (NEW v1.2)
            AppLogger.info("Generating memory resonance data (NEW v1.2)")
            for i in range(batches_needed['memory_resonance']):
                batch = self.generate_memory_resonance_batch()
                if batch:
                    results['memory_resonance'].extend(batch)
                    self.save_batch(batch, 'memory_resonance', i, timestamp)
                pbar.update(1)
                time.sleep(1)
            
            # 5. Personality Traits
            AppLogger.info("Generating personality trait data")
            for i in range(batches_needed['personality_traits']):
                batch = self.generate_personality_trait_batch()
                if batch:
                    results['personality_traits'].extend(batch)
                    self.save_batch(batch, 'personality_traits', i, timestamp)
                pbar.update(1)
                time.sleep(0.5)
            
            # 6. Relationship Scoring
            AppLogger.info("Generating relationship scoring data")
            for i in range(batches_needed['relationship_scoring']):
                batch = self.generate_relationship_scoring_batch()
                if batch:
                    results['relationship_scoring'].extend(batch)
                    self.save_batch(batch, 'relationship_scoring', i, timestamp)
                pbar.update(1)
                time.sleep(0.5)
            
            pbar.close()
            
            # Quality validation
            AppLogger.info("Running Master Truths v1.2 quality validation")
            validation_results = []
            for data_type, data in results.items():
                if len(data) > 5:
                    validation = self.validate_with_qwen3_32b(data, data_type)
                    validation_results.append({
                        'type': data_type,
                        'quality': validation.get('overall_quality', 0.5),
                        'meets_v1_2': validation.get('meets_v1_2_standards', False),
                        'sample_size': len(data)
                    })
            
            # Summary
            elapsed = time.time() - start_time
            total_generated = sum(len(data) for data in results.values())
            
            AppLogger.success("Production cycle complete (Master Truths v1.2)", data={
                'duration_hours': f'{elapsed/3600:.1f}',
                'total_samples': total_generated,
                'validation_scores': validation_results
            })
            
            return results
            
        except KeyboardInterrupt:
            AppLogger.warning("Production interrupted")
            for data_type, data in results.items():
                if data:
                    self.save_batch(data, f"{data_type}_PARTIAL", 0, timestamp)
            return results
