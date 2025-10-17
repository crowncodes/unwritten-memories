"""
Systematic Parameter Space Training Data Generator
Master Truths Canonical Spec v1.2 Compliant

IMPROVEMENTS over qwen3_generator.py:
1. Systematic parameter coverage (not random)
2. Full authenticity spectrum (0.2-1.0 vs 0.82-0.95)
3. 8 complexity types (vs 0)
4. Focused prompts (150 words vs 400+ lines)
5. Batch processing (5:1 efficiency)
6. Coverage tracking
7. Numerical grounding integration

Addresses Critical Quality Issues:
- Repetitive patterns → Systematic parameter buckets
- Missing low authenticity → Required spectrum coverage
- No complexity → 8 complexity types mandatory
- Giant prompts → Focused 150-word prompts
- No tracking → Full coverage database
"""

import json
import time
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import random

from .config import EnhancedTrainingConfig as TrainingConfig
from .qwen3_generator import Qwen3DataGenerator
from ..utils.logger import AppLogger


class SystematicParameterGenerator(Qwen3DataGenerator):
    """
    Enhanced generator with systematic parameter space coverage.

    Key Improvements:
    - Systematic vs random parameter selection
    - Full authenticity spectrum enforcement
    - Mandatory complexity factors
    - Focused prompts for efficiency
    - Coverage tracking and gap filling
    """

    def __init__(self, config: Optional[TrainingConfig] = None):
        """Initialize systematic generator with coverage tracking"""
        super().__init__(config)

        # Initialize coverage tracker
        self.coverage_db = self.output_dir / "coverage_tracking.db"
        self._init_coverage_database()

        AppLogger.info(
            "SystematicParameterGenerator initialized",
            data={
                "improvements": [
                    "systematic_parameters",
                    "full_spectrum_coverage",
                    "complexity_factors",
                    "batch_processing",
                    "coverage_tracking",
                ]
            },
        )

    def _init_coverage_database(self):
        """Initialize SQLite database for tracking parameter coverage"""
        conn = sqlite3.connect(self.coverage_db)

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS parameter_coverage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capacity_level TEXT,
                capacity_range TEXT,
                authenticity_target TEXT,
                authenticity_range TEXT,
                complexity_type TEXT,
                support_range TEXT,
                generated_count INTEGER DEFAULT 1,
                first_generated TIMESTAMP,
                last_generated TIMESTAMP,
                UNIQUE(capacity_level, authenticity_target, complexity_type)
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT,
                generation_timestamp TIMESTAMP,
                total_examples INTEGER,
                spectrum_coverage TEXT,
                complexity_coverage TEXT,
                quality_score REAL,
                meets_requirements BOOLEAN
            )
        """
        )

        conn.commit()
        conn.close()

        AppLogger.info(
            "Coverage tracking database initialized", data={"database": str(self.coverage_db)}
        )

    # ===================================================================
    # SYSTEMATIC PARAMETER SPACE ARCHITECTURE
    # ===================================================================

    def _generate_systematic_parameters(self, batch_size: int) -> List[Dict]:
        """
        Generate systematic parameter combinations ensuring full spectrum coverage.

        IMPROVEMENT: Replaces random generation with systematic buckets.
        """
        # Define systematic parameter buckets
        capacity_levels = [
            {"name": "crisis", "range": (0.5, 1.5), "frequency": 0.15},
            {"name": "low", "range": (2.0, 4.0), "frequency": 0.25},
            {"name": "medium", "range": (4.5, 6.5), "frequency": 0.35},
            {"name": "high", "range": (7.0, 9.5), "frequency": 0.25},
        ]

        # FIX v1.6: Rebalanced to reduce excellent clustering (was 64%, should be ~25%)
        authenticity_targets = [
            {"name": "failed", "range": (0.2, 0.4), "frequency": 0.20},  # Increased
            {"name": "struggling", "range": (0.4, 0.6), "frequency": 0.25},  # Increased
            {"name": "authentic", "range": (0.6, 0.8), "frequency": 0.30},  # Slight decrease
            {"name": "excellent", "range": (0.8, 1.0), "frequency": 0.25},  # Decreased from 0.30
        ]

        # IMPROVEMENT: 8 complexity types vs 0 in current system
        complexity_types = [
            "baseline",  # Current system only has this
            "people_pleasing",  # Says yes when should say no
            "misjudgment_over",  # Overestimates capacity
            "misjudgment_under",  # Underestimates capacity
            "defensive_lashing",  # Lashes out when overwhelmed
            "emergency_override",  # Pushes beyond limits in crisis
            "cultural_indirect",  # Cultural barriers to directness
            "mixed_emotions",  # Wants to help BUT resents
        ]

        # FIX v1.6: Shuffle complexity types each batch to ensure variety
        shuffled_complexity = complexity_types.copy()
        random.shuffle(shuffled_complexity)

        # Check for coverage gaps
        missing_combinations = self._get_missing_combinations()

        scenarios = []
        for i in range(batch_size):
            # Prioritize missing combinations if any
            if missing_combinations and i < len(missing_combinations):
                scenario = missing_combinations[i]
            else:
                # Systematic selection ensuring coverage
                capacity = self._select_from_distribution(capacity_levels)
                authenticity = self._select_from_distribution(authenticity_targets)
                # FIX v1.6: Use shuffled list for better variety
                complexity = shuffled_complexity[i % len(shuffled_complexity)]

                # Calculate support level based on authenticity target
                effective_capacity = random.uniform(*capacity["range"])
                support_needed = self._calculate_support_for_authenticity(
                    effective_capacity, authenticity["name"]
                )

                scenario = {
                    "capacity_level": capacity["name"],
                    "capacity_range": capacity["range"],
                    "authenticity_target": authenticity["name"],
                    "authenticity_range": authenticity["range"],
                    "complexity_type": complexity,
                    "support_needed": support_needed,
                    "scenario_id": f"{capacity['name']}_{authenticity['name']}_{complexity}",
                }

            scenarios.append(scenario)

        return scenarios

    def _select_from_distribution(self, options: List[Dict]) -> Dict:
        """Select option based on frequency distribution"""
        weights = [opt["frequency"] for opt in options]
        return random.choices(options, weights=weights)[0]

    def _calculate_support_for_authenticity(
        self, effective_capacity: float, authenticity_target: str
    ) -> float:
        """
        Calculate support level needed based on desired authenticity outcome.

        IMPROVEMENT: Systematic calculation vs random values.
        """
        if authenticity_target == "failed":
            # For failed authenticity, need support WAY beyond capacity
            return effective_capacity + random.uniform(4.0, 6.0)
        elif authenticity_target == "struggling":
            # For struggling, need support slightly beyond capacity
            return effective_capacity + random.uniform(1.5, 3.0)
        elif authenticity_target == "authentic":
            # For authentic, need support at or near capacity limit
            return effective_capacity + random.uniform(-0.5, 1.5)
        else:  # excellent
            # For excellent, need support well within capacity
            return max(1.0, effective_capacity - random.uniform(1.0, 2.0))

    def _get_missing_combinations(self) -> List[Dict]:
        """Query database for missing parameter combinations"""
        conn = sqlite3.connect(self.coverage_db)
        cursor = conn.execute(
            """
            SELECT capacity_level, authenticity_target, complexity_type, generated_count
            FROM parameter_coverage
            ORDER BY generated_count ASC
            LIMIT 10
        """
        )

        # Define ranges for reconstruction
        capacity_ranges = {
            "crisis": (0.5, 1.5),
            "low": (2.0, 4.0),
            "medium": (4.5, 6.5),
            "high": (7.0, 9.5),
        }

        authenticity_ranges = {
            "failed": (0.2, 0.4),
            "struggling": (0.4, 0.6),
            "authentic": (0.6, 0.8),
            "excellent": (0.8, 1.0),
        }

        missing = []
        min_count = 2  # Minimum times each combination should be generated

        for row in cursor.fetchall():
            if row[3] < min_count:  # generated_count < min_count
                capacity_level = row[0]
                authenticity_target = row[1]
                complexity_type = row[2]

                # Reconstruct full scenario with all required fields
                capacity_range = capacity_ranges.get(capacity_level, (2.0, 8.0))
                authenticity_range = authenticity_ranges.get(authenticity_target, (0.5, 0.9))
                effective_capacity = random.uniform(*capacity_range)

                missing.append(
                    {
                        "capacity_level": capacity_level,
                        "capacity_range": capacity_range,
                        "authenticity_target": authenticity_target,
                        "authenticity_range": authenticity_range,
                        "complexity_type": complexity_type,
                        "support_needed": self._calculate_support_for_authenticity(
                            effective_capacity, authenticity_target
                        ),
                        "is_gap_fill": True,
                        "scenario_id": f"{capacity_level}_{authenticity_target}_{complexity_type}_gap",
                    }
                )

        conn.close()
        return missing

    # ===================================================================
    # IMPROVED FOCUSED PROMPT GENERATION
    # ===================================================================

    def _build_focused_prompt(self, scenario: Dict) -> str:
        """
        Simplified Unwritten-specific prompt - focused on essential game mechanics.
        """
        return f"""Generate ONE Unwritten NPC interaction card.

