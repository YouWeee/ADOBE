"""
Relevance Ranker Module
Ranks document sections by relevance to persona and job requirements.
"""

import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from section_extractor import ExtractedSection
from persona_analyzer import PersonaAnalysis
from model_manager import ModelManager


@dataclass
class RankedSection:
    """Data class for ranked sections with relevance scores."""
    section: ExtractedSection
    relevance_score: float
    ranking_factors: Dict[str, float]
    importance_rank: int


class RelevanceRanker:
    """
    Ranks document sections based on their relevance to the persona and job requirements.
    
    This is a basic stub implementation for testing.
    Will be enhanced with semantic similarity models in Step 2.
    """
    
    def __init__(self, model_manager: ModelManager = None):
        """Initialize the relevance ranker."""
        self.logger = logging.getLogger(__name__)
        self.model_manager = model_manager or ModelManager()
        
        # Weights for different ranking factors (configurable)
        self.ranking_weights = {
            'keyword_match': 0.25,
            'semantic_similarity': 0.35,  # New: semantic relevance
            'section_type_importance': 0.25,
            'content_length': 0.05,
            'position_bias': 0.05,
            'title_relevance': 0.05
        }
    
    def rank_sections(self, sections: List[ExtractedSection], 
                     persona_analysis: PersonaAnalysis) -> List[RankedSection]:
        """
        Rank sections by relevance to persona and job requirements (stub implementation).
        
        Args:
            sections: List of extracted sections
            persona_analysis: Analysis of persona and job requirements
            
        Returns:
            List of RankedSection objects sorted by relevance
        """
        self.logger.info(f"Ranking {len(sections)} sections for relevance...")
        
        ranked_sections = []
        
        for section in sections:
            try:
                # Calculate relevance score
                relevance_score, factors = self._calculate_relevance_score(section, persona_analysis)
                
                ranked_sections.append(RankedSection(
                    section=section,
                    relevance_score=relevance_score,
                    ranking_factors=factors,
                    importance_rank=0  # Will be set after sorting
                ))
                
            except Exception as e:
                self.logger.error(f"Error ranking section '{section.section_title}': {str(e)}")
                continue
        
        # Sort by relevance score (highest first)
        ranked_sections.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Assign importance ranks
        for i, ranked_section in enumerate(ranked_sections, 1):
            ranked_section.importance_rank = i
        
        self.logger.info(f"Completed ranking with top score: {ranked_sections[0].relevance_score:.3f}")
        
        return ranked_sections
    
    def _calculate_relevance_score(self, section: ExtractedSection, 
                                 persona_analysis: PersonaAnalysis) -> tuple[float, Dict[str, float]]:
        """Calculate relevance score for a section (stub implementation)."""
        
        factors = {}
        
        # Factor 1: Keyword matching
        factors['keyword_match'] = self._calculate_keyword_match_score(section, persona_analysis)
        
        # Factor 2: NEW - Semantic similarity
        factors['semantic_similarity'] = self._calculate_semantic_similarity_score(section, persona_analysis)
        
        # Factor 3: Section type importance
        factors['section_type_importance'] = self._calculate_section_type_score(section, persona_analysis)
        
        # Factor 4: Content length factor
        factors['content_length'] = self._calculate_content_length_score(section)
        
        # Factor 5: Position bias (earlier sections might be more important)
        factors['position_bias'] = self._calculate_position_bias_score(section)
        
        # Factor 6: Title relevance
        factors['title_relevance'] = self._calculate_title_relevance_score(section, persona_analysis)
        
        # Calculate weighted total score
        total_score = sum(factors[factor] * self.ranking_weights[factor] 
                         for factor in factors.keys())
        
        return total_score, factors
    
    def _calculate_keyword_match_score(self, section: ExtractedSection, 
                                     persona_analysis: PersonaAnalysis) -> float:
        """Calculate keyword matching score (stub implementation)."""
        section_text_lower = section.section_text.lower()
        section_title_lower = section.section_title.lower()
        
        # Combine all relevant keywords from persona analysis
        all_keywords = (persona_analysis.expertise_areas + 
                       persona_analysis.key_interests + 
                       persona_analysis.priority_keywords)
        
        if not all_keywords:
            return 0.0
        
        matches = 0
        total_keywords = len(all_keywords)
        
        for keyword in all_keywords:
            keyword_lower = keyword.lower()
            # Check both title and content
            if keyword_lower in section_title_lower:
                matches += 2  # Title matches are more important
            elif keyword_lower in section_text_lower:
                matches += 1
        
        # Normalize to 0-1 scale
        return min(matches / (total_keywords * 1.5), 1.0)
    
    def _calculate_section_type_score(self, section: ExtractedSection, 
                                    persona_analysis: PersonaAnalysis) -> float:
        """Calculate section type importance score (stub implementation)."""
        
        # Different personas value different section types
        job_lower = persona_analysis.job_to_be_done.lower()
        section_type = section.section_type
        
        # Basic heuristics for section importance based on job type
        if 'literature review' in job_lower or 'review' in job_lower:
            type_scores = {
                'abstract': 0.9,
                'introduction': 0.8,
                'methods': 0.7,
                'results': 0.6,
                'discussion': 0.8,
                'conclusion': 0.7,
                'references': 0.5
            }
        elif 'analysis' in job_lower or 'analyze' in job_lower:
            type_scores = {
                'abstract': 0.7,
                'introduction': 0.6,
                'methods': 0.9,
                'results': 0.9,
                'discussion': 0.8,
                'conclusion': 0.7,
                'references': 0.3
            }
        elif 'exam' in job_lower or 'study' in job_lower:
            type_scores = {
                'abstract': 0.6,
                'introduction': 0.8,
                'methods': 0.7,
                'results': 0.5,
                'discussion': 0.6,
                'conclusion': 0.8,
                'references': 0.2
            }
        else:
            # Default scoring
            type_scores = {
                'abstract': 0.7,
                'introduction': 0.7,
                'methods': 0.6,
                'results': 0.6,
                'discussion': 0.6,
                'conclusion': 0.6,
                'references': 0.3
            }
        
        return type_scores.get(section_type, 0.5)  # Default for unknown types
    
    def _calculate_content_length_score(self, section: ExtractedSection) -> float:
        """Calculate content length score (prefer substantial content)."""
        text_length = len(section.section_text)
        
        # Optimal length range: 500-3000 characters
        if text_length < 100:
            return 0.1  # Too short
        elif text_length < 500:
            return 0.6  # Short but acceptable
        elif text_length <= 3000:
            return 1.0  # Ideal length
        elif text_length <= 5000:
            return 0.8  # Long but manageable
        else:
            return 0.6  # Very long, might be less focused
    
    def _calculate_position_bias_score(self, section: ExtractedSection) -> float:
        """Calculate position bias score (earlier sections often more important)."""
        page_num = section.page_number
        
        # Simple linear decrease in importance by page
        if page_num <= 2:
            return 1.0
        elif page_num <= 5:
            return 0.8
        elif page_num <= 10:
            return 0.6
        else:
            return 0.4
    
    def _calculate_title_relevance_score(self, section: ExtractedSection, 
                                       persona_analysis: PersonaAnalysis) -> float:
        """Calculate title relevance score (stub implementation)."""
        title_lower = section.section_title.lower()
        
        # Check if title contains job-related keywords
        job_keywords = persona_analysis.job_to_be_done.lower().split()
        
        # Filter out common words
        meaningful_keywords = [word for word in job_keywords 
                              if len(word) > 3 and word not in {'that', 'with', 'from', 'this'}]
        
        if not meaningful_keywords:
            return 0.5  # Default score
        
        matches = sum(1 for keyword in meaningful_keywords if keyword in title_lower)
        return min(matches / len(meaningful_keywords), 1.0)
    
    def _calculate_semantic_similarity_score(self, section: ExtractedSection, 
                                           persona_analysis: PersonaAnalysis) -> float:
        """Calculate semantic similarity score using NLP models."""
        try:
            # Create context from persona and job
            context = f"{persona_analysis.persona} {persona_analysis.job_to_be_done}"
            
            # Get section content (title + beginning of text for efficiency)
            section_content = section.section_title
            if len(section.section_text) > 0:
                # Add first 500 characters of content
                section_content += " " + section.section_text[:500]
            
            # Compute semantic similarity
            similarity = self.model_manager.compute_similarity(context, section_content)
            
            # Apply boosting for highly relevant sections
            if similarity > 0.7:
                similarity = min(similarity * 1.2, 1.0)  # Boost high-similarity sections
            
            return similarity
            
        except Exception as e:
            self.logger.error(f"Error computing semantic similarity: {e}")
            # Fallback to keyword-based similarity
            return self._fallback_semantic_score(section, persona_analysis)
    
    def _fallback_semantic_score(self, section: ExtractedSection, 
                                persona_analysis: PersonaAnalysis) -> float:
        """Fallback semantic scoring when models are unavailable."""
        try:
            # Use fuzzy string matching as fallback 
            from fuzzywuzzy import fuzz
            
            context = f"{persona_analysis.persona} {persona_analysis.job_to_be_done}"
            section_content = f"{section.section_title} {section.section_text[:300]}"
            
            # Compute fuzzy similarity
            ratio = fuzz.partial_ratio(context.lower(), section_content.lower())
            return ratio / 100.0  # Normalize to 0-1
            
        except ImportError:
            # If fuzzywuzzy not available, use simple overlap
            return self._simple_overlap_score(section, persona_analysis)
        except Exception as e:
            self.logger.error(f"Error in fallback semantic scoring: {e}")
            return 0.3  # Default moderate score
    
    def _simple_overlap_score(self, section: ExtractedSection, 
                            persona_analysis: PersonaAnalysis) -> float:
        """Simple word overlap scoring as last resort."""
        context_words = set((persona_analysis.persona + " " + persona_analysis.job_to_be_done).lower().split())
        section_words = set((section.section_title + " " + section.section_text[:300]).lower().split())
        
        if not context_words or not section_words:
            return 0.0
        
        overlap = len(context_words.intersection(section_words))
        union = len(context_words.union(section_words))
        
        return overlap / union if union > 0 else 0.0
    
    def rank_sections_enhanced(self, sections: List[ExtractedSection], 
                             persona_analysis: PersonaAnalysis) -> List[RankedSection]:
        """Enhanced ranking with semantic similarity (public method)."""
        self.logger.info(f"Enhanced ranking of {len(sections)} sections...")
        
        # Use the standard ranking which now includes semantic similarity
        return self.rank_sections(sections, persona_analysis)
