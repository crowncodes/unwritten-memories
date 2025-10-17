"""
Enhanced Training Configuration with Systematic Coverage & Numerical Grounding
Master Truths Canonical Spec v1.2 Compliant

IMPROVEMENTS over config.py:
1. Systematic coverage requirements (missing in current)
2. Numerical grounding validation (missing in current)
3. Batch processing configuration (missing in current)
4. Coverage tracking settings (missing in current)
5. Quality gates for spectrum validation (missing in current)
6. Performance monitoring configuration (missing in current)

Addresses Critical Issues:
- No systematic parameter tracking → Full coverage database
- Random generation → Systematic parameter buckets
- Missing authenticity spectrum → Required spectrum enforcement
- No complexity tracking → 8 complexity types tracked
- Lenient validation → Strict spectrum validation
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path


@dataclass
class EnhancedTrainingConfig:
    """Enhanced configuration for systematic training data generation"""

    # ===================================================================
    # GENERATION MODE (addresses over-engineering concerns)
    # ===================================================================

    # Mode: "strict" | "balanced" | "organic"
    # - strict: Enforce all systematic requirements (100% coverage)
    # - balanced: Systematic coverage with natural variation (default)
    # - organic: Minimal constraints, more random (higher authenticity)
    generation_mode: str = "balanced"

    # ===================================================================
    # BASE CONFIGURATION (from original config.py)
    # ===================================================================

    # Ollama connection
    ollama_url: str = "http://localhost:11434/api/generate"

    # Model names (Qwen3 via Ollama)
    # v2.2: Using 8B - 30B variants keep returning empty responses
    model_primary: str = "qwen3:8b"  # 8B for reliability
    model_speed: str = "qwen3:8b"  # Fast generation
    model_validation: str = "qwen3:8b"  # 8B validation

    # Daily production targets
    target_emotional_authenticity: int = 2000
    target_dramatic_irony: int = 1500
    target_tension_building: int = 1200
    target_memory_resonance: int = 1000
    target_personality_traits: int = 2500
    target_relationship_scoring: int = 1000

    # v1.6.3: Single-example generation to prevent crashes (30B model memory-intensive)
    batch_size_emotional: int = 1  # Generate one at a time for stability
    batch_size_dramatic: int = 1  # One at a time
    batch_size_tension: int = 1  # One at a time
    batch_size_memory: int = 1  # One at a time
    batch_size_personality: int = 1  # One at a time
    batch_size_relationship: int = 1  # One at a time

    # Temperature settings (v1.6.3: balanced for creativity without confusion)
    temp_emotional: float = 0.92  # High creativity, not paralyzing (was 0.98)
    temp_dramatic: float = 0.92  # High creativity
    temp_tension: float = 0.92  # High creativity
    temp_memory: float = 0.88  # High creativity
    temp_personality: float = 0.92  # High creativity
    temp_relationship: float = 0.92  # High creativity
    temp_validation: float = 0.25  # Keep low for consistent validation

    # Output settings
    output_dir: str = field(
        default_factory=lambda: os.path.join(os.getcwd(), "training_output_v1.2_systematic")
    )
    log_file: str = "training_generation_systematic.log"

    # Quality thresholds (Master Truths v1.2 Section 17)
    min_emotional_authenticity: float = 0.7
    min_tension_building: float = 0.6
    min_dramatic_irony: float = 0.5
    min_hook_effectiveness: float = 0.6
    min_overall_quality: float = 0.7
    validation_sample_rate: float = 0.25  # Increased from 0.15 - more validation

    # Canonical constants
    capacity_default: float = 5.0
    capacity_low_threshold: float = 5.0
    capacity_high_threshold: float = 8.0
    capacity_crisis_threshold: float = 1.0

    # Hardware settings
    max_tokens: int = 4000  # v1.6.3: Reduced for stability (was 16000 - too memory-intensive)
    request_timeout: int = 2400  # 40 minutes (4x increase for stability)

    # Model-specific timeouts (auto-selected based on model) - 4x increased for complex generation
    timeout_8b: int = 480  # 8 minutes for qwen3:8b (4x increase)
    timeout_30b: int = 2400  # 40 minutes for qwen3:30b (4x increase)
    timeout_validation: int = 1200  # 20 minutes for validation (4x increase)

    # ===================================================================
    # IMPROVEMENT 2: SYSTEMATIC COVERAGE REQUIREMENTS (NEW)
    # ===================================================================

    systematic_coverage: Dict = field(
        default_factory=lambda: {
            "authenticity_spectrum": {
                "failed": {"min_examples": 2, "target_range": (0.2, 0.4)},
                "struggling": {"min_examples": 3, "target_range": (0.4, 0.6)},
                "authentic": {"min_examples": 4, "target_range": (0.6, 0.8)},
                "excellent": {"min_examples": 3, "target_range": (0.8, 1.0)},
            },
            "complexity_types": {
                "baseline": {"min_examples": 2},
                "people_pleasing": {"min_examples": 2},
                "misjudgment_over": {"min_examples": 2},
                "misjudgment_under": {"min_examples": 1},
                "defensive_lashing": {"min_examples": 1},
                "emergency_override": {"min_examples": 2},
                "cultural_indirect": {"min_examples": 1},
                "mixed_emotions": {"min_examples": 2},
            },
            "capacity_levels": {
                "crisis": {"min_examples": 2, "range": (0.5, 1.5)},
                "low": {"min_examples": 3, "range": (2.0, 4.0)},
                "medium": {"min_examples": 4, "range": (4.5, 6.5)},
                "high": {"min_examples": 3, "range": (7.0, 9.5)},
            },
        }
    )

    # ===================================================================
    # IMPROVEMENT 3: QUALITY THRESHOLDS ENHANCED (NEW)
    # ===================================================================

    quality_thresholds_enhanced: Dict = field(
        default_factory=lambda: {
            # Master Truths v1.2 core thresholds (keep existing)
            "emotional_authenticity": 0.7,
            "tension_building": 0.6,
            "dramatic_irony": 0.5,
            "hook_effectiveness": 0.6,
            "overall_quality": 0.7,
            # NEW: Spectrum validation thresholds
            "spectrum_coverage": {
                "min_failed_examples": 2,  # Must have some failure examples
                "min_struggling_examples": 3,  # Must have struggling examples
                "max_excellent_percentage": 0.4,  # Can't be all excellent scores
                "authenticity_variance": 0.3,  # Must have variance across spectrum
            },
            # NEW: Complexity coverage thresholds
            "complexity_coverage": {
                "min_complexity_types": 5,  # Must cover at least 5 complexity types
                "baseline_percentage": 0.3,  # Max 30% can be baseline (no complexity)
                "required_people_pleasing": 2,  # Must have people-pleasing examples
            },
            # NEW: Realistic constraint validation
            "constraint_realism": {
                "capacity_violation_tolerance": 0.1,  # Max 10% can violate capacity rules
                "unrealistic_resilience_threshold": 0.05,  # Max 5% unrealistically resilient
                "melodrama_threshold": 0.05,  # Max 5% melodramatic
            },
        }
    )

    # ===================================================================
    # IMPROVEMENT 4: BATCH PROCESSING CONFIGURATION (NEW)
    # ===================================================================

    batch_processing: Dict = field(
        default_factory=lambda: {
            "enable_batch_api_calls": False,  # v1.6.3: DISABLED - generate one at a time
            "batch_api_max_examples": 1,  # Single example only
            "batch_timeout_seconds": 480,  # Timeout for batch calls (4x increase)
            "fallback_to_individual": True,  # Always individual now
            "batch_cost_threshold": 0.01,  # Max cost per batch call
        }
    )

    # ===================================================================
    # IMPROVEMENT 5: COVERAGE TRACKING CONFIGURATION (NEW)
    # ===================================================================

    coverage_tracking: Dict = field(
        default_factory=lambda: {
            "enable_tracking": True,
            "database_path": "coverage_tracking.db",
            "track_parameters": [
                "authenticity_score",
                "complexity_type",
                "capacity_level",
                "support_level_needed",
                "relationship_impact",
            ],
            "coverage_report_frequency": 10,  # Generate report every 10 batches
            "gap_filling_priority": True,  # Prioritize filling gaps
            "max_duplicate_combinations": 2,  # Max times to generate same parameter combo
        }
    )

    # ===================================================================
    # IMPROVEMENT 6: NUMERICAL GROUNDING REQUIREMENTS (NEW)
    # ===================================================================

    # CONCERN ADDRESSED: "Numerical grounding might make responses feel calculated"
    # SOLUTION: Background validation, not explicit in prompts (balanced/organic modes)
    numerical_grounding: Dict = field(
        default_factory=lambda: {
            "require_calculation_steps": True,  # Validate math (background)
            "require_qualitative_anchors": False,  # Don't force tier identification
            "require_formula_validation": True,  # Check math correctness
            "require_tier_consistency": False,  # Allow natural description
            "min_grounding_score": 0.8,  # Reduced from 0.9 (less strict)
            "track_calculation_accuracy": True,  # Monitor but don't enforce
            "enforce_calibration_guide": False,  # Allow natural variation
            "show_in_prompts": False,  # Keep math validation background
        }
    )

    # NEW: Calculation validation thresholds
    calculation_validation: Dict = field(
        default_factory=lambda: {
            "capacity_calculation": {
                "max_math_error": 0.1,  # Allow 0.1 rounding error
                "require_stressor_breakdown": True,  # Must show each stressor
                "require_base_reasoning": True,  # Must explain base capacity
                "validate_stacking_penalty": False,  # Check circumstance stacking (optional)
            },
            "relationship_impact": {
                "max_math_error": 0.05,  # Stricter for impact calculation
                "require_component_breakdown": False,  # Must show base × urgency × trust (optional)
                "require_tier_identification": False,  # Must identify harm tier (optional)
                "validate_personality_modifier": False,  # Check personality effects (optional)
            },
            "authenticity_scoring": {
                "require_target_range_check": True,  # Must be in target range
                "require_tier_justification": True,  # Must explain tier choice
                "require_behavior_consistency": True,  # Must match capacity
                "min_reasoning_length": 20,  # Minimum explanation length
            },
        }
    )

    # ===================================================================
    # IMPROVEMENT 7: ENHANCED VALIDATION SETTINGS (NEW)
    # ===================================================================

    validation_enhanced: Dict = field(
        default_factory=lambda: {
            "validate_spectrum_distribution": True,  # Check authenticity spectrum
            "validate_complexity_coverage": True,  # Check complexity type coverage
            "validate_capacity_constraints": True,  # Check X+2 rule adherence
            "validate_realistic_responses": True,  # Check for melodrama/unrealism
            "validation_sample_rate": 0.25,  # Validate 25% vs current 15%
            "require_passing_validation": True,  # Must pass validation to save
            "max_validation_retries": 2,  # Retry failed validation up to 2x
        }
    )

    # ===================================================================
    # IMPROVEMENT 8: EFFICIENCY OPTIMIZATION SETTINGS (NEW)
    # ===================================================================

    efficiency_optimization: Dict = field(
        default_factory=lambda: {
            "prompt_compression": True,  # Use compressed prompts
            "context_caching": False,  # Cache repeated context (optional)
            "model_routing": {
                "simple_examples": "qwen3:8b",  # Use smaller model for simple
                "complex_examples": "qwen3:8b",  # Use same for now
                "validation": "qwen3:30b-a3b",  # Use validation model
            },
            "token_budget_management": {
                "max_tokens_per_prompt": 2000,  # Reduced from current 6000
                "context_token_limit": 1500,  # Limit context size
                "response_token_target": 800,  # Target response size
            },
        }
    )

    # ===================================================================
    # IMPROVEMENT 9: PERFORMANCE MONITORING (NEW)
    # ===================================================================

    performance_monitoring: Dict = field(
        default_factory=lambda: {
            "track_generation_time": True,
            "track_api_costs": False,  # Optional cost tracking
            "track_quality_scores": True,
            "track_coverage_progress": True,
            "alert_on_quality_drop": True,
            "alert_on_coverage_gaps": True,
            "performance_report_interval": 50,  # Generate report every 50 batches
        }
    )

    # ===================================================================
    # IMPROVEMENT 10: NATURAL VARIATION SAFEGUARDS (NEW)
    # ===================================================================

    # CONCERNS ADDRESSED:
    # 1. "Forcing 8 complexity types may create artificial variation"
    # 2. "Target gaming: Explicitly targeting scores could be formulaic"
    # 3. "Forcing percentages may reduce organic variation"

    natural_variation: Dict = field(
        default_factory=lambda: {
            # Allow complexity to emerge naturally vs forcing all 8 types
            "allow_complexity_emergence": True,  # Let some complexity occur naturally
            "complexity_suggestion_weight": 0.6,  # 60% suggested, 40% organic
            "min_complexity_types": 4,  # Require at least 4 (not all 8)
            # Allow score variation vs strict targeting
            "score_target_flexibility": 0.2,  # ±20% from target ranges
            "allow_score_drift": True,  # Let scores vary naturally
            "authenticity_bands_not_targets": True,  # Suggest bands not exact targets
            # Organic spectrum distribution
            "suggest_spectrum_not_force": True,  # Guide but don't mandate distribution
            "allow_natural_clustering": True,  # OK if some clusters form naturally
            "spectrum_tolerance": 0.3,  # 30% tolerance on distribution requirements
            # AI self-validation concerns
            "use_external_validation": False,  # Don't rely only on AI validation
            "validation_sample_size": 5,  # Validate subset, not all
            "trust_but_verify": True,  # Spot check vs comprehensive
            # Prompt naturalness
            "implicit_vs_explicit_constraints": "implicit",  # Hint at requirements vs demand
            "allow_creative_deviations": True,  # OK to deviate if high quality
            "prioritize_authenticity_over_coverage": True,  # Quality > completeness
        }
    )

    # ===================================================================
    # IMPROVEMENT 11: MODE-SPECIFIC OVERRIDES
    # ===================================================================

    def get_mode_adjustments(self) -> Dict:
        """Get configuration adjustments based on generation_mode"""

        if self.generation_mode == "strict":
            # Maximize systematic coverage, accept less natural variation
            return {
                "complexity_types_required": 8,
                "min_complexity_types": 8,
                "spectrum_tolerance": 0.1,
                "score_target_flexibility": 0.1,
                "allow_complexity_emergence": False,
                "prioritize_authenticity_over_coverage": False,
            }

        elif self.generation_mode == "organic":
            # Maximize natural variation, accept less systematic coverage
            return {
                "complexity_types_required": 3,
                "min_complexity_types": 3,
                "spectrum_tolerance": 0.5,
                "score_target_flexibility": 0.4,
                "allow_complexity_emergence": True,
                "prioritize_authenticity_over_coverage": True,
                "coverage_tracking": {"enable_tracking": False},  # Disable tracking
            }

        else:  # "balanced" (default)
            # Balance systematic coverage with natural variation
            return {
                "complexity_types_required": 5,
                "min_complexity_types": 4,
                "spectrum_tolerance": 0.3,
                "score_target_flexibility": 0.2,
                "allow_complexity_emergence": True,
                "prioritize_authenticity_over_coverage": True,
            }

    # ===================================================================
    # HELPER PROPERTIES
    # ===================================================================

    @property
    def total_daily_target(self) -> int:
        """Calculate total daily sample target"""
        return (
            self.target_emotional_authenticity
            + self.target_dramatic_irony
            + self.target_tension_building
            + self.target_memory_resonance
            + self.target_personality_traits
            + self.target_relationship_scoring
        )

    @property
    def models(self) -> Dict[str, str]:
        """Return model dictionary for compatibility"""
        return {
            "primary": self.model_primary,
            "speed": self.model_speed,
            "validation": self.model_validation,
        }

    @property
    def quality_thresholds(self) -> Dict[str, float]:
        """Return quality thresholds for validation"""
        return {
            "emotional_authenticity": self.min_emotional_authenticity,
            "tension_building": self.min_tension_building,
            "dramatic_irony": self.min_dramatic_irony,
            "hook_effectiveness": self.min_hook_effectiveness,
            "overall_quality": self.min_overall_quality,
        }

    # ===================================================================
    # SYSTEMATIC COVERAGE HELPERS
    # ===================================================================

    def get_systematic_batch_size(self, data_type: str) -> int:
        """Get batch size optimized for systematic coverage"""
        if data_type == "emotional_authenticity":
            # Need to cover 8 complexity types minimum
            complexity_count = len(self.systematic_coverage["complexity_types"])
            return max(self.batch_size_emotional, complexity_count)
        elif data_type == "dramatic_irony":
            return self.batch_size_dramatic
        elif data_type == "tension_building":
            return max(self.batch_size_tension, 4)  # 4 tension types
        else:
            return getattr(self, f"batch_size_{data_type}", 5)

    def calculate_coverage_target(self, data_type: str, total_target: int) -> Dict:
        """Calculate how many examples needed for each category"""
        if data_type == "emotional_authenticity":
            spectrum_reqs = self.systematic_coverage["authenticity_spectrum"]
            complexity_reqs = self.systematic_coverage["complexity_types"]

            # Calculate minimum examples needed
            min_spectrum = sum(req["min_examples"] for req in spectrum_reqs.values())
            min_complexity = sum(req["min_examples"] for req in complexity_reqs.values())

            # Use higher requirement
            min_required = max(min_spectrum, min_complexity)

            return {
                "total_target": max(total_target, min_required),
                "spectrum_targets": spectrum_reqs,
                "complexity_targets": complexity_reqs,
                "min_required": min_required,
            }

        return {"total_target": total_target}

    @property
    def total_systematic_requirements(self) -> Dict:
        """Calculate total systematic requirements across all data types"""
        return {
            "emotional_authenticity": {
                "spectrum_minimum": sum(
                    config["min_examples"]
                    for config in self.systematic_coverage["authenticity_spectrum"].values()
                ),
                "complexity_minimum": sum(
                    config["min_examples"]
                    for config in self.systematic_coverage["complexity_types"].values()
                ),
            },
            "capacity_distribution": self.systematic_coverage["capacity_levels"],
            "quality_gates": self.quality_thresholds_enhanced["constraint_realism"],
        }

    # ===================================================================
    # VALIDATION
    # ===================================================================

    def validate(self) -> None:
        """Validate configuration settings"""
        # Basic validation
        if not (0.0 < self.validation_sample_rate <= 1.0):
            raise ValueError("validation_sample_rate must be between 0 and 1")

        if self.min_overall_quality < 0.7:
            raise ValueError("min_overall_quality must be >= 0.7 (Master Truths v1.2)")

        # Systematic coverage validation
        spectrum_config = self.systematic_coverage["authenticity_spectrum"]
        total_min_examples = sum(config["min_examples"] for config in spectrum_config.values())

        # v1.6.3: Allow batch_size=1 for single-example mode (stability)
        if self.batch_processing["enable_batch_api_calls"] and self.batch_size_emotional < 5:
            raise ValueError("batch_size_emotional too small for batch systematic coverage")

        if self.batch_size_emotional < 1:
            raise ValueError("batch_size_emotional must be at least 1")

        # Validate complexity coverage requirements
        complexity_config = self.systematic_coverage["complexity_types"]
        min_complexity_examples = sum(
            config["min_examples"] for config in complexity_config.values()
        )

        if min_complexity_examples > self.target_emotional_authenticity:
            raise ValueError(
                f"Daily target {self.target_emotional_authenticity} too low for "
                f"complexity coverage requirement {min_complexity_examples}"
            )

        # Validate batch processing settings
        if self.batch_processing["batch_api_max_examples"] > 10:
            raise ValueError("batch_api_max_examples should not exceed 10 for quality")

        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"✅ Created output directory: {self.output_dir}")

        print("✅ Enhanced configuration validated (systematic coverage compliant)")

    def validate_enhanced(self) -> None:
        """Enhanced validation including systematic coverage requirements"""
        self.validate()  # Run base validation first

        # Additional enhanced validation
        if self.numerical_grounding["min_grounding_score"] < 0.8:
            raise ValueError("Minimum grounding score too low (<0.8)")

        if self.validation_enhanced["validation_sample_rate"] < 0.2:
            raise ValueError("Validation sample rate should be >= 0.2 for quality")

        print("✅ All enhanced validations passed")


# ===================================================================
# CONVENIENCE FUNCTION
# ===================================================================


def initialize_enhanced_config(config_overrides: Dict = None) -> EnhancedTrainingConfig:
    """
    Initialize enhanced configuration with optional overrides.

    Usage:
        config = initialize_enhanced_config({
            'batch_size_emotional': 10,
            'target_emotional_authenticity': 3000
        })
    """
    config = EnhancedTrainingConfig()

    # Apply any overrides
    if config_overrides:
        for key, value in config_overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                print(f"⚠️ Warning: Unknown config parameter '{key}'")

    # Validate
    config.validate_enhanced()

    # Calculate and display systematic targets
    emotional_targets = config.calculate_coverage_target(
        "emotional_authenticity", config.target_emotional_authenticity
    )

    print(f"\n✅ Systematic coverage targets:")
    print(f"   Emotional authenticity: {emotional_targets['total_target']} examples")
    print(f"   Minimum spectrum coverage: {emotional_targets.get('min_required', 0)} examples")
    print(
        f"   Batch size optimized: {config.get_systematic_batch_size('emotional_authenticity')} per batch"
    )
    print(f"   Complexity types required: {len(config.systematic_coverage['complexity_types'])}")

    return config


# ===================================================================
# BACKWARDS COMPATIBILITY ALIAS
# ===================================================================

# Alias for backwards compatibility with existing code
TrainingConfig = EnhancedTrainingConfig
