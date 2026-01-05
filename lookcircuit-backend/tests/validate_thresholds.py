"""
Standalone Validation for Style Analysis Thresholds
Tests accuracy without requiring MediaPipe face detection.
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import only the standalone detectors (not the full analyzer)
from ai.face_analysis.skin_tone import SkinToneDetector, FitzpatrickType, Undertone
from ai.face_analysis.face_shape import FaceShapeClassifier, FaceShape


ACCURACY_TARGET = 0.95  # 95% accuracy requirement


def create_synthetic_skin_image(l_value: float, undertone: str = "neutral") -> np.ndarray:
    """Create a synthetic skin-colored image for testing."""
    if undertone == "warm":
        a_value = 15
        b_value = 25
    elif undertone == "cool":
        a_value = 18
        b_value = 10
    else:
        a_value = 16
        b_value = 18
    
    lab_img = np.zeros((100, 100, 3), dtype=np.float32)
    lab_img[:, :, 0] = l_value * 255 / 100
    lab_img[:, :, 1] = a_value + 128
    lab_img[:, :, 2] = b_value + 128
    
    lab_img = lab_img.astype(np.uint8)
    bgr_img = cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)
    
    return bgr_img


def validate_skin_tone():
    """Validate skin tone classification thresholds."""
    print("\n" + "=" * 60)
    print("SKIN TONE THRESHOLD VALIDATION")
    print("=" * 60)
    
    detector = SkinToneDetector()
    
    # Test each Fitzpatrick type with L* values that should map correctly
    test_cases = [
        # L* value, expected Fitzpatrick, undertone for synthetic image
        (85, 1, "cool"),   # Type I - Very light (75-100)
        (70, 2, "warm"),   # Type II - Light (65-75)
        (60, 3, "neutral"), # Type III - Medium (55-65)
        (50, 4, "cool"),   # Type IV - Olive (45-55)
        (40, 5, "warm"),   # Type V - Brown (35-45)
        (28, 6, "neutral"), # Type VI - Dark (0-35)
    ]
    
    correct = 0
    total = len(test_cases)
    results = []
    
    for l_value, expected_fitz, undertone in test_cases:
        skin_region = create_synthetic_skin_image(l_value, undertone)
        result = detector.analyze([skin_region])
        
        if result:
            predicted_fitz = result.fitzpatrick_type.value
            is_correct = predicted_fitz == expected_fitz
            if is_correct:
                correct += 1
            
            status = "PASS" if is_correct else "FAIL"
            results.append({
                'l_value': l_value,
                'expected': expected_fitz,
                'predicted': predicted_fitz,
                'correct': is_correct
            })
            print(f"  [{status}] L*={l_value}: Expected Type {expected_fitz}, Got Type {predicted_fitz}")
        else:
            print(f"  [FAIL] L*={l_value}: Analysis failed")
    
    accuracy = correct / total if total > 0 else 0
    passed = accuracy >= ACCURACY_TARGET
    
    print(f"\n  Skin Tone Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"  Status: {'PASS' if passed else 'FAIL - NEEDS TUNING'}")
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'results': results,
        'passed': passed
    }


def validate_face_shape():
    """Validate face shape classification thresholds."""
    print("\n" + "=" * 60)
    print("FACE SHAPE THRESHOLD VALIDATION")
    print("=" * 60)
    
    classifier = FaceShapeClassifier()
    
    # Test cases: length_width_ratio, forehead_jaw_ratio, jawline_angle, expected_shape
    test_cases = [
        (1.2, 1.0, 140, "oval"),       # Balanced proportions
        (1.05, 0.98, 135, "round"),    # Short, equal width/length
        (1.4, 1.0, 140, "oblong"),     # Long face
        (1.15, 1.2, 145, "heart"),     # Wide forehead
        (1.1, 0.85, 140, "triangle"),  # Wide jaw
        (1.05, 1.0, 160, "square"),    # Angular jaw
        (1.2, 1.0, 140, "oval"),       # Default balanced
    ]
    
    correct = 0
    total = len(test_cases)
    results = []
    
    for lw, fj, ja, expected in test_cases:
        measurements = {
            'face_length': 200,
            'face_width': 200 / lw,
            'forehead_width': 100,
            'jaw_width': 100 / fj,
            'cheekbone_width': 95,
            'jawline_angle': ja,
            'length_width_ratio': lw,
            'forehead_jaw_ratio': fj
        }
        
        result = classifier.classify(measurements)
        predicted = result.shape.value
        is_correct = predicted == expected
        
        if is_correct:
            correct += 1
        
        status = "PASS" if is_correct else "FAIL"
        results.append({
            'lw': lw, 'fj': fj, 'ja': ja,
            'expected': expected, 'predicted': predicted,
            'correct': is_correct
        })
        print(f"  [{status}] LW={lw}, FJ={fj}, JA={ja}: Expected '{expected}', Got '{predicted}'")
    
    accuracy = correct / total if total > 0 else 0
    passed = accuracy >= ACCURACY_TARGET
    
    print(f"\n  Face Shape Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"  Status: {'PASS' if passed else 'FAIL - NEEDS TUNING'}")
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'results': results,
        'passed': passed
    }


def run_validation():
    """Run complete validation."""
    print("\n" + "=" * 60)
    print("LOOKCIRCUIT STYLE ANALYSIS VALIDATION")
    print("Target Accuracy: >=95%")
    print("=" * 60)
    
    skin_results = validate_skin_tone()
    shape_results = validate_face_shape()
    
    total_correct = skin_results['correct'] + shape_results['correct']
    total_tests = skin_results['total'] + shape_results['total']
    overall_accuracy = total_correct / total_tests if total_tests > 0 else 0
    
    all_passed = skin_results['passed'] and shape_results['passed']
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"  Skin Tone Accuracy:  {skin_results['accuracy']:.1%} {'[PASS]' if skin_results['passed'] else '[FAIL]'}")
    print(f"  Face Shape Accuracy: {shape_results['accuracy']:.1%} {'[PASS]' if shape_results['passed'] else '[FAIL]'}")
    print(f"  Overall Accuracy:    {overall_accuracy:.1%}")
    print(f"\n  OVERALL: {'PASSED' if all_passed else 'NEEDS THRESHOLD TUNING'}")
    print("=" * 60)
    
    return {
        'skin_tone': skin_results,
        'face_shape': shape_results,
        'overall_accuracy': overall_accuracy,
        'passed': all_passed
    }


if __name__ == "__main__":
    results = run_validation()
    
    if not results['passed']:
        print("\n>>> Accuracy below 95% - Proceeding to threshold tuning...")
        sys.exit(1)
    else:
        print("\n>>> All accuracy targets met!")
        sys.exit(0)
