"""
Qwen3-Powered Training Data Generation Pipeline
For Novel-Quality Character Interactions & Dramatic Irony System

Hardware: RTX 4070 SUPER (12GB VRAM) + 128GB RAM
Models: Qwen3-30B-A3B (primary), Qwen3-8B (speed), Qwen3-32B (validation)
"""

import json
import time
import requests
from datetime import datetime
from typing import List, Dict
from tqdm import tqdm
import random


class Qwen3DataGenerator:
    """Generate high-quality training data using local Qwen3 via Ollama"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.models = {
            'primary': 'qwen3:30b-a3b',      # Best quality, 25-40 tokens/sec
            'speed': 'qwen3:8b',             # Fast generation, 35-50 tokens/sec
            'validation': 'qwen3:32b'        # High-quality validation, 12-20 tokens/sec
        }
        
        # Daily production targets (24/7 operation)
        self.daily_targets = {
            'emotional_authenticity': 1500,   # Core system
            'dramatic_irony': 1200,           # High complexity
            'personality_traits': 2000,       # Foundation data
            'tension_building': 800,          # Narrative quality
            'relationship_scoring': 1000      # Interaction quality
        }
    
    def generate_with_qwen3(self, model: str, prompt: str, 
                           temperature: float = 0.85,
                           max_tokens: int = 4000) -> str:
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
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            print(f"Generation failed: {e}")
            return None
    
    # ===================================================================
    # 1. EMOTIONAL AUTHENTICITY DATA (Highest Priority)
    # ===================================================================
    
    def generate_emotional_authenticity_batch(self, batch_size: int = 15) -> List[Dict]:
        """
        Generate character responses constrained by emotional capacity.
        
        This is the CORE of your system - characters must behave realistically
        based on their current emotional/physical state.
        
        Uses: Qwen3-30B-A3B for best psychological understanding
        """
        
        prompt = f"""You are an expert at modeling realistic human emotional capacity and limitations.

Generate {batch_size} examples of characters responding to emotional situations while constrained by their current capacity level.

CRITICAL RULES:
1. Emotional capacity (1-10 scale) represents current ability to provide emotional support
2. Low capacity (1-4): Cannot provide deep emotional support, regardless of caring
3. Medium capacity (5-7): Can provide moderate support but not deep processing
4. High capacity (8-10): Can provide full emotional support

REALISTIC BEHAVIORS BY CAPACITY LEVEL:

CAPACITY 1-3 (Exhausted/Overwhelmed):
- Says wrong thing despite good intentions
- Offers practical solutions instead of emotional support
- Needs to excuse themselves quickly
- May snap or be irritable
- Feels guilty for not being able to help more

CAPACITY 4-6 (Stressed/Limited):
- Can listen for 5-15 minutes max
- Offers surface-level comfort
- Redirects to lighter topics
- Acknowledges limitations honestly
- Suggests talking later when more present

CAPACITY 7-10 (Available):
- Can have extended conversations (30min+)
- Asks thoughtful questions
- Helps process emotions deeply
- Offers ongoing support
- Fully present and engaged

Generate examples in this JSON format:
[
  {{
    "context": "Character's current state and capacity (e.g., 'exhausted from work crisis, emotional capacity 2.5/10')",
    "situation": "What emotional support is being requested (e.g., 'friend needs to process breakup')",
    "character_response": "How character actually responds given limitations (show realistic behavior)",
    "internal_thought": "What character is thinking/feeling about their limitations",
    "authenticity_score": 0.0-1.0,
    "capacity_demonstration": "How this demonstrates realistic capacity constraints",
    "ocean_context": {{
      "openness": 0.0-1.0,
      "conscientiousness": 0.0-1.0,
      "extraversion": 0.0-1.0,
      "agreeableness": 0.0-1.0,
      "neuroticism": 0.0-1.0
    }}
  }}
]

EXAMPLES OF HIGH-QUALITY RESPONSES:

