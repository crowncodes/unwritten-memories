"""
Multi-Step Training Data Generation Pipeline

Instead of generating everything in one massive prompt, break into focused steps:
1. NPC Primitives (OCEAN, capacity, relationship)
2. Situational Context (urgency, support_needed, stressors)
3. Tension/Memory Elements (hooks, backstory, subtext)
4. Dialogue Generation (uses all above)
5. Outcome Calculation (trust change, capacity cost)

Benefits:
- Faster generation (smaller prompts)
- Modular (swap components to create variations)
- Reusable (1 base scenario → many dialogue variations)
- Testable (validate each step independently)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import random

from unwritten.training.qwen3_generator import Qwen3DataGenerator
from unwritten.training.config import EnhancedTrainingConfig
from unwritten.utils.logger import AppLogger


@dataclass
class NPCPrimitives:
    """Step 1: Core NPC attributes"""

    name: str
    ocean: Dict[str, float]  # 0.0-5.0 scale
    base_capacity: float
    relationship_level: int  # 0-5
    trust: float  # 0.0-1.0
    interaction_count: int


@dataclass
class SituationalContext:
    """Step 2: Current situation state"""

    capacity_factors: List[Dict]  # [{factor, impact, description}]
    effective_capacity: float
    support_needed: float
    urgency_level: str  # routine/important/urgent/crisis
    urgency_multiplier: float
    situation_description: str
    location: str
    time_context: str


@dataclass
class TensionMemoryElements:
    """Step 3: Narrative hooks and emotional context"""

    tension_hook: Dict[str, str]  # {type, element}
    relevant_memories: List[str]  # Past interactions that inform this moment
    subtext: str  # What NPC is feeling but not saying
    internal_conflict: Optional[str]  # If applicable


@dataclass
class DialogueOutput:
    """Step 4: Generated dialogue"""

    setting_context: str
    dialogue_prose: str  # 60-120 words
    primary_action: str
    word_count: int


@dataclass
class GameOutcomes:
    """Step 5: Calculated game impacts"""

    trust_change: float
    trust_calculation: Dict
    player_emotional_impact: float
    npc_capacity_cost: float
    unlocks_card_evolution: bool


class MultiStepPipeline(Qwen3DataGenerator):
    """
    Multi-step training data generation pipeline.

    Generates Unwritten NPC interaction data in focused steps:
    primitives → context → tension → dialogue → outcomes
    """

    def __init__(self, config: EnhancedTrainingConfig):
        super().__init__(config)
        self.config = config

    # ===================================================================
    # STEP 1: NPC PRIMITIVES
    # ===================================================================

    def generate_npc_primitives(self, complexity_type: str = "baseline") -> NPCPrimitives:
        """
        Generate core NPC attributes.

        Fast, focused prompt (< 30 seconds).
        Returns: OCEAN traits, base capacity, relationship state.
        """
        prompt = f"""Generate ONE Unwritten NPC profile for complexity: {complexity_type}

{{
    "name": "Jordan",
    "ocean": {{"openness": 3.2, "conscientiousness": 4.1, "extraversion": 2.8, "agreeableness": 4.5, "neuroticism": 2.9}},
    "base_capacity": 7.5,
    "relationship_level": 3,
    "trust": 0.65,
    "interaction_count": 42
}}

Generate YOUR OWN with different name and traits.
{complexity_type} traits: {"High Agreeableness >4.0" if complexity_type == "people_pleasing" else "Balanced"}
Return ONLY JSON."""

        response = self.generate_with_qwen3(
            model=self.models["primary"],
            prompt=prompt,
            temperature=0.7,  # Lower for consistent primitives
            max_tokens=3000,  # HIGH to avoid Ollama bug
        )

        data = self._parse_json_response(response, "npc_primitives")[0]

        return NPCPrimitives(
            name=data["name"],
            ocean=data["ocean"],
            base_capacity=data["base_capacity"],
            relationship_level=data["relationship_level"],
            trust=data["trust"],
            interaction_count=data["interaction_count"],
        )

    # ===================================================================
    # STEP 2: SITUATIONAL CONTEXT
    # ===================================================================

    def generate_situational_context(
        self,
        primitives: NPCPrimitives,
        target_capacity_level: str,
        target_support_needed: float,
    ) -> SituationalContext:
        """
        Generate current situation state.

        Fast, focused prompt (< 30 seconds).
        Returns: capacity factors, urgency, support needs.
        """
        capacity_ranges = {
            "crisis": (1.5, 2.5),
            "low": (3.0, 4.5),
            "medium": (5.0, 6.5),
            "high": (7.0, 9.0),
        }
        target_capacity = random.uniform(*capacity_ranges[target_capacity_level])

        prompt = f"""Generate capacity context for NPC "{primitives.name}".
