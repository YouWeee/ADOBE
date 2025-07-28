# Use Python 3.9 slim image for smaller size and better compatibility
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download required NLTK data
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Models will be downloaded at runtime to avoid compatibility issues

# Copy configuration and source code
COPY config.yaml .
COPY approach_explanation.md .
COPY sample_test_cases.md .
COPY src/ ./src/
COPY run.py .

# Create necessary directories
RUN mkdir -p data/sample_documents data/sample_outputs models

# Set environment variables for optimization
ENV PYTHONPATH=/app/src
ENV TORCH_NUM_THREADS=1
ENV TOKENIZERS_PARALLELISM=false
ENV TRANSFORMERS_CACHE=/app/models
ENV SENTENCE_TRANSFORMERS_HOME=/app/models

# Create non-root user for security
RUN useradd -m -u 1000 analyst && chown -R analyst:analyst /app
USER analyst

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.append('/app/src'); from model_manager import ModelManager; print('OK')"

# Copy batch processing scripts
COPY batch_process.py .
COPY batch_process_combined.py .

# Default command - combined batch process all PDFs in /app/input
CMD ["python", "batch_process_combined.py"]

# Competition Usage (Exact format they expect):
# 
# Build:
# docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
# 
# Run:
# docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
#
# This will:
# - Process all PDFs from /app/input automatically
# - Generate filename.json for each filename.pdf
# - Save results to /app/output
# - Work offline (--network none)
