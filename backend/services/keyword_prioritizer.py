"""
Keyword Prioritizer Service
Scores and ranks keywords based on importance in job description.
Helps determine which keywords to prioritize for ATS optimization.
"""

from typing import List, Dict, Tuple
import re


class KeywordPrioritizer:
    """
    Analyzes job description to prioritize keywords based on:
    - Frequency of appearance
    - Section importance (required vs nice-to-have)
    - Context (technical skills vs soft skills)
    - Position in job description (earlier = more important)
    """
    
    def __init__(self):
        # Weight multipliers for different sections
        self.section_weights = {
            'required': 3.0,
            'must_have': 3.0,
            'qualifications': 2.5,
            'technical_skills': 2.0,
            'responsibilities': 1.8,
            'preferred': 1.2,
            'nice_to_have': 0.8,
            'bonus': 0.6
        }
        
        # Context bonus multipliers
        self.context_bonuses = {
            'job_title': 2.0,
            'first_paragraph': 1.5,
            'repeated_multiple_times': 1.3
        }
    
    def prioritize_keywords(
        self, 
        keywords: List[str], 
        job_description: str,
        job_title: str = ""
    ) -> List[Dict[str, any]]:
        """
        Score and rank keywords by importance.
        
        Args:
            keywords: List of keywords to prioritize
            job_description: Full job description text
            job_title: Job title for additional context
            
        Returns:
            List of dicts with keyword, score, and reasoning
        """
        job_desc_lower = job_description.lower()
        job_title_lower = job_title.lower()
        
        scored_keywords = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Base score from frequency
            frequency = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', job_desc_lower))
            score = frequency * 1.0
            
            reasons = []
            
            # Frequency bonus
            if frequency >= 3:
                score *= 1.3
                reasons.append(f"Mentioned {frequency}x")
            elif frequency >= 2:
                score *= 1.15
                reasons.append(f"Mentioned {frequency}x")
            
            # Job title match (highest priority)
            if keyword_lower in job_title_lower:
                score *= self.context_bonuses['job_title']
                reasons.append("In job title")
            
            # Section detection
            section_found = self._detect_section(keyword_lower, job_description)
            if section_found:
                weight = self.section_weights.get(section_found, 1.0)
                score *= weight
                reasons.append(f"In {section_found} section")
            
            # First paragraph bonus (usually most important)
            first_para = job_description[:500].lower()
            if keyword_lower in first_para:
                score *= self.context_bonuses['first_paragraph']
                reasons.append("Early mention")
            
            # Technical specificity bonus
            if self._is_technical_keyword(keyword):
                score *= 1.2
                reasons.append("Technical term")
            
            scored_keywords.append({
                'keyword': keyword,
                'score': round(score, 2),
                'frequency': frequency,
                'priority': 'HIGH' if score >= 5.0 else 'MEDIUM' if score >= 2.0 else 'LOW',
                'reasons': reasons
            })
        
        # Sort by score descending
        scored_keywords.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_keywords
    
    def _detect_section(self, keyword: str, job_description: str) -> str:
        """Detect which section of the job description contains the keyword."""
        job_desc_lower = job_description.lower()
        
        # Find keyword position
        keyword_pos = job_desc_lower.find(keyword)
        if keyword_pos == -1:
            return None
        
        # Look backwards from keyword position for section headers
        text_before = job_desc_lower[:keyword_pos]
        
        # Check for section markers
        section_markers = {
            'required': ['required', 'must have', 'requirements', 'qualifications'],
            'technical_skills': ['technical skills', 'tech stack', 'technologies'],
            'responsibilities': ['responsibilities', 'what you\'ll do', 'your role'],
            'preferred': ['preferred', 'nice to have', 'bonus', 'plus'],
        }
        
        # Find the closest section header before the keyword
        closest_section = None
        closest_distance = float('inf')
        
        for section_name, markers in section_markers.items():
            for marker in markers:
                marker_pos = text_before.rfind(marker)
                if marker_pos != -1:
                    distance = keyword_pos - marker_pos
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_section = section_name
        
        return closest_section
    
    def _is_technical_keyword(self, keyword: str) -> bool:
        """Determine if keyword is a technical term (programming language, tool, etc.)."""
        # Common technical indicators
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms (API, SQL, AWS)
            r'^[a-z]+\.[a-z]+$',  # Dotted notation (Node.js, React.js)
            r'^\d+\.\d+',  # Version numbers (Python 3.x)
        ]
        
        for pattern in technical_patterns:
            if re.search(pattern, keyword):
                return True
        
        # Common technical keywords
        technical_terms = [
            'python', 'javascript', 'java', 'c++', 'golang', 'rust',
            'react', 'angular', 'vue', 'node', 'django', 'flask',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'postgresql', 'mongodb', 'redis', 'sql',
            'pytorch', 'tensorflow', 'machine learning', 'ml',
            'api', 'rest', 'graphql', 'microservices',
            'git', 'ci/cd', 'devops', 'agile'
        ]
        
        return keyword.lower() in technical_terms
    
    def get_top_keywords(
        self, 
        scored_keywords: List[Dict], 
        limit: int = 10,
        min_priority: str = 'LOW'
    ) -> List[str]:
        """
        Get top N keywords filtered by priority.
        
        Args:
            scored_keywords: Output from prioritize_keywords()
            limit: Maximum number of keywords to return
            min_priority: Minimum priority level (LOW, MEDIUM, HIGH)
            
        Returns:
            List of top keyword strings
        """
        priority_order = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
        min_level = priority_order.get(min_priority, 0)
        
        filtered = [
            kw for kw in scored_keywords 
            if priority_order.get(kw['priority'], 0) >= min_level
        ]
        
        return [kw['keyword'] for kw in filtered[:limit]]
