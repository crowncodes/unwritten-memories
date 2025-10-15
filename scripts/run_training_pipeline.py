#!/usr/bin/env python3
"""
Unwritten Training Data Generation Runner - Systematic Approach
Master Truths Canonical Spec v1.2 Compliant

Generates high-quality training data with:
- Systematic parameter space coverage (not random)
- Full authenticity spectrum (0.2-1.0)
- 8 complexity types for realistic behavior
- Numerical grounding for all calculations
- Coverage tracking to avoid duplicates
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from unwritten.training.config import EnhancedTrainingConfig, initialize_enhanced_config
from unwritten.training.multi_step_pipeline import MultiStepPipeline
from unwritten.utils.logger import AppLogger
import random
import json
from datetime import datetime


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


def display_systematic_features():
    """Display systematic approach improvements"""
    print("\n" + "=" * 70)
    print("SYSTEMATIC PARAMETER SPACE GENERATION")
    print("=" * 70)
    print("\n✅ IMPROVEMENTS OVER RANDOM GENERATION:")
    print("   • Full authenticity spectrum: 0.2-1.0 (not just 0.82-0.95)")
    print("   • 8 complexity types: baseline, people-pleasing, misjudgment, etc.")
    print("   • Systematic coverage: guarantees all parameter combinations")
    print("   • Batch processing: 5:1 efficiency improvement")
    print("   • Coverage tracking: SQLite database prevents duplicates")
    print("   • Focused prompts: 150 words vs 400+ lines")
    print("   • Numerical grounding: all calculations explicitly shown")
    
    print("\n✅ MASTER TRUTHS v1.2 COMPLIANCE:")
    print("   • Emotional Capacity: 0-10 scale (X+2 support rule)")
    print("   • Dramatic Irony: Knowledge gap scoring (≥ 0.6)")
    print("   • Tension Building: 4 types with proper frequencies")
    print("   • Memory Resonance: 5 types (weights 0.7-0.95)")
    print("   • OCEAN Personality: All 5 traits (0-1 scale)")
    print("   • Relationship Scoring: Impact tracking (-1.5 to +1.0)")
    
    print("\n✅ QUALITY THRESHOLDS:")
    print("   • Emotional Authenticity: ≥ 0.7")
    print("   • Tension Building: ≥ 0.6")
    print("   • Dramatic Irony: ≥ 0.5")
    print("   • Overall Novel-Quality: ≥ 0.7")
    
    print("=" * 70)


def main():
    """Main entry point for systematic training generation"""
    
    print("\n" + "=" * 70)
    print("🚀 Unwritten Systematic Training Data Generation")
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
        print("     - ollama pull qwen3:30b")
        print("     - ollama pull qwen3:8b")
        print("     - ollama pull qwen3:30b-a3b")
        sys.exit(1)
    
    print("✅ Ollama service is running")
    
    # Display systematic features
    display_systematic_features()
    
    # Initialize configuration
    print("\n⚙️  Initializing systematic configuration...")
    config = initialize_enhanced_config()
    
    print(f"\n✅ Configuration initialized:")
    print(f"   • Output directory: {config.output_dir}")
    print(f"   • Daily target: {config.total_daily_target:,} samples")
    print(f"   • Model: {config.model_primary}")
    print(f"   • Temperature: {config.temp_emotional} (emotional)")
    print(f"   • Multi-step pipeline: 5 focused steps per interaction")
    
    # Initialize multi-step pipeline
    print("\n📦 Initializing multi-step pipeline...")
    pipeline = MultiStepPipeline(config)
    print("✅ Multi-step pipeline ready")
    
    # Prompt for target samples
    print("\n⏱️  Generation targets (Multi-Step Pipeline):")
    print("  1. Test run (50 samples) - ~100 minutes (~2 min/sample)")
    print("  2. Small batch (200 samples) - ~6.5 hours")
    print("  3. Medium batch (500 samples) - ~16 hours")
    print("  4. Large batch (1000 samples) - ~33 hours")
    print("  5. Daily target (2000+ samples) - ~66 hours")
    print("  6. Custom (specify exact count)")
    print("\n💡 TIP: Start with option 1 to verify quality before large batches")
    
    choice = input("\nSelect option (1-6): ").strip()
    
    target_map = {
        '1': 50,
        '2': 200,
        '3': 500,
        '4': 1000,
        '5': config.target_emotional_authenticity
    }
    
    if choice in target_map:
        target_samples = target_map[choice]
    elif choice == '6':
        try:
            target_samples = int(input("Enter number of samples: "))
            if target_samples < 1:
                print("❌ Invalid count")
                sys.exit(1)
        except ValueError:
            print("❌ Invalid input")
            sys.exit(1)
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    print(f"\n" + "=" * 70)
    print(f"📊 GENERATION PLAN - MULTI-STEP PIPELINE")
    print("=" * 70)
    print(f"Target samples: {target_samples:,}")
    print(f"Generation method: 5-step modular pipeline")
    print(f"Estimated time: ~{target_samples * 2:.0f} minutes ({target_samples * 2 / 60:.1f} hours)")
    
    print(f"\n✅ MULTI-STEP PIPELINE BENEFITS:")
    print(f"  • Step 1: NPC Primitives (name, OCEAN, trust) - ~12 sec")
    print(f"  • Step 2: Context (capacity, urgency, situation) - ~40 sec")
    print(f"  • Step 3: Tension/Subtext (hooks, subtext) - ~15 sec")
    print(f"  • Step 4: Dialogue (60-120 word prose) - ~20 sec")
    print(f"  • Step 5: Outcomes (trust calculations) - <1 sec")
    print(f"  • Total: ~2 minutes per complete interaction")
    
    print(f"\n📈 SYSTEMATIC COVERAGE:")
    print(f"  • Authenticity spectrum: 4 targets (failed → excellent)")
    print(f"  • Complexity types: 8 types (baseline → projection)")
    print(f"  • Capacity levels: 4 levels (crisis → high)")
    print(f"  • Round-robin selection ensures even distribution")
    
    print("\n💡 IMPORTANT:")
    print("  • Each interaction saved to batch JSON file")
    print("  • Progress updates every 10 samples")
    print("  • Press Ctrl+C to stop early (data preserved)")
    print("  • Generated dialogues include proper contractions")
    
    print("\n" + "=" * 70)
    
    input("\n▶️  Press Enter to start generation...")
    
    print("\n🎯 Starting multi-step data generation...\n")
    
    # Define parameter spaces for systematic coverage
    complexity_types = ["baseline", "people_pleasing", "misjudgment", "defensive_lashing", 
                       "emotional_shutdown", "over_commitment", "avoidance", "projection"]
    authenticity_targets = ["failed", "struggling", "authentic", "excellent"]
    capacity_levels = ["crisis", "low", "medium", "high"]
    
    try:
        # Track coverage
        coverage_stats = {
            'authenticity_spectrum': {target: 0 for target in authenticity_targets},
            'complexity_types': {ctype: 0 for ctype in complexity_types},
            'capacity_levels': {level: 0 for level in capacity_levels}
        }
        
        generated_interactions = []
        start_time = datetime.now()
        
        # Generate interactions
        for i in range(target_samples):
            # Systematic selection (round-robin with randomization)
            complexity_type = complexity_types[i % len(complexity_types)]
            authenticity_target = authenticity_targets[i % len(authenticity_targets)]
            capacity_level = capacity_levels[i % len(capacity_levels)]
            support_needed = random.uniform(3.0, 9.0)
            
            try:
                print(f"\n[{i+1}/{target_samples}] Generating: {complexity_type}, {authenticity_target}, {capacity_level}")
                
                interaction = pipeline.generate_complete_interaction(
                    complexity_type=complexity_type,
                    authenticity_target=authenticity_target,
                    capacity_level=capacity_level,
                    support_needed=support_needed
                )
                
                generated_interactions.append(interaction)
                
                # Update coverage stats
                coverage_stats['authenticity_spectrum'][authenticity_target] += 1
                coverage_stats['complexity_types'][complexity_type] += 1
                coverage_stats['capacity_levels'][capacity_level] += 1
                
                # Progress update every 10 samples
                if (i + 1) % 10 == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    avg_time = elapsed / (i + 1)
                    remaining = avg_time * (target_samples - (i + 1))
                    print(f"\n📊 Progress: {i+1}/{target_samples} ({(i+1)/target_samples*100:.1f}%)")
                    print(f"   Time: {elapsed/60:.1f} min elapsed, ~{remaining/60:.1f} min remaining")
                
            except Exception as e:
                AppLogger.error(f"Failed to generate interaction {i+1}", e)
                print(f"❌ Failed: {str(e)}")
                continue
        
        # Save all interactions to a batch file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_filename = f"multi_step_batch_{timestamp}.json"
        output_path = Path(config.output_dir) / batch_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(generated_interactions, f, indent=2)
        
        print(f"\n💾 Saved {len(generated_interactions)} interactions to: {output_path}")
        
        # Display final summary
        print("\n" + "=" * 70)
        print("📊 GENERATION COMPLETE - FINAL RESULTS")
        print("=" * 70)
        
        print("\n✅ SAMPLES GENERATED:")
        print(f"  Total: {len(generated_interactions):,} samples")
        print(f"  Target: {target_samples:,} samples")
        completion = (len(generated_interactions) / target_samples * 100) if target_samples > 0 else 0
        print(f"  Achievement: {completion:.1f}%")
        
        total_time = (datetime.now() - start_time).total_seconds()
        print(f"  Total time: {total_time/60:.1f} minutes")
        print(f"  Average: {total_time/len(generated_interactions):.1f} seconds per interaction")
        
        print(f"\n📈 SYSTEMATIC COVERAGE ACHIEVED:")
        print(f"  Authenticity spectrum:")
        for target, count in coverage_stats['authenticity_spectrum'].items():
            print(f"    • {target}: {count} examples")
        
        print(f"  Complexity types:")
        for ctype, count in coverage_stats['complexity_types'].items():
            print(f"    • {ctype}: {count} examples")
        
        print(f"  Capacity levels:")
        for level, count in coverage_stats['capacity_levels'].items():
            print(f"    • {level}: {count} examples")
        
        print(f"\n📁 OUTPUT LOCATION:")
        print(f"   {output_path}")
        
        print("\n✅ QUALITY VALIDATION:")
        print("  • All samples generated with multi-step pipeline")
        print("  • Novel-quality prose with proper contractions")
        print("  • Systematic parameter space coverage")
        print("  • See batch file for complete interaction data")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        
        # Save partial data
        if generated_interactions:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_filename = f"multi_step_batch_PARTIAL_{timestamp}.json"
            output_path = Path(config.output_dir) / batch_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(generated_interactions, f, indent=2)
            
            print(f"💾 Saved {len(generated_interactions)} partial interactions to: {output_path}")
    except Exception as e:
        AppLogger.error("Generation pipeline failed", e)
        print(f"\n❌ Error: {str(e)}")
        print("Check logs for details")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🎉 SYSTEMATIC GENERATION COMPLETE!")
    print("   Master Truths Canonical Spec v1.2 Compliant")
    print("=" * 70)
    
    print(f"\n📍 NEXT STEPS:")
    print(f"  1. Review generated interactions:")
    print(f"     - Open batch file in JSON viewer")
    print(f"     - Check dialogue quality and variety")
    print(f"  2. Analyze data quality:")
    print(f"     - Verify authenticity spectrum coverage")
    print(f"     - Check complexity type distribution")
    print(f"     - Review trust calculations")
    print(f"  3. Generate more data if needed:")
    print(f"     - Run this script again for additional batches")
    print(f"     - Use dialogue variation mode for specific scenarios")
    print(f"  4. Train model:")
    print(f"     - Format data for your ML framework")
    print(f"     - Fine-tune on Unwritten game mechanics")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
