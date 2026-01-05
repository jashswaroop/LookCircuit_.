"""
Test script for Face Analysis module.
Run this to verify the AI pipeline works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.face_analysis import FaceAnalyzer
import cv2
import numpy as np


def test_with_sample_image():
    """Test face analysis with a sample image."""
    print("=" * 60)
    print("LookCircuit Face Analysis Test")
    print("=" * 60)
    
    # Initialize analyzer
    print("\n1. Initializing Face Analyzer...")
    analyzer = FaceAnalyzer()
    print("   ✓ Analyzer initialized")
    
    # Create a simple test image (or use a real one if available)
    print("\n2. Testing with sample...")
    
    # Check if a test image exists
    test_paths = [
        "test_face.jpg",
        "sample.jpg",
        "../test_face.jpg"
    ]
    
    test_image = None
    for path in test_paths:
        if os.path.exists(path):
            test_image = cv2.imread(path)
            print(f"   Found test image: {path}")
            break
    
    if test_image is None:
        print("   No test image found. Creating synthetic test...")
        # Create a blank image for basic structure test
        test_image = np.zeros((480, 480, 3), dtype=np.uint8)
        test_image[:] = (200, 180, 160)  # Skin-like color
        print("   Note: Use a real face image for accurate testing")
    
    # Run analysis
    print("\n3. Running analysis...")
    result = analyzer.analyze(test_image)
    
    print(f"\n4. Results:")
    print(f"   Face Detected: {result.detected}")
    
    if result.detected:
        print(f"   Overall Confidence: {result.overall_confidence:.2%}")
        
        if result.skin_tone:
            print(f"\n   Skin Tone Analysis:")
            print(f"     - Fitzpatrick Type: {result.skin_tone.fitzpatrick_type.name}")
            print(f"     - Undertone: {result.skin_tone.undertone.value}")
            print(f"     - Color: {result.skin_tone.hex_color}")
            print(f"     - Confidence: {result.skin_tone.confidence:.2%}")
        
        if result.face_shape:
            print(f"\n   Face Shape Analysis:")
            print(f"     - Shape: {result.face_shape.shape.value}")
            print(f"     - Confidence: {result.face_shape.confidence:.2%}")
            print(f"     - Reasoning: {result.face_shape.reasoning}")
        
        if result.hair_coverage:
            print(f"\n   Hair Coverage Analysis:")
            print(f"     - Level: {result.hair_coverage.coverage_level.value}")
            print(f"     - Coverage: {result.hair_coverage.coverage_percentage:.1f}%")
            print(f"     - Alt Styling Needed: {result.hair_coverage.requires_alternative_styling}")
        
        if result.color_season:
            print(f"\n   Color Season: {result.color_season.upper()}")
        
        # Export as dict (for API)
        print("\n5. API Response Format:")
        api_response = result.to_dict()
        print(f"   {api_response}")
    else:
        print("   No face detected in image. Try with a clear face photo.")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_with_sample_image()
