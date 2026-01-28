"""
Adaptive Tech Validator (Layer 1 - Pure AI)
NO hardcoded dictionaries - 100% intelligent and adaptive!

This validator works with:
- Technologies invented in 2030 (future-proof)
- ANY domain (finance, healthcare, law, not just software)
- Emerging tech (Mojo, Bun, Deno, Zig, etc.)
- Domain-specific terminology

Replaces tech_ecosystem_validator.py's hardcoded dictionaries with pure AI.
"""

from typing import Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class AdaptiveTechValidator:
    """
    100% AI-powered tech compatibility validator.
    Zero hardcoded rules - adapts to ANY technology, ANY domain.
    
    Benefits over hardcoded approach:
    - ✅ Works with new tech (Bun, Deno, Mojo, Zig, future inventions)
    - ✅ Adapts to ANY domain (software, finance, healthcare, law)
    - ✅ Zero maintenance (no dictionaries to update)
    - ✅ Future-proof (will work in 2030)
    """
    
    def __init__(self, llm_client):
        """
        Args:
            llm_client: The Groq/Ollama client for making LLM calls
        """
        self.client = llm_client
        self.model = "llama-3.3-70b-versatile"
        
        # Cache for speed (optional optimization)
        self.compatibility_cache = {}
        
        logger.info("✅ Adaptive Tech Validator initialized (100% AI-powered, zero hardcoded rules)")
    
    def validate_keyword_in_context(self, keyword: str, context: str) -> Dict:
        """
        Main validation method: Uses AI to determine if keyword fits in context.
        NO hardcoded rules - pure intelligence!
        
        Args:
            keyword: The technology/skill to validate
            context: The bullet point or section text
        
        Returns:
            {
                'valid': bool,
                'confidence': 'HIGH'/'MEDIUM'/'LOW',
                'reason': str,
                'ecosystem_relationship': str,
                'suggestion': str (if not valid)
            }
        """
        # Check cache first (performance optimization)
        cache_key = f"{keyword.lower()}::{context[:50].lower()}"
        if cache_key in self.compatibility_cache:
            cached = self.compatibility_cache[cache_key]
            logger.debug(f"✅ Cache hit for '{keyword}'")
            return cached
        
        # Ask AI to intelligently validate
        prompt = f"""You are a technical expert and career advisor. Analyze if adding this keyword to the resume context would be believable and appropriate.

Keyword/Technology: "{keyword}"

Resume Context:
"{context}"

Determine:
1. Does this keyword naturally fit in this context?
2. Would these technologies/skills typically be used together?
3. Is this a believable combination for a real professional?

Respond ONLY with valid JSON (no markdown, no code blocks):
{{
  "compatible": true or false,
  "confidence": "HIGH" or "MEDIUM" or "LOW",
  "reason": "one clear sentence explaining why it fits or doesn't fit",
  "ecosystem_relationship": "commonly paired" or "sometimes together" or "rarely combined" or "incompatible domains",
  "suggestion": "if not compatible, suggest where this keyword would fit better"
}}

Examples:
- pytorch + "machine learning pipeline" → compatible (ML ecosystem)
- pytorch + "Azure DevOps CI/CD" → incompatible (ML vs DevOps)
- kubernetes + "container deployment" → compatible (DevOps ecosystem)
- Excel + "financial analysis" → compatible (finance domain)
- blockchain + "supply chain tracking" → compatible (emerging tech use case)
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for consistent, logical responses
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up markdown if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            result = json.loads(content)
            
            # Map to our standard format
            validation_result = {
                'valid': result.get('compatible', False),
                'confidence': result.get('confidence', 'LOW'),
                'reason': result.get('reason', 'No explanation provided'),
                'ecosystem_relationship': result.get('ecosystem_relationship', 'unknown'),
                'suggestion': result.get('suggestion', 'Review manually'),
                'keyword_ecosystems': [],  # AI-determined, not from hardcoded list
                'context_ecosystems': []   # AI-determined, not from hardcoded list
            }
            
            # Cache result for future use (performance optimization)
            self.compatibility_cache[cache_key] = validation_result
            
            logger.debug(f"{'✅' if validation_result['valid'] else '❌'} AI validation: {keyword} → {validation_result['reason'][:80]}")
            
            return validation_result
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse AI response: {e}")
            # Fallback: allow with low confidence (don't block user completely)
            return {
                'valid': True,
                'confidence': 'LOW',
                'reason': 'AI validation unavailable, allowing with caution',
                'ecosystem_relationship': 'unknown',
                'suggestion': 'Manual review recommended',
                'keyword_ecosystems': [],
                'context_ecosystems': []
            }
        except Exception as e:
            logger.error(f"AI validation error: {e}")
            # Fallback: allow with low confidence
            return {
                'valid': True,
                'confidence': 'LOW',
                'reason': f'Validation unavailable: {str(e)}',
                'ecosystem_relationship': 'unknown',
                'suggestion': 'Manual review recommended',
                'keyword_ecosystems': [],
                'context_ecosystems': []
            }
    
    def batch_validate(self, keywords: List[str], context: str) -> List[Dict]:
        """Validate multiple keywords against the same context."""
        results = []
        for keyword in keywords:
            result = self.validate_keyword_in_context(keyword, context)
            result['keyword'] = keyword
            results.append(result)
        return results
    
    def clear_cache(self):
        """Clear the compatibility cache (useful for testing or retraining)."""
        self.compatibility_cache.clear()
        logger.info("✅ Compatibility cache cleared")
    
    def get_cache_stats(self) -> Dict:
        """Get statistics about cache performance."""
        return {
            'cache_size': len(self.compatibility_cache),
            'estimated_api_calls_saved': len(self.compatibility_cache)
        }
