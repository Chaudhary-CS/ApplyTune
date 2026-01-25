"""
Smart Keyword Prioritizer - Add keywords by IMPORTANCE, not alphabetically!

Based on research into Jobscan, Teal, and Resume Worded algorithms.
"""

import re
from typing import List, Dict, Tuple
from collections import Counter


class KeywordPrioritizer:
    """
    Prioritize keywords by actual importance using industry-standard methods.
    
    Formula: Priority = Frequency × Section Weight × Context Score
    
    This ensures we add "Python" (mentioned 8x in Requirements) before
    "Java" (mentioned 1x in Nice-to-have).
    """
    
    # Section weights based on Jobscan's research
    SECTION_WEIGHTS = {
        'requirements': 3.0,        # CRITICAL - must have
        'required': 3.0,
        'must have': 3.0,
        'qualifications': 2.5,
        'responsibilities': 2.0,    # IMPORTANT - what you'll do
        'preferred': 1.5,
        'nice to have': 1.0,        # OPTIONAL - bonus
        'plus': 1.0,
        'bonus': 0.8,
        'default': 1.0              # Mentioned but no specific section
    }
    
    def prioritize_keywords(
        self, 
        missing_keywords: List[str], 
        job_description: str
    ) -> List[Tuple[str, float]]:
        """
        Sort keywords by importance for THIS specific job.
        
        Args:
            missing_keywords: Keywords not in resume
            job_description: Full job posting text
            
        Returns:
            List of (keyword, priority_score) sorted by priority (highest first)
        """
        scored_keywords = []
        
        for keyword in missing_keywords:
            score = self._calculate_priority_score(keyword, job_description)
            scored_keywords.append((keyword, score))
        
        # Sort by score (highest first)
        scored_keywords.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n📊 Keyword Prioritization Results:")
        print(f"   Top 5 keywords to add:")
        for kw, score in scored_keywords[:5]:
            print(f"      {score:6.1f} pts - {kw}")
        
        return scored_keywords
    
    def _calculate_priority_score(self, keyword: str, job_description: str) -> float:
        """
        Calculate priority score for a single keyword.
        
        Score = Frequency × Section Weight × Context Bonus
        """
        # 1. Count frequency (case-insensitive)
        frequency = self._count_frequency(keyword, job_description)
        
        # 2. Determine section weight (where it appears)
        section_weight = self._get_section_weight(keyword, job_description)
        
        # 3. Context bonus (appears in title, first paragraph, etc.)
        context_bonus = self._get_context_bonus(keyword, job_description)
        
        # Calculate final score
        base_score = frequency * section_weight
        final_score = base_score * (1.0 + context_bonus)
        
        return final_score
    
    def _count_frequency(self, keyword: str, text: str) -> int:
        """
        Count how many times keyword appears (case-insensitive).
        
        Example:
        - "Python" appears 8 times → frequency = 8
        - "Java" appears 2 times → frequency = 2
        """
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return len(matches)
    
    def _get_section_weight(self, keyword: str, job_description: str) -> float:
        """
        Determine which section the keyword appears in.
        
        "Requirements" = 3.0x weight
        "Responsibilities" = 2.0x weight  
        "Nice to have" = 1.0x weight
        """
        # Split job description into sections
        sections = self._identify_sections(job_description)
        
        # Find which section contains this keyword
        keyword_lower = keyword.lower()
        
        for section_name, section_text in sections.items():
            if keyword_lower in section_text.lower():
                # Return weight for this section
                for weight_key, weight_value in self.SECTION_WEIGHTS.items():
                    if weight_key in section_name.lower():
                        return weight_value
                
                # Default weight if section name doesn't match known categories
                return self.SECTION_WEIGHTS['default']
        
        # If not in any specific section, default weight
        return self.SECTION_WEIGHTS['default']
    
    def _identify_sections(self, job_description: str) -> Dict[str, str]:
        """
        Split job description into sections.
        
        Common sections:
        - "Requirements" / "Qualifications"
        - "Responsibilities" / "What You'll Do"
        - "Preferred" / "Nice to have" / "Bonus"
        """
        sections = {}
        
        # Common section headers (case-insensitive)
        section_patterns = [
            r'(?:^|\n)[\s]*(?:###?|##?)?\s*(requirements?|qualifications?|must have)',
            r'(?:^|\n)[\s]*(?:###?|##?)?\s*(responsibilities|what you\'?ll do|duties)',
            r'(?:^|\n)[\s]*(?:###?|##?)?\s*(preferred|nice to have|bonus|plus)',
            r'(?:^|\n)[\s]*(?:###?|##?)?\s*(required skills?|technical requirements?)',
            r'(?:^|\n)[\s]*(?:###?|##?)?\s*(what you\'?ll bring|what we\'?re looking for)',
        ]
        
        # Try to split by section headers
        last_end = 0
        current_section = "Introduction"
        
        for pattern in section_patterns:
            matches = list(re.finditer(pattern, job_description, re.IGNORECASE | re.MULTILINE))
            for match in matches:
                # Save previous section
                section_text = job_description[last_end:match.start()]
                if section_text.strip():
                    sections[current_section] = section_text
                
                # Start new section
                current_section = match.group(1)
                last_end = match.end()
        
        # Add final section
        if last_end < len(job_description):
            sections[current_section] = job_description[last_end:]
        
        # If no sections found, treat entire JD as "Requirements"
        if not sections:
            sections["Requirements"] = job_description
        
        return sections
    
    def _get_context_bonus(self, keyword: str, job_description: str) -> float:
        """
        Bonus points for appearing in critical locations.
        
        - Job title: +0.5 bonus (50% boost)
        - First paragraph: +0.3 bonus (30% boost)
        - Capitalized/emphasized: +0.2 bonus (20% boost)
        """
        bonus = 0.0
        
        # Extract first 200 characters (intro/title area)
        intro = job_description[:200]
        
        # Bonus 1: Appears in intro/title area
        if keyword.lower() in intro.lower():
            bonus += 0.3
        
        # Bonus 2: Appears capitalized (likely emphasized)
        if re.search(r'\b' + re.escape(keyword.upper()) + r'\b', job_description):
            bonus += 0.2
        
        # Bonus 3: Appears in bold/emphasized text (Markdown or emphasis indicators)
        if re.search(r'[\*_]{1,2}' + re.escape(keyword) + r'[\*_]{1,2}', job_description, re.IGNORECASE):
            bonus += 0.2
        
        return min(bonus, 1.0)  # Cap at 100% bonus
    
    def get_top_keywords(
        self, 
        missing_keywords: List[str], 
        job_description: str, 
        top_n: int = 15
    ) -> List[str]:
        """
        Get top N keywords to add, sorted by priority.
        
        This is what the optimizer should use!
        """
        scored = self.prioritize_keywords(missing_keywords, job_description)
        return [kw for kw, score in scored[:top_n]]
    
    def explain_priority(self, keyword: str, job_description: str) -> Dict:
        """
        Explain WHY a keyword has its priority score.
        Useful for showing to users.
        """
        frequency = self._count_frequency(keyword, job_description)
        section_weight = self._get_section_weight(keyword, job_description)
        context_bonus = self._get_context_bonus(keyword, job_description)
        
        score = frequency * section_weight * (1.0 + context_bonus)
        
        return {
            'keyword': keyword,
            'score': score,
            'frequency': frequency,
            'section_weight': section_weight,
            'context_bonus': context_bonus,
            'explanation': f"Mentioned {frequency}x, appears in important section (weight: {section_weight}x), context bonus: +{context_bonus*100:.0f}%"
        }
