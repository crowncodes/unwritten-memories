"""
Quick verification that run_training_pipeline.py imports work correctly.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

print("Testing imports...")

try:
    from unwritten.training.config import EnhancedTrainingConfig, initialize_enhanced_config
    print("✅ Config imports OK")
    
    from unwritten.training.multi_step_pipeline import MultiStepPipeline
    print("✅ MultiStepPipeline import OK")
    
    from unwritten.utils.logger import AppLogger
    print("✅ AppLogger import OK")
    
    import random
    import json
    from datetime import datetime
    print("✅ Standard library imports OK")
    
    # Try initializing config
    config = initialize_enhanced_config()
    print("✅ Config initialization OK")
    
    # Try initializing pipeline
    pipeline = MultiStepPipeline(config)
    print("✅ Pipeline initialization OK")
    
    print("\n🎉 All imports and initialization successful!")
    print("run_training_pipeline.py is ready to use.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


