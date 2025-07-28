# Sample Test Cases

This document provides sample inputs and expected outputs for the three main test scenarios.

## Test Case 1: Academic Research

### Input:
```bash
python run.py \
    -d "research_paper1.pdf" -d "research_paper2.pdf" -d "research_paper3.pdf" -d "research_paper4.pdf" \
    -p "PhD Researcher in Computational Biology" \
    -j "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

### Expected Output Structure:
```json
{
  "metadata": {
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
    "total_documents_processed": 4
  },
  "extracted_sections": [
    {
      "document": "research_paper1.pdf",
      "section_title": "Methodology",
      "importance_rank": 1,
      "relevance_score": 0.85,
      "section_type": "methods"
    }
  ],
  "subsection_analysis": [
    {
      "document": "research_paper1.pdf",
      "refined_text": "Our methodology consists of...",
      "key_insights": ["Novel graph convolution approach", "92% accuracy achieved"]
    }
  ]
}
```

## Test Case 2: Business Analysis

### Input:
```bash
python run.py \
    -d "company_a_2024.pdf" -d "company_b_2024.pdf" -d "company_c_2024.pdf" \
    -p "Investment Analyst" \
    -j "Analyze revenue trends, R&D investments, and market positioning strategies"
```

### Expected Output Focus:
- High relevance for financial sections
- Revenue and R&D data extraction
- Market analysis prioritization

## Test Case 3: Educational Content

### Input:
```bash
python run.py \
    -d "chem_chapter1.pdf" -d "chem_chapter2.pdf" -d "chem_chapter3.pdf" -d "chem_chapter4.pdf" -d "chem_chapter5.pdf" \
    -p "Undergraduate Chemistry Student" \
    -j "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
```

### Expected Output Focus:
- Concept definitions prioritized
- Example problems highlighted
- Kinetics mechanisms extracted

## Performance Benchmarks

### Expected Processing Times:
- **First run**: 10-15 seconds (including model loading)
- **Subsequent runs**: 2-5 seconds (cached models)
- **Multiple documents (5 PDFs)**: Under 30 seconds

### Expected Accuracy Metrics:
- **Relevant section identification**: >80% precision
- **Section ranking**: Top 3 sections should contain target content
- **Cross-domain consistency**: Similar performance across academic/business/educational content

## Validation Criteria

For each test case, verify:
1. ✅ All input documents processed successfully
2. ✅ Sections ranked by relevance to persona and job
3. ✅ Output follows exact required structure
4. ✅ Processing completes within time constraints
5. ✅ Key insights extracted appropriately for domain
