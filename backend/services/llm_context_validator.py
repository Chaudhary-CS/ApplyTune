"""
LLM-Powered Context Validator (Layer 2)
Uses AI to validate if keyword insertions are believable and truthful.
"""

from typing import Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)

class LLMContextValidator:
    """
    Uses LLM to validate if adding a keyword to a context would be believable.
    This is Layer 2 - catches contextual issues that rule-based systems miss.
    """
    
    def __init__(self, llm_client):
        """
        Args:
            llm_client: The Groq/Ollama client for making LLM calls
        """
        self.client = llm_client
        self.model = "llama-3.3-70b-versatile"  # Using Groq's latest model
    
    def validate_keyword_insertion(self, keyword: str, bullet_point: str, 
                                   job_context: Optional[str] = None) -> Dict:
        """
        Ask LLM if inserting a keyword into a bullet point would be believable.
        
        Args:
            keyword: The keyword to potentially insert
            bullet_point: The original bullet point text
            job_context: Optional job description context for better validation
        
        Returns:
            {
                'valid': bool,
                'confidence': 'HIGH'/'MEDIUM'/'LOW',
                'reason': str,
                'risk_level': 'SAFE'/'CAUTION'/'FABRICATION',
                'suggestion': str (alternative approach if not valid)
            }
        """
        # Build context-aware prompt
        job_context_text = f"\n\nJob requirement context: {job_context}" if job_context else ""
        
        prompt = f"""You are a senior technical resume reviewer. Analyze if adding the keyword "{keyword}" to this resume bullet point would be TRUTHFUL and BELIEVABLE.

Original bullet point:
"{bullet_point}"
{job_context_text}

Question: Would adding "{keyword}" to this bullet point make sense and look authentic, or would it seem fabricated?

Consider:
1. Does the keyword relate to what the bullet describes?
2. Would a recruiter believe this person actually used this technology?
3. Could this be verified (e.g., in code, GitHub, projects)?

Respond ONLY with valid JSON (no markdown, no code blocks):
{{
  "is_believable": true or false,
  "confidence": "HIGH" or "MEDIUM" or "LOW",
  "risk_level": "SAFE" or "CAUTION" or "FABRICATION",
  "reason": "one clear sentence explanation",
  "suggestion": "if not believable, suggest where this keyword could naturally fit, or say 'Add to Skills section only'"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for consistent, logical validation
                max_tokens=300
            )
            
            # Parse LLM response
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            result = json.loads(content)
            
            # Map LLM response to our standard format
            return {
                'valid': result.get('is_believable', False),
                'confidence': result.get('confidence', 'LOW'),
                'reason': result.get('reason', 'No explanation provided'),
                'risk_level': result.get('risk_level', 'CAUTION'),
                'suggestion': result.get('suggestion', 'Review manually')
            }
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM response: {e}. Raw content: {content[:200]}")
            # Fallback: allow but with low confidence
            return {
                'valid': True,
                'confidence': 'LOW',
                'reason': 'LLM validation failed, allowing with caution',
                'risk_level': 'CAUTION',
                'suggestion': 'Manual review recommended'
            }
        except Exception as e:
            logger.error(f"LLM validation error: {e}")
            # On error, be conservative and allow (don't block user completely)
            return {
                'valid': True,
                'confidence': 'LOW',
                'reason': f'Validation unavailable: {str(e)}',
                'risk_level': 'CAUTION',
                'suggestion': 'Manual review recommended'
            }
    
    def validate_multiple_insertions(self, keywords: list, bullet_point: str, 
                                    job_context: Optional[str] = None) -> Dict:
        """
        Validate inserting multiple keywords at once (batch validation).
        This checks if adding ALL keywords together would be suspicious.
        """
        keywords_str = '", "'.join(keywords)
        job_context_text = f"\n\nJob requirement context: {job_context}" if job_context else ""
        
        prompt = f"""You are a senior technical resume reviewer. Analyze if adding these keywords: "{keywords_str}" to this resume bullet point would look authentic or like keyword stuffing.

Original bullet point:
"{bullet_point}"
{job_context_text}

Question: Would adding ALL these keywords together be believable, or is it too many changes?

Respond ONLY with valid JSON (no markdown, no code blocks):
{{
  "is_believable": true or false,
  "confidence": "HIGH" or "MEDIUM" or "LOW",
  "risk_level": "SAFE" or "CAUTION" or "FABRICATION",
  "reason": "one clear sentence",
  "max_safe_keywords": 2,
  "priority_keywords": ["keyword1", "keyword2"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            result = json.loads(content)
            
            return {
                'valid': result.get('is_believable', False),
                'confidence': result.get('confidence', 'LOW'),
                'reason': result.get('reason', 'No explanation'),
                'risk_level': result.get('risk_level', 'CAUTION'),
                'max_safe_keywords': result.get('max_safe_keywords', 1),
                'priority_keywords': result.get('priority_keywords', keywords[:1])
            }
            
        except Exception as e:
            logger.error(f"Batch validation error: {e}")
            # Fallback: limit to 1 keyword per bullet
            return {
                'valid': len(keywords) <= 1,
                'confidence': 'LOW',
                'reason': 'Batch validation unavailable',
                'risk_level': 'CAUTION',
                'max_safe_keywords': 1,
                'priority_keywords': keywords[:1]
            }