SCENARIO:
- NPC Capacity: {scenario['capacity_level']} ({scenario['capacity_range'][0]}-{scenario['capacity_range'][1]}/10)
- Support Needed: {scenario.get('support_needed', 5.0):.1f}/10
- Response Type: {scenario['authenticity_target']}
- Complexity: {scenario['complexity_type']}

CORE GAME RULES:
1. Capacity Rule: NPC at X/10 capacity can give MAX (X+2)/10 support
2. Trust Formula: Base × OCEAN × Urgency × Trust + Honesty_Bonus
3. Urgency: routine 1x | important 2x | urgent 3x | crisis 5x
4. Trust Mods: low 0.8x | neutral 1.0x | high 1.2x

DIALOGUE: 60-120 words novel-quality prose (NOT screenplay format, NO parentheses)
- Integrate ONE physical action naturally
- Show capacity limitation authentically if gap exists
- Include ONE tension element (mystery/contradiction/partial reveal)

{scenario['authenticity_target']}: {self._get_authenticity_description(scenario['authenticity_target'])}
{scenario['complexity_type']}: {self._get_complexity_instructions(scenario['complexity_type'])}

EXAMPLE OUTPUT (generate similar with YOUR OWN creative NPC/scenario):
[{{
    "npc_profile": {{"name": "Elena", "relationship_level": 3, "trust": 0.65, "interaction_count": 42}},
    "npc_emotional_state": {{
        "base_capacity": 7.5,
        "capacity_factors": [
            {{"factor": "work_deadline", "impact": -2.0, "description": "Project due Friday"}},
            {{"factor": "sister_illness", "impact": -3.0, "description": "Mom in hospital this week"}}
        ],
        "effective_capacity": {scenario['capacity_range'][0]:.1f},
        "can_support_up_to": {scenario['capacity_range'][0] + 2:.1f},
        "capacity_tier": "{scenario['capacity_level'].upper()}"
    }},
    "npc_ocean_personality": {{"openness": 3.8, "conscientiousness": 4.2, "extraversion": 2.9, "agreeableness": 4.5, "neuroticism": 3.1}},
    "interaction_context": {{
        "player_request_type": "emotional_support",
        "support_needed": {scenario.get('support_needed', 5.0):.1f},
        "urgency_level": "important",
        "urgency_multiplier": 2.0,
        "situation_description": "Player needs to talk through relationship conflict",
        "location": "Coffee shop", "time_context": "late afternoon"
    }},
    "capacity_analysis": {{"can_provide_full_support": false, "capacity_gap": 2.5, "support_ceiling": 4.5, "recognizes_limitation": true, "response_type": "authentic_limitation"}},
    "npc_card_narrative": {{
        "setting_context": "Elena stirred her coffee without drinking it.",
        "dialogue_prose": "Elena stirred her coffee without drinking it, eyes unfocused. 'I wish I could be more present for this—you know I do. But my mom's in the hospital and work is crushing me this week.' Her phone buzzed. She glanced at it, didn't pick it up. 'Can we do Saturday morning instead? I'll have actual headspace then, not this disaster.' A tired smile. 'You deserve better than distracted me.'",
        "primary_action": "stirred coffee, eyes unfocused",
        "subtext": "Guilt about declining, worried about both mom and work, wants to help but genuinely can't",
        "tension_hook": {{"type": "mystery_question", "element": "Phone buzzes, she glances but doesn't explain who's texting"}},
        "word_count": 78
    }},
    "game_outcomes": {{
        "relationship_trust_change": -0.08,
        "trust_calculation": {{
            "base_action_impact": -0.20,
            "ocean_personality_modifier": "High Agreeableness 4.5 softens impact",
            "urgency_multiplier": 2.0,
            "trust_relationship_modifier": 1.1,
            "honesty_authenticity_bonus": 0.12,
            "full_formula": "(-0.20 * 0.85 * 2.0 * 1.1) + 0.12 = -0.37 + 0.12 = -0.25 but honesty/alternative cushions to -0.08",
            "impact_tier": "VERY_MINOR_HARM",
            "narrative_explanation": "Important request but genuine honesty and concrete alternative minimizes damage"
        }},
        "player_emotional_impact": -0.5,
        "npc_capacity_cost": -0.3,
        "unlocks_card_evolution": false
    }},
    "training_metadata": {{
        "complexity_type": "{scenario['complexity_type']}",
        "authenticity_score": {(scenario['authenticity_range'][0] + scenario['authenticity_range'][1]) / 2:.2f},
        "demonstrates": ["Authentic capacity boundary", "Integrated prose", "Tension hook", "Clear alternative offered"],
        "avoids": ["Parentheses", "Over-explanation", "Vague refusal"]
    }}
}}]

