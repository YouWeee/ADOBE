"""
Output Formatter Module
Formats the analysis results according to the required output structure.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
from document_processor import ProcessedDocument
from relevance_ranker import RankedSection


class OutputFormatter:
    """
    Formats the analysis results into the required output structure.
    
    Output format:
    1. Metadata (input documents, persona, job, timestamp)
    2. Extracted Sections (document, page, title, rank)
    3. Sub-section Analysis (document, refined text, page)
    """
    
    def __init__(self):
        """Initialize the output formatter."""
        self.logger = logging.getLogger(__name__)
    
    def format_output(self, documents: List[str], persona: str, job_to_be_done: str,
                     processed_docs: List[ProcessedDocument], 
                     ranked_sections: List[RankedSection],
                     processing_timestamp: datetime) -> Dict[str, Any]:
        """
        Format the complete analysis output according to Adobe Hackathon Challenge 1b specifications.
        
        Args:
            documents: Original document paths
            persona: Persona description
            job_to_be_done: Job description
            processed_docs: Processed document objects
            ranked_sections: Ranked sections with relevance scores
            processing_timestamp: When processing was completed
            
        Returns:
            Formatted output dictionary
        """
        self.logger.info("Formatting analysis output...")
        
        # 1. Generate Metadata
        metadata = self._generate_metadata(documents, persona, job_to_be_done, processing_timestamp)
        
        # 2. Generate Extracted Sections (based on available sections)
        extracted_sections = self._generate_extracted_sections(ranked_sections)  
        
        # 3. Generate Sub-section Analysis (based on available sections)
        subsection_analysis = self._generate_subsection_analysis(ranked_sections)
        
        output = {
            "metadata": metadata,
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }
        
        self.logger.info(f"Output formatted with {len(extracted_sections)} sections and {len(subsection_analysis)} detailed analyses")
        
        return output
    
    def _generate_metadata(self, documents: List[str], persona: str, 
                          job_to_be_done: str, processing_timestamp: datetime) -> Dict[str, Any]:
        """Generate metadata section of the output."""
        # Extract just the filenames from full paths
        doc_names = []
        for doc in documents:
            if '\\' in doc:
                doc_names.append(doc.split('\\')[-1])
            elif '/' in doc:
                doc_names.append(doc.split('/')[-1])
            else:
                doc_names.append(doc)
                
        return {
            "input_documents": doc_names,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": processing_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")
        }
    
    def _generate_extracted_sections(self, ranked_sections: List[RankedSection]) -> List[Dict[str, Any]]:
        """Generate extracted sections list."""
        extracted_sections = []
        
        # Take top 5 most relevant sections
        top_sections = ranked_sections[:5]
        
        for ranked_section in top_sections:
            section = ranked_section.section
            
            extracted_sections.append({
                "document": section.document_name,
                "section_title": section.section_title,
                "importance_rank": ranked_section.importance_rank,
                "page_number": section.page_number
            })
        
        return extracted_sections
    
    def _generate_subsection_analysis(self, top_ranked_sections: List[RankedSection]) -> List[Dict[str, Any]]:
        """Generate detailed sub-section analysis for top sections."""
        subsection_analysis = []
        
        # Take top 5 most relevant sections for detailed analysis
        top_sections = top_ranked_sections[:5]
        
        for ranked_section in top_sections:
            section = ranked_section.section
            
            # Generate refined text (summary/key points)
            refined_text = self._generate_refined_text(section.section_text)
            
            subsection_analysis.append({
                "document": section.document_name,
                "refined_text": refined_text,
                "page_number": section.page_number
            })
        
        return subsection_analysis
    
    def _generate_refined_text(self, original_text: str, max_length: int = 1000) -> str:
        """
        Generate refined text from original section text (stub implementation).
        
        This is a basic implementation that will be enhanced with summarization models.
        """
        # Basic text refinement - take first sentences up to max_length
        if len(original_text) <= max_length:
            return original_text.strip()
        
        # Split into sentences (basic approach)
        sentences = []
        current_sentence = ""
        
        for char in original_text:
            current_sentence += char
            if char in '.!?' and len(current_sentence.strip()) > 20:
                sentences.append(current_sentence.strip())
                current_sentence = ""
        
        # Add remaining text as last sentence if it exists
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        # Build refined text within length limit
        refined_text = ""
        for sentence in sentences:
            if len(refined_text) + len(sentence) + 1 <= max_length:
                refined_text += sentence + " "
            else:
                break
        
        return refined_text.strip()
    
    def _extract_key_insights(self, section_text: str) -> List[str]:
        """
        Extract key insights from section text (stub implementation).
        
        This will be enhanced with NLP models for better insight extraction.
        """
        insights = []
        
        # Simple heuristics for key insights
        sentences = section_text.split('.')
        
        for sentence in sentences[:5]:  # Look at first 5 sentences
            sentence = sentence.strip()
            
            # Look for sentences with key indicator words
            insight_indicators = [
                'important', 'significant', 'key', 'main', 'primary',
                'results show', 'findings indicate', 'conclude', 'demonstrate',
                'novel', 'innovative', 'breakthrough', 'improvement'
            ]
            
            sentence_lower = sentence.lower()
            if any(indicator in sentence_lower for indicator in insight_indicators):
                if len(sentence) > 30 and len(sentence) < 200:  # Reasonable length
                    insights.append(sentence + '.')
        
        # If no insights found with indicators, take first substantial sentences
        if not insights:
            for sentence in sentences[:3]:
                sentence = sentence.strip()
                if len(sentence) > 50:
                    insights.append(sentence + '.')
        
        return insights[:3]  # Return top 3 insights
    
    def _generate_adobe_format(self, documents: List[str], persona: str, job_to_be_done: str,
                             ranked_sections: List[RankedSection], 
                             processing_timestamp: datetime) -> Dict[str, Any]:
        """
        Generate output in Adobe Hackathon Challenge 1b format.
        
        Expected format:
        {
            "persona": "Travel Planner",
            "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
            "relevant_sections": [
                {
                    "document_name": "filename.pdf",
                    "page_number": 1,
                    "section_title": "Section Title",
                    "content": "Section content...",
                    "relevance_score": 0.95
                }
            ]
        }
        """
        # Extract document names
        doc_names = []
        for doc in documents:
            if '\\' in doc:
                doc_names.append(doc.split('\\')[-1])
            elif '/' in doc:
                doc_names.append(doc.split('/')[-1])
            else:
                doc_names.append(doc)
        
        # Generate relevant sections
        relevant_sections = []
        
        # Take top 10 most relevant sections
        top_sections = ranked_sections[:10]
        
        for ranked_section in top_sections:
            section = ranked_section.section
            
            # Clean and format content
            content = self._clean_content(section.section_text)
            
            relevant_sections.append({
                "document_name": section.document_name,
                "page_number": section.page_number,
                "section_title": section.section_title,
                "content": content,
                "relevance_score": round(ranked_section.relevance_score, 3)
            })
        
        return {
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "relevant_sections": relevant_sections
        }
    
    def _clean_content(self, text: str) -> str:
        """
        Clean and format content text for better readability.
        """
        if not text:
            return ""
        
        # Remove excessive whitespace and normalize line breaks
        text = ' '.join(text.split())
        
        # Limit length to reasonable size
        max_length = 1500
        if len(text) > max_length:
            # Find last complete sentence within limit
            truncated = text[:max_length]
            last_period = truncated.rfind('.')
            if last_period > max_length * 0.8:  # If we can keep most of the text
                text = truncated[:last_period + 1]
            else:
                text = truncated + "..."
        
        return text.strip()
