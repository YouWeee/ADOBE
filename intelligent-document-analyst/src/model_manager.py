"""
Model Manager Module
Provides offline text processing methods without external model dependencies.
"""

import logging
import re
import math
import yaml
import torch
from typing import Dict, Any, Optional, List
from pathlib import Path
from collections import Counter
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer


class ModelManager:
    """
    Manages all NLP models with size and performance constraints.
    
    Total model budget: < 1GB
    Target models:
    - Sentence encoder: all-MiniLM-L6-v2 (~23MB)
    - Text classifier: distilbert-base-uncased (~268MB) 
    - Total: ~291MB (well under 1GB)
    """
    
    def __init__(self, models_dir: str = "models", config_path: str = None):
        """Initialize the model manager."""
        self.logger = logging.getLogger(__name__)
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Model storage
        self._sentence_encoder = None
        self._text_classifier = None
        self._tokenizer = None
        
        # Model specifications (name -> size estimate)
        self.model_specs = {
            'sentence_encoder': {
                'name': 'all-MiniLM-L6-v2',
                'size_mb': 23,
                'description': 'Lightweight sentence embeddings'
            },
            'text_classifier': {
                'name': 'distilbert-base-uncased',
                'size_mb': 268,
                'description': 'Distilled BERT for text classification'
            }
        }
        
        self.logger.info("Model Manager initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration file."""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                self.logger.warning(f"Could not load config: {e}")
        
        # Default configuration
        return {
            'models': {
                'sentence_encoder': 'all-MiniLM-L6-v2',
                'text_classifier': 'distilbert-base-uncased'
            }
        }
    
    def get_sentence_encoder(self):
        """Get sentence encoder model (offline fallback only)."""
        # Always return None to force fallback methods
        self.logger.info("Using offline-only mode - no external models")
        return None
    
    def get_text_classifier(self):
        """Get text classification pipeline (offline fallback only)."""
        # Always return None to force fallback methods
        self.logger.info("Using offline-only mode - no external models")
        return None
    
    def get_tokenizer(self, model_name: str = None):
        """Get tokenizer for text processing (offline fallback only)."""
        # Always return None to force fallback methods
        self.logger.info("Using offline-only mode - no external models")
        return None
    
    def encode_sentences(self, texts: list):
        """Encode sentences to embeddings (offline fallback only)."""
        encoder = self.get_sentence_encoder()
        if encoder is None:
            self.logger.info("No sentence encoder available - using offline mode")
            return None
        
        try:
            embeddings = encoder.encode(texts, convert_to_tensor=True)
            return embeddings
        except Exception as e:
            self.logger.error(f"Error encoding sentences: {e}")
            return None
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts (offline fallback only)."""
        encoder = self.get_sentence_encoder()
        if encoder is None:
            # Use fallback similarity based on word overlap
            return self._fallback_similarity_score(text1, text2)
        
        try:
            embeddings = encoder.encode([text1, text2], convert_to_tensor=True)
            
            # Compute cosine similarity
            similarity = torch.cosine_similarity(
                embeddings[0].unsqueeze(0), 
                embeddings[1].unsqueeze(0)
            ).item()
            
            return max(0.0, similarity)  # Ensure non-negative
            
        except Exception as e:
            self.logger.error(f"Error computing similarity: {e}")
            return self._fallback_similarity_score(text1, text2)
    
    def classify_text_relevance(self, text: str, context: str) -> float:
        """Classify text relevance to a given context."""
        classifier = self.get_text_classifier()
        
        if classifier is None:
            # Fallback: use simple keyword matching
            return self._fallback_relevance_score(text, context)
        
        try:
            # Combine text and context for classification
            combined_text = f"{context} [SEP] {text}"
            
            # Limit text length to avoid issues
            if len(combined_text) > 512:
                combined_text = combined_text[:512]
            
            results = classifier(combined_text)
            
            # Extract confidence score (assuming binary classification)
            if results and len(results) > 0:
                scores = results[0]
                # Find the positive/relevant class score
                for score_info in scores:
                    if 'POSITIVE' in score_info.get('label', '').upper():
                        return score_info['score']
            
            return 0.5  # Neutral score if unclear
            
        except Exception as e:
            self.logger.error(f"Error in text classification: {e}")
            return self._fallback_relevance_score(text, context)
    
    def _fallback_relevance_score(self, text: str, context: str) -> float:
        """Fallback relevance scoring using simple methods."""
        text_lower = text.lower()
        context_lower = context.lower()
        
        # Simple word overlap scoring
        text_words = set(text_lower.split())
        context_words = set(context_lower.split())
        
        if not text_words or not context_words:
            return 0.0
        
        overlap = len(text_words.intersection(context_words))
        union = len(text_words.union(context_words))
        
        return overlap / union if union > 0 else 0.0
    
    def _fallback_similarity_score(self, text1: str, text2: str) -> float:
        """Fallback similarity scoring using simple word overlap."""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Simple word overlap scoring
        words1 = set(text1_lower.split())
        words2 = set(text2_lower.split())
        
        if not words1 or not words2:
            return 0.0
        
        overlap = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return overlap / union if union > 0 else 0.0
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models."""
        info = {
            'sentence_encoder_loaded': self._sentence_encoder is not None,
            'text_classifier_loaded': self._text_classifier is not None,
            'estimated_total_size_mb': sum(spec['size_mb'] for spec in self.model_specs.values()),
            'model_specs': self.model_specs
        }
        
        return info
    
    def warm_up_models(self):
        """Pre-load all models to avoid lazy loading delays."""
        self.logger.info("Warming up models...")
        
        try:
            # Load sentence encoder
            encoder = self.get_sentence_encoder()
            test_embedding = encoder.encode(["test sentence"], convert_to_tensor=True)
            self.logger.info("✅ Sentence encoder warmed up")
            
            # Load text classifier
            classifier = self.get_text_classifier()
            if classifier:
                test_result = classifier("test text")
                self.logger.info("✅ Text classifier warmed up")
            
        except Exception as e:
            self.logger.error(f"Error during model warm-up: {e}")
    
    def cleanup(self):
        """Clean up loaded models to free memory."""
        self._sentence_encoder = None
        self._text_classifier = None
        self._tokenizer = None
        
        # Force garbage collection
        import gc
        gc.collect()
        
        self.logger.info("Models cleaned up")
