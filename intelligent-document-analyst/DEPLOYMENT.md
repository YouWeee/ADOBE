# Deployment and Execution Instructions

## Quick Start

### Option 1: Direct Python Execution

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run analysis
python run.py \
    -d "document1.pdf" -d "document2.pdf" \
    -p "Your Persona" \
    -j "Your job to be done" \
    -o "results.json"
```

### Option 2: Docker Deployment (Recommended)

```bash
# 1. Build container
docker build -t intelligent-document-analyst .

# 2. Run with volume mount
docker run -v /path/to/documents:/app/input \
           -v /path/to/output:/app/output \
           intelligent-document-analyst \
    -d input/doc1.pdf -d input/doc2.pdf \
    -p "PhD Researcher in Computational Biology" \
    -j "Prepare comprehensive literature review" \
    -o output/results.json
```

## Detailed Setup Instructions

### Prerequisites
- Python 3.9+ (for direct execution)
- Docker (for containerized deployment)
- PDF documents to analyze

### Environment Setup

#### Local Python Environment:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_setup.py
```

#### Docker Environment:
```bash
# Build optimized container
docker build -t intelligent-document-analyst .

# Test container
docker run intelligent-document-analyst --help
```

## Usage Examples

### Academic Research Analysis
```bash
python run.py \
    -d "paper1.pdf" -d "paper2.pdf" -d "paper3.pdf" -d "paper4.pdf" \
    -p "PhD Researcher in Computational Biology" \
    -j "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks" \
    -o "academic_analysis.json"
```

### Business Intelligence Analysis
```bash
python run.py \
    -d "annual_report_2022.pdf" -d "annual_report_2023.pdf" -d "annual_report_2024.pdf" \
    -p "Investment Analyst" \
    -j "Analyze revenue trends, R&D investments, and market positioning strategies" \
    -o "business_analysis.json"
```

### Educational Content Analysis
```bash
python run.py \
    -d "chapter1.pdf" -d "chapter2.pdf" -d "chapter3.pdf" -d "chapter4.pdf" -d "chapter5.pdf" \
    -p "Undergraduate Chemistry Student" \
    -j "Identify key concepts and mechanisms for exam preparation on reaction kinetics" \
    -o "study_guide.json"
```

## Configuration Options

### Command Line Parameters:
- `-d, --documents`: PDF files to analyze (required, multiple allowed)
- `-p, --persona`: Persona description (required)
- `-j, --job`: Job to be done (required)
- `-o, --output`: Output file path (default: output.json)
- `-c, --config`: Configuration file path (optional)

### Configuration File (config.yaml):
```yaml
models:
  sentence_encoder: "all-MiniLM-L6-v2"
  text_classifier: "distilbert-base-uncased"

processing:
  max_processing_time: 60
  chunk_size: 1000
  max_sections_per_doc: 10

ranking:
  weights:
    semantic_similarity: 0.35
    keyword_match: 0.25
    section_type_importance: 0.25
    content_length: 0.05
    position_bias: 0.05
    title_relevance: 0.05
```

## Performance Optimization

### For First-Time Setup:
- Models download automatically on first run (~91MB)
- Initial processing: 10-15 seconds
- Subsequent runs: 2-5 seconds (cached models)

### For Production Deployment:
- Use Docker for consistent environment
- Mount document directories as volumes
- Pre-download models in container build

### Resource Requirements:
- **RAM**: 2-4GB recommended
- **Storage**: 500MB for models + document space
- **CPU**: Any modern CPU (no GPU required)

## Troubleshooting

### Common Issues:

#### "No module named" errors:
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

#### Model download failures:
```bash
# Check internet connection for first run
# Models cached locally after download
```

#### PDF processing errors:
```bash
# Ensure PDFs are not corrupted or password-protected
# Check file paths are correct
```

#### Performance issues:
```bash
# Reduce number of documents per batch
# Use faster storage (SSD recommended)
# Increase available RAM
```

## Output Validation

Verify output contains required structure:
- ✅ `metadata` with persona, job, timestamp
- ✅ `extracted_sections` with ranked results  
- ✅ `subsection_analysis` with refined text

## Production Deployment

### Docker Compose (Recommended):
```yaml
version: '3.8'
services:
  document-analyst:
    build: .
    volumes:
      - ./documents:/app/input
      - ./results:/app/output
    environment:
      - TORCH_NUM_THREADS=1
```

### Kubernetes Deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: document-analyst
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: analyst
        image: intelligent-document-analyst:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

## Support

For issues or questions:
1. Check this deployment guide
2. Review sample_test_cases.md for examples
3. Run `python test_setup.py` to validate installation
