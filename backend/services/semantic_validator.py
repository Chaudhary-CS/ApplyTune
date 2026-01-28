"""
Semantic Similarity Validator (Layer 3)
Uses sentence embeddings to compute numerical similarity scores.
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SemanticValidator:
    """
    Uses sentence transformers to compute semantic similarity between keywords and context.
    This is Layer 3 - provides precise numerical confidence scores.
    """
    
    def __init__(self):
        self.model = None
        self._model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Lazy load the sentence transformer model."""
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            
            # Use lightweight model (~80MB, fast inference)
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.np = np
            self._model_loaded = True
            logger.info("✅ Sentence transformer model loaded successfully")
            
        except ImportError:
            logger.warning("⚠️ sentence-transformers not installed. Layer 3 validation disabled.")
            logger.warning("Install with: pip install sentence-transformers")
            self._model_loaded = False
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            self._model_loaded = False
    
    def compute_similarity(self, keyword: str, context: str) -> float:
        """
        Compute cosine similarity between keyword and context.
        Returns a score between 0 and 1 (higher = more similar).
        """
        if not self._model_loaded:
            # Return neutral score if model not available
            return 0.5
        
        try:
            # Generate embeddings
            keyword_embedding = self.model.encode(keyword)
            context_embedding = self.model.encode(context)
            
            # Compute cosine similarity
            similarity = self.np.dot(keyword_embedding, context_embedding) / (
                self.np.linalg.norm(keyword_embedding) * self.np.linalg.norm(context_embedding)
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity computation error: {e}")
            return 0.5  # Neutral score on error
    
    def validate_keyword_similarity(self, keyword: str, context: str, 
                                   threshold: float = 0.3) -> Dict:
        """
        Validate if keyword is semantically similar to context.
        
        Args:
            keyword: The keyword to validate
            context: The context to compare against
            threshold: Minimum similarity score (0-1) to be considered valid
        
        Returns:
            {
                'valid': bool,
                'confidence': 'HIGH'/'MEDIUM'/'LOW',
                'similarity_score': float (0-1),
                'reason': str
            }
        """
        similarity = self.compute_similarity(keyword, context)
        
        # Determine confidence level
        if similarity >= 0.6:
            confidence = 'HIGH'
            valid = True
            reason = f'Strong semantic match (score: {similarity:.2f})'
        elif similarity >= threshold:
            confidence = 'MEDIUM'
            valid = True
            reason = f'Moderate semantic match (score: {similarity:.2f})'
        else:
            confidence = 'HIGH'  # High confidence in rejection
            valid = False
            reason = f'Weak semantic match (score: {similarity:.2f}), likely unrelated'
        
        return {
            'valid': valid,
            'confidence': confidence,
            'similarity_score': round(similarity, 3),
            'reason': reason
        }
    
    def batch_validate_similarities(self, keywords: List[str], context: str, 
                                   threshold: float = 0.3) -> List[Dict]:
        """Validate multiple keywords against the same context."""
        results = []
        for keyword in keywords:
            result = self.validate_keyword_similarity(keyword, context, threshold)
            result['keyword'] = keyword
            results.append(result)
        return results
    
    def find_best_matches(self, keywords: List[str], contexts: List[str], 
                         top_k: int = 3) -> Dict:
        """
        For each keyword, find the best matching contexts.
        Useful for suggesting where to place keywords.
        
        Returns:
            {
                'keyword1': [
                    {'context': 'text', 'score': 0.75},
                    {'context': 'text', 'score': 0.65},
                    ...
                ]
            }
        """
        if not self._model_loaded:
            return {}
        
        matches = {}
        
        for keyword in keywords:
            keyword_scores = []
            
            for context in contexts:
                score = self.compute_similarity(keyword, context)
                keyword_scores.append({
                    'context': context,
                    'score': round(score, 3)
                })
            
            # Sort by score and take top-k
            keyword_scores.sort(key=lambda x: x['score'], reverse=True)
            matches[keyword] = keyword_scores[:top_k]
        
        return matches
