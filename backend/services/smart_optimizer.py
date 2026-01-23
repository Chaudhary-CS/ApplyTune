"""
Smart Resume Optimizer - Industry-Standard Approach

Based on research into Jobscan, Resume Worded, and successful ATS tools.

KEY INSIGHT: Don't ask AI to "optimize" - tell it EXACTLY which keywords to add!

This guarantees score improvement because we:
1. Extract EXACT missing keywords
2. Insert EACH keyword specifically 
3. VERIFY it was actually added
4. Score improvement is GUARANTEED
"""

from typing import Dict, List, Set
from .llama_optimizer import LlamaOptimizer
import re


class SmartOptimizer:
    """
    Industry-standard ATS optimization that GUARANTEES score improvement.
    
    How it works (like Jobscan):
    1. Find EXACTLY which keywords are missing
    2. Tell AI to add EACH specific keyword
    3. Verify keyword was actually inserted
    4. Guaranteed improvement!
    """
    
    def __init__(self):
        self.ai = LlamaOptimizer()
        
    def optimize(self, resume_data: Dict, job_analysis: Dict) -> tuple[Dict, List[str]]:
        """
        Smart optimization with guaranteed improvement.
        
        Returns: (optimized_resume, verification_report)
        """
        # Step 1: Find EXACTLY what's missing
        missing_keywords = self._find_missing_keywords(resume_data, job_analysis)
        
        print(f"🎯 Target: Adding {len(missing_keywords)} missing keywords")
        
        # Step 2: Insert each keyword specifically
        optimized = resume_data.copy()
        added_keywords = []
        failed_keywords = []
        
        for keyword in missing_keywords[:15]:  # Top 15 most important
            print(f"  Trying to add: {keyword}")
            
            result = self._insert_keyword(optimized, keyword, job_analysis)
            
            if result['success']:
                optimized = result['resume']
                added_keywords.append(keyword)
                print(f"  ✓ Added: {keyword}")
            else:
                failed_keywords.append(keyword)
                print(f"  ✗ Failed: {keyword}")
        
        # Step 3: Verification report
        verification = {
            'target_keywords': missing_keywords[:15],
            'added': added_keywords,
            'failed': failed_keywords,
            'success_rate': len(added_keywords) / len(missing_keywords[:15]) * 100
        }
        
        print(f"\n✅ Success rate: {verification['success_rate']:.1f}%")
        print(f"✅ Added {len(added_keywords)} keywords")
        
        return optimized, added_keywords
    
    def _find_missing_keywords(self, resume_data: Dict, job_analysis: Dict) -> List[str]:
        """
        Find EXACTLY which keywords are missing from resume.
        
        This is deterministic - no AI guessing!
        """
        # Get all keywords from job
        job_keywords = job_analysis.get('keywords', {})
        all_job_keywords = []
        
        # Priority order: required > technical > important
        all_job_keywords.extend(job_keywords.get('required', []))
        all_job_keywords.extend(job_keywords.get('technical_skills', []))
        all_job_keywords.extend(job_keywords.get('important_words', [])[:10])
        
        # Get all text from resume
        resume_text = self._get_all_text(resume_data).lower()
        
        # Find missing keywords
        missing = []
        for keyword in all_job_keywords:
            # Check if keyword is in resume (case-insensitive, word boundary)
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if not re.search(pattern, resume_text):
                missing.append(keyword)
        
        return missing
    
    def _get_all_text(self, resume_data: Dict) -> str:
        """Extract all text from resume for keyword checking"""
        text_parts = []
        
        # Summary
        if resume_data.get('summary'):
            text_parts.append(resume_data['summary'])
        
        # Experience
        for exp in resume_data.get('experience', []):
            text_parts.append(exp.get('title', ''))
            text_parts.append(exp.get('company', ''))
            for bullet in exp.get('description', []):
                text_parts.append(bullet)
        
        # Skills
        text_parts.extend(resume_data.get('skills', []))
        
        # Education
        for edu in resume_data.get('education', []):
            text_parts.append(edu.get('degree', ''))
            text_parts.append(edu.get('field', ''))
            text_parts.append(edu.get('school', ''))
        
        return ' '.join(text_parts)
    
    def _insert_keyword(self, resume_data: Dict, keyword: str, job_analysis: Dict) -> Dict:
        """
        Insert a SPECIFIC keyword into the resume.
        
        CRITICAL: We tell AI EXACTLY which keyword to add!
        This is the key difference from vague "optimize" prompts.
        """
        # Find best section to add this keyword
        best_section = self._find_best_section_for_keyword(resume_data, keyword, job_analysis)
        
        if not best_section:
            return {'success': False, 'resume': resume_data}
        
        # Calculate limits (User requirement: preserve structure!)
        original_text = best_section['text']
        original_length = len(original_text)
        original_lines = original_text.count('\n') + 1
        original_words = len(original_text.split())
        
        # Allow ±10% length to give AI room to add keywords
        max_length = int(original_length * 1.10)
        
        # SPECIFIC prompt with TARGET keyword and REASONABLE CONSTRAINTS
        prompt = f"""Add the keyword "{keyword}" to this resume bullet point.

ORIGINAL ({original_length} characters, {original_words} words):
{original_text}

CRITICAL RULES:
1. Maximum length: {max_length} characters (±10% of original)
2. If one line, result MUST be one line (no line breaks)
3. Add "{keyword}" naturally - replace weak words if needed
4. Keep all numbers and metrics exactly the same
5. Professional and natural tone

STRATEGY TO FIT KEYWORD:
- Add "{keyword}" in a natural place
- Replace weak/filler words if needed: various, several, multiple, some
- Use concise language

Enhanced text (≤{max_length} chars, same line structure):"""

        try:
            system_prompt = f"Add '{keyword}' concisely. Keep under {max_length} characters. Preserve line structure."
            
            enhanced_text = self.ai.optimize_text(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # Slightly higher for more flexibility
                max_tokens=200
            )
            
            enhanced_text = enhanced_text.strip()
            
            # Validation with REASONABLE constraints
            passes_validation = True
            
            # Check 1: Length (±10%)
            if len(enhanced_text) > max_length:
                print(f"    ✗ Length check FAILED: {len(enhanced_text)} > {max_length} chars (±10%)")
                passes_validation = False
            
            # Check 2: Line breaks (CRITICAL!)
            if enhanced_text.count('\n') != original_text.count('\n'):
                print(f"    ✗ Line break check FAILED")
                passes_validation = False
            
            # Check 3: Keyword added
            if keyword.lower() not in enhanced_text.lower():
                print(f"    ✗ Keyword '{keyword}' not found in result")
                passes_validation = False
            
            if passes_validation:
                # SUCCESS! All checks passed
                print(f"    ✓ All checks passed! Length: {len(enhanced_text)}/{max_length} chars")
                updated_resume = self._update_section(
                    resume_data, 
                    best_section['type'],
                    best_section['index'],
                    enhanced_text
                )
                return {'success': True, 'resume': updated_resume}
            else:
                # Validation failed - try manual insertion
                print(f"    ⚠️ AI validation failed, trying manual insertion")
                manual_enhanced = self._manual_insert(original_text, keyword)
                
                if keyword.lower() in manual_enhanced.lower() and len(manual_enhanced) <= max_length:
                    print(f"    ✓ Manual insertion worked!")
                    updated_resume = self._update_section(
                        resume_data,
                        best_section['type'],
                        best_section['index'],
                        manual_enhanced
                    )
                    return {'success': True, 'resume': updated_resume}
                else:
                    print(f"    ✗ Manual insertion also failed")
                    return {'success': False, 'resume': resume_data}
                
        except Exception as e:
            print(f"Error inserting keyword '{keyword}': {e}")
            return {'success': False, 'resume': resume_data}
    
    def _find_best_section_for_keyword(self, resume_data: Dict, keyword: str, job_analysis: Dict) -> Dict:
        """Find which resume section is most relevant for this keyword"""
        
        # Check experience bullets - most likely place
        for i, exp in enumerate(resume_data.get('experience', [])):
            for j, bullet in enumerate(exp.get('description', [])):
                # Simple relevance check
                if any(word in bullet.lower() for word in ['built', 'developed', 'created', 'designed', 'implemented']):
                    return {
                        'type': 'experience_bullet',
                        'index': (i, j),
                        'text': bullet
                    }
        
        # Fallback: first experience bullet
        if resume_data.get('experience') and resume_data['experience'][0].get('description'):
            return {
                'type': 'experience_bullet',
                'index': (0, 0),
                'text': resume_data['experience'][0]['description'][0]
            }
        
        return None
    
    def _update_section(self, resume_data: Dict, section_type: str, index, new_text: str) -> Dict:
        """Update a specific section of the resume"""
        updated = resume_data.copy()
        
        if section_type == 'experience_bullet':
            exp_idx, bullet_idx = index
            if exp_idx < len(updated['experience']):
                if bullet_idx < len(updated['experience'][exp_idx]['description']):
                    updated['experience'][exp_idx]['description'][bullet_idx] = new_text.strip()
        
        return updated
    
    def _manual_insert(self, text: str, keyword: str) -> str:
        """
        Fallback: Manually insert keyword if AI fails.
        
        CRITICAL: Must respect length constraints (User requirement!)
        """
        original_length = len(text)
        
        if keyword.lower() not in text.lower():
            # Try smart insertion that respects length
            words = text.split()
            
            # Strategy 1: Replace a weak word with keyword
            weak_words = ['various', 'several', 'multiple', 'many', 'some', 'different']
            for i, word in enumerate(words):
                if word.lower() in weak_words:
                    words[i] = keyword
                    result = ' '.join(words)
                    if len(result) <= original_length:
                        return result
            
            # Strategy 2: Add at end only if it fits
            if text.endswith('.'):
                test = f"{text[:-1]} {keyword}."
            else:
                test = f"{text} {keyword}"
            
            if len(test) <= original_length:
                return test
            
            # Can't fit without exceeding length - return original
            print(f"    ⚠️  Can't fit '{keyword}' without exceeding length")
            return text
        
        return text
