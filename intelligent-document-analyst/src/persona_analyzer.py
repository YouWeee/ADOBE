"""
Persona Analyzer Module
Analyzes persona and job-to-be-done requirements.
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from model_manager import ModelManager


@dataclass
class PersonaAnalysis:
    """Data class for persona analysis results."""
    persona: str
    job_to_be_done: str
    expertise_areas: List[str]
    key_interests: List[str]
    priority_keywords: List[str]
    analysis_context: Dict[str, Any]


class PersonaAnalyzer:
    """
    Analyzes persona and job requirements to understand what content is relevant.
    
    This is a basic stub implementation for testing.
    Will be enhanced with NLP models in Step 2.
    """
    
    def __init__(self, model_manager: ModelManager = None):
        """Initialize the persona analyzer."""
        self.logger = logging.getLogger(__name__)
        self.model_manager = model_manager or ModelManager()
        
        # Initialize NLTK components (download if needed)
        self._init_nltk()
        
        # TF-IDF vectorizer for keyword extraction
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=20,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def analyze_persona(self, persona: str, job_to_be_done: str) -> PersonaAnalysis:
        """
        Analyze persona and job requirements (stub implementation).
        
        Args:
            persona: Persona description
            job_to_be_done: Job/task description
            
        Returns:
            PersonaAnalysis object with extracted insights
        """
        self.logger.info("Analyzing persona and job requirements...")
        
        # Basic keyword extraction (stub - will be enhanced with NLP)
        expertise_areas = self._extract_expertise_areas(persona)
        key_interests = self._extract_key_interests(job_to_be_done)
        priority_keywords = self._extract_priority_keywords(persona, job_to_be_done)
        
        return PersonaAnalysis(
            persona=persona,
            job_to_be_done=job_to_be_done,
            expertise_areas=expertise_areas,
            key_interests=key_interests,
            priority_keywords=priority_keywords,
            analysis_context={
                "method": "basic_stub",
                "confidence": 0.5
            }
        )
    
    def _extract_expertise_areas(self, persona: str) -> List[str]:
        """Extract expertise areas from persona (stub implementation)."""
        # Simple keyword matching - will be enhanced with NLP
        expertise_keywords = {
            "researcher": ["research", "analysis", "methodology", "data"],
            "analyst": ["analysis", "trends", "metrics", "performance"],
            "student": ["learning", "concepts", "fundamentals", "exam"],
            "investment": ["financial", "revenue", "market", "growth"],
            "phd": ["advanced", "theoretical", "methodology", "literature"],
            "chemistry": ["chemical", "reactions", "compounds", "mechanisms"]
        }
        
        persona_lower = persona.lower()
        areas = []
        
        for key, keywords in expertise_keywords.items():
            if key in persona_lower:
                areas.extend(keywords)
        
        return areas[:5]  # Limit to top 5
    
    def _extract_key_interests(self, job_to_be_done: str) -> List[str]:
        """Extract key interests from job description (stub implementation)."""
        # Simple keyword extraction
        interest_keywords = [
            "methodology", "dataset", "benchmark", "performance",
            "revenue", "trend", "investment", "strategy",
            "concept", "mechanism", "kinetics", "reaction",
            "review", "analysis", "summary", "comparison"
        ]
        
        job_lower = job_to_be_done.lower()
        interests = [kw for kw in interest_keywords if kw in job_lower]
        
        return interests[:5]  # Limit to top 5
    
    def _extract_priority_keywords(self, persona: str, job_to_be_done: str) -> List[str]:
        """Extract priority keywords from both persona and job (stub implementation)."""
        combined_text = f"{persona} {job_to_be_done}".lower()
        
        # Simple word extraction (will be enhanced with TF-IDF, etc.)
        words = combined_text.split()
        
        # Filter out common words and get unique meaningful terms
        stop_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        priority_words = [word.strip(".,!?;:") for word in words 
                         if len(word) > 3 and word not in stop_words]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_words = []
        for word in priority_words:
            if word not in seen:
                seen.add(word)
                unique_words.append(word)
        
        return unique_words[:10]  # Top 10 priority keywords
    
    def _init_nltk(self):
        """Initialize NLTK data (download if needed)."""
        try:
            # Try to download required NLTK data silently
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                self.logger.info("Downloaded NLTK data")
            except Exception as e:
                self.logger.warning(f"Could not download NLTK data: {e}")
    
    def extract_priority_keywords_enhanced(self, persona: str, job_to_be_done: str) -> List[str]:
        """Enhanced keyword extraction using TF-IDF and NLP models."""
        try:
            combined_text = f"{persona} {job_to_be_done}"
            
            # Method 1: TF-IDF based extraction
            tfidf_keywords = self._extract_tfidf_keywords([combined_text])
            
            # Method 2: Use semantic similarity for domain-specific terms
            semantic_keywords = self._extract_semantic_keywords(persona, job_to_be_done)
            
            # Combine and deduplicate
            all_keywords = list(set(tfidf_keywords + semantic_keywords))
            
            return all_keywords[:10]
            
        except Exception as e:
            self.logger.error(f"Error in enhanced keyword extraction: {e}")
            # Fallback to basic method
            return self._extract_priority_keywords(persona, job_to_be_done)
    
    def _extract_tfidf_keywords(self, texts: List[str]) -> List[str]:
        """Extract keywords using TF-IDF."""
        try:
            # Add some domain-specific texts to improve TF-IDF
            expanded_texts = texts + [
                "research methodology analysis data science machine learning",
                "financial analysis investment revenue market trends performance",
                "academic literature review study examination concepts theory"
            ]
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(expanded_texts)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores for the original text (first in list)
            scores = tfidf_matrix[0].toarray()[0]
            
            # Get top keywords
            keyword_scores = [(feature_names[i], scores[i]) for i in range(len(scores))]
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [kw for kw, score in keyword_scores[:10] if score > 0]
            
        except Exception as e:
            self.logger.error(f"Error in TF-IDF extraction: {e}")
            return []
    
    def _extract_semantic_keywords(self, persona: str, job_to_be_done: str) -> List[str]:
        """Extract keywords using semantic similarity."""
        try:
            # Define domain-specific keyword pools
            domain_keywords = {
                'research': ['methodology', 'analysis', 'data', 'study', 'experiment', 'hypothesis'],
                'finance': ['revenue', 'investment', 'market', 'financial', 'profit', 'growth'],
                'academic': ['literature', 'review', 'theory', 'concept', 'examination', 'study'],
                'technology': ['machine learning', 'algorithm', 'neural network', 'data science'],
                'chemistry': ['reaction', 'compound', 'molecular', 'chemical', 'synthesis']
            }
            
            combined_text = f"{persona} {job_to_be_done}"
            relevant_keywords = []
            
            # Use semantic similarity to find relevant domain keywords
            for domain, keywords in domain_keywords.items():
                for keyword in keywords:
                    try:
                        similarity = self.model_manager.compute_similarity(combined_text, keyword)
                        if similarity > 0.3:  # Threshold for relevance
                            relevant_keywords.append(keyword)
                    except Exception as e:
                        # Fallback to simple matching if model fails
                        if keyword.lower() in combined_text.lower():
                            relevant_keywords.append(keyword)
            
            return relevant_keywords[:10]
            
        except Exception as e:
            self.logger.error(f"Error in semantic keyword extraction: {e}")
            return []
    
    def analyze_persona_enhanced(self, persona: str, job_to_be_done: str) -> PersonaAnalysis:
        """Enhanced persona analysis using NLP models."""
        self.logger.info("Running enhanced persona analysis...")
        
        try:
            # Enhanced keyword extraction
            priority_keywords = self.extract_priority_keywords_enhanced(persona, job_to_be_done)
            
            # Enhanced expertise area extraction
            expertise_areas = self._extract_expertise_areas_enhanced(persona)
            
            # Enhanced interest extraction
            key_interests = self._extract_key_interests_enhanced(job_to_be_done)
            
            return PersonaAnalysis(
                persona=persona,
                job_to_be_done=job_to_be_done,
                expertise_areas=expertise_areas,
                key_interests=key_interests,
                priority_keywords=priority_keywords,
                analysis_context={
                    "method": "enhanced_nlp",
                    "confidence": 0.8,
                    "model_used": True
                }
            )
            
        except Exception as e:
            self.logger.error(f"Enhanced analysis failed, falling back to basic: {e}")
            # Fallback to basic analysis
            return self.analyze_persona(persona, job_to_be_done)
    
    def _extract_expertise_areas_enhanced(self, persona: str) -> List[str]:
        """Enhanced expertise area extraction."""
        # Start with basic extraction
        basic_areas = self._extract_expertise_areas(persona)
        
        try:
            # Use semantic similarity to find related terms
            expertise_pool = [
                'research', 'analysis', 'methodology', 'data science', 'machine learning',
                'financial analysis', 'investment', 'market research', 'statistics',
                'academic research', 'literature review', 'theoretical analysis',
                'computational biology', 'bioinformatics', 'chemistry', 'biochemistry'
            ]
            
            enhanced_areas = basic_areas.copy()
            
            for term in expertise_pool:
                if term not in enhanced_areas:
                    similarity = self.model_manager.compute_similarity(persona, term)
                    if similarity > 0.4:  # Higher threshold for expertise
                        enhanced_areas.append(term)
            
            return enhanced_areas[:7]  # Slightly more than basic
            
        except Exception as e:
            self.logger.error(f"Error in enhanced expertise extraction: {e}")
            return basic_areas
    
    def _extract_key_interests_enhanced(self, job_to_be_done: str) -> List[str]:
        """Enhanced key interest extraction."""
        # Start with basic extraction
        basic_interests = self._extract_key_interests(job_to_be_done)
        
        try:
            # Use TF-IDF to find important terms
            tfidf_interests = self._extract_tfidf_keywords([job_to_be_done])
            
            # Combine and deduplicate
            all_interests = list(set(basic_interests + tfidf_interests))
            
            return all_interests[:7]
            
        except Exception as e:
            self.logger.error(f"Error in enhanced interest extraction: {e}")
            return basic_interests