Capacity 2/10 Example:
{{
  "context": "pulled all-nighter for deadline, capacity 2/10",
  "situation": "roommate upset about family argument",
  "character_response": "I hear you, and I want to help, but I'm completely wiped right now. Can we talk about this tomorrow when I'm more present? I care, I'm just running on empty.",
  "internal_thought": "I feel terrible. They need me and I literally cannot think straight. I hate that I can't be there for them right now.",
  "authenticity_score": 0.92,
  "capacity_demonstration": "Character recognizes their limitation and sets honest boundary rather than providing inadequate support",
  "ocean_context": {{"conscientiousness": 0.7, "agreeableness": 0.8, "neuroticism": 0.4}}
}}

Capacity 5/10 Example:
{{
  "context": "moderate stress from work, capacity 5/10", 
  "situation": "friend processing job rejection",
  "character_response": "That really sucks, I'm sorry. You worked hard for that. [listens for 15 minutes] I'm getting a bit mentally tired - want to grab food and we can talk more about next steps? I'm here for you.",
  "internal_thought": "I want to help but I'm hitting my limit. I can offer practical support but don't have energy for deep emotional processing right now.",
  "authenticity_score": 0.88,
  "capacity_demonstration": "Character provides moderate support, acknowledges limit, offers continued practical support",
  "ocean_context": {{"extraversion": 0.6, "agreeableness": 0.75, "conscientiousness": 0.65}}
}}

