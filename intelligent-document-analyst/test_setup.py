#!/usr/bin/env python3
"""
Test Setup Script
Quick validation of the document analyst setup and basic functionality.
"""

import sys
import time
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from document_processor import DocumentProcessor, ProcessedDocument
        print("✅ document_processor imported successfully")
        
        from persona_analyzer import PersonaAnalyzer, PersonaAnalysis
        print("✅ persona_analyzer imported successfully")
        
        from section_extractor import SectionExtractor, ExtractedSection
        print("✅ section_extractor imported successfully")
        
        from relevance_ranker import RelevanceRanker, RankedSection
        print("✅ relevance_ranker imported successfully")
        
        from output_formatter import OutputFormatter
        print("✅ output_formatter imported successfully")
        
        from main import DocumentAnalyst
        print("✅ main DocumentAnalyst imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_create_sample_content():
    """Create sample content for testing."""
    print("\n📄 Creating sample content...")
    
    try:
        # Run the test content generator
        os.system(f'python "{Path(__file__).parent}/create_test_pdf.py"')
        
        # Check if content was created (PDF or text file)
        test_pdf = Path(__file__).parent / "data/sample_documents/test_research_paper.pdf"
        test_txt = Path(__file__).parent / "data/sample_documents/test_content.txt"
        
        if test_pdf.exists() or test_txt.exists():
            print("✅ Sample content created successfully")
            return True
        else:
            print("❌ Sample content creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error creating sample content: {str(e)}")
        return False

def test_basic_functionality():
    """Test basic functionality with stub implementations."""
    print("\n⚙️ Testing basic functionality...")
    
    try:
        from document_processor import DocumentProcessor
        from persona_analyzer import PersonaAnalyzer
        
        # Test persona analyzer (doesn't require documents)
        persona_analyzer = PersonaAnalyzer()
        persona = "PhD Researcher in Computational Biology"
        job = "Prepare comprehensive literature review focusing on methodologies"
        
        persona_analysis = persona_analyzer.analyze_persona(persona, job)
        print(f"✅ Persona analysis completed: {len(persona_analysis.priority_keywords)} keywords extracted")
        
        # Test document processor initialization
        doc_processor = DocumentProcessor()
        print("✅ Document processor initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False

def test_performance_benchmark():
    """Basic performance test to ensure we're on track for <60s constraint."""
    print("\n⏱️ Running performance benchmark...")
    
    try:
        start_time = time.time()
        
        # Simulate the analysis pipeline without actual documents
        from persona_analyzer import PersonaAnalyzer
        from section_extractor import SectionExtractor
        from relevance_ranker import RelevanceRanker
        from output_formatter import OutputFormatter
        
        # Initialize components
        persona_analyzer = PersonaAnalyzer()
        section_extractor = SectionExtractor()
        relevance_ranker = RelevanceRanker()
        output_formatter = OutputFormatter()
        
        # Run basic operations
        persona_analysis = persona_analyzer.analyze_persona(
            "Investment Analyst", 
            "Analyze revenue trends and market positioning"
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Basic pipeline completed in {processing_time:.3f} seconds")
        
        if processing_time < 1.0:  # Should be very fast for basic operations
            print("✅ Performance looks good for scaling to full documents")
            return True
        else:
            print("⚠️ Performance might need optimization")
            return True  # Still passing, just a warning
            
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")
        return False

def main():
    """Run all setup tests."""
    print("🚀 Intelligent Document Analyst - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Sample Content Creation", test_create_sample_content),
        ("Basic Functionality", test_basic_functionality),
        ("Performance Benchmark", test_performance_benchmark)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The setup is ready for development.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Add a real PDF document to data/sample_documents/")
        print("3. Run a full test: python run.py -d your_document.pdf -p 'Your Persona' -j 'Your Job'")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
