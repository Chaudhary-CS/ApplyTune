"""
Multi-Layer Context Validator
Combines all 3 validation layers for maximum accuracy.
"""

from typing import Dict, List, Optional
import logging
import os
from .adaptive_tech_validator import AdaptiveTechValidator
from .tech_ecosystem_validator import TechEcosystemValidator  # Keep as fallback
from .llm_context_validator import LLMContextValidator
from .semantic_validator import SemanticValidator

logger = logging.getLogger(__name__)

class MultiLayerValidator:
    """
    Unified validator that combines 3 layers:
    - Layer 1: AI-Powered Tech Validator (100% adaptive, zero hardcoded)
    - Layer 2: LLM Context Validation (smart, context-aware)
    - Layer 3: Semantic Similarity (precise, numerical)
    
    NEW: Layer 1 is now 100% AI-powered - no hardcoded tech dictionaries!
    Works with ANY technology (even ones invented in 2030).
    """
    
    def __init__(self, llm_client=None, use_adaptive=True):
        """
        Args:
            llm_client: Optional Groq/Ollama client for AI validation
            use_adaptive: If True, uses AI-powered validator (recommended). 
                         If False, falls back to hardcoded dictionaries.
        """
        # Layer 1: Choose adaptive (AI) or hardcoded (fallback)
        use_adaptive_layer1 = use_adaptive and os.getenv('ADAPTIVE_VALIDATION', 'true').lower() == 'true'
        
        if use_adaptive_layer1 and llm_client:
            self.layer1 = AdaptiveTechValidator(llm_client)
            logger.info("🧠 Using ADAPTIVE Layer 1 (100% AI, zero hardcoded rules)")
        else:
            self.layer1 = TechEcosystemValidator()
            logger.info("📚 Using HARDCODED Layer 1 (fallback mode)")
        
        # Layer 2: LLM Context Validator
        self.layer2 = LLMContextValidator(llm_client) if llm_client else None
        
        # Layer 3: Semantic Similarity
        self.layer3 = SemanticValidator()
        
        # Track statistics
        self.stats = {
            'total_validations': 0,
            'layer1_rejections': 0,
            'layer2_rejections': 0,
            'layer3_rejections': 0,
            'approved': 0
        }
        
        logger.info("🛡️ Multi-layer validator initialized")
        logger.info(f"  ✅ Layer 1: Tech Ecosystem Graph")
        logger.info(f"  {'✅' if self.layer2 else '⚠️'} Layer 2: LLM Validator {'(enabled)' if self.layer2 else '(disabled - no LLM client)'}")
        logger.info(f"  ✅ Layer 3: Semantic Similarity")
    
    def validate_keyword(self, keyword: str, context: str, 
                        job_context: Optional[str] = None,
                        strict_mode: bool = False) -> Dict:
        """
        Main validation method: runs keyword through all 3 layers.
        
        Args:
            keyword: The keyword to validate
            context: The bullet point or section text
            job_context: Optional job description for better LLM validation
            strict_mode: If True, requires all layers to approve. If False, majority vote.
        
        Returns:
            {
                'valid': bool,
                'overall_confidence': 'HIGH'/'MEDIUM'/'LOW',
                'reason': str (primary reason for decision),
                'layer1_result': dict,
                'layer2_result': dict or None,
                'layer3_result': dict,
                'decision_path': str (which layers were used)
            }
        """
        self.stats['total_validations'] += 1
        
        results = {
            'layer1_result': None,
            'layer2_result': None,
            'layer3_result': None,
            'decision_path': []
        }
        
        # ========== LAYER 1: Tech Ecosystem Graph (FAST) ==========
        layer1_result = self.layer1.validate_keyword_in_context(keyword, context)
        results['layer1_result'] = layer1_result
        results['decision_path'].append('Layer1')
        
        # If Layer 1 rejects with HIGH confidence, stop here (saves time)
        if not layer1_result['valid'] and layer1_result['confidence'] == 'HIGH':
            self.stats['layer1_rejections'] += 1
            logger.debug(f"❌ Layer 1 REJECT: {keyword} - {layer1_result['reason']}")
            return {
                'valid': False,
                'overall_confidence': 'HIGH',
                'reason': f"Layer 1: {layer1_result['reason']}",
                **results,
                'decision_path': ' → '.join(results['decision_path'])
            }
        
        # ========== LAYER 2: LLM Validation (SMART) ==========
        if self.layer2:
            layer2_result = self.layer2.validate_keyword_insertion(
                keyword, context, job_context
            )
            results['layer2_result'] = layer2_result
            results['decision_path'].append('Layer2')
            
            # If Layer 2 detects FABRICATION risk, reject
            if layer2_result['risk_level'] == 'FABRICATION':
                self.stats['layer2_rejections'] += 1
                logger.debug(f"❌ Layer 2 REJECT: {keyword} - {layer2_result['reason']}")
                return {
                    'valid': False,
                    'overall_confidence': 'HIGH',
                    'reason': f"Layer 2: {layer2_result['reason']}",
                    **results,
                    'decision_path': ' → '.join(results['decision_path'])
                }
        
        # ========== LAYER 3: Semantic Similarity (PRECISE) ==========
        layer3_result = self.layer3.validate_keyword_similarity(keyword, context)
        results['layer3_result'] = layer3_result
        results['decision_path'].append('Layer3')
        
        # If Layer 3 shows very low similarity and we're in strict mode, reject
        if strict_mode and not layer3_result['valid'] and layer3_result['confidence'] == 'HIGH':
            self.stats['layer3_rejections'] += 1
            logger.debug(f"❌ Layer 3 REJECT: {keyword} - {layer3_result['reason']}")
            return {
                'valid': False,
                'overall_confidence': 'MEDIUM',
                'reason': f"Layer 3: {layer3_result['reason']}",
                **results,
                'decision_path': ' → '.join(results['decision_path'])
            }
        
        # ========== FINAL DECISION: Combine All Layers ==========
        valid_votes = sum([
            1 if layer1_result['valid'] else 0,
            1 if results['layer2_result'] and results['layer2_result']['valid'] else 0,
            1 if layer3_result['valid'] else 0
        ])
        
        total_layers = 2 + (1 if self.layer2 else 0)  # Layer 1 + 3 always active, Layer 2 optional
        
        if strict_mode:
            # Strict: ALL layers must approve
            final_valid = valid_votes == total_layers
        else:
            # Lenient: Majority approval (2 out of 3, or 2 out of 2 if no LLM)
            final_valid = valid_votes >= (total_layers / 2)
        
        # Determine overall confidence
        high_confidence_count = sum([
            1 if layer1_result['confidence'] == 'HIGH' else 0,
            1 if results['layer2_result'] and results['layer2_result']['confidence'] == 'HIGH' else 0,
            1 if layer3_result['confidence'] == 'HIGH' else 0
        ])
        
        if high_confidence_count >= 2:
            overall_confidence = 'HIGH'
        elif high_confidence_count >= 1:
            overall_confidence = 'MEDIUM'
        else:
            overall_confidence = 'LOW'
        
        # Build combined reason
        if final_valid:
            self.stats['approved'] += 1
            reasons = []
            if layer1_result['valid']:
                reasons.append(f"✓ Ecosystem match")
            if results['layer2_result'] and results['layer2_result']['valid']:
                reasons.append(f"✓ LLM approved")
            if layer3_result['valid']:
                reasons.append(f"✓ Semantic similarity: {layer3_result['similarity_score']}")
            
            reason = f"Approved by {valid_votes}/{total_layers} layers: {', '.join(reasons)}"
        else:
            reasons = []
            if not layer1_result['valid']:
                reasons.append(f"✗ {layer1_result['reason']}")
            if results['layer2_result'] and not results['layer2_result']['valid']:
                reasons.append(f"✗ {results['layer2_result']['reason']}")
            if not layer3_result['valid']:
                reasons.append(f"✗ {layer3_result['reason']}")
            
            reason = f"Rejected: {reasons[0]}"  # Use first rejection reason
        
        logger.debug(f"{'✅' if final_valid else '❌'} {keyword}: {reason}")
        
        return {
            'valid': final_valid,
            'overall_confidence': overall_confidence,
            'reason': reason,
            **results,
            'decision_path': ' → '.join(results['decision_path'])
        }
    
    def batch_validate(self, keywords: List[str], context: str, 
                      job_context: Optional[str] = None,
                      strict_mode: bool = False) -> List[Dict]:
        """Validate multiple keywords against the same context."""
        results = []
        for keyword in keywords:
            result = self.validate_keyword(keyword, context, job_context, strict_mode)
            result['keyword'] = keyword
            results.append(result)
        return results
    
    def get_validation_stats(self) -> Dict:
        """Get statistics about validation performance."""
        total = self.stats['total_validations']
        if total == 0:
            return self.stats
        
        return {
            **self.stats,
            'approval_rate': f"{(self.stats['approved'] / total) * 100:.1f}%",
            'layer1_rejection_rate': f"{(self.stats['layer1_rejections'] / total) * 100:.1f}%",
            'layer2_rejection_rate': f"{(self.stats['layer2_rejections'] / total) * 100:.1f}%",
            'layer3_rejection_rate': f"{(self.stats['layer3_rejections'] / total) * 100:.1f}%"
        }
    
    def find_best_placement(self, keyword: str, bullet_points: List[str]) -> Dict:
        """
        Find the best bullet point to place a keyword.
        Uses all 3 layers to score each possible placement.
        """
        scores = []
        
        for bullet in bullet_points:
            validation = self.validate_keyword(keyword, bullet)
            
            # Compute overall score (0-100)
            if not validation['valid']:
                score = 0
            else:
                # Base score from semantic similarity
                semantic_score = validation['layer3_result']['similarity_score'] * 100
                
                # Boost if Layer 1 approved
                if validation['layer1_result']['valid']:
                    semantic_score += 10
                
                # Boost if Layer 2 approved
                if validation['layer2_result'] and validation['layer2_result']['valid']:
                    semantic_score += 10
                
                score = min(100, semantic_score)
            
            scores.append({
                'bullet': bullet,
                'score': round(score, 1),
                'recommendation': 'BEST' if score >= 70 else 'GOOD' if score >= 50 else 'WEAK' if score >= 30 else 'AVOID'
            })
        
        # Sort by score
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'keyword': keyword,
            'placements': scores,
            'best_match': scores[0] if scores else None
        }
