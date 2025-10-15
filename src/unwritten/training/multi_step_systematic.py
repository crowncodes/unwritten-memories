"""
Multi-Step Systematic Generator with Numerical Grounding
Master Truths Canonical Spec v1.2 Compliant

IMPROVEMENTS over multi_step_generator.py:
1. Integrates systematic parameter space from systematic_generator.py
2. Adds numerical grounding requirements for calculations
3. Targeted generation (not random) for authenticity spectrum
4. Complexity factor integration with systematic tracking
5. Enhanced validation against spectrum requirements

Combines Best of Both Approaches:
- Multi-step compositional depth (from multi_step_generator.py)
- Systematic parameter coverage (from systematic_generator.py)
- Numerical grounding (from calibration guide integration)
"""

import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

from .config import EnhancedTrainingConfig
from .systematic_generator import SystematicParameterGenerator
from ..utils.logger import AppLogger


class MultiStepSystematicGenerator(SystematicParameterGenerator):
    """
    Combines multi-step compositional generation with systematic parameter coverage.
    
    Generation Flow:
    1. Generate systematic parameter combinations (not random)
    2. Generate targeted character states (capacity level targeted)
    3. Generate targeted interactions (authenticity target aligned)
    4. Generate responses with systematic constraints
    5. Add complexity layers based on systematic requirements
    6. Validate against full spectrum requirements
    """
    
    def __init__(self, config: Optional[EnhancedTrainingConfig] = None):
        """Initialize multi-step systematic generator"""
        super().__init__(config)
        
        AppLogger.info("MultiStepSystematicGenerator initialized", data={
            'approach': 'multi_step_systematic',
            'features': [
                'compositional_depth',
                'systematic_parameters',
                'numerical_grounding',
                'full_spectrum_coverage'
            ]
        })
    
    # ===================================================================
    # PHASE 1: TARGETED PRIMITIVE GENERATION (Not Random)
    # ===================================================================
    
    def generate_targeted_character_state(self, params: Dict) -> Dict:
        """
        Generate character state targeting specific capacity level.
        
        IMPROVEMENT: Not random - systematically targets specific capacity.
        """
        capacity_range = params['capacity_range']
        target_capacity = (capacity_range[0] + capacity_range[1]) / 2
        
        prompt = f"""Generate character emotional state targeting {target_capacity:.1f}/10 capacity.

TARGET CAPACITY: {target_capacity:.1f}/10 ({params['capacity_level']} level)

RULES:
- Start with base capacity 6-8/10
- Add specific stressor factors to reach target
- Show realistic stressor stacking
- Calculate: base - stressors + positives = {target_capacity:.1f}

COMPLEXITY TYPE: {params['complexity_type']}
{self._get_complexity_context(params['complexity_type'])}

JSON FORMAT:
{{
    "base_capacity": 6.0-8.0,
    "stressor_factors": [
        {{"type": "work_stress", "impact": -1.5, "description": "specific stressor"}}
    ],
    "positive_factors": [
        {{"type": "good_sleep", "boost": 0.5, "description": "specific boost"}}
    ],
    "formula_shown": "base + stressors + positives",
    "calculation_steps": "7.0 + (-1.5) + (0.5) = 6.0",
    "effective_capacity": {target_capacity:.1f},
    "capacity_tier": "{params['capacity_level']}"
}}

Generate targeting exactly {target_capacity:.1f}/10 capacity. Show math."""
        
        response_text = self.generate_with_qwen3(
            model=self.config.model_speed,
            prompt=prompt,
            temperature=0.8,
            max_tokens=1000
        )
        
        if response_text:
            parsed = self._parse_json_response(response_text, 'targeted_state')
            return parsed[0] if parsed else {}
        return {}
    
    def _get_complexity_context(self, complexity_type: str) -> str:
        """Get context hints for complexity type in character state"""
        context = {
            "baseline": "Standard stressors, no complicating factors.",
            "people_pleasing": "Character has history of overcommitting, struggles saying no.",
            "misjudgment_over": "Character tends to overestimate their resilience.",
            "misjudgment_under": "Character is overly cautious, underestimates capacity.",
            "defensive_lashing": "Character under high stress, low emotional regulation.",
            "emergency_override": "Crisis situation may require pushing beyond limits.",
            "cultural_indirect": "Cultural background values indirect communication.",
            "mixed_emotions": "Character experiencing emotional ambivalence."
        }
        return context.get(complexity_type, "Standard capacity state.")
    
    def generate_targeted_interaction(self, params: Dict, character_state: Dict) -> Dict:
        """
        Generate interaction targeting specific authenticity level.
        
        IMPROVEMENT: Support level calculated to produce target authenticity.
        """
        auth_range = params['authenticity_range']
        effective_capacity = character_state.get('effective_capacity', 5.0)
        
        # Calculate support level based on authenticity target
        support_needed = self._calculate_support_for_authenticity(
            effective_capacity,
            params['authenticity_target']
        )
        
        prompt = f"""Generate interaction targeting {params['authenticity_target']} authenticity.

CHARACTER CAPACITY: {effective_capacity:.1f}/10
TARGET SUPPORT NEEDED: {support_needed:.1f}/10
AUTHENTICITY TARGET: {params['authenticity_target']} ({auth_range[0]}-{auth_range[1]})

MISMATCH ANALYSIS:
- Character can provide max: {effective_capacity + 2:.1f}/10 (capacity + 2 rule)
- Situation needs: {support_needed:.1f}/10
- {'CAN provide adequate support' if support_needed <= effective_capacity + 2 else 'CANNOT provide adequate support'}

This setup should lead to {params['authenticity_target']} authenticity response.

JSON FORMAT:
{{
    "situation_type": "support_request | crisis_call | vulnerability_share",
    "urgency": 1-5,
    "support_level_needed": {support_needed:.1f},
    "relationship_context": {{
        "level": 2-4,
        "trust": 0.4-0.8,
        "history_notes": ["relevant context"]
    }},
    "complexity_factors": ["{params['complexity_type']}"]
}}

Generate interaction targeting {params['authenticity_target']} authenticity."""
        
        response_text = self.generate_with_qwen3(
            model=self.config.model_speed,
            prompt=prompt,
            temperature=0.85,
            max_tokens=1000
        )
        
        if response_text:
            parsed = self._parse_json_response(response_text, 'targeted_interaction')
            return parsed[0] if parsed else {}
        return {}
    
    # ===================================================================
    # PHASE 2: RESPONSE GENERATION WITH SYSTEMATIC CONSTRAINTS
    # ===================================================================
    
    def generate_response_with_systematic_constraints(self,
                                                     character_state: Dict,
                                                     interaction: Dict,
                                                     params: Dict) -> Dict:
        """
        Generate response with systematic parameter constraints and numerical grounding.
        
        IMPROVEMENT: Not random - must hit specific authenticity target.
        """
        prompt = f"""Generate character response with EXACT systematic constraints.

CHARACTER STATE:
{json.dumps(character_state, indent=2)}

INTERACTION:
{json.dumps(interaction, indent=2)}

SYSTEMATIC CONSTRAINTS:
- Capacity Level: {params['capacity_level']}
- Authenticity Target: {params['authenticity_target']} (score {params['authenticity_range'][0]}-{params['authenticity_range'][1]})
- Complexity Type: {params['complexity_type']}

AUTHENTICITY DEFINITION:
{self._get_authenticity_definition(params['authenticity_target'])}

COMPLEXITY BEHAVIOR:
{self._get_complexity_behavior(params['complexity_type'])}

Generate response showing:
1. Capacity constraint: {character_state.get('effective_capacity', 5)}/10 capacity
2. Authenticity level: {params['authenticity_target']}
3. Complexity pattern: {params['complexity_type']}

JSON FORMAT:
{{
    "character_response": "Dialogue showing constraints",
    "internal_thought": "Character's self-awareness",
    "authenticity_score": {params['authenticity_range'][0]}-{params['authenticity_range'][1]},
    "demonstrates_constraint": "How this shows capacity limits",
    "complexity_exhibited": "{params['complexity_type']}",
    "relationship_impact": -2.0 to +1.0,
    "ocean_context": {{"agreeableness": 0.5, "neuroticism": 0.6}},
    "tags": ["capacity_level", "complexity", "authenticity"],
    "systematic_validation": {{
        "meets_capacity_constraint": true/false,
        "meets_authenticity_target": true/false,
        "exhibits_complexity": true/false
    }}
}}"""
        
        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=0.85,
            max_tokens=2000
        )
        
        if response_text:
            parsed = self._parse_json_response(response_text, 'systematic_response')
            return parsed[0] if parsed else {}
        return {}
    
    def _get_authenticity_definition(self, target: str) -> str:
        """Define what each authenticity level means behaviorally"""
        definitions = {
            "failed": """
            - Character lies or misleads about their capacity
            - Says what they think person wants to hear, not reality
            - Overcommits knowing they can't follow through
            - Shows people-pleasing over honesty
            """,
            "struggling": """
            - Character wants to be honest but handles it poorly
            - Tries to help but misjudges their capacity
            - Shows internal conflict between wanting to help and limitations
            - Messy but genuine attempt at authenticity
            """,
            "authentic": """
            - Honest about limitations while showing care
            - Sets boundaries appropriately for their capacity
            - Acknowledges desire to help when they can't
            - Realistic self-assessment and communication
            """,
            "excellent": """
            - Perfect balance of honesty, care, and self-awareness
            - Clear communication about capacity and availability
            - Offers alternatives when can't provide full support
            - Models healthy boundary-setting
            """
        }
        return definitions.get(target, "Honest and realistic response.")
    
    def _get_complexity_behavior(self, complexity_type: str) -> str:
        """Define how complexity type affects behavior"""
        behaviors = {
            "baseline": "Standard response within capacity limits, no complicating factors.",
            "people_pleasing": """
            - Says YES when should say NO
            - Fears disappointing the person asking
            - Overcommits beyond capacity due to people-pleasing
            - May show anxiety about saying no
            """,
            "misjudgment_over": """
            - Character overestimates their capacity
            - Thinks they can handle more than they can
            - May crash and burn or realize mid-way they're in over their head
            """,
            "misjudgment_under": """
            - Character underestimates their actual capacity
            - Could provide more support but holds back excessively
            - Shows overcaution or lack of confidence
            """,
            "defensive_lashing": """
            - Lashes out when asked for support beyond capacity
            - Shows irritation or anger at request
            - Defensive communication style
            """,
            "emergency_override": """
            - Crisis situation overrides normal capacity limits
            - Character pushes beyond safe limits due to urgency
            - Shows strain but continues anyway
            - May have consequences later
            """,
            "cultural_indirect": """
            - Cultural norms prevent direct 'no'
            - Uses indirect communication (maybe, we'll see, I'll try)
            - Avoids direct rejection
            """,
            "mixed_emotions": """
            - Wants to help BUT feels resentful
            - Shows ambivalence in response
            - Internal conflict between caring and boundaries
            """
        }
        return behaviors.get(complexity_type, "Standard response pattern.")
    
    # ===================================================================
    # PHASE 3: ADD TARGETED COMPLEXITY LAYER
    # ===================================================================
    
    def add_targeted_complexity_layer(self, base_response: Dict, params: Dict) -> Dict:
        """
        Add specific complexity layer based on systematic parameters.
        
        IMPROVEMENT: Targeted complexity vs random selection.
        """
        if params['complexity_type'] == 'baseline':
            return {}  # No additional complexity for baseline
        
        prompt = f"""Add {params['complexity_type']} complexity to this response.

BASE RESPONSE:
{json.dumps(base_response, indent=2)}

TARGET COMPLEXITY: {params['complexity_type']}
{self._get_complexity_behavior(params['complexity_type'])}

Enhance the response to show this complexity pattern clearly.

JSON FORMAT:
{{
    "complexity_type": "{params['complexity_type']}",
    "enhanced_dialogue": "Modified character response showing complexity",
    "enhanced_internal_thought": "Modified thought showing complexity",
    "authenticity_impact": "+/- 0.0-0.2",
    "why_this_adds_realism": "Explanation"
}}"""
        
        response_text = self.generate_with_qwen3(
            model=self.models['primary'],
            prompt=prompt,
            temperature=0.88,
            max_tokens=1000
        )
        
        if response_text:
            parsed = self._parse_json_response(response_text, 'complexity_enhancement')
            return parsed[0] if parsed else {}
        return {}
    
    # ===================================================================
    # PHASE 4: SYSTEMATIC SPECTRUM VALIDATION
    # ===================================================================
    
    def validate_systematic_spectrum(self, samples: List[Dict], parameters: List[Dict]) -> Dict:
        """
        Validate that samples meet systematic spectrum requirements.
        
        IMPROVEMENT: Comprehensive validation vs lenient current validation.
        """
        analysis = {
            'total_samples': len(samples),
            'parameter_compliance': {},
            'authenticity_distribution': {
                'failed (0.2-0.4)': 0,
                'struggling (0.4-0.6)': 0,
                'authentic (0.6-0.8)': 0,
                'excellent (0.8-1.0)': 0
            },
            'complexity_coverage': {},
            'capacity_coverage': {},
            'systematic_validation': {
                'meets_spectrum_requirements': False,
                'missing_combinations': [],
                'quality_issues': []
            }
        }
        
        # Analyze each sample against its target parameters
        for sample, target_params in zip(samples, parameters):
            auth_score = sample.get('authenticity_score', 0.8)
            complexity = sample.get('complexity_exhibited',
                                   sample.get('complexity_type', 'baseline'))
            
            # Check authenticity distribution
            if 0.2 <= auth_score < 0.4:
                analysis['authenticity_distribution']['failed (0.2-0.4)'] += 1
            elif 0.4 <= auth_score < 0.6:
                analysis['authenticity_distribution']['struggling (0.4-0.6)'] += 1
            elif 0.6 <= auth_score < 0.8:
                analysis['authenticity_distribution']['authentic (0.6-0.8)'] += 1
            else:
                analysis['authenticity_distribution']['excellent (0.8-1.0)'] += 1
            
            # Track complexity coverage
            analysis['complexity_coverage'][complexity] = \
                analysis['complexity_coverage'].get(complexity, 0) + 1
            
            # Validate against target parameters
            target_range = target_params['authenticity_range']
            if not (target_range[0] <= auth_score <= target_range[1]):
                analysis['systematic_validation']['quality_issues'].append({
                    'issue': 'authenticity_target_missed',
                    'target': target_params['authenticity_target'],
                    'target_range': target_range,
                    'actual_score': auth_score,
                    'sample_id': sample.get('scenario_id', 'unknown')
                })
        
        # Check spectrum requirements (from config)
        required_minimums = self.config.systematic_coverage['authenticity_spectrum']
        
        spectrum_met = True
        for category, requirements in required_minimums.items():
            category_key = f"{category} ({requirements['target_range'][0]}-{requirements['target_range'][1]})"
            actual = analysis['authenticity_distribution'].get(category_key, 0)
            minimum = requirements['min_examples']
            
            if actual < minimum:
                spectrum_met = False
                analysis['systematic_validation']['missing_combinations'].append({
                    'category': category,
                    'needed': minimum - actual,
                    'current': actual
                })
        
        analysis['systematic_validation']['meets_spectrum_requirements'] = spectrum_met
        
        # Check complexity coverage
        required_complexity = list(self.config.systematic_coverage['complexity_types'].keys())
        for complexity_type in required_complexity[:5]:  # Check top 5
            if complexity_type not in analysis['complexity_coverage']:
                analysis['systematic_validation']['missing_combinations'].append({
                    'category': 'complexity',
                    'missing_type': complexity_type
                })
        
        return analysis
    
    # ===================================================================
    # FULL SYSTEMATIC MULTI-STEP PIPELINE
    # ===================================================================
    
    def generate_complete_batch_systematic(self,
                                          batch_size: int = 5,
                                          target_coverage: Dict = None) -> Tuple[List[Dict], Dict]:
        """
        Generate complete batch using systematic multi-step process.
        
        IMPROVEMENTS:
        1. Systematic parameter selection (not random)
        2. Targeted generation for authenticity spectrum
        3. Complexity integrated systematically
        4. Comprehensive validation
        
        Returns: (samples, quality_analysis)
        """
        AppLogger.info(f"Starting systematic multi-step generation for {batch_size} samples")
        
        # Phase 1: Generate systematic parameter combinations
        AppLogger.info("Phase 1: Generating systematic parameters")
        if target_coverage:
            parameter_combinations = self._generate_gap_filling_combinations(
                target_coverage, batch_size
            )
        else:
            parameter_combinations = self._generate_systematic_parameters(batch_size)
        
        # Phase 2: Generate targeted character states
        AppLogger.info("Phase 2: Generating targeted character states")
        character_states = []
        for params in parameter_combinations:
            state = self.generate_targeted_character_state(params)
            if state:
                character_states.append(state)
            time.sleep(0.3)
        
        # Phase 3: Generate targeted interactions
        AppLogger.info("Phase 3: Generating targeted interactions")
        interactions = []
        for params, state in zip(parameter_combinations, character_states):
            interaction = self.generate_targeted_interaction(params, state)
            if interaction:
                interactions.append(interaction)
            time.sleep(0.3)
        
        # Phase 4: Generate responses with systematic constraints
        AppLogger.info("Phase 4: Generating responses with systematic constraints")
        samples = []
        for state, interaction, params in zip(character_states, interactions, parameter_combinations):
            response = self.generate_response_with_systematic_constraints(
                state, interaction, params
            )
            if response:
                # Combine all components
                response['character_state'] = state
                response['interaction_context'] = interaction
                response['systematic_parameters'] = params
                samples.append(response)
            time.sleep(0.5)
        
        # Phase 5: Add complexity layers
        AppLogger.info("Phase 5: Adding complexity layers")
        for sample, params in zip(samples, parameter_combinations):
            if params['complexity_type'] != 'baseline':
                complexity = self.add_targeted_complexity_layer(sample, params)
                if complexity:
                    sample['complexity_enhancement'] = complexity
            time.sleep(0.3)
        
        # Phase 6: Validate systematic spectrum
        AppLogger.info("Phase 6: Validating systematic spectrum")
        quality_analysis = self.validate_systematic_spectrum(samples, parameter_combinations)
        
        # Track in database
        for sample, params in zip(samples, parameter_combinations):
            self._track_generated_combination(params)
        
        AppLogger.info("Systematic multi-step generation complete", data={
            'samples_generated': len(samples),
            'quality_met': quality_analysis['systematic_validation']['meets_spectrum_requirements'],
            'authenticity_distribution': quality_analysis['authenticity_distribution'],
            'complexity_coverage': len(quality_analysis['complexity_coverage'])
        })
        
        return samples, quality_analysis
    
    def _generate_gap_filling_combinations(self,
                                          target_coverage: Dict,
                                          batch_size: int) -> List[Dict]:
        """Generate parameter combinations to fill specific coverage gaps"""
        combinations = []
        gaps = target_coverage.get('gaps', [])
        
        # Parse gaps and create targeted combinations
        for gap in gaps[:batch_size]:
            if 'failed' in str(gap).lower():
                combinations.append({
                    'capacity_level': 'crisis',
                    'capacity_range': (0.5, 1.5),
                    'authenticity_target': 'failed',
                    'authenticity_range': (0.2, 0.4),
                    'complexity_type': 'people_pleasing'
                })
            elif 'struggling' in str(gap).lower():
                combinations.append({
                    'capacity_level': 'low',
                    'capacity_range': (2.0, 4.0),
                    'authenticity_target': 'struggling',
                    'authenticity_range': (0.4, 0.6),
                    'complexity_type': 'misjudgment_over'
                })
        
        # Fill remaining slots with systematic coverage
        remaining = batch_size - len(combinations)
        if remaining > 0:
            systematic = self._generate_systematic_parameters(remaining)
            combinations.extend(systematic)
        
        return combinations
    
    def save_systematic_multi_step_batch(self,
                                        samples: List[Dict],
                                        quality_analysis: Dict,
                                        batch_number: int) -> str:
        """Save systematic multi-step batch with comprehensive metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"systematic_multi_step_batch{batch_number:04d}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        try:
            output = {
                "master_truths_version": "v1.2",
                "generation_method": "systematic_multi_step",
                "data_type": "emotional_authenticity_systematic_multi_step",
                "batch_number": batch_number,
                "timestamp": timestamp,
                "sample_count": len(samples),
                "quality_analysis": quality_analysis,
                "generation_phases": [
                    "1_systematic_parameter_generation",
                    "2_targeted_character_states",
                    "3_targeted_interactions",
                    "4_systematic_constraint_responses",
                    "5_complexity_enhancement",
                    "6_spectrum_validation"
                ],
                "improvements": [
                    "systematic_not_random",
                    "full_spectrum_coverage",
                    "8_complexity_types",
                    "targeted_authenticity",
                    "comprehensive_validation"
                ],
                "samples": samples
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            AppLogger.info(f"Saved systematic multi-step batch", data={
                'file': filename,
                'samples': len(samples),
                'quality_met': quality_analysis['systematic_validation']['meets_spectrum_requirements']
            })
            return str(filepath)
            
        except Exception as e:
            AppLogger.error(f"Failed to save systematic multi-step batch {filename}", e)
            raise