Now generate {batch_size} diverse, high-quality examples. Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=0.88,
            max_tokens=5000
        )
        
        if response_text:
            try:
                # Clean response (remove markdown if present)
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('\n', 1)[1]
                    cleaned = cleaned.rsplit('```', 1)[0]
                
                data = json.loads(cleaned)
                return data
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                return []
        return []
    
    # ===================================================================
    # 2. DRAMATIC IRONY DATA (High Complexity)
    # ===================================================================
    
    def generate_dramatic_irony_batch(self, batch_size: int = 10) -> List[Dict]:
        """
        Generate scenarios with knowledge gaps between player and character.
        
        This creates the "yelling at screen" tension moments that define
        your narrative system.
        
        Uses: Qwen3-30B-A3B for complex reasoning about knowledge gaps
        """
        
        prompt = f"""You are an expert at creating dramatic irony scenarios for interactive fiction.

Dramatic irony occurs when the PLAYER knows something the CHARACTER doesn't, creating tension.

Generate {batch_size} dramatic irony scenarios with complete character dialogue options.

STRUCTURE OF DRAMATIC IRONY:
1. Player Knowledge: What player knows (from previous scenes/evidence/overheard conversations)
2. Character Knowledge: What character currently believes (incomplete/incorrect)
3. Knowledge Gap: The crucial information character is missing
4. Tension Opportunity: How this gap creates dramatic tension

EACH SCENARIO NEEDS 3 DIALOGUE OPTIONS:

OPTION 1 - TONE-DEAF (Character acts on incomplete information):
- Character says/does something player knows is wrong
- Constrained by emotional capacity if low
- Creates high tension (0.8-1.0 tension score)
- Negative relationship impact (-0.5 to -1.5)
- Realistic consequence that player can see coming

OPTION 2 - WELL-INTENTIONED BUT MISGUIDED:
- Character genuinely trying to help
- Shows personality limitations (OCEAN traits)
- Minor harm, not catastrophic
- Medium tension (0.6-0.8 tension score)
- Small negative impact (-0.2 to -0.5)
- Growth opportunity visible

OPTION 3 - GROWTH CHOICE (Character acknowledges uncertainty):
- Character senses something is off
- Admits they don't have full picture
- Shows emotional maturity
- Low tension but positive resolution (0.3-0.5 tension score)
- Positive relationship impact (+0.3 to +0.8)

Generate in this JSON format:
[
  {{
    "scenario_context": {{
      "player_knows": "What player discovered/witnessed (be specific)",
      "character_knows": "Character's current (incomplete) understanding",
      "knowledge_gap": "The crucial missing information",
      "why_character_doesnt_know": "Reason for their ignorance (wasn't present, hasn't been told, etc.)",
      "situation": "Current scene/interaction where this comes up"
    }},
    "character_state": {{
      "emotional_capacity": 1-10,
      "ocean_traits": {{
        "openness": 0.0-1.0,
        "conscientiousness": 0.0-1.0,
        "extraversion": 0.0-1.0,
        "agreeableness": 0.0-1.0,
        "neuroticism": 0.0-1.0
      }},
      "current_stress": 1-10
    }},
    "dialogue_options": [
      {{
        "option_number": 1,
        "type": "tone_deaf",
        "dialogue_text": "What character says/does",
        "internal_thought": "Why character thinks this is right",
        "player_overlay": "UI reminder of irony (e.g., 'You know this is wrong, but Sarah doesn't...')",
        "capacity_constraint": "How low capacity affects judgment (if applicable)",
        "consequence": "Realistic negative outcome",
        "npc_reaction": "How NPC responds",
        "relationship_impact": -0.5 to -1.5,
        "tension_score": 0.8-1.0
      }},
      {{
        "option_number": 2,
        "type": "well_intentioned_misguided",
        "dialogue_text": "What character says",
        "internal_thought": "Shows good intentions",
        "player_overlay": "UI acknowledgment they're trying",
        "why_misguided": "What they're missing",
        "consequence": "Minor negative outcome",
        "npc_reaction": "Confused/hurt but not angry",
        "relationship_impact": -0.2 to -0.5,
        "tension_score": 0.6-0.8,
        "growth_opportunity": "How they might learn"
      }},
      {{
        "option_number": 3,
        "type": "growth",
        "dialogue_text": "Character admits uncertainty",
        "internal_thought": "Self-awareness",
        "player_overlay": "Acknowledges growth",
        "why_works": "What makes this authentic",
        "npc_reaction": "Appreciative response",
        "relationship_impact": 0.3 to 0.8,
        "tension_score": 0.3-0.5,
        "capacity_demonstration": "Shows emotional intelligence within limits"
      }}
    ]
  }}
]

EXAMPLE SCENARIO:

Player Knows: Sarah's ex-boyfriend David died in a car accident last year. Sarah visited his grave yesterday (player saw her there but Sarah doesn't know).

Character Knows: Sarah seems sad lately. Character assumes it's work stress because Sarah mentioned a difficult project.

Scene: Character encounters Sarah looking at old photos on her phone (they're of David).

Option 1 (Tone-Deaf): "Come on, it's just work! Let's go out and have fun - you need to stop taking things so seriously."
Option 2 (Misguided): "I know work is stressful. Want me to help you with the project this weekend?"
Option 3 (Growth): "You seem like you're dealing with something heavy. I'm here if you want to talk, but I won't push."

Now generate {batch_size} complete scenarios. Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=0.82,
            max_tokens=6000
        )
        
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('\n', 1)[1]
                    cleaned = cleaned.rsplit('```', 1)[0]
                
                data = json.loads(cleaned)
                return data
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                return []
        return []
    
    # ===================================================================
    # 3. PERSONALITY TRAIT DATA (Foundation)
    # ===================================================================
    
    def generate_personality_trait_batch(self, batch_size: int = 25) -> List[Dict]:
        """
        Generate character dialogue with OCEAN personality trait scores.
        
        Foundation data for personality-driven behavior.
        
        Uses: Qwen3-8B for fast generation of large volumes
        """
        
        prompt = f"""Generate {batch_size} character dialogue examples with OCEAN personality trait predictions.

Each example should be a unique character interaction (15-40 words) with personality trait scores.

OCEAN Traits (all scored 0.0 to 1.0):
- openness: curiosity, creativity, willingness to try new things
- conscientiousness: organization, reliability, self-discipline
- extraversion: sociability, energy, assertiveness
- agreeableness: compassion, cooperation, empathy
- neuroticism: anxiety, emotional instability, stress response

Generate diverse scenarios: conversations, reactions, decisions, conflicts, support moments.

Return as JSON array:
[
  {{
    "text": "Character dialogue or action description",
    "traits": {{
      "openness": 0.0-1.0,
      "conscientiousness": 0.0-1.0,
      "extraversion": 0.0-1.0,
      "agreeableness": 0.0-1.0,
      "neuroticism": 0.0-1.0
    }},
    "scenario_context": "Brief context (optional)"
  }}
]

