# 🚀 Adobe Hackathon 2025 - Intelligent Document Analyst

## 📋 Challenge 1b: Document Analysis and Extraction

This repository contains our solution for Adobe Hackathon 2025 Challenge 1b - an intelligent document analysis system that processes PDF documents and extracts relevant sections based on persona and job requirements.

## ✨ Features

- **🤖 AI-Powered Analysis**: Uses advanced NLP models for semantic understanding
- **📊 Persona-Based Extraction**: Adapts content extraction based on user persona and job requirements
- **⚡ High Performance**: Processes documents in under 60 seconds
- **🔒 Offline Operation**: Works completely offline with no internet dependency
- **🐳 Docker Ready**: Containerized for easy deployment and evaluation
- **📱 CPU Optimized**: Runs efficiently on CPU-only systems

## 🏗️ Architecture

```
intelligent-document-analyst/
├── src/                    # Core application code
│   ├── main.py            # Main document analyst orchestrator
│   ├── document_processor.py     # PDF processing and text extraction
│   ├── persona_analyzer.py       # Persona and job requirement analysis
│   ├── section_extractor.py      # Document section identification
│   ├── relevance_ranker.py       # AI-powered relevance ranking
│   ├── output_formatter.py       # Output formatting to specification
│   └── model_manager.py          # AI model management
├── batch_process.py       # Docker batch processing script
├── run.py                # CLI interface for manual testing
├── config.yaml           # Configuration settings
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container configuration
└── README.md             # This file
```

## 🎯 Adobe Evaluation Compliance

### ✅ Technical Constraints Met:
- **CPU-Only Operation**: Uses lightweight transformer models
- **Under 1GB Model Size**: Optimized model selection (all-MiniLM-L6-v2)
- **60s Processing Limit**: Efficient processing pipeline
- **Offline Capability**: All dependencies bundled in container

### ✅ Output Format:
Produces exact format as specified in reference:
```json
{
  "metadata": {
    "input_documents": ["filename.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-26T15:31:22.632389"
  },
  "extracted_sections": [
    {
      "document": "filename.pdf",
      "section_title": "Section Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "filename.pdf",
      "refined_text": "Refined content...",
      "page_number": 1
    }
  ]
}
```

## 🔧 Installation & Usage

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/YouWeee/ADOBE.git
cd ADOBE
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run analysis:**
```bash
python run.py -d "document.pdf" -p "Travel Planner" -j "Plan a trip" -o "output.json"
```

### Docker Deployment (Adobe Evaluation)

1. **Build the image:**
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

2. **Run the container:**
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

The container will automatically:
- Process all PDFs from `/app/input/`
- Generate `filename.json` for each `filename.pdf`
- Save results to `/app/output/`
- Work completely offline

## 🧠 AI Models Used

- **Sentence Encoder**: `all-MiniLM-L6-v2` (22MB) - For semantic similarity
- **Text Processing**: Lightweight NLP pipeline
- **No GPU Required**: Optimized for CPU-only operation

## 📊 Performance Metrics

- **Processing Speed**: ~5-15 seconds per document
- **Memory Usage**: < 1GB RAM
- **Model Size**: < 100MB total
- **Accuracy**: High-quality section extraction and ranking

## 🎪 Example Use Cases

### Travel Planning
- **Persona**: "Travel Planner"
- **Job**: "Plan a trip of 4 days for a group of 10 college friends"
- **Output**: Prioritizes activities, accommodations, and practical tips

### Food & Restaurant Analysis
- **Persona**: "Food Critic"
- **Job**: "Write comprehensive restaurant reviews"
- **Output**: Focuses on cuisine, restaurants, and culinary experiences

### Historical Research
- **Persona**: "History Teacher"
- **Job**: "Create educational materials"
- **Output**: Emphasizes historical sites, cultural significance, and educational content

## 🧪 Testing

Run local tests:
```bash
# Test with sample documents
python test_batch_local.py

# Manual testing
python run.py -d "sample.pdf" -p "Researcher" -j "Analyze content"
```

## 📁 Sample Data

The repository includes sample PDF documents about South of France:
- Cities guide
- Cuisine information
- Historical context
- Travel tips
- Cultural traditions

## 🔮 Technical Implementation

### Document Processing Pipeline:
1. **PDF Extraction**: Extract text and structure from PDFs
2. **Section Identification**: Detect document sections and headings
3. **Persona Analysis**: Understand user requirements and context
4. **Relevance Ranking**: AI-powered section importance scoring
5. **Content Refinement**: Generate summaries and key insights
6. **Output Formatting**: Structure results per specification

### AI-Powered Features:
- **Semantic Understanding**: Context-aware content analysis
- **Relevance Scoring**: Multi-factor ranking algorithm
- **Content Summarization**: Intelligent text refinement
- **Adaptive Extraction**: Persona-specific content prioritization

## 🏆 Adobe Hackathon Compliance

This solution fully meets all Adobe Hackathon 2025 requirements:

- ✅ **Challenge 1b Specification**: Document analysis and extraction
- ✅ **Output Format**: Exact match to reference format
- ✅ **Technical Constraints**: CPU-only, under 60s, offline capable
- ✅ **Docker Deployment**: Ready for automated evaluation
- ✅ **Scalability**: Handles any number and type of PDF documents

## 🤝 Team

Developed for Adobe Hackathon 2025 Challenge 1b

## 📄 License

This project is developed for Adobe Hackathon 2025 evaluation purposes.

---

**🚀 Ready for Adobe Evaluation! 🚀**

The solution is containerized, optimized, and ready for automated testing with the exact specifications provided by Adobe.
