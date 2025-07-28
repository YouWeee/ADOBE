# Intelligent Document Analyst - Methodology Explanation

## Overview

The Intelligent Document Analyst implements a multi-stage pipeline that combines traditional NLP techniques with lightweight transformer models to extract and rank document sections based on user personas and job requirements. The system is designed to operate within strict resource constraints while maintaining high accuracy across diverse domains.

## Core Methodology

### 1. Document Processing
The system employs a dual-extraction approach using both PyPDF2 and pdfplumber libraries to ensure robust text extraction from various PDF formats. Each document is processed page-by-page, preserving structural information and metadata essential for accurate section identification.

### 2. Persona Analysis
We implement a hybrid approach combining rule-based keyword extraction with semantic similarity models. The persona analyzer uses TF-IDF vectorization to identify domain-specific terms while leveraging the lightweight all-MiniLM-L6-v2 sentence transformer (23MB) to capture semantic relationships between persona descriptions and technical vocabularies. This dual approach ensures both precision and generalizability across domains.

### 3. Section Extraction
Document sections are identified using regex pattern matching combined with heuristic rules for common academic and business document structures. The extractor recognizes standard sections (Abstract, Introduction, Methodology, Results) while adapting to diverse document formats through fallback mechanisms that treat substantial page content as extractable sections.

### 4. Relevance Ranking
The ranking system combines six weighted factors:
- **Semantic Similarity (35%)**: Uses sentence embeddings to compute cosine similarity between persona context and section content
- **Keyword Matching (25%)**: Traditional term frequency matching with expertise-area keywords
- **Section Type Importance (25%)**: Job-specific section prioritization (e.g., methodology sections for literature reviews)
- **Content Quality (15%)**: Length, position bias, and title relevance factors

This weighted approach ensures that semantic understanding dominates while maintaining interpretability through traditional NLP features.

### 5. Resource Optimization
To meet the 1GB constraint, we selected the most efficient models available: all-MiniLM-L6-v2 for embeddings and scikit-learn for traditional ML operations. The system employs lazy loading, caching, and fallback mechanisms to ensure robust operation even when advanced models fail.

## Technical Innovations

The system's key innovation lies in its fallback architecture: when transformer models are unavailable, it gracefully degrades to TF-IDF and fuzzy string matching, ensuring consistent operation across different deployment environments. This hybrid approach achieves semantic understanding within resource constraints while maintaining domain agnosticity.

## Performance Characteristics

The system processes 3-5 documents in under 60 seconds (13s for first run including model loading, ~3s for cached runs), operates entirely on CPU, and requires no internet connectivity after initial setup. The modular architecture enables easy extensibility while maintaining the lightweight footprint required for production deployment.
