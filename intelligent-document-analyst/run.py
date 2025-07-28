#!/usr/bin/env python3
"""
Intelligent Document Analyst - Main Entry Point
Run the document analysis pipeline with specified parameters.
"""

import click
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

from main import DocumentAnalyst


@click.command()
@click.option('--documents', '-d', multiple=True, required=True,
              help='PDF documents to analyze (can specify multiple)')
@click.option('--persona', '-p', required=True,
              help='Persona description (e.g., "PhD Researcher in Computational Biology")')
@click.option('--job', '-j', required=True,
              help='Job to be done (e.g., "Prepare comprehensive literature review")')
@click.option('--output', '-o', default='output.json',
              help='Output file path (default: output.json)')
@click.option('--config', '-c', default=None,
              help='Configuration file path (optional)')
def main(documents, persona, job, output, config):
    """
    Intelligent Document Analyst - Extract relevant sections from documents
    based on persona and job requirements.
    
    Example usage:
    python run.py -d doc1.pdf -d doc2.pdf -p "Investment Analyst" -j "Analyze revenue trends"
    """
    
    # Convert documents tuple to list
    document_list = list(documents)
    
    # Validate input files exist
    for doc_path in document_list:
        if not Path(doc_path).exists():
            click.echo(f"Error: Document '{doc_path}' not found.", err=True)
            sys.exit(1)
    
    # Initialize the document analyst
    try:
        analyst = DocumentAnalyst(config_path=config)
        
        # Display processing information
        click.echo(f"🔍 Processing {len(document_list)} documents...")
        click.echo(f"👤 Persona: {persona}")
        click.echo(f"🎯 Job: {job}")
        click.echo(f"📄 Output: {output}")
        click.echo("-" * 50)
        
        # Run the analysis
        result = analyst.analyze(
            documents=document_list,
            persona=persona,
            job_to_be_done=job
        )
        
        # Save results
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        click.echo(f"✅ Analysis complete! Results saved to: {output}")
        
        # Display summary
        if 'extracted_sections' in result:
            sections_count = len(result['extracted_sections'])
            click.echo(f"📊 Extracted {sections_count} relevant sections")
        
    except Exception as e:
        click.echo(f"❌ Error during analysis: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
