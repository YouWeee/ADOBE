"""
Create a simple test PDF for testing the document analyst.
This script creates a basic PDF with sample academic content.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_test_pdf():
    """Create a simple test PDF with academic content."""
    
    filename = "data/sample_documents/test_research_paper.pdf"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Page 1
    y_position = height - 50
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_position, "Graph Neural Networks for Drug Discovery")
    y_position -= 30
    
    # Authors
    c.setFont("Helvetica", 12)
    c.drawString(50, y_position, "Authors: Dr. Jane Smith, Prof. John Doe")
    y_position -= 50
    
    # Abstract
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "Abstract")
    y_position -= 20
    
    c.setFont("Helvetica", 11)
    abstract_text = """
    This paper presents a comprehensive methodology for applying graph neural networks
    to drug discovery processes. Our approach demonstrates significant improvements in
    predicting molecular properties and identifying potential drug candidates. The
    proposed methodology achieves 92% accuracy on benchmark datasets, outperforming
    traditional machine learning approaches by 15%. Key contributions include novel
    graph convolution techniques and enhanced feature extraction methods.
    """
    
    lines = abstract_text.strip().split('\n')
    for line in lines:
        c.drawString(50, y_position, line.strip())
        y_position -= 15
    
    y_position -= 30
    
    # Introduction
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "1. Introduction")
    y_position -= 20
    
    c.setFont("Helvetica", 11)
    intro_text = """
    Drug discovery is a complex and expensive process that typically takes 10-15 years
    and costs billions of dollars. Recent advances in machine learning, particularly
    graph neural networks (GNNs), offer promising solutions for accelerating this
    process. This research focuses on developing novel methodologies for molecular
    property prediction using advanced graph-based approaches.
    """
    
    lines = intro_text.strip().split('\n')
    for line in lines:
        if y_position < 100:  # Start new page if running out of space
            c.showPage()
            y_position = height - 50
        c.drawString(50, y_position, line.strip())
        y_position -= 15
    
    # Page 2
    c.showPage()
    y_position = height - 50
    
    # Methodology
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "2. Methodology")
    y_position -= 20
    
    c.setFont("Helvetica", 11)
    method_text = """
    Our methodology consists of three main components:
    
    2.1 Graph Construction: Molecular structures are represented as graphs where
    atoms are nodes and bonds are edges. Each node contains chemical properties
    such as atomic number, valence, and hybridization state.
    
    2.2 Graph Neural Network Architecture: We employ a multi-layer GNN with
    attention mechanisms to capture both local and global molecular features.
    The network uses graph convolution operations to propagate information
    across the molecular structure.
    
    2.3 Property Prediction: The final layer maps graph representations to
    target properties such as solubility, toxicity, and bioactivity scores.
    """
    
    lines = method_text.strip().split('\n')
    for line in lines:
        if y_position < 100:
            break
        c.drawString(50, y_position, line.strip())
        y_position -= 15
    
    y_position -= 30
    
    # Results
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "3. Results")
    y_position -= 20
    
    c.setFont("Helvetica", 11)
    results_text = """
    Our experiments demonstrate significant performance improvements:
    - Accuracy: 92.3% on molecular property prediction
    - Precision: 89.7% for drug-target interaction prediction  
    - Recall: 94.1% for active compound identification
    - Processing time: 50% faster than baseline methods
    """
    
    lines = results_text.strip().split('\n')
    for line in lines:
        if y_position < 100:
            break
        c.drawString(50, y_position, line.strip())
        y_position -= 15
    
    c.save()
    print(f"Test PDF created: {filename}")

if __name__ == "__main__":
    # Try to create PDF, but don't fail if reportlab isn't installed
    try:
        create_test_pdf()
    except ImportError:
        print("reportlab not installed. Creating a text file instead for testing.")
        
        # Create a simple text file that we can manually convert to PDF
        filename = "data/sample_documents/test_content.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            f.write("""Graph Neural Networks for Drug Discovery

Abstract
This paper presents a comprehensive methodology for applying graph neural networks to drug discovery processes. Our approach demonstrates significant improvements in predicting molecular properties and identifying potential drug candidates. The proposed methodology achieves 92% accuracy on benchmark datasets, outperforming traditional machine learning approaches by 15%.

1. Introduction
Drug discovery is a complex and expensive process that typically takes 10-15 years and costs billions of dollars. Recent advances in machine learning, particularly graph neural networks (GNNs), offer promising solutions for accelerating this process.

2. Methodology
Our methodology consists of three main components: graph construction, neural network architecture, and property prediction. The approach uses novel graph convolution techniques and enhanced feature extraction methods.

3. Results
Our experiments demonstrate significant performance improvements with 92.3% accuracy on molecular property prediction and 50% faster processing time than baseline methods.
""")
        
        print(f"Test content created: {filename}")
        print("Please manually convert this to PDF or install reportlab: pip install reportlab")
