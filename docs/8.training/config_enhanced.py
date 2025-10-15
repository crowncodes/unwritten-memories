"""
Training configuration for Qwen3 data generation.
Aligned with Master Truths Canonical Spec v1.2

Manages model settings, batch sizes, and generation parameters.
"""

import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TrainingConfig:
    """Configuration for training data generation (Master Truths v1.2 compliant)"""
    
    # Ollama connection
    ollama_url: str = "http://localhost:11434/api/generate"
    
    # Model names (Qwen3 via Ollama)
    model_primary: str = "qwen3:30b-a3b"       # Best quality, emotional depth
    model_speed: str = "qwen3:8b"              # Fast generation
    model_validation: str = "qwen3:32b"        # Quality validation
    
    # Daily production targets (24/7 operation)
    # Prioritized by canonical importance (Master Truths Section 16-17)
    target_emotional_authenticity: int = 2000   # CORE: capacity-constrained behavior
    target_dramatic_irony: int = 1500           # HIGH: knowledge gap tension
    target_tension_building: int = 1200         # HIGH: narrative hooks
    target_memory_resonance: int = 1000         # NEW v1.2: emotional callbacks
    target_personality_traits: int = 2500       # FOUNDATION: OCEAN traits
    target_relationship_scoring: int = 1000     # FOUNDATION: interaction quality
    
    # Batch sizes (optimized for RTX 4070 SUPER)
    batch_size_emotional: int = 12              # Reduced for quality focus
    batch_size_dramatic: int = 8                # Complex reasoning
    batch_size_tension: int = 10                # Narrative sophistication
    batch_size_memory: int = 15                 # NEW: resonance examples
    batch_size_personality: int = 25            # High volume foundation
    batch_size_relationship: int = 20           # Moderate volume
    
    # Temperature settings aligned with data complexity
    temp_emotional: float = 0.82       # Controlled variety, realistic constraints
    temp_dramatic: float = 0.85        # Creative tension scenarios
    temp_tension: float = 0.88         # Sophisticated hooks
    temp_memory: float = 0.80          # Emotionally coherent
    temp_personality: float = 0.9      # Maximum diversity
    temp_relationship: float = 0.85    # Varied interactions
    temp_validation: float = 0.25      # Strict evaluation
    
    # Output settings
    output_dir: str = field(default_factory=lambda: os.path.join(os.getcwd(), "training_output_v1.2"))
    log_file: str = "training_generation_v1.2.log"
    
    # Quality thresholds (Master Truths v1.2 Section 17)
    min_emotional_authenticity: float = 0.7
    min_tension_building: float = 0.6
    min_dramatic_irony: float = 0.5
    min_hook_effectiveness: float = 0.6
    min_overall_quality: float = 0.7
    validation_sample_rate: float = 0.15  # Validate 15% of samples
    
    # Canonical constants (Master Truths v1.2 Section 15)
    capacity_default: float = 5.0
    capacity_low_threshold: float = 5.0
    capacity_high_threshold: float = 8.0
    capacity_crisis_threshold: float = 1.0
    
    # Tension injection frequencies (Master Truths v1.2 Section 17)
    tension_freq_level_1_2: float = 0.33  # 1 in 3
    tension_freq_level_3_4: float = 0.50  # 1 in 2
    tension_freq_level_5: float = 0.90    # Nearly every
    
    # Memory resonance weights (Master Truths v1.2 Section 17)
    resonance_same_emotion: float = 0.8
    resonance_opposite_emotion: float = 0.9
    resonance_trauma_trigger: float = 0.95
    resonance_joy_sadness: float = 0.85
    resonance_growth_callback: float = 0.7
    
    # Hardware settings
    max_tokens: int = 6000
    request_timeout: int = 180  # Increased for complex generations
    
    @property
    def total_daily_target(self) -> int:
        """Calculate total daily sample target"""
        return (
            self.target_emotional_authenticity +
            self.target_dramatic_irony +
            self.target_tension_building +
            self.target_memory_resonance +
            self.target_personality_traits +
            self.target_relationship_scoring
        )
    
    @property
    def models(self) -> Dict[str, str]:
        """Return model dictionary for compatibility"""
        return {
            'primary': self.model_primary,
            'speed': self.model_speed,
            'validation': self.model_validation
        }
    
    @property
    def quality_thresholds(self) -> Dict[str, float]:
        """Return quality thresholds for validation"""
        return {
            'emotional_authenticity': self.min_emotional_authenticity,
            'tension_building': self.min_tension_building,
            'dramatic_irony': self.min_dramatic_irony,
            'hook_effectiveness': self.min_hook_effectiveness,
            'overall_quality': self.min_overall_quality
        }
    
    def validate(self) -> None:
        """Validate configuration settings"""
        if not (0.0 < self.validation_sample_rate <= 1.0):
            raise ValueError("validation_sample_rate must be between 0 and 1")
        
        # Validate quality thresholds align with Master Truths
        if self.min_overall_quality < 0.7:
            raise ValueError(f"min_overall_quality must be >= 0.7 (Master Truths v1.2)")
        
        if self.min_emotional_authenticity < 0.7:
            raise ValueError(f"min_emotional_authenticity must be >= 0.7 (Master Truths v1.2)")
        
        if self.min_tension_building < 0.6:
            raise ValueError(f"min_tension_building must be >= 0.6 (Master Truths v1.2)")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"✅ Created output directory: {self.output_dir}")
        
        print(f"✅ Configuration validated (Master Truths v1.2 compliant)")
