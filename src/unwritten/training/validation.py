"""
Comprehensive Training Data Validation
Master Truths Canonical Spec v1.2 Compliant

Validates generated training data against:
1. Authenticity spectrum requirements (0.2-1.0 coverage)
2. Complexity type coverage (8 types)
3. Capacity constraint adherence (X+2 rule)
4. Numerical grounding accuracy
5. Realistic response validation
"""

from typing import Dict, List, Tuple
import re


class TrainingDataValidator:
    """Validates training data quality and compliance"""
    
    def __init__(self, config):
        """Initialize validator with configuration"""
        self.config = config
        self.validation_errors = []
        self.validation_warnings = []
    
    # ===================================================================
    # SPECTRUM VALIDATION
    # ===================================================================
    
    def validate_authenticity_spectrum(self, samples: List[Dict]) -> Dict:
        """
        Validate that samples cover full authenticity spectrum.
        
        Requirements:
        - At least 2 failed examples (0.2-0.4)
        - At least 3 struggling examples (0.4-0.6)
        - At least 4 authentic examples (0.6-0.8)
        - At least 3 excellent examples (0.8-1.0)
        - Not more than 40% excellent
        """
        scores = [s.get('authenticity_score', 0.8) for s in samples]
        
        distribution = {
            'failed': sum(1 for s in scores if 0.2 <= s < 0.4),
            'struggling': sum(1 for s in scores if 0.4 <= s < 0.6),
            'authentic': sum(1 for s in scores if 0.6 <= s < 0.8),
            'excellent': sum(1 for s in scores if 0.8 <= s <= 1.0)
        }
        
        total = len(scores)
        
        # Check requirements
        requirements = self.config.systematic_coverage['authenticity_spectrum']
        passed = True
        issues = []
        
        for tier, config in requirements.items():
            min_required = config['min_examples']
            actual = distribution.get(tier, 0)
            
            if actual < min_required:
                passed = False
                issues.append(f"{tier}: need {min_required}, got {actual}")
        
        # Check not too many excellent
        excellent_pct = distribution['excellent'] / total if total > 0 else 0
        max_excellent = self.config.quality_thresholds_enhanced['spectrum_coverage']['max_excellent_percentage']
        
        if excellent_pct > max_excellent:
            passed = False
            issues.append(f"Too many excellent: {excellent_pct:.1%} > {max_excellent:.1%}")
        
        # Check variance
        if len(scores) > 1:
            import statistics
            variance = statistics.variance(scores)
            min_variance = self.config.quality_thresholds_enhanced['spectrum_coverage']['authenticity_variance']
            
            if variance < min_variance:
                passed = False
                issues.append(f"Low variance: {variance:.3f} < {min_variance}")
        
        return {
            'passed': passed,
            'distribution': distribution,
            'total_samples': total,
            'excellent_percentage': excellent_pct,
            'issues': issues,
            'validation_type': 'authenticity_spectrum'
        }
    
    # ===================================================================
    # COMPLEXITY VALIDATION
    # ===================================================================
    
    def validate_complexity_coverage(self, samples: List[Dict]) -> Dict:
        """
        Validate that samples cover required complexity types.
        
        Requirements:
        - At least 5 different complexity types
        - No more than 30% baseline (simple examples)
        - At least 2 people-pleasing examples
        """
        complexity_counts = {}
        
        for sample in samples:
            # Try different fields where complexity might be stored
            complexity = (
                sample.get('complexity_type') or
                sample.get('complexity_exhibited') or
                sample.get('_systematic_metadata', {}).get('complexity_type', 'unknown')
            )
            
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        total = len(samples)
        types_covered = len([c for c in complexity_counts if c != 'unknown'])
        
        # Check requirements
        requirements = self.config.quality_thresholds_enhanced['complexity_coverage']
        passed = True
        issues = []
        
        # Minimum types
        min_types = requirements['min_complexity_types']
        if types_covered < min_types:
            passed = False
            issues.append(f"Too few complexity types: {types_covered} < {min_types}")
        
        # Baseline percentage
        baseline_count = complexity_counts.get('baseline', 0)
        baseline_pct = baseline_count / total if total > 0 else 0
        max_baseline = requirements['baseline_percentage']
        
        if baseline_pct > max_baseline:
            passed = False
            issues.append(f"Too many baseline: {baseline_pct:.1%} > {max_baseline:.1%}")
        
        # People-pleasing requirement
        people_pleasing = complexity_counts.get('people_pleasing', 0)
        required_people_pleasing = requirements['required_people_pleasing']
        
        if people_pleasing < required_people_pleasing:
            passed = False
            issues.append(f"Need {required_people_pleasing} people-pleasing, got {people_pleasing}")
        
        return {
            'passed': passed,
            'types_covered': types_covered,
            'complexity_counts': complexity_counts,
            'total_samples': total,
            'baseline_percentage': baseline_pct,
            'issues': issues,
            'validation_type': 'complexity_coverage'
        }
    
    # ===================================================================
    # CAPACITY CONSTRAINT VALIDATION (X+2 RULE)
    # ===================================================================
    
    def validate_capacity_constraints(self, samples: List[Dict]) -> Dict:
        """
        Validate capacity constraints (X+2 rule).
        
        Characters can provide support up to capacity + 2.
        If request exceeds capacity + 2, character MUST show limitation.
        """
        violations = []
        
        for i, sample in enumerate(samples):
            capacity = sample.get('effective_capacity', 5.0)
            support_needed = sample.get('support_level_needed', 5.0)
            max_support = capacity + 2
            
            # If support exceeds capacity + 2, must show limitation
            if support_needed > max_support:
                response = sample.get('character_response', '').lower()
                
                # Check for limitation signals
                limitation_signals = [
                    "can't", "cannot", "unable", "sorry", "don't have",
                    "need to", "have to", "later", "tomorrow", "not right now",
                    "too much", "overwhelmed", "exhausted", "wiped",
                    "running on empty", "barely", "can barely"
                ]
                
                has_limitation = any(signal in response for signal in limitation_signals)
                
                if not has_limitation:
                    violations.append({
                        'sample_index': i,
                        'capacity': capacity,
                        'support_needed': support_needed,
                        'max_support': max_support,
                        'issue': 'Character acts beyond capacity without showing limitation',
                        'response_preview': response[:100]
                    })
        
        total = len(samples)
        violation_count = len(violations)
        pass_rate = ((total - violation_count) / total * 100) if total > 0 else 0
        
        # Check tolerance
        tolerance = self.config.quality_thresholds_enhanced['constraint_realism']['capacity_violation_tolerance']
        violation_rate = violation_count / total if total > 0 else 0
        passed = violation_rate <= tolerance
        
        return {
            'passed': passed,
            'total_samples': total,
            'violations': violation_count,
            'pass_rate': pass_rate,
            'violation_rate': violation_rate,
            'tolerance': tolerance,
            'violation_details': violations[:5],  # First 5 violations
            'validation_type': 'capacity_constraints'
        }
    
    # ===================================================================
    # NUMERICAL GROUNDING VALIDATION
    # ===================================================================
    
    def validate_numerical_grounding(self, sample: Dict) -> Dict:
        """
        Validate numerical grounding in a single sample.
        
        Checks:
        1. Calculation steps shown explicitly
        2. Math is correct (within tolerance)
        3. Tier identification present
        4. Formula used correctly
        """
        issues = []
        warnings = []
        
        # Check capacity calculation
        if 'capacity_factors' in sample:
            capacity_result = self._validate_capacity_calculation(sample)
            if not capacity_result['passed']:
                issues.extend(capacity_result['issues'])
            warnings.extend(capacity_result.get('warnings', []))
        
        # Check relationship impact calculation
        if 'relationship_impact' in sample:
            impact_result = self._validate_impact_calculation(sample)
            if not impact_result['passed']:
                issues.extend(impact_result['issues'])
            warnings.extend(impact_result.get('warnings', []))
        
        # Check authenticity scoring
        if 'authenticity_score' in sample:
            auth_result = self._validate_authenticity_scoring(sample)
            if not auth_result['passed']:
                issues.extend(auth_result['issues'])
            warnings.extend(auth_result.get('warnings', []))
        
        grounding_score = 1.0 - (len(issues) * 0.2) - (len(warnings) * 0.05)
        grounding_score = max(0.0, grounding_score)
        
        min_score = self.config.numerical_grounding['min_grounding_score']
        passed = grounding_score >= min_score and len(issues) == 0
        
        return {
            'passed': passed,
            'grounding_score': grounding_score,
            'min_required': min_score,
            'issues': issues,
            'warnings': warnings,
            'validation_type': 'numerical_grounding'
        }
    
    def _validate_capacity_calculation(self, sample: Dict) -> Dict:
        """Validate capacity calculation math"""
        issues = []
        warnings = []
        
        base = sample.get('base_capacity', 5.0)
        factors = sample.get('capacity_factors', [])
        effective = sample.get('effective_capacity', 5.0)
        
        # Calculate expected value
        stressor_sum = sum(f.get('reduction', 0) for f in factors if f.get('factor_type') == 'stressor')
        boost_sum = sum(f.get('boost', 0) for f in factors if f.get('factor_type') == 'boost')
        
        expected = base - stressor_sum + boost_sum
        expected = max(0.0, min(10.0, expected))  # Clamp 0-10
        
        # Check math accuracy
        max_error = self.config.calculation_validation['capacity_calculation']['max_math_error']
        error = abs(expected - effective)
        
        if error > max_error:
            issues.append(f"Capacity calculation error: expected {expected:.1f}, got {effective:.1f}")
        
        # Check for reasoning
        if self.config.calculation_validation['capacity_calculation']['require_base_reasoning']:
            if 'capacity_reasoning' not in sample and 'reasoning' not in sample:
                warnings.append("Missing capacity calculation reasoning")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    def _validate_impact_calculation(self, sample: Dict) -> Dict:
        """Validate relationship impact calculation"""
        issues = []
        warnings = []
        
        impact = sample.get('relationship_impact', 0.0)
        
        # Check if in valid range
        if not (-2.0 <= impact <= 1.0):
            issues.append(f"Impact out of range: {impact} not in [-2.0, 1.0]")
        
        # Check for reasoning
        if 'impact_reasoning' not in sample and 'relationship_impact_reasoning' not in sample:
            warnings.append("Missing impact calculation reasoning")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    def _validate_authenticity_scoring(self, sample: Dict) -> Dict:
        """Validate authenticity score reasoning"""
        issues = []
        warnings = []
        
        score = sample.get('authenticity_score', 0.8)
        
        # Check if in valid range
        if not (0.0 <= score <= 1.0):
            issues.append(f"Authenticity score out of range: {score}")
        
        # Check for reasoning
        reasoning = sample.get('authenticity_reasoning', '') or sample.get('reasoning', '')
        min_length = self.config.calculation_validation['authenticity_scoring']['min_reasoning_length']
        
        if len(reasoning) < min_length:
            warnings.append(f"Authenticity reasoning too short: {len(reasoning)} < {min_length} chars")
        
        # Check tier consistency
        capacity = sample.get('effective_capacity', 5.0)
        support_needed = sample.get('support_level_needed', 5.0)
        response = sample.get('character_response', '')
        
        # If capacity very low and they help anyway, score should reflect inauthenticity
        if capacity < 2.0 and support_needed > capacity + 2 and "yes" in response.lower():
            if score > 0.6:
                warnings.append(f"Score {score} seems high for low capacity overcommitment")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    # ===================================================================
    # REALISTIC RESPONSE VALIDATION
    # ===================================================================
    
    def validate_realistic_responses(self, samples: List[Dict]) -> Dict:
        """
        Validate that responses are realistic (not melodramatic or unrealistic).
        
        Checks for:
        - Unrealistic resilience (acting beyond capacity with no cost)
        - Melodrama (overly dramatic responses)
        - Inconsistent behavior
        """
        unrealistic_resilience = []
        melodrama = []
        
        for i, sample in enumerate(samples):
            capacity = sample.get('effective_capacity', 5.0)
            support_needed = sample.get('support_level_needed', 5.0)
            response = sample.get('character_response', '').lower()
            
            # Check for unrealistic resilience
            if capacity < 3.0 and support_needed > 7.0:
                # Very low capacity, very high need
                positive_signals = ["of course", "no problem", "happy to", "glad to", "definitely"]
                if any(signal in response for signal in positive_signals):
                    unrealistic_resilience.append(i)
            
            # Check for melodrama
            melodrama_signals = ["absolutely devastated", "completely destroyed", 
                                "utterly impossible", "totally broken", "entirely shattered"]
            if any(signal in response for signal in melodrama_signals):
                melodrama.append(i)
        
        total = len(samples)
        resilience_rate = len(unrealistic_resilience) / total if total > 0 else 0
        melodrama_rate = len(melodrama) / total if total > 0 else 0
        
        thresholds = self.config.quality_thresholds_enhanced['constraint_realism']
        resilience_threshold = thresholds['unrealistic_resilience_threshold']
        melodrama_threshold = thresholds['melodrama_threshold']
        
        passed = (resilience_rate <= resilience_threshold and 
                 melodrama_rate <= melodrama_threshold)
        
        return {
            'passed': passed,
            'total_samples': total,
            'unrealistic_resilience_count': len(unrealistic_resilience),
            'unrealistic_resilience_rate': resilience_rate,
            'melodrama_count': len(melodrama),
            'melodrama_rate': melodrama_rate,
            'issues': [],
            'validation_type': 'realistic_responses'
        }
    
    # ===================================================================
    # COMPREHENSIVE VALIDATION
    # ===================================================================
    
    def validate_batch(self, samples: List[Dict]) -> Dict:
        """
        Run all validations on a batch of samples.
        
        Returns comprehensive validation report.
        """
        results = {
            'total_samples': len(samples),
            'validations': {},
            'overall_passed': True,
            'critical_failures': [],
            'warnings': []
        }
        
        # Run all validations
        validations = [
            ('authenticity_spectrum', self.validate_authenticity_spectrum),
            ('complexity_coverage', self.validate_complexity_coverage),
            ('capacity_constraints', self.validate_capacity_constraints),
            ('realistic_responses', self.validate_realistic_responses)
        ]
        
        for name, validator_func in validations:
            result = validator_func(samples)
            results['validations'][name] = result
            
            if not result['passed']:
                results['overall_passed'] = False
                results['critical_failures'].append(name)
                
                if 'issues' in result:
                    results['warnings'].extend([
                        f"{name}: {issue}" for issue in result['issues']
                    ])
        
        # Numerical grounding validation (sample-level)
        grounding_scores = []
        grounding_failures = 0
        
        for sample in samples:
            grounding_result = self.validate_numerical_grounding(sample)
            grounding_scores.append(grounding_result['grounding_score'])
            
            if not grounding_result['passed']:
                grounding_failures += 1
        
        avg_grounding = sum(grounding_scores) / len(grounding_scores) if grounding_scores else 0
        grounding_pass_rate = 1.0 - (grounding_failures / len(samples)) if samples else 0
        
        results['validations']['numerical_grounding'] = {
            'passed': grounding_pass_rate >= 0.8,  # 80% must pass
            'average_score': avg_grounding,
            'pass_rate': grounding_pass_rate,
            'failures': grounding_failures,
            'validation_type': 'numerical_grounding'
        }
        
        if grounding_pass_rate < 0.8:
            results['overall_passed'] = False
            results['critical_failures'].append('numerical_grounding')
        
        return results
    
    def get_validation_summary(self, validation_results: Dict) -> str:
        """Get human-readable validation summary"""
        lines = []
        lines.append("=" * 70)
        lines.append("VALIDATION SUMMARY")
        lines.append("=" * 70)
        
        overall = "✅ PASSED" if validation_results['overall_passed'] else "❌ FAILED"
        lines.append(f"\nOverall: {overall}")
        lines.append(f"Total samples: {validation_results['total_samples']}")
        
        lines.append("\nValidation Results:")
        for name, result in validation_results['validations'].items():
            status = "✅" if result['passed'] else "❌"
            lines.append(f"  {status} {name}")
            
            if not result['passed'] and 'issues' in result:
                for issue in result['issues'][:3]:  # Show first 3 issues
                    lines.append(f"      - {issue}")
        
        if validation_results['critical_failures']:
            lines.append(f"\nCritical failures: {', '.join(validation_results['critical_failures'])}")
        
        if validation_results['warnings']:
            lines.append(f"\nWarnings ({len(validation_results['warnings'])}):")
            for warning in validation_results['warnings'][:5]:  # Show first 5
                lines.append(f"  ⚠️  {warning}")
        
        lines.append("=" * 70)
        return "\n".join(lines)

