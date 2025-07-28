"""
Document Processor Module
Handles PDF processing and text extraction.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
# import pdfplumber  # Temporarily disabled
from dataclasses import dataclass


@dataclass
class ProcessedDocument:
    """Data class for processed document information."""
    filename: str
    full_path: str
    text_content: str
    page_contents: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class DocumentProcessor:
    """
    Processes PDF documents and extracts text content.
    
    Handles:
    - PDF text extraction using multiple methods
    - Page-by-page processing
    - Metadata extraction
    - Error handling for corrupted PDFs
    """
    
    def __init__(self):
        """Initialize the document processor."""
        self.logger = logging.getLogger(__name__)
    
    def process_documents(self, document_paths: List[str]) -> List[ProcessedDocument]:
        """
        Process a list of PDF documents and extract text content.
        
        Args:
            document_paths: List of paths to PDF files
            
        Returns:
            List of ProcessedDocument objects containing extracted content
        """
        processed_docs = []
        
        for doc_path in document_paths:
            try:
                self.logger.info(f"Processing document: {doc_path}")
                processed_doc = self._process_single_document(doc_path)
                processed_docs.append(processed_doc)
                
            except Exception as e:
                self.logger.error(f"Error processing document {doc_path}: {str(e)}")
                # Continue processing other documents
                continue
        
        return processed_docs
    
    def _process_single_document(self, doc_path: str) -> ProcessedDocument:
        """
        Process a single PDF document.
        
        Args:
            doc_path: Path to the PDF file
            
        Returns:
            ProcessedDocument object
        """
        doc_path = Path(doc_path)
        
        # Use PyPDF2 for now (pdfplumber temporarily disabled)
        try:
            text_content, page_contents = self._extract_with_pypdf2(doc_path)
        except Exception as e:
            self.logger.error(f"PDF extraction failed for {doc_path}: {str(e)}")
            raise
        
        # Extract metadata
        metadata = self._extract_metadata(doc_path)
        
        return ProcessedDocument(
            filename=doc_path.name,
            full_path=str(doc_path.absolute()),
            text_content=text_content,
            page_contents=page_contents,
            metadata=metadata
        )
    
    def _extract_with_pdfplumber(self, doc_path: Path) -> tuple[str, List[Dict[str, Any]]]:
        """Extract text using pdfplumber."""
        full_text = ""
        page_contents = []
        
        with pdfplumber.open(doc_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text() or ""
                    full_text += page_text + "\n\n"
                    
                    page_contents.append({
                        "page_number": page_num,
                        "text": page_text,
                        "char_count": len(page_text),
                        "extraction_method": "pdfplumber"
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Error extracting page {page_num}: {str(e)}")
                    continue
        
        return full_text.strip(), page_contents
    
    def _extract_with_pypdf2(self, doc_path: Path) -> tuple[str, List[Dict[str, Any]]]:
        """Extract text using PyPDF2 as fallback."""
        full_text = ""
        page_contents = []
        
        with open(doc_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text() or ""
                    full_text += page_text + "\n\n"
                    
                    page_contents.append({
                        "page_number": page_num,
                        "text": page_text,
                        "char_count": len(page_text),
                        "extraction_method": "PyPDF2"
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Error extracting page {page_num}: {str(e)}")
                    continue
        
        return full_text.strip(), page_contents
    
    def _extract_metadata(self, doc_path: Path) -> Dict[str, Any]:
        """Extract document metadata."""
        metadata = {
            "file_size": doc_path.stat().st_size,
            "file_name": doc_path.name,
            "file_extension": doc_path.suffix
        }
        
        try:
            with open(doc_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata.update({
                    "page_count": len(pdf_reader.pages),
                    "pdf_metadata": pdf_reader.metadata or {}
                })
        except Exception as e:
            self.logger.warning(f"Could not extract PDF metadata: {str(e)}")
        
        return metadata
