#!/usr/bin/env python3
"""
Combined Batch Processing Script for Docker Deployment
Processes all PDFs from /app/input together and generates a single combined JSON output.
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


def load_json_config() -> Dict[str, Any]:
    """
    Load configuration from JSON file if present.
    Looks for config.json in /app/input directory.
    """
    config_path = Path("/app/input/config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Loaded configuration from {config_path}")
            return config
        except Exception as e:
            print(f"⚠️  Failed to load config.json: {e}")
            return None
    return None


def get_persona_and_job_from_config(config: Dict[str, Any], pdf_files: List[Path]) -> tuple[str, str, List[str]]:
    """
    Extract persona, job, and document list from JSON configuration.
    Returns (persona, job, document_paths) or falls back to other methods.
    """
    if not config:
        return None, None, None
    
    try:
        persona = config.get('persona', '').strip()
        job = config.get('job_to_be_done', '').strip()
        
        # Get document list from config if available
        documents_config = config.get('documents', [])
        if documents_config:
            # Map document names from config to actual file paths
            input_dir = Path("/app/input")
            document_paths = []
            
            for doc_config in documents_config:
                # Handle different formats of document specification
                if isinstance(doc_config, dict):
                    filename = doc_config.get('filename', doc_config.get('name', ''))
                elif isinstance(doc_config, str):
                    filename = doc_config
                else:
                    continue
                
                if filename:
                    # Look for the file in input directory
                    file_path = input_dir / filename
                    if file_path.exists():
                        document_paths.append(str(file_path))
                    else:
                        print(f"⚠️  Document specified in config not found: {filename}")
            
            if document_paths:
                print(f"📄 Using {len(document_paths)} documents from config:")
                for doc_path in document_paths:
                    print(f"  - {Path(doc_path).name}")
                return persona, job, document_paths
        
        # If no valid documents in config, return persona/job only
        if persona and job:
            print(f"📋 Using persona and job from config, but processing all PDF files found")
            return persona, job, None
            
    except Exception as e:
        print(f"⚠️  Error parsing configuration: {e}")
    
    return None, None, None


def get_persona_and_job_interactive(pdf_files: List[Path]) -> tuple[str, str]:
    """
    Get persona and job either from environment variables or interactive prompts.
    Falls back to auto-detection based on document types if no input provided.
    """
    # First, try to get from environment variables
    persona = os.environ.get('PERSONA')
    job = os.environ.get('JOB_TO_BE_DONE')
    
    # If environment variables not set, try interactive prompts
    if not persona or not job:
        try:
            print("\n" + "="*60)
            print("INTERACTIVE DOCUMENT ANALYSIS SETUP")
            print("="*60)
            print(f"Found {len(pdf_files)} PDF files to process:")
            for pdf_file in pdf_files:
                print(f"  - {pdf_file.name}")
            print()
            
            if not persona:
                print("Please specify the persona (role) for analysis:")
                print("Examples: 'Travel Planner', 'Food Contractor', 'Business Analyst', 'Research Assistant'")
                persona = input("Enter persona: ").strip()
                
            if not job:
                print("\nPlease specify the job to be done:")
                print("Examples: 'Plan a 4-day trip for 10 college friends', 'Prepare a vegetarian dinner menu'")
                job = input("Enter job to be done: ").strip()
                
            print("\n" + "="*60)
            
        except (EOFError, KeyboardInterrupt):
            print("\nInteractive input interrupted. Falling back to auto-detection...")
            persona = None
            job = None
    
    # If still no persona/job, fall back to auto-detection
    if not persona or not job:
        persona, job = detect_persona_and_job_from_context(pdf_files)
        print(f"Auto-detected persona: {persona}")
        print(f"Auto-detected job: {job}")
    
    return persona, job


def detect_persona_and_job_from_context(pdf_files: List[Path]) -> tuple[str, str]:
    """
    Detect appropriate persona and job based on the types of documents present.
    This function analyzes the filenames to determine the most appropriate context.
    """
    filenames = [f.name.lower() for f in pdf_files]
    
    # Check for food/menu related documents
    food_keywords = ['menu', 'recipe', 'food', 'dinner', 'lunch', 'breakfast', 'cuisine', 'restaurant']
    if any(keyword in filename for filename in filenames for keyword in food_keywords):
        return "Food Contractor", "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
    
    # Check for travel related documents
    travel_keywords = ['travel', 'trip', 'city', 'cities', 'hotel', 'restaurant', 'guide', 'france']
    if any(keyword in filename for filename in filenames for keyword in travel_keywords):
        return "Travel Planner", "Plan a trip of 4 days for a group of 10 college friends."
    
    # Default fallback
    return "Document Analyst", "Analyze and extract key information from the provided documents."





def setup_logging():
    """Setup logging for batch processing."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - BATCH - %(levelname)s - %(message)s'
    )


def batch_process_pdfs_combined():
    """
    Main combined batch processing function.
    Processes all PDFs from /app/input together and generates a single JSON file in /app/output.
    Can read configuration from config.json file for persona, job, and document list.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Define paths
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # First, try to load JSON configuration
    config = load_json_config()
    
    # Get persona, job, and document list from config if available
    persona = None
    job = None
    document_paths = None
    
    if config:
        persona, job, document_paths = get_persona_and_job_from_config(config, [])
    
    # If no specific document list from config, find all PDF files
    if not document_paths:
        pdf_files = list(input_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning("No PDF files found in /app/input directory")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to process together")
        document_paths = [str(pdf_file) for pdf_file in pdf_files]
    else:
        pdf_files = [Path(doc_path) for doc_path in document_paths]
        logger.info(f"Using {len(document_paths)} documents from configuration")
    
    # Initialize document analyst
    try:
        analyst = DocumentAnalyst()
        logger.info("Document Analyst initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Document Analyst: {e}")
        return
    
    try:
        # If no persona/job from config, get them interactively or auto-detect
        if not persona or not job:
            persona, job = get_persona_and_job_interactive(pdf_files)
        
        logger.info(f"Using persona: {persona}")
        logger.info(f"Using job: {job}")
        
        logger.info(f"Processing {len(document_paths)} documents together...")
        
        # Run combined analysis on all documents
        result = analyst.analyze(
            documents=document_paths,
            persona=persona,
            job_to_be_done=job
        )
        
        # Generate output filename - use a descriptive name
        if len(pdf_files) == 1:
            output_filename = pdf_files[0].stem + ".json"
        else:
            output_filename = "combined_analysis.json"
        
        output_path = output_dir / output_filename
        
        # Save results
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Successfully processed {len(pdf_files)} documents -> {output_filename}")
        
    except Exception as e:
        logger.error(f"❌ Failed to process documents: {e}")
        
        # Create error output file
        error_output = {
            "error": str(e),
            "documents": [f.name for f in pdf_files],
            "status": "failed"
        }
        
        output_path = output_dir / "error_output.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(error_output, f, indent=2, ensure_ascii=False)
    
    logger.info("Combined batch processing completed")


if __name__ == "__main__":
    batch_process_pdfs_combined()
