# Intelligent Document Analyst System
**Theme**: "Connect What Matters — For the User Who Matters"

## Project Overview

Build a system that acts as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done.

## Core Requirements

### Input Specification
1. **Document Collection**: 3-10 related PDFs
2. **Persona Definition**: Role description with specific expertise and focus areas
3. **Job-to-be-Done**: Concrete task the persona needs to accomplish

### System Characteristics
- **Domain Agnostic**: Handle documents from any field (research papers, financial reports, news articles, school/college books, etc.)
- **Persona Flexibility**: Work with diverse roles (Researcher, Student, Salesperson, Journalist, Entrepreneur, etc.)
- **Task Variety**: Support different job-to-be-done scenarios (literature reviews, study planning, financial analysis, etc.)

## Sample Test Cases

### Test Case 1: Academic Research
- **Documents**: 4 research papers on "Graph Neural Networks for Drug Discovery"    
- **Persona**: PhD Researcher in Computational Biology
- **Job**: "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

### Test Case 2: Business Analysis
- **Documents**: 3 annual reports from competing tech companies (2022-2024)
- **Persona**: Investment Analyst
- **Job**: "Analyze revenue trends, R&D investments, and market positioning strategies"

### Test Case 3: Educational Content
- **Documents**: 5 chapters from organic chemistry textbooks
- **Persona**: Undergraduate Chemistry Student
- **Job**: "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

## Output Structure

### 1. Metadata
- a. Input documents
- b. Persona
- c. Job to be done
- d. Processing timestamp

### 2. Extracted Section
- a. Document
- b. Page number
- c. Section title
- d. Importance rank

### 3. Sub-section Analysis
- a. Document
- b. Refined Text
- c. Page Number

## Technical Constraints

- **Must run on CPU only** (no GPU dependency)
- **Model size ≤ 1GB**
- **Processing time ≤ 60 seconds** for document collection (3-5 documents)
- **No internet access** allowed during execution (fully offline operation)

## Deliverables

1. **approach_explanation.md** (300-500 words explaining methodology)
2. **Dockerfile and execution instructions**
3. **Sample input/output for testing**

## Technical Considerations

The system must be:
- **Lightweight**: Efficient models within 1GB constraint
- **Fast**: Optimized for sub-60-second processing
- **Offline**: All models and dependencies bundled
- **Accurate**: Meaningful analysis despite size constraints
- **Generic**: Adaptable to diverse domains and personas

## Key Challenges

1. **Context Understanding**: Interpreting persona expertise and job requirements
2. **Relevance Ranking**: Prioritizing document sections based on persona needs
3. **Cross-Domain Generalization**: Working across academic, business, and educational contexts
4. **Resource Optimization**: Balancing accuracy with speed and size constraints
5. **Section Extraction**: Intelligently identifying and extracting relevant document portions

## Success Criteria

The system should demonstrate:
- Accurate identification of persona-relevant content
- Proper ranking of section importance
- Fast processing within time constraints
- Consistent performance across different domains
- Clear, structured output format
