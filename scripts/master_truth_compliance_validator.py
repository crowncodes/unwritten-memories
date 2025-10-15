#!/usr/bin/env python3
"""
Master Truth Compliance Validator

Validates specification documents against Master Truths v1.2 canonical spec.
Identifies contradictions, divergences, and missing integrations.

Usage:
    python master_truth_compliance_validator.py --doc <path> [--fix]
    python master_truth_compliance_validator.py --scan-all
    python master_truth_compliance_validator.py --report

Author: Unwritten Team
Version: 1.0.0
Compliance: master_truths_canonical_spec_v_1_2.md
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ComplianceIssue:
    """Represents a single compliance issue."""
    severity: str  # CRITICAL, MAJOR, MINOR
    category: str  # terminology, pricing, scale, integration, missing
    issue: str
    location: str  # file:line
    master_truth_ref: str  # Section reference in Master Truths
    current_value: str
    expected_value: str
    fix_suggestion: Optional[str] = None


@dataclass
class ComplianceReport:
    """Complete compliance report for a document."""
    document_path: str
    scan_timestamp: str
    overall_score: float  # 0.0-1.0
    critical_issues: List[ComplianceIssue]
    major_issues: List[ComplianceIssue]
    minor_issues: List[ComplianceIssue]
    strengths: List[str]
    
    def to_dict(self):
        return {
            'document_path': self.document_path,
            'scan_timestamp': self.scan_timestamp,
            'overall_score': self.overall_score,
            'critical_issues': [asdict(i) for i in self.critical_issues],
            'major_issues': [asdict(i) for i in self.major_issues],
            'minor_issues': [asdict(i) for i in self.minor_issues],
            'strengths': self.strengths
        }


class MasterTruthValidator:
    """Validates documents against Master Truths v1.2."""
    
    # Canonical vocabulary from Master Truths v1.2
    CANONICAL_TERMS = {
        'emotional_states': {
            'deprecated': {'DRAINED': 'EXHAUSTED'},
            'canonical': [
                'EXHAUSTED', 'OVERWHELMED', 'MOTIVATED', 'INSPIRED', 
                'EXCITED', 'CONFIDENT', 'CONTENT', 'PEACEFUL', 'GRATEFUL', 
                'REFLECTIVE', 'FRUSTRATED', 'ANXIOUS', 'RESTLESS', 'PASSIONATE',
                'MELANCHOLY', 'DISCOURAGED', 'NUMB', 'CURIOUS', 'FOCUSED', 'BALANCED'
            ]
        },
        'relationship_levels': {
            'range': (0, 5),
            'level_0': 'Not Met',
            'display_rule': 'Never display "Level 0"'
        },
        'trust_scale': {
            'range': (0.0, 1.0),
            'type': 'continuous'
        },
        'emotional_capacity': {
            'range': (0.0, 10.0),
            'default': 5.0,
            'support_rule': 'capacity + 2',
            'crisis_threshold': 1.0
        },
        'season_lengths': [12, 24, 36],
        'turns_per_day': 3,
        'subscription_pricing': {
            'Plus': '$14.99/month',
            'Ultimate': '$29.99/month'
        },
        'urgency_multipliers': {
            'routine': 1.0,
            'important': 2.0,
            'urgent': 3.0,
            'crisis': 5.0
        },
        'memory_resonance_weights': {
            'same_emotion_different_context': 0.8,
            'opposite_emotion_growth': 0.9,
            'past_trauma_trigger': 0.95,
            'past_joy_current_sadness': 0.85,
            'emotional_growth_callback': 0.7
        },
        'novel_quality_thresholds': {
            'emotional_authenticity': 0.7,
            'tension_building': 0.6,
            'dramatic_irony': 0.5,
            'hook_effectiveness': 0.6,
            'overall': 0.7
        },
        'tension_frequency': {
            'level_1_2': '1 in 3',
            'level_3_4': '1 in 2',
            'level_5': 'nearly every'
        }
    }
    
    def __init__(self, master_truth_path: Optional[Path] = None):
        """Initialize validator with optional Master Truths document path."""
        self.master_truth_path = master_truth_path or Path("docs/master_truths_canonical_spec_v_1_2.md")
        self.master_truth_version = "v1.2"
        
    def validate_document(self, doc_path: Path) -> ComplianceReport:
        """Validate a single document against Master Truths."""
        print(f"Validating: {doc_path}")
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        critical_issues = []
        major_issues = []
        minor_issues = []
        strengths = []
        
        # Check 1: Emotional State Terminology
        critical_issues.extend(self._check_emotional_states(content, lines, doc_path))
        
        # Check 2: Subscription Pricing
        critical_issues.extend(self._check_subscription_pricing(content, lines, doc_path))
        
        # Check 3: Relationship Levels Scale
        major_issues.extend(self._check_relationship_levels(content, lines, doc_path))
        
        # Check 4: Emotional Capacity Scale
        major_issues.extend(self._check_emotional_capacity(content, lines, doc_path))
        
        # Check 5: NPC Response Framework Integration
        major_issues.extend(self._check_npc_response_framework(content, lines, doc_path))
        
        # Check 6: Memory Resonance Factors
        minor_issues.extend(self._check_memory_resonance(content, lines, doc_path))
        
        # Check 7: Tension Injection Framework
        minor_issues.extend(self._check_tension_framework(content, lines, doc_path))
        
        # Check 8: Novel Quality Thresholds
        minor_issues.extend(self._check_quality_thresholds(content, lines, doc_path))
        
        # Check 9: Compliance Checklist Present
        if not self._has_compliance_checklist(content):
            minor_issues.append(ComplianceIssue(
                severity="MINOR",
                category="missing",
                issue="Document missing Master Truths v1.2 compliance checklist",
                location=f"{doc_path}:end",
                master_truth_ref="Section 13",
                current_value="No checklist found",
                expected_value="Compliance checklist at end of document",
                fix_suggestion="Add compliance checklist from Master Truths Section 13"
            ))
        
        # Check for strengths
        strengths = self._identify_strengths(content)
        
        # Calculate overall score
        total_issues = len(critical_issues) * 5 + len(major_issues) * 2 + len(minor_issues) * 1
        max_score = 100
        score = max(0.0, (max_score - total_issues) / max_score)
        
        return ComplianceReport(
            document_path=str(doc_path),
            scan_timestamp=datetime.now().isoformat(),
            overall_score=score,
            critical_issues=critical_issues,
            major_issues=major_issues,
            minor_issues=minor_issues,
            strengths=strengths
        )
    
    def _check_emotional_states(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check for deprecated emotional state terminology."""
        issues = []
        
        # Check for deprecated "DRAINED" term
        for i, line in enumerate(lines, 1):
            if re.search(r'\bDRAINED\b', line) and 'deprecated' not in line.lower():
                issues.append(ComplianceIssue(
                    severity="CRITICAL",
                    category="terminology",
                    issue="Using deprecated emotional state 'DRAINED'",
                    location=f"{doc_path}:{i}",
                    master_truth_ref="Section 2: Canonical Vocabulary",
                    current_value="DRAINED",
                    expected_value="EXHAUSTED",
                    fix_suggestion=f"Replace 'DRAINED' with 'EXHAUSTED' on line {i}"
                ))
        
        return issues
    
    def _check_subscription_pricing(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check subscription pricing consistency."""
        issues = []
        
        # Pattern: $X.XX/month or $X.XX/mo
        plus_pattern = r'\$14\.99\s*/\s*(month|mo)'
        ultimate_pattern = r'\$29\.99\s*/\s*(month|mo)'
        
        # Check for wrong Plus pricing
        wrong_plus = re.findall(r'\$(\d+\.\d+)\s*/\s*(month|mo).*[Pp]lus', content)
        for price, _ in wrong_plus:
            if price != '14.99':
                line_num = self._find_line_number(content, lines, f"${price}")
                issues.append(ComplianceIssue(
                    severity="CRITICAL",
                    category="pricing",
                    issue=f"Incorrect Plus subscription price: ${price}",
                    location=f"{doc_path}:{line_num}",
                    master_truth_ref="Section 10: Monetization",
                    current_value=f"${price}/month",
                    expected_value="$14.99/month",
                    fix_suggestion=f"Update Plus pricing to $14.99/month"
                ))
        
        # Check for wrong Ultimate pricing
        wrong_ultimate = re.findall(r'\$(\d+\.\d+)\s*/\s*(month|mo).*[Uu]ltimate', content)
        for price, _ in wrong_ultimate:
            if price != '29.99':
                line_num = self._find_line_number(content, lines, f"${price}")
                issues.append(ComplianceIssue(
                    severity="CRITICAL",
                    category="pricing",
                    issue=f"Incorrect Ultimate subscription price: ${price}",
                    location=f"{doc_path}:{line_num}",
                    master_truth_ref="Section 10: Monetization",
                    current_value=f"${price}/month",
                    expected_value="$29.99/month",
                    fix_suggestion=f"Update Ultimate pricing to $29.99/month"
                ))
        
        return issues
    
    def _check_relationship_levels(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check relationship levels scale (0-5)."""
        issues = []
        
        # Check for mentions of Level 6 or higher
        for i, line in enumerate(lines, 1):
            if re.search(r'\bLevel [6-9]\b|\bLevel 10\b', line):
                issues.append(ComplianceIssue(
                    severity="MAJOR",
                    category="scale",
                    issue=f"Invalid relationship level mentioned (Level 6+)",
                    location=f"{doc_path}:{i}",
                    master_truth_ref="Section 2: Canonical Vocabulary - Relationships",
                    current_value=re.search(r'Level \d+', line).group(),
                    expected_value="Levels 0-5 only",
                    fix_suggestion="Relationship levels are 0-5. Level 5 is maximum (Soulmate/Best Friend)"
                ))
        
        # Check for "Level 0" displayed to user
        for i, line in enumerate(lines, 1):
            if re.search(r'[Dd]isplay.*Level 0|show.*Level 0|UI.*Level 0', line):
                issues.append(ComplianceIssue(
                    severity="MAJOR",
                    category="scale",
                    issue="Document suggests displaying 'Level 0' to users",
                    location=f"{doc_path}:{i}",
                    master_truth_ref="Section 2: Relationships",
                    current_value="Display Level 0",
                    expected_value="Display 'Not Met' instead",
                    fix_suggestion="Level 0 should never be displayed; show 'Not Met' instead"
                ))
        
        return issues
    
    def _check_emotional_capacity(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check emotional capacity scale (0-10)."""
        issues = []
        
        # Check for capacity ranges that don't match 0.0-10.0
        capacity_mentions = re.findall(r'capacity.*?(\d+\.?\d*)\s*(?:to|-)\s*(\d+\.?\d*)', content.lower())
        
        for start, end in capacity_mentions:
            start_f = float(start)
            end_f = float(end)
            if end_f > 10.0:
                line_num = self._find_line_number(content, lines, f"{start}")
                issues.append(ComplianceIssue(
                    severity="MAJOR",
                    category="scale",
                    issue=f"Emotional capacity scale exceeds maximum (0-10)",
                    location=f"{doc_path}:{line_num}",
                    master_truth_ref="Section 2: Emotional Systems",
                    current_value=f"{start}-{end}",
                    expected_value="0.0-10.0",
                    fix_suggestion="Emotional capacity scale is 0.0-10.0 (continuous)"
                ))
        
        return issues
    
    def _check_npc_response_framework(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check NPC Response Framework integration."""
        issues = []
        
        # Check if document mentions NPCs or character responses
        if re.search(r'\bNPC|\bcharacter response|\bpersonality.*response', content, re.IGNORECASE):
            # Check if it references the response framework
            has_framework = bool(re.search(r'NPC Response Framework|OCEAN.*urgency|situational multiplier', content, re.IGNORECASE))
            
            if not has_framework:
                issues.append(ComplianceIssue(
                    severity="MAJOR",
                    category="integration",
                    issue="Document discusses NPC behavior without referencing NPC Response Framework",
                    location=f"{doc_path}:various",
                    master_truth_ref="Section 11: NPC Response Framework",
                    current_value="No framework integration",
                    expected_value="Apply OCEAN → Urgency → Trust → Capacity hierarchy",
                    fix_suggestion="Integrate NPC Response Framework from Master Truths Section 11"
                ))
        
        return issues
    
    def _check_memory_resonance(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check memory resonance factors."""
        issues = []
        
        # Check if document mentions memory system
        if re.search(r'\bmemory|\brecall|\bresonance', content, re.IGNORECASE):
            # Check for resonance weights
            has_weights = bool(re.search(r'0\.[7-9]\d*.*weight|resonance.*0\.[7-9]', content))
            
            if not has_weights and 'memory' in content.lower():
                issues.append(ComplianceIssue(
                    severity="MINOR",
                    category="integration",
                    issue="Memory system lacks resonance weight integration",
                    location=f"{doc_path}:various",
                    master_truth_ref="Section 17: Memory Resonance",
                    current_value="No resonance weights found",
                    expected_value="Weights: 0.7-0.95 for different memory types",
                    fix_suggestion="Apply memory resonance weights (0.7-0.95) from Master Truths v1.2"
                ))
        
        return issues
    
    def _check_tension_framework(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check tension injection framework."""
        issues = []
        
        # Check if document mentions card evolution or narrative generation
        if re.search(r'evolution|narrative.*generation|story.*generation', content, re.IGNORECASE):
            # Check for tension frequency guidelines
            has_tension = bool(re.search(r'tension.*frequency|1 in 3|1 in 2', content, re.IGNORECASE))
            
            if not has_tension:
                issues.append(ComplianceIssue(
                    severity="MINOR",
                    category="integration",
                    issue="Content generation lacks tension injection frequency guidelines",
                    location=f"{doc_path}:various",
                    master_truth_ref="Section 17: Tension Injection Framework",
                    current_value="No tension frequency mentioned",
                    expected_value="Level 1-2: 1 in 3, Level 3-4: 1 in 2, Level 5: nearly every",
                    fix_suggestion="Apply tension frequency guidelines from Master Truths v1.2"
                ))
        
        return issues
    
    def _check_quality_thresholds(self, content: str, lines: List[str], doc_path: Path) -> List[ComplianceIssue]:
        """Check novel-quality validation thresholds."""
        issues = []
        
        # Check if document mentions quality or validation
        if re.search(r'quality.*threshold|validation.*score', content, re.IGNORECASE):
            # Check for correct thresholds
            wrong_thresholds = []
            
            # Emotional authenticity should be >= 0.7
            if re.search(r'emotional.*authenticity.*0\.[0-6]\d*', content, re.IGNORECASE):
                wrong_thresholds.append("emotional_authenticity")
            
            # Tension building should be >= 0.6
            if re.search(r'tension.*0\.[0-5]\d*', content, re.IGNORECASE):
                wrong_thresholds.append("tension_building")
            
            for threshold in wrong_thresholds:
                line_num = self._find_line_number(content, lines, threshold.replace('_', ' '))
                issues.append(ComplianceIssue(
                    severity="MINOR",
                    category="scale",
                    issue=f"Incorrect quality threshold for {threshold}",
                    location=f"{doc_path}:{line_num}",
                    master_truth_ref="Section 17: Novel-Quality Thresholds",
                    current_value="< 0.7 for authenticity or < 0.6 for tension",
                    expected_value="≥ 0.7 for authenticity, ≥ 0.6 for tension",
                    fix_suggestion="Update thresholds to match Master Truths v1.2 Section 17"
                ))
        
        return issues
    
    def _has_compliance_checklist(self, content: str) -> bool:
        """Check if document has compliance checklist."""
        return bool(re.search(r'Compliance Checklist|Master Truths.*v1\.2', content, re.IGNORECASE))
    
    def _identify_strengths(self, content: str) -> List[str]:
        """Identify well-implemented areas."""
        strengths = []
        
        if re.search(r'relationship.*level.*0.*5|trust.*0\.0.*1\.0', content, re.IGNORECASE):
            strengths.append("Properly references relationship levels (0-5) and trust (0.0-1.0)")
        
        if re.search(r'season.*12.*24.*36|12w.*24w.*36w', content):
            strengths.append("Correctly implements season structure (12/24/36 weeks)")
        
        if re.search(r'3 turns.*day|turns.*per.*day.*3', content, re.IGNORECASE):
            strengths.append("Properly references turn structure (3 per day)")
        
        if re.search(r'EXHAUSTED.*OVERWHELMED', content):
            strengths.append("Uses canonical emotional state terminology")
        
        if re.search(r'\$14\.99.*\$29\.99|Plus.*\$14\.99|Ultimate.*\$29\.99', content):
            strengths.append("Correct subscription pricing ($14.99/$29.99)")
        
        if re.search(r'capacity.*0.*10|emotional capacity.*scale', content, re.IGNORECASE):
            strengths.append("Implements emotional capacity system (0-10 scale)")
        
        if re.search(r'NPC Response Framework|OCEAN.*urgency.*trust.*capacity', content):
            strengths.append("Integrates NPC Response Framework")
        
        return strengths
    
    def _find_line_number(self, content: str, lines: List[str], search_term: str) -> int:
        """Find approximate line number for a term."""
        for i, line in enumerate(lines, 1):
            if search_term.lower() in line.lower():
                return i
        return 1
    
    def scan_all_docs(self, docs_dir: Path) -> Dict[str, ComplianceReport]:
        """Scan all markdown documents in a directory."""
        reports = {}
        
        for md_file in docs_dir.rglob("*.md"):
            if 'archive' in str(md_file).lower():
                continue  # Skip archived documents
            
            try:
                report = self.validate_document(md_file)
                reports[str(md_file)] = report
            except Exception as e:
                print(f"Error validating {md_file}: {e}")
        
        return reports
    
    def generate_summary_report(self, reports: Dict[str, ComplianceReport], output_path: Path):
        """Generate comprehensive summary report."""
        total_docs = len(reports)
        compliant_docs = sum(1 for r in reports.values() if r.overall_score >= 0.95)
        
        critical_count = sum(len(r.critical_issues) for r in reports.values())
        major_count = sum(len(r.major_issues) for r in reports.values())
        minor_count = sum(len(r.minor_issues) for r in reports.values())
        
        avg_score = sum(r.overall_score for r in reports.values()) / total_docs if total_docs > 0 else 0
        
        # Generate markdown report
        report_lines = [
            "# Master Truth Compliance Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Master Truths Version:** v1.2",
            f"**Documents Scanned:** {total_docs}",
            "",
            "## Executive Summary",
            "",
            f"- **Overall Compliance Score:** {avg_score:.1%}",
            f"- **Compliant Documents (≥95%):** {compliant_docs}/{total_docs} ({compliant_docs/total_docs*100:.1f}%)",
            f"- **Critical Issues:** {critical_count}",
            f"- **Major Issues:** {major_count}",
            f"- **Minor Issues:** {minor_count}",
            "",
            "## Compliance Tier Distribution",
            ""
        ]
        
        # Tier analysis
        excellent = sum(1 for r in reports.values() if r.overall_score >= 0.95)
        good = sum(1 for r in reports.values() if 0.85 <= r.overall_score < 0.95)
        needs_work = sum(1 for r in reports.values() if 0.70 <= r.overall_score < 0.85)
        critical = sum(1 for r in reports.values() if r.overall_score < 0.70)
        
        report_lines.extend([
            f"- **Excellent (≥95%):** {excellent} documents",
            f"- **Good (85-94%):** {good} documents",
            f"- **Needs Work (70-84%):** {needs_work} documents",
            f"- **Critical (<70%):** {critical} documents",
            "",
            "## Critical Issues Requiring Immediate Attention",
            ""
        ])
        
        # List all critical issues
        critical_issues_found = False
        for doc_path, report in sorted(reports.items(), key=lambda x: x[1].overall_score):
            if report.critical_issues:
                critical_issues_found = True
                report_lines.append(f"### {doc_path}")
                report_lines.append("")
                for issue in report.critical_issues:
                    report_lines.extend([
                        f"**{issue.category.upper()}: {issue.issue}**",
                        f"- Location: `{issue.location}`",
                        f"- Current: `{issue.current_value}`",
                        f"- Expected: `{issue.expected_value}`",
                        f"- Fix: {issue.fix_suggestion}",
                        f"- Reference: Master Truths {issue.master_truth_ref}",
                        ""
                    ])
        
        if not critical_issues_found:
            report_lines.append("[OK] **No critical issues found!**")
            report_lines.append("")
        
        # Document-by-document summary
        report_lines.extend([
            "",
            "## Document-by-Document Summary",
            "",
            "| Document | Score | Critical | Major | Minor | Status |",
            "|----------|-------|----------|-------|-------|--------|"
        ])
        
        for doc_path, report in sorted(reports.items(), key=lambda x: x[1].overall_score, reverse=True):
            status = "[OK] Compliant" if report.overall_score >= 0.95 else ("[WARNING] Needs Review" if report.overall_score >= 0.70 else "[CRITICAL]")
            doc_name = Path(doc_path).name
            report_lines.append(
                f"| {doc_name} | {report.overall_score:.1%} | {len(report.critical_issues)} | {len(report.major_issues)} | {len(report.minor_issues)} | {status} |"
            )
        
        report_lines.extend([
            "",
            "## Recommendations",
            "",
            "### Immediate Actions (Week 1-2)",
            ""
        ])
        
        if critical_count > 0:
            report_lines.append(f"1. **Resolve {critical_count} critical issues** - These contradict Master Truths v1.2")
            report_lines.append("2. **Update subscription pricing** where incorrect")
            report_lines.append("3. **Fix deprecated terminology** (DRAINED -> EXHAUSTED)")
        else:
            report_lines.append("1. [OK] No critical issues - proceed to major issues")
        
        report_lines.extend([
            "",
            "### Short-term (Week 3-4)",
            "",
            f"1. Address {major_count} major issues (scale inconsistencies, missing integrations)",
            "2. Add NPC Response Framework references where missing",
            "3. Integrate emotional capacity constraints",
            "",
            "### Medium-term (Month 2-3)",
            "",
            f"1. Resolve {minor_count} minor issues (validation thresholds, tension framework)",
            "2. Add compliance checklists to all documents",
            "3. Implement automated compliance checking in CI/CD",
            "",
            "## Conclusion",
            ""
        ])
        
        if avg_score >= 0.95:
            report_lines.append(f"**Overall Status: EXCELLENT [OK]**")
            report_lines.append("")
            report_lines.append(f"The codebase shows {avg_score:.1%} compliance with Master Truths v1.2. Continue monitoring for new documents.")
        elif avg_score >= 0.85:
            report_lines.append(f"**Overall Status: GOOD [WARNING]**")
            report_lines.append("")
            report_lines.append(f"The codebase shows {avg_score:.1%} compliance. Address critical and major issues to reach excellent status.")
        else:
            report_lines.append(f"**Overall Status: NEEDS WORK [CRITICAL]**")
            report_lines.append("")
            report_lines.append(f"The codebase shows {avg_score:.1%} compliance. Immediate attention required on critical issues.")
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"\n[OK] Summary report written to: {output_path}")
        
        # Also save JSON version
        json_path = output_path.with_suffix('.json')
        json_data = {
            'generated': datetime.now().isoformat(),
            'master_truths_version': 'v1.2',
            'summary': {
                'total_docs': total_docs,
                'compliant_docs': compliant_docs,
                'avg_score': avg_score,
                'critical_issues': critical_count,
                'major_issues': major_count,
                'minor_issues': minor_count
            },
            'reports': {path: report.to_dict() for path, report in reports.items()}
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"[OK] JSON data written to: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Master Truth Compliance Validator")
    parser.add_argument('--doc', type=Path, help="Validate a single document")
    parser.add_argument('--scan-all', action='store_true', help="Scan all documents in docs/")
    parser.add_argument('--report', type=Path, help="Output path for summary report")
    parser.add_argument('--docs-dir', type=Path, default=Path('docs'), help="Documentation directory")
    
    args = parser.parse_args()
    
    validator = MasterTruthValidator()
    
    if args.doc:
        # Validate single document
        report = validator.validate_document(args.doc)
        
        print(f"\n{'='*60}")
        print(f"COMPLIANCE REPORT: {args.doc}")
        print(f"{'='*60}")
        print(f"Overall Score: {report.overall_score:.1%}")
        print(f"Critical Issues: {len(report.critical_issues)}")
        print(f"Major Issues: {len(report.major_issues)}")
        print(f"Minor Issues: {len(report.minor_issues)}")
        
        if report.critical_issues:
            print(f"\n🔴 CRITICAL ISSUES:")
            for issue in report.critical_issues:
                print(f"  - {issue.issue}")
                print(f"    Location: {issue.location}")
                print(f"    Fix: {issue.fix_suggestion}")
        
        if report.major_issues:
            print(f"\n🟡 MAJOR ISSUES:")
            for issue in report.major_issues:
                print(f"  - {issue.issue}")
        
        if report.strengths:
            print(f"\n[OK] STRENGTHS:")
            for strength in report.strengths:
                print(f"  - {strength}")
    
    elif args.scan_all:
        # Scan all documents
        print(f"Scanning all documents in {args.docs_dir}...")
        reports = validator.scan_all_docs(args.docs_dir)
        
        output_path = args.report or Path('docs/MASTER_TRUTH_COMPLIANCE_REPORT.md')
        validator.generate_summary_report(reports, output_path)
        
        print(f"\n[OK] Scan complete! {len(reports)} documents analyzed.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