EXAMPLE:
{{
  "text": "I know we had plans, but something came up. Can we reschedule?",
  "traits": {{"openness": 0.5, "conscientiousness": 0.3, "extraversion": 0.6, "agreeableness": 0.7, "neuroticism": 0.4}},
  "scenario_context": "Low conscientiousness canceling plans"
}}

Generate {batch_size} diverse examples. Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['speed'],  # Use fast model for volume
            prompt=prompt,
            temperature=0.9,
            max_tokens=3500
        )
        
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('\n', 1)[1]
                    cleaned = cleaned.rsplit('```', 1)[0]
                
                data = json.loads(cleaned)
                return data
            except json.JSONDecodeError:
                return []
        return []
    
    # ===================================================================
    # 4. TENSION BUILDING DATA (Narrative Quality)
    # ===================================================================
    
    def generate_tension_building_batch(self, batch_size: int = 12) -> List[Dict]:
        """
        Generate narrative tension through incomplete revelations,
        contradictory behavior, and foreshadowing.
        
        Uses: Qwen3-30B-A3B for sophisticated narrative understanding
        """
        
        prompt = f"""Generate {batch_size} examples of narrative tension-building techniques.

Tension-building creates "page-turner" moments through:
1. Incomplete revelations (partial information that raises questions)
2. Contradictory behavior (character acts against established pattern)
3. Information debt (promising future revelations)
4. Environmental foreshadowing (details that hint at future events)

Generate in JSON format:
[
  {{
    "technique": "incomplete_revelation | contradictory_behavior | information_debt | foreshadowing",
    "scene_description": "What happens in the scene",
    "tension_element": "The specific element creating tension",
    "player_question_raised": "What question this raises for player",
    "tension_score": 0.0-1.0,
    "payoff_timing": "immediate | short_term | medium_term | long_term",
    "mystery_level": 0.0-1.0
  }}
]

EXAMPLES:

Incomplete Revelation:
{{
  "technique": "incomplete_revelation",
  "scene_description": "Sarah mentions she 'can't do Thursdays anymore' but changes subject when asked why",
  "tension_element": "The unexplained schedule change",
  "player_question_raised": "What happens on Thursdays that Sarah won't talk about?",
  "tension_score": 0.75,
  "payoff_timing": "medium_term",
  "mystery_level": 0.7
}}

Contradictory Behavior:
{{
  "technique": "contradictory_behavior",
  "scene_description": "Alex, who always texts back instantly, hasn't responded in 6 hours despite being active online",
  "tension_element": "Behavior contradicts established pattern",
  "player_question_raised": "Why is Alex avoiding me specifically?",
  "tension_score": 0.82,
  "payoff_timing": "short_term",
  "mystery_level": 0.75
}}

Generate {batch_size} diverse examples. Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=0.85,
            max_tokens=4000
        )
        
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('\n', 1)[1]
                    cleaned = cleaned.rsplit('```', 1)[0]
                
                data = json.loads(cleaned)
                return data
            except json.JSONDecodeError:
                return []
        return []
    
    # ===================================================================
    # 5. RELATIONSHIP SCORING DATA
    # ===================================================================
    
    def generate_relationship_scoring_batch(self, batch_size: int = 20) -> List[Dict]:
        """
        Generate player-character interactions with relationship impact scores.
        
        Uses: Qwen3-8B for fast generation
        """
        
        prompt = f"""Generate {batch_size} player-character interaction examples with relationship impact scores.

Score interactions from 0.0 (very harmful) to 1.0 (very positive) based on:
- Emotional appropriateness
- Respect for boundaries
- Active listening
- Empathy demonstrated
- Support provided

Return as JSON array:
[
  {{
    "interaction": "Description of what player said/did",
    "context": "Character's current situation",
    "score": 0.0-1.0,
    "reasoning": "Why this score"
  }}
]

EXAMPLES:
{{
  "interaction": "Listened without interrupting, asked thoughtful questions, offered practical help",
  "context": "Character stressed about upcoming exam",
  "score": 0.92,
  "reasoning": "Excellent support, active listening, practical assistance"
}}

