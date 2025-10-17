#!/usr/bin/env python3
"""
Training Data Analysis & Combination Tool
Master Truths v1.2 Compliant

Analyzes, validates, combines, and exports training data batches
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import statistics


class TrainingDataAnalyzer:
    """Analyze and process Master Truths v1.2 training data"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.data_by_type = defaultdict(list)
        self.quality_stats = {}
        
    def load_all_batches(self) -> Dict[str, int]:
        """Load all batch files from output directory"""
        files = list(self.output_dir.glob("*.json"))
        
        print(f"📂 Found {len(files)} batch files")
        
        counts = defaultdict(int)
        
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle both formats
                if 'samples' in data:
                    data_type = data.get('data_type', 'unknown')
                    samples = data['samples']
                elif isinstance(data, list):
                    # Infer type from filename
                    data_type = self._infer_type_from_filename(file.name)
                    samples = data
                else:
                    print(f"⚠️  Skipping {file.name}: unknown format")
                    continue
                
                self.data_by_type[data_type].extend(samples)
                counts[data_type] += len(samples)
                
            except Exception as e:
                print(f"❌ Error loading {file.name}: {e}")
        
        print(f"\n✅ Loaded {sum(counts.values()):,} total samples")
        for dtype, count in counts.items():
            print(f"   • {dtype}: {count:,}")
        
        return counts
    
    def _infer_type_from_filename(self, filename: str) -> str:
        """Infer data type from filename"""
        filename_lower = filename.lower()
        
        if 'emotional' in filename_lower:
            return 'emotional_authenticity'
        elif 'dramatic' in filename_lower:
            return 'dramatic_irony'
        elif 'tension' in filename_lower:
            return 'tension_building'
        elif 'memory' in filename_lower:
            return 'memory_resonance'
        elif 'personality' in filename_lower:
            return 'personality_traits'
        elif 'relationship' in filename_lower:
            return 'relationship_scoring'
        else:
            return 'unknown'
    
    def analyze_quality(self) -> Dict[str, Dict]:
        """Analyze quality metrics for each data type"""
        print("\n📊 Analyzing Quality Metrics...")
        
        for data_type, samples in self.data_by_type.items():
            if not samples:
                continue
            
            stats = {
                'total_samples': len(samples),
                'quality_scores': [],
                'excellent': 0,  # ≥ 0.9
                'good': 0,       # 0.7-0.89
                'acceptable': 0, # 0.5-0.69
                'poor': 0,       # < 0.5
                'missing_scores': 0,
                'avg_score': 0.0,
                'median_score': 0.0,
                'min_score': 1.0,
                'max_score': 0.0
            }
            
            # Get appropriate score field
            score_field = self._get_score_field(data_type)
            
            for sample in samples:
                score = sample.get(score_field, None)
                
                if score is None:
                    stats['missing_scores'] += 1
                    continue
                
                stats['quality_scores'].append(score)
                
                if score >= 0.9:
                    stats['excellent'] += 1
                elif score >= 0.7:
                    stats['good'] += 1
                elif score >= 0.5:
                    stats['acceptable'] += 1
                else:
                    stats['poor'] += 1
            
            # Calculate statistics
            if stats['quality_scores']:
                stats['avg_score'] = statistics.mean(stats['quality_scores'])
                stats['median_score'] = statistics.median(stats['quality_scores'])
                stats['min_score'] = min(stats['quality_scores'])
                stats['max_score'] = max(stats['quality_scores'])
            
            self.quality_stats[data_type] = stats
        
        return self.quality_stats
    
    def _get_score_field(self, data_type: str) -> str:
        """Get the appropriate quality score field for data type"""
        score_fields = {
            'emotional_authenticity': 'authenticity_score',
            'dramatic_irony': 'dramatic_irony_score',
            'tension_building': 'tension_score',
            'memory_resonance': 'emotional_authenticity',
            'personality_traits': 'quality_score',
            'relationship_scoring': 'quality_score'
        }
        return score_fields.get(data_type, 'quality_score')
    
    def print_quality_report(self):
        """Print detailed quality report"""
        print("\n" + "="*70)
        print("QUALITY ANALYSIS REPORT")
        print("="*70)
        
        for data_type, stats in self.quality_stats.items():
            print(f"\n📋 {data_type.upper().replace('_', ' ')}")
            print("-" * 70)
            print(f"Total Samples: {stats['total_samples']:,}")
            
            if stats['quality_scores']:
                print(f"\nQuality Distribution:")
                print(f"  ⭐⭐⭐ Excellent (≥ 0.9): {stats['excellent']:,} ({stats['excellent']/stats['total_samples']*100:.1f}%)")
                print(f"  ⭐⭐  Good (0.7-0.89):    {stats['good']:,} ({stats['good']/stats['total_samples']*100:.1f}%)")
                print(f"  ⭐    Acceptable (0.5-0.69): {stats['acceptable']:,} ({stats['acceptable']/stats['total_samples']*100:.1f}%)")
                print(f"  ❌    Poor (< 0.5):     {stats['poor']:,} ({stats['poor']/stats['total_samples']*100:.1f}%)")
                
                if stats['missing_scores'] > 0:
                    print(f"  ⚠️    Missing Score:    {stats['missing_scores']:,}")
                
                print(f"\nStatistics:")
                print(f"  Average:  {stats['avg_score']:.3f}")
                print(f"  Median:   {stats['median_score']:.3f}")
                print(f"  Min:      {stats['min_score']:.3f}")
                print(f"  Max:      {stats['max_score']:.3f}")
                
                # Master Truths v1.2 threshold check
                threshold = self._get_threshold(data_type)
                passing = stats['excellent'] + stats['good']
                pass_rate = (passing / stats['total_samples']) * 100
                
                print(f"\nMaster Truths v1.2 Compliance:")
                print(f"  Threshold: ≥ {threshold}")
                print(f"  Passing: {passing:,} ({pass_rate:.1f}%)")
                
                if pass_rate >= 80:
                    print(f"  Status: ✅ EXCELLENT (≥ 80% passing)")
                elif pass_rate >= 60:
                    print(f"  Status: ⚠️  ACCEPTABLE (60-80% passing)")
                else:
                    print(f"  Status: ❌ NEEDS IMPROVEMENT (< 60% passing)")
    
    def _get_threshold(self, data_type: str) -> float:
        """Get Master Truths v1.2 quality threshold"""
        thresholds = {
            'emotional_authenticity': 0.7,
            'dramatic_irony': 0.5,
            'tension_building': 0.6,
            'memory_resonance': 0.7,
            'personality_traits': 0.6,
            'relationship_scoring': 0.6
        }
        return thresholds.get(data_type, 0.7)
    
    def filter_by_quality(self, min_score: float = 0.7) -> Dict[str, List]:
        """Filter samples by minimum quality score"""
        print(f"\n🔍 Filtering samples (minimum score: {min_score})")
        
        filtered = {}
        
        for data_type, samples in self.data_by_type.items():
            score_field = self._get_score_field(data_type)
            
            filtered_samples = [
                s for s in samples 
                if s.get(score_field, 0) >= min_score
            ]
            
            filtered[data_type] = filtered_samples
            
            original = len(samples)
            kept = len(filtered_samples)
            removed = original - kept
            
            print(f"  {data_type}: {kept:,} / {original:,} ({kept/original*100:.1f}% kept, {removed:,} removed)")
        
        return filtered
    
    def combine_batches(self, output_file: str = "combined_training_data.json",
                       min_quality: float = 0.0):
        """Combine all batches into single files per data type"""
        print(f"\n📦 Combining batches (min_quality: {min_quality})")
        
        if min_quality > 0:
            data_to_combine = self.filter_by_quality(min_quality)
        else:
            data_to_combine = self.data_by_type
        
        output_path = self.output_dir / output_file
        
        combined = {
            'master_truths_version': 'v1.2',
            'combined_date': str(Path().cwd()),
            'min_quality_filter': min_quality,
            'data_types': {}
        }
        
        for data_type, samples in data_to_combine.items():
            combined['data_types'][data_type] = {
                'sample_count': len(samples),
                'samples': samples
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        
        total_samples = sum(len(s) for s in data_to_combine.values())
        print(f"\n✅ Combined {total_samples:,} samples into: {output_path}")
        
        return str(output_path)
    
    def export_by_type(self, min_quality: float = 0.0):
        """Export separate files for each data type"""
        print(f"\n📤 Exporting by type (min_quality: {min_quality})")
        
        if min_quality > 0:
            data_to_export = self.filter_by_quality(min_quality)
        else:
            data_to_export = self.data_by_type
        
        exported_files = []
        
        for data_type, samples in data_to_export.items():
            if not samples:
                continue
            
            filename = f"{data_type}_combined_v1.2.json"
            filepath = self.output_dir / filename
            
            output = {
                'master_truths_version': 'v1.2',
                'data_type': data_type,
                'sample_count': len(samples),
                'min_quality_filter': min_quality,
                'samples': samples
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            exported_files.append(str(filepath))
            print(f"  ✅ {data_type}: {len(samples):,} samples → {filename}")
        
        return exported_files
    
    def validate_capacity_constraints(self) -> Dict[str, List]:
        """Validate that emotional authenticity samples follow X+2 rule"""
        print("\n🔍 Validating Capacity Constraints (X+2 rule)...")
        
        violations = []
        
        if 'emotional_authenticity' not in self.data_by_type:
            print("  ⚠️  No emotional_authenticity data to validate")
            return {}
        
        samples = self.data_by_type['emotional_authenticity']
        
        for i, sample in enumerate(samples):
            capacity = sample.get('effective_capacity', 0)
            max_support = capacity + 2
            support_needed = sample.get('support_level_needed', 0)
            response = sample.get('character_response', '').lower()
            
            # If support needed exceeds capacity+2, should show limitation
            if support_needed > max_support:
                # Check for limitation signals
                limitation_signals = [
                    "can't", "cannot", "unable", "sorry", "tired", 
                    "wiped", "exhausted", "don't have", "need to",
                    "have to", "later", "tomorrow", "running on empty"
                ]
                
                has_limitation = any(signal in response for signal in limitation_signals)
                
                if not has_limitation:
                    violations.append({
                        'sample_index': i,
                        'capacity': capacity,
                        'max_support': max_support,
                        'support_needed': support_needed,
                        'issue': 'Character acts beyond capacity without showing limitation',
                        'response_preview': response[:100]
                    })
        
        total = len(samples)
        violation_count = len(violations)
        pass_rate = ((total - violation_count) / total * 100) if total > 0 else 0
        
        print(f"\n  Total Samples: {total:,}")
        print(f"  Violations: {violation_count:,}")
        print(f"  Pass Rate: {pass_rate:.1f}%")
        
        if pass_rate >= 95:
            print(f"  Status: ✅ EXCELLENT (≥ 95% compliance)")
        elif pass_rate >= 85:
            print(f"  Status: ⚠️  GOOD (85-95% compliance)")
        else:
            print(f"  Status: ❌ NEEDS IMPROVEMENT (< 85% compliance)")
        
        if violations:
            print(f"\n  ⚠️  Sample violations (first 5):")
            for v in violations[:5]:
                print(f"    - Sample {v['sample_index']}: "
                      f"capacity {v['capacity']}, needs {v['support_needed']}, "
                      f"max {v['max_support']}")
        
        return {'violations': violations, 'pass_rate': pass_rate}
    
    def generate_training_splits(self, train_ratio: float = 0.8,
                                val_ratio: float = 0.1,
                                test_ratio: float = 0.1):
        """Split data into train/validation/test sets"""
        import random
        
        print(f"\n✂️  Generating Training Splits ({train_ratio}/{val_ratio}/{test_ratio})")
        
        splits = {
            'train': {},
            'validation': {},
            'test': {}
        }
        
        for data_type, samples in self.data_by_type.items():
            if not samples:
                continue
            
            # Shuffle samples
            shuffled = samples.copy()
            random.shuffle(shuffled)
            
            total = len(shuffled)
            train_end = int(total * train_ratio)
            val_end = train_end + int(total * val_ratio)
            
            splits['train'][data_type] = shuffled[:train_end]
            splits['validation'][data_type] = shuffled[train_end:val_end]
            splits['test'][data_type] = shuffled[val_end:]
            
            print(f"  {data_type}:")
            print(f"    Train: {len(splits['train'][data_type]):,}")
            print(f"    Val:   {len(splits['validation'][data_type]):,}")
            print(f"    Test:  {len(splits['test'][data_type]):,}")
        
        # Save splits
        for split_name, split_data in splits.items():
            filename = f"{split_name}_set_v1.2.json"
            filepath = self.output_dir / filename
            
            output = {
                'master_truths_version': 'v1.2',
                'split': split_name,
                'data': split_data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            total_samples = sum(len(s) for s in split_data.values())
            print(f"\n✅ Saved {split_name} set: {total_samples:,} samples → {filename}")
        
        return splits


def main():
    parser = argparse.ArgumentParser(
        description='Analyze and process Master Truths v1.2 training data'
    )
    parser.add_argument(
        'output_dir',
        help='Directory containing training data batches'
    )
    parser.add_argument(
        '--analyze', '-a',
        action='store_true',
        help='Analyze quality metrics'
    )
    parser.add_argument(
        '--combine', '-c',
        action='store_true',
        help='Combine all batches into single file'
    )
    parser.add_argument(
        '--export-by-type', '-e',
        action='store_true',
        help='Export separate files by data type'
    )
    parser.add_argument(
        '--validate-capacity', '-v',
        action='store_true',
        help='Validate capacity constraints (X+2 rule)'
    )
    parser.add_argument(
        '--generate-splits', '-s',
        action='store_true',
        help='Generate train/val/test splits'
    )
    parser.add_argument(
        '--min-quality', '-q',
        type=float,
        default=0.0,
        help='Minimum quality score to include (default: 0.0)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all analysis and export operations'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("TRAINING DATA ANALYSIS & PROCESSING")
    print("Master Truths Canonical Spec v1.2")
    print("="*70)
    
    analyzer = TrainingDataAnalyzer(args.output_dir)
    
    # Load all batches
    analyzer.load_all_batches()
    
    # Analyze quality
    if args.analyze or args.all:
        analyzer.analyze_quality()
        analyzer.print_quality_report()
    
    # Validate capacity constraints
    if args.validate_capacity or args.all:
        analyzer.validate_capacity_constraints()
    
    # Combine batches
    if args.combine or args.all:
        analyzer.combine_batches(min_quality=args.min_quality)
    
    # Export by type
    if args.export_by_type or args.all:
        analyzer.export_by_type(min_quality=args.min_quality)
    
    # Generate splits
    if args.generate_splits or args.all:
        analyzer.generate_training_splits()
    
    print("\n" + "="*70)
    print("✅ Analysis Complete!")
    print("="*70)


if __name__ == "__main__":
    main()

