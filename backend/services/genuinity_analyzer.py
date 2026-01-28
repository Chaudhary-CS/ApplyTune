"""
Genuinity Analyzer Service
Analyzes resume authenticity and scores how genuine/believable the optimizations are.
Helps prevent fake-looking resumes that ATS might flag or recruiters might question.
"""

from typing import Dict, List, Tuple
import re
from .context_validator import ContextValidator
from .keyword_prioritizer import KeywordPrioritizer


class GenuinityAnalyzer:
    """
    Analyzes resume changes to score authenticity on a scale of 0-100.
    
    Factors considered:
    - Tech stack consistency across projects
    - Keyword insertion naturalness
    - Claim verifiability risk
    - Over-optimization detection
    - Keyword stuffing detection
    """
    
    def __init__(self):
        self.context_validator = ContextValidator()
        self.keyword_prioritizer = KeywordPrioritizer()
        
        # Thresholds for analysis
        self.max_keyword_density = 0.15  # Max 15% of text should be keywords
        self.suspicious_phrase_patterns = [
            r'experience with (\w+) and (\w+) and (\w+) and',  # Too many "and"s
            r'proficient in (\w+), (\w+), (\w+), (\w+), (\w+)',  # Laundry list
            r'expert in everything',
            r'skilled in all',
        ]
    
    def analyze_resume_authenticity(
        self,
        original_text: str,
        optimized_text: str,
        keywords_added: List[str],
        changes_made: List[Dict] = None,
        resume_sections: Dict[str, str] = None
    ) -> Dict:
        """
        Comprehensive authenticity analysis.
        
        Args:
            original_text: Original resume text
            optimized_text: AI-optimized resume text
            keywords_added: List of keywords that were added
            changes_made: List of specific changes with context
            resume_sections: Dict of section_name: content for validation
            
        Returns:
            Dict with genuinity score and detailed analysis
        """
        analysis = {
            'genuinity_score': 100.0,  # Start at 100, deduct for issues
            'risk_level': 'LOW',
            'issues': [],
            'warnings': [],
            'strengths': [],
            'recommendations': []
        }
        
        # 1. Check for keyword stuffing
        keyword_density_score = self._analyze_keyword_density(
            optimized_text, keywords_added
        )
        analysis['genuinity_score'] -= (100 - keyword_density_score) * 0.3
        
        if keyword_density_score < 70:
            analysis['issues'].append({
                'type': 'KEYWORD_STUFFING',
                'severity': 'HIGH',
                'description': f'Keyword density is {keyword_density_score:.1f}% - resume may appear over-optimized',
                'impact': -30
            })
        elif keyword_density_score < 85:
            analysis['warnings'].append({
                'type': 'HIGH_KEYWORD_DENSITY',
                'severity': 'MEDIUM',
                'description': f'Keyword density is somewhat high at {keyword_density_score:.1f}%',
                'impact': -15
            })
        
        # 2. Validate tech stack consistency
        if changes_made:
            tech_consistency_score = self._analyze_tech_consistency(
                changes_made, resume_sections or {}
            )
            analysis['genuinity_score'] -= (100 - tech_consistency_score) * 0.4
            
            if tech_consistency_score < 60:
                analysis['issues'].append({
                    'type': 'TECH_STACK_INCONSISTENCY',
                    'severity': 'HIGH',
                    'description': 'Some technology additions don\'t match project contexts',
                    'impact': -40
                })
        
        # 3. Check for suspicious phrases
        suspicious_score = self._detect_suspicious_phrases(optimized_text)
        analysis['genuinity_score'] -= (100 - suspicious_score) * 0.2
        
        if suspicious_score < 80:
            analysis['warnings'].append({
                'type': 'UNNATURAL_PHRASING',
                'severity': 'MEDIUM',
                'description': 'Some phrases may sound artificial or overly generic',
                'impact': -20
            })
        
        # 4. Analyze change naturalness
        if changes_made:
            naturalness_score = self._analyze_change_naturalness(changes_made)
            analysis['genuinity_score'] -= (100 - naturalness_score) * 0.3
            
            if naturalness_score < 70:
                analysis['issues'].append({
                    'type': 'UNNATURAL_CHANGES',
                    'severity': 'MEDIUM',
                    'description': 'Some modifications may not flow naturally',
                    'impact': -30
                })
        
        # 5. Check for verifiable information changes
        verifiable_risk_score = self._check_verifiable_risks(
            changes_made or [], resume_sections or {}
        )
        analysis['genuinity_score'] -= (100 - verifiable_risk_score) * 0.5
        
        if verifiable_risk_score < 50:
            analysis['issues'].append({
                'type': 'VERIFIABLE_INFO_CHANGED',
                'severity': 'CRITICAL',
                'description': 'Changes detected in verifiable sections (projects, education, certifications)',
                'impact': -50
            })
        
        # 6. Detect over-optimization
        optimization_intensity = len(keywords_added) / max(len(original_text.split()), 1) * 100
        if optimization_intensity > 5:  # More than 5% new keywords
            analysis['genuinity_score'] -= (optimization_intensity - 5) * 2
            analysis['warnings'].append({
                'type': 'OVER_OPTIMIZATION',
                'severity': 'MEDIUM',
                'description': f'Resume was heavily modified ({optimization_intensity:.1f}% keyword addition rate)',
                'impact': -(optimization_intensity - 5) * 2
            })
        
        # Ensure score stays in 0-100 range
        analysis['genuinity_score'] = max(0, min(100, analysis['genuinity_score']))
        
        # Determine risk level
        if analysis['genuinity_score'] >= 80:
            analysis['risk_level'] = 'LOW'
            analysis['strengths'].append('Resume maintains authentic and believable content')
        elif analysis['genuinity_score'] >= 60:
            analysis['risk_level'] = 'MEDIUM'
            analysis['recommendations'].append('Review changes to ensure they accurately reflect your experience')
        else:
            analysis['risk_level'] = 'HIGH'
            analysis['recommendations'].append('Consider using fewer keyword modifications or being more selective')
            analysis['recommendations'].append('Ensure all added skills are genuine and you can discuss them')
        
        # Add general recommendations
        if analysis['genuinity_score'] < 90:
            analysis['recommendations'].append('Focus on adding keywords to Skills and Experience sections')
            analysis['recommendations'].append('Avoid modifying project tech stacks that can be verified on GitHub')
        
        return analysis
    
    def _analyze_keyword_density(self, text: str, keywords: List[str]) -> float:
        """
        Calculate keyword density score (0-100).
        Higher is better - means keywords are not overly dense.
        """
        total_words = len(text.split())
        if total_words == 0:
            return 100
        
        # Count keyword occurrences
        text_lower = text.lower()
        keyword_word_count = 0
        
        for keyword in keywords:
            keyword_words = len(keyword.split())
            occurrences = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
            keyword_word_count += occurrences * keyword_words
        
        density = keyword_word_count / total_words
        
        # Score based on density
        if density <= self.max_keyword_density:
            return 100
        elif density <= 0.25:
            return 100 - ((density - self.max_keyword_density) / 0.10) * 30
        else:
            return max(0, 40 - (density - 0.25) * 100)
    
    def _analyze_tech_consistency(
        self, 
        changes: List[Dict],
        sections: Dict[str, str]
    ) -> float:
        """
        Analyze if tech keyword additions are consistent with existing stack.
        Returns score 0-100.
        """
        if not changes:
            return 100
        
        total_changes = len(changes)
        consistent_changes = 0
        
        for change in changes:
            keyword = change.get('keyword', '')
            section = change.get('section', '')
            context = sections.get(section, '')
            
            # Validate with context validator
            validation = self.context_validator.validate_keyword_insertion(
                keyword=keyword,
                context=context,
                section_type=section
            )
            
            # Score based on risk level
            if validation['risk_level'] == 'SAFE':
                consistent_changes += 1.0
            elif validation['risk_level'] == 'LOW_RISK':
                consistent_changes += 0.8
            elif validation['risk_level'] == 'MEDIUM_RISK':
                consistent_changes += 0.5
            elif validation['risk_level'] == 'HIGH_RISK':
                consistent_changes += 0.2
            # FABRICATION gets 0
        
        return (consistent_changes / total_changes) * 100 if total_changes > 0 else 100
    
    def _detect_suspicious_phrases(self, text: str) -> float:
        """Detect suspicious or unnatural phrases. Returns score 0-100."""
        text_lower = text.lower()
        suspicion_count = 0
        
        for pattern in self.suspicious_phrase_patterns:
            matches = re.findall(pattern, text_lower)
            suspicion_count += len(matches)
        
        # Check for excessive use of buzzwords
        buzzwords = ['synergy', 'leverage', 'utilize', 'facilitate', 'innovative', 
                     'cutting-edge', 'best-in-class', 'world-class']
        buzzword_count = sum(text_lower.count(word) for word in buzzwords)
        
        if buzzword_count > 5:
            suspicion_count += (buzzword_count - 5)
        
        # Score calculation
        if suspicion_count == 0:
            return 100
        elif suspicion_count <= 2:
            return 90 - (suspicion_count * 10)
        else:
            return max(0, 70 - (suspicion_count * 10))
    
    def _analyze_change_naturalness(self, changes: List[Dict]) -> float:
        """
        Analyze how natural the changes are.
        Checks for awkward insertions, forced keywords, etc.
        Returns score 0-100.
        """
        if not changes:
            return 100
        
        natural_changes = 0
        total_changes = len(changes)
        
        for change in changes:
            before = change.get('before', '')
            after = change.get('after', '')
            
            # Check length change (dramatic changes are suspicious)
            length_ratio = len(after) / max(len(before), 1)
            
            if 0.8 <= length_ratio <= 1.2:
                # Good - similar length
                natural_changes += 1.0
            elif 0.6 <= length_ratio <= 1.4:
                # Acceptable - moderate change
                natural_changes += 0.7
            else:
                # Suspicious - dramatic length change
                natural_changes += 0.3
        
        return (natural_changes / total_changes) * 100 if total_changes > 0 else 100
    
    def _check_verifiable_risks(
        self, 
        changes: List[Dict],
        sections: Dict[str, str]
    ) -> float:
        """
        Check if changes were made to verifiable sections.
        Returns score 0-100 (100 = no risky changes).
        """
        risky_sections = ['project', 'education', 'certification', 'publication', 'award']
        
        risky_change_count = 0
        total_changes = len(changes)
        
        if total_changes == 0:
            return 100
        
        for change in changes:
            section = change.get('section', '').lower()
            
            # Check if change is in a risky section
            if any(risky in section for risky in risky_sections):
                risky_change_count += 1
        
        # Calculate score
        safe_changes_ratio = 1 - (risky_change_count / total_changes)
        return safe_changes_ratio * 100
    
    def get_authenticity_report(self, analysis: Dict) -> str:
        """
        Generate a human-readable authenticity report.
        
        Args:
            analysis: Output from analyze_resume_authenticity()
            
        Returns:
            Formatted string report
        """
        score = analysis['genuinity_score']
        risk = analysis['risk_level']
        
        report = f"""
╔══════════════════════════════════════════════════╗
║         RESUME AUTHENTICITY ANALYSIS            ║
╚══════════════════════════════════════════════════╝

🎯 Genuinity Score: {score:.1f}/100
⚠️  Risk Level: {risk}

"""
        
        if analysis['issues']:
            report += "🚨 ISSUES DETECTED:\n"
            for issue in analysis['issues']:
                report += f"  • [{issue['severity']}] {issue['description']} (Impact: {issue['impact']})\n"
            report += "\n"
        
        if analysis['warnings']:
            report += "⚠️  WARNINGS:\n"
            for warning in analysis['warnings']:
                report += f"  • {warning['description']}\n"
            report += "\n"
        
        if analysis['strengths']:
            report += "✅ STRENGTHS:\n"
            for strength in analysis['strengths']:
                report += f"  • {strength}\n"
            report += "\n"
        
        if analysis['recommendations']:
            report += "💡 RECOMMENDATIONS:\n"
            for rec in analysis['recommendations']:
                report += f"  • {rec}\n"
            report += "\n"
        
        # Overall verdict
        if score >= 85:
            report += "✅ VERDICT: Your resume appears authentic and professional. Safe to use.\n"
        elif score >= 70:
            report += "⚠️  VERDICT: Your resume is mostly authentic but has minor concerns. Review recommended.\n"
        elif score >= 50:
            report += "⚠️  VERDICT: Your resume has noticeable authenticity issues. Revisions recommended.\n"
        else:
            report += "🚨 VERDICT: Your resume may appear fake or over-optimized. Significant revisions needed.\n"
        
        return report