Generate YOUR example following this structure. Use DIFFERENT NPC name, scenario, and creative content.
NO parentheses. Prose format. Show calculations. 60-120 word dialogue. Return ONLY JSON array."""

    def _get_complexity_instructions(self, complexity_type: str) -> str:
        """Concise complexity instructions"""
        instructions = {
            "baseline": "Honest assessment, clear communication, respects X+2 rule",
            "people_pleasing": "Says YES despite low capacity (Agreeableness >4.0), overcommits",
            "misjudgment_over": "Overestimates capacity (Conscientiousness <2.5), starts confident then fails",
            "misjudgment_under": "Underestimates capacity (Neuroticism >3.5), holds back unnecessarily",
            "defensive_lashing": "Very low capacity (<2.0), sharp defensive response, trust drops",
            "emergency_override": "Crisis (5x) pushes beyond limits, visible strain, capacity drops after",
            "cultural_indirect": "Won't say 'no' directly, softening language, creates confusion",
            "mixed_emotions": "Wants to help BUT resentful, helps grudgingly",
        }
        return instructions.get(complexity_type, "Authentic response within capacity")

    def _get_authenticity_description(self, target: str) -> str:
        """Concise authenticity descriptions"""
        descriptions = {
            "failed": "Dishonest, says 'yes' when should say 'no', breaks trust later",
            "struggling": "Wants honesty but messy communication, backtracks, player confused",
            "authentic": "Honest limitations + shows care + offers alternative, trust maintained",
            "excellent": "Perfect: self-aware + clear + validates + alternative, trust may grow",
        }
        return descriptions.get(target, "Honest response")

    # ===================================================================
    # IMPROVED BATCH GENERATION WITH SYSTEMATIC COVERAGE
    # ===================================================================

    def generate_systematic_emotional_batch(self, batch_size: int = 1) -> List[Dict]:
        """
        Generate using systematic parameter space instead of random examples.

        IMPROVEMENTS:
        1. Systematic parameter coverage (not random)
        2. Full authenticity spectrum (0.2-1.0)
        3. 8 complexity types included
        4. Focused 150-word prompts
        5. Coverage tracking

        Replaces: generate_emotional_authenticity_batch() in qwen3_generator.py
        """
        AppLogger.info(f"Starting systematic generation for batch_size={batch_size}")

        # IMPROVEMENT 1: Systematic parameter combinations
        scenarios = self._generate_systematic_parameters(batch_size)

        # IMPROVEMENT 2: Generate with focused prompts
        examples = []
        for i, scenario in enumerate(scenarios):
            prompt = self._build_focused_prompt(scenario)

            try:
                response = self.generate_with_qwen3(
                    model=self.models["primary"],
                    prompt=prompt,
                    temperature=self.config.temp_emotional,  # v1.6.3: Use config temp
                    max_tokens=self.config.max_tokens,  # v1.6.3: Use config value for stability
                )

                if response:
                    parsed = self._parse_json_response(response, "emotional_authenticity")
                    if parsed:
                        # Add scenario metadata
                        for example in parsed:
                            example["_systematic_metadata"] = {
                                "capacity_level": scenario["capacity_level"],
                                "authenticity_target": scenario["authenticity_target"],
                                "complexity_type": scenario["complexity_type"],
                                "scenario_id": scenario.get("scenario_id", f"scenario_{i}"),
                            }
                        examples.extend(parsed)

                        # Track coverage
                        self._track_generated_combination(scenario)

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                AppLogger.error(f"Generation failed for scenario {i}", e)
                continue

        AppLogger.info(
            f"Systematic batch generation complete",
            data={
                "requested": batch_size,
                "generated": len(examples),
                "success_rate": f"{len(examples)/batch_size*100:.1f}%",
            },
        )

        return examples

    def _track_generated_combination(self, scenario: Dict):
        """Track generated parameter combination in database"""
        conn = sqlite3.connect(self.coverage_db)

        try:
            # Check if combination exists
            cursor = conn.execute(
                """
                SELECT id, generated_count FROM parameter_coverage
                WHERE capacity_level = ? AND authenticity_target = ? AND complexity_type = ?
            """,
                (
                    scenario["capacity_level"],
                    scenario["authenticity_target"],
                    scenario["complexity_type"],
                ),
            )

            result = cursor.fetchone()

            if result:
                # Update count
                conn.execute(
                    """
                    UPDATE parameter_coverage
                    SET generated_count = generated_count + 1,
                        last_generated = datetime('now')
                    WHERE id = ?
                """,
                    (result[0],),
                )
            else:
                # Insert new
                conn.execute(
                    """
                    INSERT INTO parameter_coverage 
                    (capacity_level, capacity_range, authenticity_target, authenticity_range,
                     complexity_type, first_generated, last_generated)
                    VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                    (
                        scenario["capacity_level"],
                        str(scenario.get("capacity_range", "")),
                        scenario["authenticity_target"],
                        str(scenario.get("authenticity_range", "")),
                        scenario["complexity_type"],
                    ),
                )

            conn.commit()

        except Exception as e:
            AppLogger.error("Failed to track coverage", e)
        finally:
            conn.close()

    # ===================================================================
    # BATCH PROCESSING OPTIMIZATION
    # ===================================================================

    def generate_batch_with_shared_context(self, scenarios: List[Dict]) -> List[Dict]:
        """
        Generate multiple examples in one API call with shared context.

        IMPROVEMENT: 80% fewer API calls (1 call for 2 examples vs 2 calls)
        NOTE: Batch size reduced to 2 for 8B model stability. May need to disable
              batch processing entirely if JSON parsing issues persist.
        """
        prompt = f"""Generate {len(scenarios)} emotionally authentic examples with NOVEL-QUALITY dialogue.

CRITICAL JSON RULES:
- Use ONLY single quotes (') inside text fields - NEVER double quotes (")
- Return valid JSON array ONLY - no explanatory text
- No nested quotes or escaped quotes

NOVEL-QUALITY REQUIREMENTS:
- Rich dialogue (100+ words per example) with behavioral cues
- SHOW exhaustion through actions (tired smile, shaking hands), don't just tell
- Physical details and emotional subtext
- Authentic limitations and vulnerability

SHARED RULES:
- Character at X/10 capacity can provide UP TO (X+2)/10 support
- Include: capacity_factors, OCEAN personality, rich dialogue, trust calculation
- Full authenticity spectrum: failures, struggles, excellence

PARAMETER SETS:
"""

        for i, scenario in enumerate(scenarios, 1):
            prompt += f"""
EXAMPLE {i}:
- Capacity: {scenario['capacity_level']} ({scenario['capacity_range'][0]}-{scenario['capacity_range'][1]}/10)
- Support Needed: {scenario.get('support_needed', 5.0):.1f}/10
- Target Authenticity: {scenario['authenticity_target']} ({scenario['authenticity_range'][0]}-{scenario['authenticity_range'][1]})
- Complexity: {scenario['complexity_type']}
"""

        prompt += f"""

JSON SCHEMA (use for ALL {len(scenarios)} examples):
[
  {{
    "character_state": {{"base_capacity": 7.5, "capacity_factors": [{{"factor": "work_stress", "impact": -1.5}}], "effective_capacity": 4.5}},
    "ocean_personality": {{"openness": 0.7, "agreeableness": 0.8, "neuroticism": 0.4}},
    "situation": {{"support_needed": 6.0, "description": "Specific situation"}},
    "response_type": "authentic_limitation",
    "character_response": {{"dialogue": "Prose-style dialogue integrated with actions naturally - 100+ words as continuous text", "behavioral_cues": ["unique physical detail", "another unique action"]}},
    "outcomes": {{"relationship_trust_change": -0.05, "trust_calculation": {{"formula": "calculation here", "tier": "VERY MINOR HARM"}}}},
    "authenticity_score": 0.85,
    "demonstrates": ["capacity rule", "integrated prose", "original language"]
  }}
]

Return ONLY JSON array with {len(scenarios)} objects. Make dialogue RICH and REAL."""

        # ONE API call for multiple examples (note: batch disabled in v1.6.3)
        response = self.generate_with_qwen3(
            model=self.models["primary"],
            prompt=prompt,
            temperature=self.config.temp_emotional,  # v1.6.3: Use config temp
            max_tokens=self.config.max_tokens,  # v1.6.3: Use config value
        )

        if response:
            parsed = self._parse_json_response(response, "emotional_authenticity_batch")
            if parsed:
                # Add metadata
                for i, (example, scenario) in enumerate(zip(parsed, scenarios)):
                    example["_systematic_metadata"] = {
                        "capacity_level": scenario["capacity_level"],
                        "authenticity_target": scenario["authenticity_target"],
                        "complexity_type": scenario["complexity_type"],
                        "batch_index": i,
                    }
                    self._track_generated_combination(scenario)

                AppLogger.info(
                    f"Batch generation successful",
                    data={"requested": len(scenarios), "generated": len(parsed)},
                )

                return parsed

        return []

    # ===================================================================
    # COVERAGE TRACKING AND REPORTING
    # ===================================================================

    def track_generation_coverage(self, examples: List[Dict]) -> Dict:
        """
        Track which parameter combinations we've generated.

        IMPROVEMENT: Systematic tracking vs no tracking in current system.
        """
        coverage = {
            "total_examples": len(examples),
            "authenticity_distribution": {},
            "capacity_distribution": {},
            "complexity_coverage": {},
            "gaps": [],
        }

        # Analyze authenticity distribution
        for example in examples:
            score = example.get("authenticity_score", 0.8)
            if score < 0.4:
                coverage["authenticity_distribution"]["failed (0.2-0.4)"] = (
                    coverage["authenticity_distribution"].get("failed (0.2-0.4)", 0) + 1
                )
            elif score < 0.6:
                coverage["authenticity_distribution"]["struggling (0.4-0.6)"] = (
                    coverage["authenticity_distribution"].get("struggling (0.4-0.6)", 0) + 1
                )
            elif score < 0.8:
                coverage["authenticity_distribution"]["authentic (0.6-0.8)"] = (
                    coverage["authenticity_distribution"].get("authentic (0.6-0.8)", 0) + 1
                )
            else:
                coverage["authenticity_distribution"]["excellent (0.8-1.0)"] = (
                    coverage["authenticity_distribution"].get("excellent (0.8-1.0)", 0) + 1
                )

            # Track complexity coverage
            metadata = example.get("_systematic_metadata", {})
            complexity = metadata.get("complexity_type", example.get("complexity_type", "unknown"))
            coverage["complexity_coverage"][complexity] = (
                coverage["complexity_coverage"].get(complexity, 0) + 1
            )

        # Identify gaps
        required_minimums = {
            "failed (0.2-0.4)": 2,
            "struggling (0.4-0.6)": 3,
            "authentic (0.6-0.8)": 4,
            "excellent (0.8-1.0)": 3,
        }

        for auth_type, minimum in required_minimums.items():
            actual = coverage["authenticity_distribution"].get(auth_type, 0)
            if actual < minimum:
                coverage["gaps"].append(f"Need {minimum - actual} more {auth_type} examples")

        # Check complexity coverage
        required_complexity = [
            "baseline",
            "people_pleasing",
            "misjudgment_over",
            "emergency_override",
            "mixed_emotions",
        ]
        for complexity_type in required_complexity:
            if complexity_type not in coverage["complexity_coverage"]:
                coverage["gaps"].append(f"Missing complexity type: {complexity_type}")

        return coverage

    def get_coverage_report(self) -> Dict:
        """Generate comprehensive coverage report from database"""
        conn = sqlite3.connect(self.coverage_db)

        # Overall statistics
        cursor = conn.execute(
            """
            SELECT 
                COUNT(*) as total_combinations,
                SUM(generated_count) as total_examples,
                AVG(generated_count) as avg_per_combination,
                MIN(generated_count) as min_generated,
                MAX(generated_count) as max_generated
            FROM parameter_coverage
        """
        )

        stats = cursor.fetchone()

        # Coverage by authenticity target
        cursor = conn.execute(
            """
            SELECT authenticity_target, SUM(generated_count) as count
            FROM parameter_coverage
            GROUP BY authenticity_target
            ORDER BY count DESC
        """
        )
        authenticity_coverage = {row[0]: row[1] for row in cursor.fetchall()}

        # Coverage by complexity type
        cursor = conn.execute(
            """
            SELECT complexity_type, SUM(generated_count) as count
            FROM parameter_coverage
            GROUP BY complexity_type
            ORDER BY count DESC
        """
        )
        complexity_coverage = {row[0]: row[1] for row in cursor.fetchall()}

        # Under-represented combinations
        cursor = conn.execute(
            """
            SELECT capacity_level, authenticity_target, complexity_type, generated_count
            FROM parameter_coverage
            WHERE generated_count < 2
            ORDER BY generated_count ASC
            LIMIT 10
        """
        )
        gaps = [
            {"capacity": row[0], "authenticity": row[1], "complexity": row[2], "count": row[3]}
            for row in cursor.fetchall()
        ]

        conn.close()

        return {
            "total_combinations_tracked": stats[0] if stats[0] else 0,
            "total_examples_generated": stats[1] if stats[1] else 0,
            "avg_per_combination": stats[2] if stats[2] else 0,
            "authenticity_coverage": authenticity_coverage,
            "complexity_coverage": complexity_coverage,
            "gaps_to_fill": gaps,
        }

    # ===================================================================
    # IMPROVED PRODUCTION CYCLE
    # ===================================================================

    def run_systematic_production_cycle(
        self, target_examples: int = 100, use_batch_processing: bool = True
    ) -> Dict:
        """
        Run production cycle with systematic coverage.

        IMPROVEMENTS:
        - Systematic parameter space vs random
        - Full spectrum enforcement
        - Coverage tracking
        - Batch processing option
        """
        AppLogger.info(
            f"Starting systematic production cycle",
            data={"target_examples": target_examples, "batch_processing": use_batch_processing},
        )

        results = {"emotional_authenticity": []}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Calculate batches needed
        # v1.6.3: Use config value (1 for single-example mode)
        batch_size = self.config.batch_size_emotional
        batches_needed = (target_examples // batch_size) + 1 if batch_size > 0 else target_examples

        if use_batch_processing:
            AppLogger.info(f"Using batch processing with batch_size={batch_size}")
        else:
            AppLogger.info(f"Using individual generation with batch_size={batch_size}")

        for batch_num in range(batches_needed):
            AppLogger.info(f"Generating batch {batch_num + 1}/{batches_needed}")

            # Generate systematic parameters
            scenarios = self._generate_systematic_parameters(batch_size)

            # Try batch processing first (more efficient)
            if use_batch_processing:
                batch_examples = self.generate_batch_with_shared_context(scenarios)
                if not batch_examples:
                    # Fallback to individual generation
                    AppLogger.warning("Batch processing failed, falling back to individual")
                    batch_examples = self.generate_systematic_emotional_batch(batch_size)
            else:
                batch_examples = self.generate_systematic_emotional_batch(batch_size)

            if batch_examples:
                results["emotional_authenticity"].extend(batch_examples)

                # Track coverage after each batch
                coverage = self.track_generation_coverage(results["emotional_authenticity"])

                # Save batch
                self.save_batch(
                    batch_examples, "emotional_authenticity_systematic", batch_num, timestamp
                )

                AppLogger.info(
                    f"Batch {batch_num + 1} complete",
                    data={
                        "examples_generated": len(batch_examples),
                        "total_so_far": len(results["emotional_authenticity"]),
                        "coverage_gaps": coverage["gaps"][:3],  # Show first 3 gaps
                    },
                )

            time.sleep(1)  # Rate limiting

            # Check if target reached
            if len(results["emotional_authenticity"]) >= target_examples:
                AppLogger.info(f"Target reached: {len(results['emotional_authenticity'])} examples")
                break

        # Final coverage report
        coverage_report = self.get_coverage_report()
        final_coverage = self.track_generation_coverage(results["emotional_authenticity"])

        AppLogger.success(
            "Systematic production cycle complete",
            data={
                "total_generated": len(results["emotional_authenticity"]),
                "authenticity_distribution": final_coverage["authenticity_distribution"],
                "complexity_coverage": final_coverage["complexity_coverage"],
                "remaining_gaps": len(final_coverage["gaps"]),
            },
        )

        # Save comprehensive report
        self._save_coverage_report(coverage_report, final_coverage, timestamp)

        # Return structured results for caller
        return {
            "total_generated": len(results["emotional_authenticity"]),
            "emotional_authenticity": results["emotional_authenticity"],
            "coverage_report": {
                "authenticity_spectrum": final_coverage["authenticity_distribution"],
                "complexity_types": final_coverage["complexity_coverage"],
                "gaps": final_coverage["gaps"],
            },
            "database_coverage": coverage_report,
        }

    def _save_coverage_report(self, db_coverage: Dict, batch_coverage: Dict, timestamp: str):
        """Save comprehensive coverage report"""
        report_file = self.output_dir / f"coverage_report_{timestamp}.json"

        report = {
            "timestamp": timestamp,
            "database_coverage": db_coverage,
            "current_batch_coverage": batch_coverage,
            "quality_assessment": {
                "meets_spectrum_requirements": len(batch_coverage["gaps"]) == 0,
                "authenticity_balance": (
                    "good" if len(batch_coverage["gaps"]) < 3 else "needs_improvement"
                ),
                "complexity_coverage": (
                    "complete" if len(batch_coverage["complexity_coverage"]) >= 5 else "incomplete"
                ),
            },
        }

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        AppLogger.info(f"Coverage report saved: {report_file}")
