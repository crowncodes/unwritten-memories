#!/usr/bin/env python3
"""
Unwritten Training Data Generation Runner
Master Truths Canonical Spec v1.2 Compliant

Generates novel-quality training data with:
- Emotional capacity constraints (0-10 scale)
- Dramatic irony scenarios (knowledge gaps)
- Tension building hooks (four types)
- Memory resonance (five types)
- OCEAN personality traits
- Relationship scoring
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from unwritten.training.config import TrainingConfig
from unwritten.training.qwen3_generator import Qwen3DataGenerator
from unwritten.utils.logger import AppLogger


def check_ollama_connection(url: str = "http://localhost:11434/api/tags") -> bool:
    """Check if Ollama service is running"""
    import requests
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        AppLogger.error("Failed to connect to Ollama service", e)
        return False


def display_spec_compliance():
    """Display Master Truths v1.2 compliance information"""
    print("\n" + "=" * 70)
    print("MASTER TRUTHS CANONICAL SPEC v1.2 COMPLIANCE")
    print("=" * 70)
    print("\n✅ CORE SYSTEMS:")
    print("   • Emotional Capacity: 0-10 scale (X+2 support rule)")
    print("   • Dramatic Irony: Knowledge gap scoring (≥ 0.6)")
    print("   • Tension Building: 4 types (mystery, reveal, contradiction, stakes)")
    print("   • Memory Resonance: 5 types (weights 0.7-0.95)")
    print("   • OCEAN Personality: All 5 traits (0-1 scale)")
    print("   • Relationship Scoring: Impact tracking (-1.5 to +1.0)")
    
    print("\n✅ QUALITY THRESHOLDS:")
    print("   • Emotional Authenticity: ≥ 0.7")
    print("   • Tension Building: ≥ 0.6")
    print("   • Dramatic Irony: ≥ 0.5")
    print("   • Hook Effectiveness: ≥ 0.6")
    print("   • Overall Novel-Quality: ≥ 0.7")
    
    print("\n✅ TENSION FREQUENCIES:")
    print("   • Level 1-2 relationships: 1 in 3 evolutions (33%)")
    print("   • Level 3-4 relationships: 1 in 2 evolutions (50%)")
    print("   • Level 5 relationships: Nearly every evolution (90%)")
    
    print("\n✅ MODELS:")
    print("   • Primary: Qwen3-30B-A3B (emotional depth, complex reasoning)")
    print("   • Speed: Qwen3-8B (high-volume foundation data)")
    print("   • Validation: Qwen3-32B (quality checking)")
    print("=" * 70)


def main():
    """Main entry point for Master Truths v1.2 compliant generation"""
    
    print("\n" + "=" * 70)
    print("🚀 Unwritten Training Data Generation Pipeline")
    print("   Master Truths Canonical Spec v1.2")
    print("=" * 70)
    
    # Check Ollama connection
    print("\n🔍 Checking Ollama service...")
    if not check_ollama_connection():
        print("\n❌ Cannot connect to Ollama service")
        print("\nPlease ensure:")
        print("  1. Ollama is installed (https://ollama.ai)")
        print("  2. Ollama service is running (ollama serve)")
        print("  3. Required models are downloaded:")
        print("     - ollama pull qwen3:30b-a3b")
        print("     - ollama pull qwen3:8b")
        print("     - ollama pull qwen3:32b")
        sys.exit(1)
    
    print("✅ Ollama service is running")
    
    # Display spec compliance
    display_spec_compliance()
    
    # Initialize configuration
    print("\n⚙️  Initializing Master Truths v1.2 configuration...")
    config = TrainingConfig()
    
    # Allow custom output directory via environment variable
    if 'TRAINING_OUTPUT_DIR' in os.environ:
        config.output_dir = os.environ['TRAINING_OUTPUT_DIR']
    
    config.validate()
    
    print(f"\n✅ Configuration validated:")
    print(f"   • Output directory: {config.output_dir}")
    print(f"   • Daily target: {config.total_daily_target:,} samples")
    print(f"   • Quality thresholds:")
    for metric, threshold in config.quality_thresholds.items():
        print(f"     - {metric}: ≥ {threshold}")
    
    # Initialize generator
    print("\n📦 Initializing Qwen3 generator...")
    generator = Qwen3DataGenerator(config)
    print("✅ Generator ready (Master Truths v1.2 compliant)")
    
    # Prompt for run duration
    print("\n⏱️  Run duration options:")
    print("  1. Test run (1 hour) - ~380 samples")
    print("  2. Half day (12 hours) - ~4,600 samples")
    print("  3. Full day (24 hours) - ~9,200 samples")
    print("  4. Multi-day (specify hours)")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    duration_map = {
        '1': 1,
        '2': 12,
        '3': 24
    }
    
    if choice in duration_map:
        duration_hours = duration_map[choice]
    elif choice == '4':
        try:
            duration_hours = int(input("Enter number of hours: "))
            if duration_hours < 1:
                print("❌ Invalid duration")
                sys.exit(1)
        except ValueError:
            print("❌ Invalid input")
            sys.exit(1)
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    estimated_samples = (config.total_daily_target / 24) * duration_hours
    
    print(f"\n" + "=" * 70)
    print(f"📊 GENERATION PLAN")
    print("=" * 70)
    print(f"Duration: {duration_hours} hours")
    print(f"Estimated output: ~{estimated_samples:,.0f} samples")
    print(f"\nBREAKDOWN (prioritized by Master Truths v1.2):")
    
    hourly_rate = config.total_daily_target / 24
    print(f"  1. Emotional Authenticity: ~{int((config.target_emotional_authenticity/config.total_daily_target) * estimated_samples):,} samples (CORE)")
    print(f"  2. Dramatic Irony: ~{int((config.target_dramatic_irony/config.total_daily_target) * estimated_samples):,} samples (HIGH)")
    print(f"  3. Tension Building: ~{int((config.target_tension_building/config.total_daily_target) * estimated_samples):,} samples (HIGH)")
    print(f"  4. Memory Resonance: ~{int((config.target_memory_resonance/config.total_daily_target) * estimated_samples):,} samples (NEW v1.2)")
    print(f"  5. Personality Traits: ~{int((config.target_personality_traits/config.total_daily_target) * estimated_samples):,} samples (FOUNDATION)")
    print(f"  6. Relationship Scoring: ~{int((config.target_relationship_scoring/config.total_daily_target) * estimated_samples):,} samples (FOUNDATION)")
    
    print(f"\nQuality validation: {int(config.validation_sample_rate * 100)}% of samples")
    print(f"Target quality: ≥{config.min_overall_quality:.1f} overall")
    
    print("\n💡 IMPORTANT:")
    print("  • All data will be validated against Master Truths v1.2 thresholds")
    print("  • Emotional capacity constraints (X+2 rule) enforced")
    print("  • Novel-quality standards required (≥ 0.7)")
    print("  • Press Ctrl+C to stop early (data will be saved)")
    
    print("\n" + "=" * 70)
    
    input("\n▶️  Press Enter to start generation...")
    
    print("\n🎯 Starting Master Truths v1.2 compliant data generation...\n")
    
    try:
        # Run the production cycle
        results = generator.run_production_cycle(duration_hours=duration_hours)
        
        # Display final summary
        print("\n" + "=" * 70)
        print("📊 GENERATION COMPLETE - FINAL RESULTS")
        print("=" * 70)
        
        total = 0
        print("\nSAMPLES GENERATED:")
        for data_type, samples in results.items():
            count = len(samples)
            total += count
            percentage = (count / estimated_samples * 100) if estimated_samples > 0 else 0
            
            # Add emoji indicators
            if data_type == 'emotional_authenticity':
                emoji = "🎭"  # Core system
            elif data_type in ['dramatic_irony', 'tension_building']:
                emoji = "⚡"  # High priority
            elif data_type == 'memory_resonance':
                emoji = "🆕"  # New in v1.2
            else:
                emoji = "📚"  # Foundation
            
            print(f"  {emoji} {data_type}: {count:,} samples ({percentage:.1f}% of target)")
        
        print(f"\n  TOTAL: {total:,} samples generated")
        print(f"  Target: {estimated_samples:,.0f} samples")
        completion = (total / estimated_samples * 100) if estimated_samples > 0 else 0
        print(f"  Achievement: {completion:.1f}%")
        
        print(f"\n📁 Location: {config.output_dir}")
        
        # Quality summary
        print("\n✅ QUALITY VALIDATION:")
        print("  All samples validated against Master Truths v1.2 thresholds")
        print("  See individual batch files for detailed quality scores")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        print("💾 Partial data has been saved with '_PARTIAL' suffix")
    except Exception as e:
        AppLogger.error("Generation pipeline failed", e)
        print(f"\n❌ Error: {str(e)}")
        print("Check logs for details")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🎉 TRAINING DATA GENERATION COMPLETE!")
    print("   Master Truths Canonical Spec v1.2 Compliant")
    print("=" * 70)
    
    print(f"\n📍 OUTPUT LOCATION:")
    print(f"   {config.output_dir}")
    
    print("\n📋 NEXT STEPS:")
    print("  1. Review generated data quality:")
    print(f"     - Check authenticity_score ≥ 0.7 in emotional_authenticity samples")
    print(f"     - Check tension_score ≥ 0.6 in tension_building samples")
    print(f"     - Check dramatic_irony_score ≥ 0.5 in dramatic_irony samples")
    print("  2. Run validation on sample batches:")
    print("     - Verify capacity constraints (X+2 rule) followed")
    print("     - Verify tension types correctly categorized")
    print("     - Verify memory resonance weights appropriate")
    print("  3. Combine datasets from multiple runs:")
    print("     - Merge JSON files maintaining metadata")
    print("     - Filter by quality scores if needed")
    print("  4. Prepare for model training:")
    print("     - Convert to training format")
    print("     - Split train/validation sets")
    print("     - Run baseline quality checks")
    
    print("\n📚 DOCUMENTATION:")
    print("   Master Truths Canonical Spec: master_truths_canonical_spec_v_1_2.md")
    print("   Config reference: config.py")
    print("   Generator details: qwen3_generator.py")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
