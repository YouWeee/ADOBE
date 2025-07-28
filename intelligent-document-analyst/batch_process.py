#!/usr/bin/env python3
"""
Batch Processing Script for Docker Deployment
Automatically processes all PDFs from /app/input and generates corresponding JSON outputs.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from main import DocumentAnalyst


def detect_persona_and_job(pdf_filename: str, all_filenames: List[str] = None) -> tuple[str, str]:
    """
    Detect appropriate persona and job based on the filename and context.
    This function analyzes the filename to determine the most appropriate context.
    """
    filename_lower = pdf_filename.lower()
    
    # If we have context of all filenames, use that for better detection
    if all_filenames:
        all_names = ' '.join(all_filenames).lower()
        
        # Check for food/menu related documents
        food_keywords = ['menu', 'recipe', 'food', 'dinner', 'lunch', 'breakfast', 'cuisine', 'restaurant']
        if any(keyword in all_names for keyword in food_keywords):
            return "Food Contractor", "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
        
        # Check for travel related documents
        travel_keywords = ['travel', 'trip', 'city', 'cities', 'hotel', 'restaurant', 'guide', 'france']
        if any(keyword in all_names for keyword in travel_keywords):
            return "Travel Planner", "Plan a trip of 4 days for a group of 10 college friends."
    
    # Individual file analysis
    if any(word in filename_lower for word in ['menu', 'recipe', 'food', 'cuisine', 'restaurant']):
        return "Food Contractor", "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
    elif any(word in filename_lower for word in ['travel', 'trip', 'city', 'cities', 'hotel', 'guide', 'france']):
        return "Travel Planner", "Plan a trip of 4 days for a group of 10 college friends."
    
    # Default fallback
    return "Document Analyst", "Analyze and extract key information from the provided documents."


def setup_logging():
    """Setup logging for batch processing."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - BATCH - %(levelname)s - %(message)s'
    )


def batch_process_pdfs():
    """
    Main batch processing function.
    Processes all PDFs from /app/input and generates corresponding JSON files in /app/output.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Define paths
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all PDF files in input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning("No PDF files found in /app/input directory")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Initialize document analyst
    try:
        analyst = DocumentAnalyst()
        logger.info("Document Analyst initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Document Analyst: {e}")
        return
    
    # Get all filenames for context-aware persona detection
    all_filenames = [pdf_file.name for pdf_file in pdf_files]
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing: {pdf_file.name}")
            
            # Detect appropriate persona and job using context
            persona, job = detect_persona_and_job(pdf_file.name, all_filenames)
            logger.info(f"Detected persona: {persona}")
            logger.info(f"Detected job: {job}")
            
            # Run analysis
            result = analyst.analyze(
                documents=[str(pdf_file)],
                persona=persona,
                job_to_be_done=job
            )
            
            # Generate output filename (replace .pdf with .json)
            output_filename = pdf_file.stem + ".json"
            output_path = output_dir / output_filename
            
            # Save results
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Successfully processed {pdf_file.name} -> {output_filename}")
            
        except Exception as e:
            logger.error(f"❌ Failed to process {pdf_file.name}: {e}")
            
            # Create error output file
            error_output = {
                "error": str(e),
                "filename": pdf_file.name,
                "status": "failed"
            }
            
            output_filename = pdf_file.stem + ".json"
            output_path = output_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(error_output, f, indent=2, ensure_ascii=False)
    
    logger.info("Batch processing completed")


if __name__ == "__main__":
    batch_process_pdfs()