Base capacity: {primitives.base_capacity:.1f} → Target: {target_capacity:.1f}

Return JSON in this format:
{{
    "effective_capacity": {target_capacity:.1f},
    "support_needed": {target_support_needed:.1f},
    "urgency_level": "important",
    "urgency_multiplier": 2.0,
    "situation_description": "What player is asking for",
    "location": "Where this happens",
    "time_context": "afternoon"
}}

Return ONLY the JSON object above with your own values."""

        response = self.generate_with_qwen3(
            model=self.models["primary"],
            prompt=prompt,
            temperature=0.5,  # Very low for reliable JSON completion
            max_tokens=4000,  # HIGH to avoid Ollama bug (returns empty if hitting limit)
        )

        parsed_data = self._parse_json_response(response, "situational_context")
        data = parsed_data[0]

        return SituationalContext(
            capacity_factors=[],  # Simplified - don't generate these
            effective_capacity=data["effective_capacity"],
            support_needed=data["support_needed"],
            urgency_level=data["urgency_level"],
            urgency_multiplier=data["urgency_multiplier"],
            situation_description=data["situation_description"],
            location=data["location"],
            time_context=data["time_context"],
        )

    # ===================================================================
    # STEP 3: TENSION/MEMORY ELEMENTS
    # ===================================================================

    def generate_tension_memory_elements(
        self, primitives: NPCPrimitives, context: SituationalContext
    ) -> TensionMemoryElements:
        """
        Generate narrative hooks and emotional subtext.

        Fast, focused prompt (< 30 seconds).
        Returns: tension hooks, relevant memories, subtext.
        """
        prompt = f"""Generate tension/subtext for NPC "{primitives.name}".
Capacity: {context.effective_capacity:.1f}/10, Support needed: {context.support_needed:.1f}/10
Situation: {context.situation_description}

Return JSON:
{{
    "subtext": "What NPC feels but doesn't say",
    "tension_type": "mystery",
    "tension_element": "Brief detail creating intrigue"
}}

Return ONLY the JSON object above with your own values."""

        response = self.generate_with_qwen3(
            model=self.models["primary"],
            prompt=prompt,
            temperature=0.85,  # Higher for creative tension
            max_tokens=3000,  # HIGH to avoid Ollama bug
        )

        parsed_data = self._parse_json_response(response, "tension_memory")
        data = parsed_data[0]

        return TensionMemoryElements(
            tension_hook={"type": data.get("tension_type", "mystery"), "element": data.get("tension_element", "")},
            relevant_memories=[],  # Simplified - don't generate these
            subtext=data["subtext"],
            internal_conflict=None,  # Simplified
        )

    # ===================================================================
    # STEP 4: DIALOGUE GENERATION
    # ===================================================================

    def generate_dialogue(
        self,
        primitives: NPCPrimitives,
        context: SituationalContext,
        tension: TensionMemoryElements,
        complexity_type: str,
        authenticity_target: str,
    ) -> DialogueOutput:
        """
        Generate novel-quality dialogue prose.

        Uses ALL previous context. Focused on dialogue only (60-120 words).
        Slightly longer (< 60 seconds) but highly targeted.
        """
        capacity_gap = context.support_needed - context.effective_capacity
        can_provide_full_support = capacity_gap <= 2.0

        prompt = f"""Generate 60-120 word dialogue for NPC "{primitives.name}".

CONTEXT:
- NPC Capacity: {context.effective_capacity:.1f}/10 (can provide up to {context.effective_capacity + 2:.1f}/10)
- Support Needed: {context.support_needed:.1f}/10
- Gap: {capacity_gap:.1f} (can provide full support: {can_provide_full_support})
- Urgency: {context.urgency_level} ({context.urgency_multiplier}x)
- Situation: {context.situation_description}
- Location: {context.location}, {context.time_context}

NPC PERSONALITY (OCEAN):
- Openness: {primitives.ocean['openness']:.1f} | Conscientiousness: {primitives.ocean['conscientiousness']:.1f}
- Extraversion: {primitives.ocean['extraversion']:.1f} | Agreeableness: {primitives.ocean['agreeableness']:.1f}
- Neuroticism: {primitives.ocean['neuroticism']:.1f}

EMOTIONAL CONTEXT:
- Subtext: {tension.subtext}
- Tension Hook: {tension.tension_hook['type']} - {tension.tension_hook['element']}
- Internal Conflict: {tension.internal_conflict or 'None'}

REQUIREMENTS:
- Complexity: {complexity_type} (e.g., people_pleasing = says yes when should say no)
- Authenticity: {authenticity_target} (honest about limitations vs dishonest)
- Format: Novel-quality prose, NO parentheses, integrate ONE physical action
- Must include tension hook: {tension.tension_hook['element']}

