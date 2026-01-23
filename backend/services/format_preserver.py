"""
Format Preserver - Ensures user's original resume formatting is maintained

This module helps us preserve the user's original resume style while
optimizing content. We want to enhance, not destroy their carefully
crafted formatting.
"""

from typing import Dict, List
import re


class FormatPreserver:
    """
    Analyzes and preserves the original formatting characteristics
    of a user's resume.
    
    This is important because people spend time perfecting their resume
    format, and we don't want to mess that up. We just want to make
    the content more ATS-friendly.
    """
    
    def analyze_format(self, resume_data: Dict) -> Dict:
        """
        Analyze the formatting characteristics of the original resume.
        
        Returns a format profile that can be used to maintain consistency
        when generating the optimized version.
        """
        format_profile = {
            'bullet_style': self._detect_bullet_style(resume_data),
            'bullet_length': self._analyze_bullet_lengths(resume_data),
            'section_order': self._get_section_order(resume_data),
            'writing_style': self._analyze_writing_style(resume_data),
            'spacing_preferences': self._analyze_spacing(resume_data)
        }
        
        return format_profile
    
    def _detect_bullet_style(self, resume_data: Dict) -> str:
        """
        Figure out what bullet style the user prefers.
        Some people use short, punchy bullets. Others use longer, detailed ones.
        """
        experience = resume_data.get('experience', [])
        
        if not experience:
            return 'standard'
        
        # Collect all bullets
        all_bullets = []
        for exp in experience:
            bullets = exp.get('description', [])
            if isinstance(bullets, list):
                all_bullets.extend(bullets)
        
        if not all_bullets:
            return 'standard'
        
        # Analyze bullet characteristics
        avg_length = sum(len(b.split()) for b in all_bullets) / len(all_bullets)
        
        if avg_length < 8:
            return 'concise'  # Short, punchy bullets
        elif avg_length > 15:
            return 'detailed'  # Longer, descriptive bullets
        else:
            return 'standard'  # Medium length
    
    def _analyze_bullet_lengths(self, resume_data: Dict) -> Dict:
        """
        Analyze how long the user's bullets typically are.
        We want to maintain similar lengths in optimized version.
        """
        experience = resume_data.get('experience', [])
        
        lengths = {
            'min': 0,
            'max': 0,
            'avg': 0,
            'typical_word_count': 0
        }
        
        all_bullets = []
        for exp in experience:
            bullets = exp.get('description', [])
            if isinstance(bullets, list):
                all_bullets.extend(bullets)
        
        if all_bullets:
            word_counts = [len(b.split()) for b in all_bullets]
            lengths['min'] = min(word_counts)
            lengths['max'] = max(word_counts)
            lengths['avg'] = sum(word_counts) / len(word_counts)
            lengths['typical_word_count'] = int(lengths['avg'])
        
        return lengths
    
    def _get_section_order(self, resume_data: Dict) -> List[str]:
        """
        Remember the order of sections in the original resume.
        Some people put skills first, others put experience first.
        """
        section_order = []
        
        # Check which sections exist and in what implied order
        # (We can't know exact order from parsed data, but we can preserve
        # what sections they have)
        
        if resume_data.get('summary'):
            section_order.append('summary')
        
        if resume_data.get('skills'):
            section_order.append('skills')
        
        if resume_data.get('experience'):
            section_order.append('experience')
        
        if resume_data.get('education'):
            section_order.append('education')
        
        if resume_data.get('projects'):
            section_order.append('projects')
        
        if resume_data.get('certifications'):
            section_order.append('certifications')
        
        return section_order
    
    def _analyze_writing_style(self, resume_data: Dict) -> Dict:
        """
        Analyze the user's writing style to maintain it.
        - Do they use first person or third person?
        - Do they use complete sentences or fragments?
        - What's their tone (formal vs casual)?
        """
        style_profile = {
            'tone': 'professional',  # Default
            'person': 'first_implied',  # Most resumes imply first person
            'sentence_style': 'fragments'  # Most bullets are fragments
        }
        
        # Analyze summary if it exists
        summary = resume_data.get('summary', '')
        if summary:
            # Check if they use "I" statements
            if re.search(r'\b[Ii]\s', summary):
                style_profile['person'] = 'first_explicit'
            
            # Check formality (presence of casual words)
            casual_indicators = ['passionate', 'love', 'excited', 'enjoy']
            formal_indicators = ['extensive', 'accomplished', 'proficient']
            
            casual_count = sum(1 for word in casual_indicators if word in summary.lower())
            formal_count = sum(1 for word in formal_indicators if word in summary.lower())
            
            if casual_count > formal_count:
                style_profile['tone'] = 'approachable'
        
        return style_profile
    
    def _analyze_spacing(self, resume_data: Dict) -> Dict:
        """
        Analyze spacing preferences from the original resume.
        """
        spacing = {
            'bullets_per_job': 0,
            'prefers_compact': False
        }
        
        experience = resume_data.get('experience', [])
        
        if experience:
            bullet_counts = []
            for exp in experience:
                bullets = exp.get('description', [])
                if isinstance(bullets, list):
                    bullet_counts.append(len(bullets))
            
            if bullet_counts:
                avg_bullets = sum(bullet_counts) / len(bullet_counts)
                spacing['bullets_per_job'] = int(avg_bullets)
                
                # If they typically use 3 or fewer bullets, they prefer compact
                spacing['prefers_compact'] = avg_bullets <= 3
        
        return spacing
    
    def apply_format_constraints(self, optimized_text: str, 
                                 format_profile: Dict, 
                                 original_length: int) -> str:
        """
        Apply format constraints to optimized text to match original style.
        
        For example, if original bullet was 10 words and optimized is 20,
        this will help trim it down while keeping the key improvements.
        """
        # Get target word count based on format profile
        target_length = original_length
        
        # Allow some flexibility (±20%)
        min_length = int(target_length * 0.8)
        max_length = int(target_length * 1.2)
        
        current_length = len(optimized_text.split())
        
        # If it's within acceptable range, return as-is
        if min_length <= current_length <= max_length:
            return optimized_text
        
        # If too long, we need to trim (but this is tricky - better to let AI handle it)
        # For now, just return as-is and rely on prompt instructions
        
        return optimized_text
    
    def validate_optimization(self, original: Dict, optimized: Dict) -> Dict:
        """
        Validate that optimization preserved key formatting characteristics.
        
        Returns a dict with validation results and warnings if format
        was changed too much.
        """
        validation = {
            'passed': True,
            'warnings': [],
            'preserved_characteristics': []
        }
        
        # Check if number of experience entries is the same
        orig_exp_count = len(original.get('experience', []))
        opt_exp_count = len(optimized.get('experience', []))
        
        if orig_exp_count == opt_exp_count:
            validation['preserved_characteristics'].append('Same number of jobs')
        else:
            validation['warnings'].append(f'Job count changed: {orig_exp_count} -> {opt_exp_count}')
            validation['passed'] = False
        
        # Check if section types are preserved
        orig_sections = set(k for k, v in original.items() if v and k != 'raw_text')
        opt_sections = set(k for k, v in optimized.items() if v and k != 'raw_text')
        
        if orig_sections == opt_sections:
            validation['preserved_characteristics'].append('All sections preserved')
        else:
            missing = orig_sections - opt_sections
            added = opt_sections - orig_sections
            if missing:
                validation['warnings'].append(f'Missing sections: {missing}')
            if added:
                validation['warnings'].append(f'Added sections: {added}')
        
        return validation