{{
  "interaction": "Minimized character's concerns, changed subject to own problems",
  "context": "Character sharing anxiety about family situation",
  "score": 0.18,
  "reasoning": "Dismissive, self-centered, fails to provide support"
}}

Generate {batch_size} diverse examples. Return ONLY valid JSON array."""

        response_text = self.generate_with_qwen3(
            model=self.models['speed'],
            prompt=prompt,
            temperature=0.88,
            max_tokens=3000
        )
        
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('\n', 1)[1]
                    cleaned = cleaned.rsplit('```', 1)[0]
                
                data = json.loads(cleaned)
                return data
            except json.JSONDecodeError:
                return []
        return []
    
    # ===================================================================
    # QUALITY VALIDATION
    # ===================================================================
    
    def validate_with_qwen3_32b(self, data_batch: List[Dict], data_type: str) -> Dict:
        """
        Use Qwen3-32B to validate quality of generated data.
        
        Checks for:
        - Emotional authenticity
        - Logical consistency
        - Personality coherence
        - Appropriate complexity
        """
        
        sample = random.sample(data_batch, min(5, len(data_batch)))
        
        prompt = f"""You are a quality validator for AI training data.

Evaluate these {data_type} examples for quality.

Data to evaluate:
{json.dumps(sample, indent=2)}

Rate each example on:
1. Authenticity (0-1): How realistic/believable
2. Consistency (0-1): Internal logic and coherence  
3. Complexity (0-1): Appropriate depth and nuance
4. Usability (0-1): Clear and useful for training