Return JSON:
{{
    "setting_context": "[One sentence scene-setting]",
    "dialogue_prose": "[60-120 words continuous prose with integrated actions]",
    "primary_action": "[One key physical behavior]",
    "word_count": [actual count]
}}

EXAMPLE FORMAT (different content):
"Elena stirred her coffee without drinking it, eyes unfocused. 'I wish I could be more present for this—you know I do. But my mom's in the hospital and work is crushing me this week.' Her phone buzzed. She glanced at it, didn't pick it up. 'Can we do Saturday morning instead? I'll have actual headspace then, not this disaster.' A tired smile. 'You deserve better than distracted me.'"

Return ONLY JSON."""

        response = self.generate_with_qwen3(
            model=self.models["primary"],
            prompt=prompt,
            temperature=self.config.temp_emotional,
            max_tokens=self.config.max_tokens,  # Use config value (4000) - avoid Ollama bug
        )

        data = self._parse_json_response(response, "dialogue")[0]

        return DialogueOutput(
            setting_context=data["setting_context"],
            dialogue_prose=data["dialogue_prose"],
            primary_action=data["primary_action"],
            word_count=data["word_count"],
        )

    # ===================================================================
    # STEP 5: CALCULATE OUTCOMES
    # ===================================================================

    def calculate_outcomes(
        self,
        primitives: NPCPrimitives,
        context: SituationalContext,
        dialogue: DialogueOutput,
        complexity_type: str,
        authenticity_target: str,
    ) -> GameOutcomes:
        """
        Calculate game impacts using Unwritten formulas.

        Deterministic calculation (no LLM needed).
        Fast (< 1 second).
        """
        # Base action impact
        capacity_gap = context.support_needed - context.effective_capacity

        if capacity_gap > 2.0:
            # NPC can't provide full support
            if authenticity_target in ["authentic", "excellent"]:
                base_impact = -0.15  # Honest decline, minimal harm
            elif authenticity_target == "struggling":
                base_impact = -0.25  # Messy communication
            else:  # failed
                base_impact = -0.40  # Dishonest response
        else:
            # NPC can provide support
            base_impact = 0.20 if authenticity_target == "excellent" else 0.10

        # OCEAN personality modifier
        if complexity_type == "people_pleasing":
            ocean_mod = 0.85  # High Agreeableness softens harm
        elif complexity_type == "defensive_lashing":
            ocean_mod = 1.3  # High Neuroticism amplifies harm
        else:
            ocean_mod = 1.0

        # Trust relationship modifier
        if primitives.trust < 0.3:
            trust_mod = 0.8
        elif primitives.trust > 0.7:
            trust_mod = 1.2
        else:
            trust_mod = 1.0

        # Honesty bonus
        honesty_bonus = 0.12 if authenticity_target in ["authentic", "excellent"] else 0.0

        # Full calculation
        trust_change = (
            base_impact * ocean_mod * context.urgency_multiplier * trust_mod
        ) + honesty_bonus

        # Capacity cost
        if capacity_gap > 2.0:
            capacity_cost = -0.3  # Emotional labor of declining
        else:
            capacity_cost = -context.support_needed * 0.2  # Cost of helping

        # Card evolution unlock
        unlocks_evolution = abs(trust_change) > 0.5 or context.urgency_level == "crisis"

        trust_calculation = {
            "base_action_impact": base_impact,
            "ocean_personality_modifier": f"{ocean_mod} ({complexity_type})",
            "urgency_multiplier": context.urgency_multiplier,
            "trust_relationship_modifier": trust_mod,
            "honesty_authenticity_bonus": honesty_bonus,
            "full_formula": f"({base_impact} * {ocean_mod} * {context.urgency_multiplier} * {trust_mod}) + {honesty_bonus} = {trust_change:.2f}",
            "impact_tier": self._get_impact_tier(trust_change),
        }

        return GameOutcomes(
            trust_change=round(trust_change, 2),
            trust_calculation=trust_calculation,
            player_emotional_impact=round(trust_change * 2, 1),
            npc_capacity_cost=round(capacity_cost, 1),
            unlocks_card_evolution=unlocks_evolution,
        )

    def _get_impact_tier(self, trust_change: float) -> str:
        """Categorize trust change magnitude"""
        abs_change = abs(trust_change)
        if abs_change < 0.1:
            return "VERY_MINOR"
        elif abs_change < 0.3:
            return "MINOR"
        elif abs_change < 0.6:
            return "MODERATE"
        else:
            return "MAJOR"

    # ===================================================================
    # FULL PIPELINE
    # ===================================================================

    def generate_complete_interaction(
        self,
        complexity_type: str = "baseline",
        authenticity_target: str = "authentic",
        capacity_level: str = "medium",
        support_needed: float = 5.0,
    ) -> Dict:
        """
        Run complete multi-step pipeline.

        Steps:
        1. Generate NPC primitives (30 sec)
        2. Generate situational context (30 sec)
        3. Generate tension/memory elements (30 sec)
        4. Generate dialogue (60 sec)
        5. Calculate outcomes (< 1 sec)

        Total: ~2-3 minutes (vs 7+ minutes monolithic)

        Returns: Complete Unwritten NPC interaction card data
        """
        AppLogger.info(
            f"Starting multi-step pipeline: {complexity_type}, {authenticity_target}, {capacity_level}"
        )

        # Step 1: Primitives
        primitives = self.generate_npc_primitives(complexity_type)
        AppLogger.info(f"Generated NPC: {primitives.name}")

        # Step 2: Context
        context = self.generate_situational_context(primitives, capacity_level, support_needed)
        AppLogger.info(
            f"Generated context: capacity={context.effective_capacity:.1f}, urgency={context.urgency_level}"
        )

        # Step 3: Tension/Memory
        tension = self.generate_tension_memory_elements(primitives, context)
        AppLogger.info(f"Generated tension: {tension.tension_hook['type']}")

        # Step 4: Dialogue
        dialogue = self.generate_dialogue(
            primitives, context, tension, complexity_type, authenticity_target
        )
        AppLogger.info(f"Generated dialogue: {dialogue.word_count} words")

        # Step 5: Outcomes
        outcomes = self.calculate_outcomes(
            primitives, context, dialogue, complexity_type, authenticity_target
        )
        AppLogger.info(f"Calculated outcomes: trust_change={outcomes.trust_change:.2f}")

        # Assemble complete interaction
        return {
            "npc_profile": {
                "name": primitives.name,
                "relationship_level": primitives.relationship_level,
                "trust": primitives.trust,
                "interaction_count": primitives.interaction_count,
            },
            "npc_emotional_state": {
                "base_capacity": primitives.base_capacity,
                "capacity_factors": context.capacity_factors,
                "effective_capacity": context.effective_capacity,
                "can_support_up_to": context.effective_capacity + 2.0,
                "capacity_tier": capacity_level.upper(),
            },
            "npc_ocean_personality": primitives.ocean,
            "interaction_context": {
                "player_request_type": "emotional_support",
                "support_needed": context.support_needed,
                "urgency_level": context.urgency_level,
                "urgency_multiplier": context.urgency_multiplier,
                "situation_description": context.situation_description,
                "location": context.location,
                "time_context": context.time_context,
            },
            "tension_memory": {
                "tension_hook": tension.tension_hook,
                "relevant_memories": tension.relevant_memories,
                "subtext": tension.subtext,
                "internal_conflict": tension.internal_conflict,
            },
            "npc_card_narrative": {
                "setting_context": dialogue.setting_context,
                "dialogue_prose": dialogue.dialogue_prose,
                "primary_action": dialogue.primary_action,
                "word_count": dialogue.word_count,
            },
            "game_outcomes": {
                "relationship_trust_change": outcomes.trust_change,
                "trust_calculation": outcomes.trust_calculation,
                "player_emotional_impact": outcomes.player_emotional_impact,
                "npc_capacity_cost": outcomes.npc_capacity_cost,
                "unlocks_card_evolution": outcomes.unlocks_card_evolution,
            },
            "training_metadata": {
                "complexity_type": complexity_type,
                "authenticity_score": self._authenticity_to_score(authenticity_target),
                "generation_method": "multi_step_pipeline",
            },
        }

    def _authenticity_to_score(self, target: str) -> float:
        """Convert authenticity target to numeric score"""
        scores = {"failed": 0.25, "struggling": 0.55, "authentic": 0.85, "excellent": 0.95}
        return scores.get(target, 0.85)

    # ===================================================================
    # VARIATION GENERATION
    # ===================================================================

    def generate_dialogue_variations(
        self,
        primitives: NPCPrimitives,
        context: SituationalContext,
        base_tension: TensionMemoryElements,
        complexity_type: str,
        authenticity_target: str,
        num_variations: int = 5,
    ) -> List[DialogueOutput]:
        """
        Generate multiple dialogue variations for the same base scenario.

        Use case: 1 base scenario → 5-10 different dialogues
        by varying tension hooks or emotional context.

        Much faster than regenerating everything from scratch.
        """
        variations = []

        for i in range(num_variations):
            # Optionally regenerate tension for variation
            if i > 0:  # Use base tension for first, generate new for rest
                tension = self.generate_tension_memory_elements(primitives, context)
            else:
                tension = base_tension

            dialogue = self.generate_dialogue(
                primitives, context, tension, complexity_type, authenticity_target
            )

            variations.append(dialogue)
            AppLogger.info(f"Generated variation {i+1}/{num_variations}")

        return variations
