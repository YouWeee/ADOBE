"""
Section Extractor Module
Identifies and extracts sections from processed documents.
"""

import logging
import re
from typing import List, Dict, Any
from dataclasses import dataclass
from document_processor import ProcessedDocument


@dataclass
class ExtractedSection:
    """Data class for extracted document sections."""
    document_name: str
    page_number: int
    section_title: str
    section_text: str
    section_type: str
    confidence_score: float
    start_position: int
    end_position: int


class SectionExtractor:
    """
    Extracts meaningful sections from processed documents.
    
    This is a basic stub implementation for testing.
    Will be enhanced with better section detection in Step 2.
    """
    
    def __init__(self):
        """Initialize the section extractor."""
        self.logger = logging.getLogger(__name__)
        
        # Basic section header patterns (stub - will be enhanced)
        self.header_patterns = [
            r"^\d+\.\s+([A-Z][^.]*)",           # "1. Introduction"
            r"^([A-Z][A-Z\s]+)$",              # "METHODOLOGY"
            r"^(Abstract)\s*$",                 # "Abstract"
            r"^(Introduction)\s*$",             # "Introduction"
            r"^(Methodology)\s*$",              # "Methodology"
            r"^(Results)\s*$",                  # "Results"
            r"^(Discussion)\s*$",               # "Discussion"
            r"^(Conclusion)\s*$",               # "Conclusion"
            r"^(References)\s*$",               # "References"
            r"^(Background)\s*$",               # "Background"
            r"^(Methods)\s*$",                  # "Methods"
        ]
    
    def extract_sections(self, processed_docs: List[ProcessedDocument]) -> List[ExtractedSection]:
        """
        Extract sections from all processed documents (stub implementation).
        
        Args:
            processed_docs: List of ProcessedDocument objects
            
        Returns:
            List of ExtractedSection objects
        """
        self.logger.info(f"Extracting sections from {len(processed_docs)} documents...")
        
        all_sections = []
        
        for doc in processed_docs:
            try:
                doc_sections = self._extract_sections_from_document(doc)
                all_sections.extend(doc_sections)
                self.logger.info(f"Extracted {len(doc_sections)} sections from {doc.filename}")
                
            except Exception as e:
                self.logger.error(f"Error extracting sections from {doc.filename}: {str(e)}")
                continue
        
        return all_sections
    
    def _extract_sections_from_document(self, doc: ProcessedDocument) -> List[ExtractedSection]:
        """Extract sections from a single document."""
        sections = []
        
        # Method 1: Try to extract from full text
        full_text_sections = self._extract_from_full_text(doc)
        sections.extend(full_text_sections)
        
        # Method 2: Extract from individual pages if full text extraction didn't work well
        if len(full_text_sections) < 2:  # If we didn't find many sections
            page_sections = self._extract_from_pages(doc)
            sections.extend(page_sections)
        
        # Remove duplicates and sort by position
        unique_sections = self._remove_duplicate_sections(sections)
        return sorted(unique_sections, key=lambda x: x.start_position)
    
    def _extract_from_full_text(self, doc: ProcessedDocument) -> List[ExtractedSection]:
        """Extract sections from full document text."""
        sections = []
        text = doc.text_content
        
        # Find all potential section headers
        for pattern in self.header_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            
            for match in matches:
                section_title = match.group(1) if match.groups() else match.group(0).strip()
                start_pos = match.start()
                
                # Find the end of this section (next header or end of document)
                end_pos = self._find_section_end(text, start_pos)
                section_text = text[start_pos:end_pos].strip()
                
                # Skip very short sections
                if len(section_text) < 50:
                    continue
                
                # Determine page number (approximate)
                page_num = self._estimate_page_number(doc, start_pos)
                
                sections.append(ExtractedSection(
                    document_name=doc.filename,
                    page_number=page_num,
                    section_title=section_title,
                    section_text=section_text,
                    section_type=self._classify_section_type(section_title),
                    confidence_score=0.7,  # Basic confidence
                    start_position=start_pos,
                    end_position=end_pos
                ))
        
        return sections
    
    def _extract_from_pages(self, doc: ProcessedDocument) -> List[ExtractedSection]:
        """Extract sections from individual pages."""
        sections = []
        
        for page_info in doc.page_contents:
            page_text = page_info.get('text', '')
            page_num = page_info.get('page_number', 1)
            
            # Simple heuristic: if page has substantial content, treat as a section
            if len(page_text.strip()) > 200:
                # Try to find a title in the first few lines
                lines = page_text.split('\n')[:5]
                potential_title = None
                
                for line in lines:
                    line = line.strip()
                    if len(line) > 0 and len(line) < 100:  # Reasonable title length
                        potential_title = line
                        break
                
                title = potential_title if potential_title else f"Page {page_num} Content"
                
                sections.append(ExtractedSection(
                    document_name=doc.filename,
                    page_number=page_num,
                    section_title=title,
                    section_text=page_text,
                    section_type="content",
                    confidence_score=0.5,  # Lower confidence for page-based extraction
                    start_position=0,  # Relative to page
                    end_position=len(page_text)
                ))
        
        return sections
    
    def _find_section_end(self, text: str, start_pos: int) -> int:
        """Find the end position of a section."""
        # Look for the next section header
        remaining_text = text[start_pos + 1:]
        
        for pattern in self.header_patterns:
            match = re.search(pattern, remaining_text, re.MULTILINE | re.IGNORECASE)
            if match:
                return start_pos + 1 + match.start()
        
        # If no next header found, go to end of text (but limit to reasonable size)
        max_section_length = 5000  # characters
        return min(start_pos + max_section_length, len(text))
    
    def _estimate_page_number(self, doc: ProcessedDocument, position: int) -> int:
        """Estimate page number based on character position."""
        if not doc.page_contents:
            return 1
        
        current_pos = 0
        for page_info in doc.page_contents:
            page_text = page_info.get('text', '')
            if current_pos + len(page_text) > position:
                return page_info.get('page_number', 1)
            current_pos += len(page_text) + 2  # +2 for added newlines
        
        return len(doc.page_contents)  # Last page
    
    def _classify_section_type(self, title: str) -> str:
        """Classify section type based on title."""
        title_lower = title.lower()
        
        type_mapping = {
            'abstract': 'abstract',
            'introduction': 'introduction', 
            'methodology': 'methods',
            'method': 'methods',
            'results': 'results',
            'discussion': 'discussion',
            'conclusion': 'conclusion',
            'references': 'references',
            'background': 'background'
        }
        
        for key, section_type in type_mapping.items():
            if key in title_lower:
                return section_type
        
        return 'content'  # Default type
    
    def _remove_duplicate_sections(self, sections: List[ExtractedSection]) -> List[ExtractedSection]:
        """Remove duplicate sections based on content similarity."""
        unique_sections = []
        seen_titles = set()
        
        for section in sections:
            # Simple deduplication based on title
            title_key = section.section_title.lower().strip()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_sections.append(section)
        
        return unique_sections