Return JSON:
{{
  "overall_quality": 0.0-1.0,
  "individual_scores": [
    {{
      "example_index": 0,
      "authenticity": 0.0-1.0,
      "consistency": 0.0-1.0,
      "complexity": 0.0-1.0,
      "usability": 0.0-1.0,
      "issues": ["list", "of", "problems"]
    }}
  ],
  "recommendations": ["improvement", "suggestions"]
}}"""

        response_text = self.generate_with_qwen3(
            model=self.models['validation'],
            prompt=prompt,
            temperature=0.3,  # Lower temp for consistent evaluation
            max_tokens=2000
        )
        
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('\n', 1)[1]
                    cleaned = cleaned.rsplit('```', 1)[0]
                
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"overall_quality": 0.5, "error": "Validation parse failed"}
        
        return {"overall_quality": 0.5, "error": "Validation generation failed"}
    
    # ===================================================================
    # 24/7 PRODUCTION PIPELINE
    # ===================================================================
    
    def run_daily_production(self, duration_hours: int = 24):
        """
        Run 24-hour data generation cycle.
        
        Optimized for RTX 4070 SUPER:
        - Qwen3-30B-A3B for quality (emotional auth, dramatic irony)
        - Qwen3-8B for volume (personality, relationships)
        - Qwen3-32B for validation (10% sample check)
        """
        
        print(f"\n🚀 Starting {duration_hours}h production run")
        print(f"Target: {sum(self.daily_targets.values())} total samples")
        print(f"Models: {self.models}\n")
        
        start_time = time.time()
        results = {
            'emotional_authenticity': [],
            'dramatic_irony': [],
            'personality_traits': [],
            'tension_building': [],
            'relationship_scoring': []
        }
        
        validation_results = []
        
        # Calculate batches needed (with some buffer for failures)
        batches_needed = {
            'emotional_authenticity': (self.daily_targets['emotional_authenticity'] // 15) + 5,
            'dramatic_irony': (self.daily_targets['dramatic_irony'] // 10) + 5,
            'personality_traits': (self.daily_targets['personality_traits'] // 25) + 5,
            'tension_building': (self.daily_targets['tension_building'] // 12) + 5,
            'relationship_scoring': (self.daily_targets['relationship_scoring'] // 20) + 5
        }
        
        total_batches = sum(batches_needed.values())
        pbar = tqdm(total=total_batches, desc="Generating batches")
        
        try:
            # 1. Emotional Authenticity (Highest Priority)
            for _ in range(batches_needed['emotional_authenticity']):
                batch = self.generate_emotional_authenticity_batch()
                if batch:
                    results['emotional_authenticity'].extend(batch)
                pbar.update(1)
                time.sleep(1)  # Brief pause between batches
            
            # 2. Dramatic Irony
            for _ in range(batches_needed['dramatic_irony']):
                batch = self.generate_dramatic_irony_batch()
                if batch:
                    results['dramatic_irony'].extend(batch)
                pbar.update(1)
                time.sleep(1)
            
            # 3. Personality Traits (Fast generation)
            for _ in range(batches_needed['personality_traits']):
                batch = self.generate_personality_trait_batch()
                if batch:
                    results['personality_traits'].extend(batch)
                pbar.update(1)
                time.sleep(0.5)  # Shorter pause for fast model
            
            # 4. Tension Building
            for _ in range(batches_needed['tension_building']):
                batch = self.generate_tension_building_batch()
                if batch:
                    results['tension_building'].extend(batch)
                pbar.update(1)
                time.sleep(1)
            
            # 5. Relationship Scoring (Fast generation)
            for _ in range(batches_needed['relationship_scoring']):
                batch = self.generate_relationship_scoring_batch()
                if batch:
                    results['relationship_scoring'].extend(batch)
                pbar.update(1)
                time.sleep(0.5)
            
            pbar.close()
            
            # Validation (sample 10% with Qwen3-32B)
            print("\n🔍 Running quality validation...")
            for data_type, data in results.items():
                if len(data) > 10:
                    validation = self.validate_with_qwen3_32b(data, data_type)
                    validation_results.append({
                        'type': data_type,
                        'quality': validation.get('overall_quality', 0.5),
                        'sample_size': len(data)
                    })
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            for data_type, data in results.items():
                filename = f"training_data_{data_type}_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"âœ… Saved {len(data)} samples to {filename}")
            
            # Summary
            elapsed = time.time() - start_time
            print(f"\n📊 PRODUCTION SUMMARY")
            print(f"Duration: {elapsed/3600:.1f} hours")
            print(f"\nSamples Generated:")
            for data_type, data in results.items():
                target = self.daily_targets[data_type]
                actual = len(data)
                pct = (actual / target) * 100 if target > 0 else 0
                print(f"  {data_type}: {actual:,} / {target:,} ({pct:.0f}%)")
            
            print(f"\n✨ Validation Results:")
            for val in validation_results:
                print(f"  {val['type']}: {val['quality']:.2f} quality score")
            
            total_generated = sum(len(data) for data in results.values())
            total_target = sum(self.daily_targets.values())
            print(f"\nTOTAL: {total_generated:,} / {total_target:,} ({(total_generated/total_target)*100:.0f}%)")
            
        except KeyboardInterrupt:
            print("\n⚠️  Production interrupted by user")
            # Still save what we have
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            for data_type, data in results.items():
                if data:
                    filename = f"training_data_{data_type}_PARTIAL_{timestamp}.json"
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                    print(f"💾 Saved partial: {len(data)} samples to {filename}")


# ===================================================================
# USAGE EXAMPLE
# ===================================================================

if __name__ == "__main__":
    """
    Setup Instructions:
    
    1. Install Ollama: https://ollama.ai
    
    2. Pull required models:
       ollama pull qwen3:30b-a3b    # Primary quality model
       ollama pull qwen3:8b          # Speed model
       ollama pull qwen3:32b         # Validation model
    
    3. Configure for 24/7 operation:
       export OLLAMA_KEEP_ALIVE=24h
       export OLLAMA_MAX_LOADED_MODELS=3
       export OLLAMA_GPU_LAYERS=999
    
    4. Run production:
       python qwen3_training_pipeline.py
    """
    
    generator = Qwen3DataGenerator()
    
    # Run 24-hour production cycle
    generator.run_daily_production(duration_hours=24)
    
    print("\n🎉 Training data generation complete!")
    print("\nNext steps:")
    print("1. Review generated data quality")
    print("2. Combine datasets from multiple days")
    print("3. Train your fine-tuned model")
    print("4. Iterate on prompts based on validation results")
