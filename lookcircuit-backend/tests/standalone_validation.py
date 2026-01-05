"""
Self-Contained Validation Script for LookCircuit Style Analysis
Tests threshold accuracy without any external module dependencies.
"""

import cv2
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Dict, List, Optional


# ============================================================================
# INLINE DEFINITIONS (copied from modules to avoid import issues)
# ============================================================================

class FitzpatrickType(Enum):
    TYPE_I = 1
    TYPE_II = 2
    TYPE_III = 3
    TYPE_IV = 4
    TYPE_V = 5
    TYPE_VI = 6


class Undertone(Enum):
    COOL = "cool"
    WARM = "warm"
    NEUTRAL = "neutral"


class FaceShape(Enum):
    OVAL = "oval"
    ROUND = "round"
    SQUARE = "square"
    HEART = "heart"
    OBLONG = "oblong"
    DIAMOND = "diamond"
    TRIANGLE = "triangle"


# Fitzpatrick thresholds (L* values in LAB)
FITZPATRICK_L_THRESHOLDS = {
    FitzpatrickType.TYPE_I: (75, 100),
    FitzpatrickType.TYPE_II: (65, 75),
    FitzpatrickType.TYPE_III: (55, 65),
    FitzpatrickType.TYPE_IV: (45, 55),
    FitzpatrickType.TYPE_V: (35, 45),
    FitzpatrickType.TYPE_VI: (0, 35),
}

ACCURACY_TARGET = 0.95


# ============================================================================
# SKIN TONE CLASSIFICATION LOGIC
# ============================================================================

def classify_fitzpatrick(l_value: float) -> Tuple[FitzpatrickType, float]:
    """Classify Fitzpatrick type from L* value."""
    for fitz_type, (low, high) in FITZPATRICK_L_THRESHOLDS.items():
        if low <= l_value < high:
            range_size = high - low
            center = (low + high) / 2
            distance_from_center = abs(l_value - center)
            confidence = 1.0 - (distance_from_center / (range_size / 2))
            return fitz_type, max(0.7, min(0.98, confidence))
    
    if l_value >= 75:
        return FitzpatrickType.TYPE_I, 0.85
    else:
        return FitzpatrickType.TYPE_VI, 0.85


def analyze_skin_region(bgr_region: np.ndarray) -> Optional[Tuple[FitzpatrickType, float]]:
    """Analyze a BGR skin region and return Fitzpatrick classification."""
    if bgr_region.size == 0:
        return None
    
    # Convert to LAB
    lab = cv2.cvtColor(bgr_region, cv2.COLOR_BGR2LAB)
    
    # Get average L* value (needs to be converted from 0-255 to 0-100 scale)
    avg_l = np.mean(lab[:, :, 0]) * 100 / 255
    
    return classify_fitzpatrick(avg_l)


# ============================================================================
# FACE SHAPE CLASSIFICATION LOGIC
# ============================================================================

def classify_face_shape(measurements: Dict[str, float]) -> Tuple[FaceShape, float]:
    """Classify face shape from measurements."""
    length_width = measurements.get('length_width_ratio', 1.0)
    forehead_jaw = measurements.get('forehead_jaw_ratio', 1.0)
    jawline_angle = measurements.get('jawline_angle', 140)
    
    cheekbone_width = measurements.get('cheekbone_width', 1)
    forehead_width = measurements.get('forehead_width', 1)
    jaw_width = measurements.get('jaw_width', 1)
    
    cheekbone_forehead_ratio = cheekbone_width / forehead_width if forehead_width > 0 else 1
    cheekbone_jaw_ratio = cheekbone_width / jaw_width if jaw_width > 0 else 1
    
    scores = {}
    
    # ROUND
    round_score = 0.0
    if length_width < 1.1:
        round_score += 0.4
    if 0.95 < forehead_jaw < 1.05:
        round_score += 0.3
    if jawline_angle < 145:
        round_score += 0.3
    scores[FaceShape.ROUND] = round_score
    
    # OBLONG
    oblong_score = 0.0
    if length_width > 1.3:
        oblong_score += 0.6
        oblong_score += min(0.4, (length_width - 1.3) * 0.5)
    if 0.9 < forehead_jaw < 1.1:
        oblong_score += 0.2
    scores[FaceShape.OBLONG] = oblong_score
    
    # HEART
    heart_score = 0.0
    if forehead_jaw > 1.1:
        heart_score += 0.5
        heart_score += min(0.3, (forehead_jaw - 1.1) * 0.3)
    if length_width > 1.0:
        heart_score += 0.2
    scores[FaceShape.HEART] = heart_score
    
    # TRIANGLE
    triangle_score = 0.0
    if forehead_jaw < 0.9:
        triangle_score += 0.5
        triangle_score += min(0.3, (0.9 - forehead_jaw) * 0.3)
    scores[FaceShape.TRIANGLE] = triangle_score
    
    # SQUARE
    square_score = 0.0
    if jawline_angle > 150:
        square_score += 0.4
    if length_width < 1.15:
        square_score += 0.3
    if 0.9 < forehead_jaw < 1.1:
        square_score += 0.3
    scores[FaceShape.SQUARE] = square_score
    
    # DIAMOND
    diamond_score = 0.0
    if cheekbone_forehead_ratio > 1.05:
        diamond_score += 0.4
    if cheekbone_jaw_ratio > 1.05:
        diamond_score += 0.4
    if 1.1 < length_width < 1.3:
        diamond_score += 0.2
    scores[FaceShape.DIAMOND] = diamond_score
    
    # OVAL
    oval_score = 0.0
    if 1.1 < length_width < 1.3:
        oval_score += 0.4
    if 0.9 < forehead_jaw < 1.1:
        oval_score += 0.3
    if 130 < jawline_angle < 150:
        oval_score += 0.3
    scores[FaceShape.OVAL] = oval_score
    
    best_shape = max(scores, key=scores.get)
    best_score = scores[best_shape]
    
    sorted_scores = sorted(scores.values(), reverse=True)
    if len(sorted_scores) > 1:
        score_gap = sorted_scores[0] - sorted_scores[1]
        confidence = min(0.98, 0.7 + score_gap * 0.5)
    else:
        confidence = 0.85
    
    if best_score < 0.3:
        best_shape = FaceShape.OVAL
        confidence = 0.6
    
    return best_shape, confidence


# ============================================================================
# SYNTHETIC IMAGE CREATION
# ============================================================================

def create_skin_image(l_value: float, undertone: str = "neutral") -> np.ndarray:
    """Create a synthetic skin-colored image."""
    if undertone == "warm":
        a_value, b_value = 15, 25
    elif undertone == "cool":
        a_value, b_value = 18, 10
    else:
        a_value, b_value = 16, 18
    
    lab_img = np.zeros((100, 100, 3), dtype=np.float32)
    lab_img[:, :, 0] = l_value * 255 / 100
    lab_img[:, :, 1] = a_value + 128
    lab_img[:, :, 2] = b_value + 128
    
    lab_img = lab_img.astype(np.uint8)
    return cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)


# ============================================================================
# VALIDATION TESTS
# ============================================================================

def validate_skin_tone():
    """Validate skin tone classification."""
    print("\n" + "=" * 60)
    print("SKIN TONE THRESHOLD VALIDATION")
    print("=" * 60)
    
    test_cases = [
        (85, 1, "cool"),   # TYPE_I (75-100)
        (70, 2, "warm"),   # TYPE_II (65-75)
        (60, 3, "neutral"), # TYPE_III (55-65)
        (50, 4, "cool"),   # TYPE_IV (45-55)
        (40, 5, "warm"),   # TYPE_V (35-45)
        (28, 6, "neutral"), # TYPE_VI (0-35)
    ]
    
    correct = 0
    total = len(test_cases)
    
    for l_value, expected, undertone in test_cases:
        skin_img = create_skin_image(l_value, undertone)
        result = analyze_skin_region(skin_img)
        
        if result:
            predicted_type, conf = result
            predicted = predicted_type.value
            is_correct = predicted == expected
            if is_correct:
                correct += 1
            status = "PASS" if is_correct else "FAIL"
            print(f"  [{status}] L*={l_value}: Expected Type {expected}, Got Type {predicted} (conf: {conf:.2f})")
        else:
            print(f"  [FAIL] L*={l_value}: Analysis failed")
    
    accuracy = correct / total
    passed = accuracy >= ACCURACY_TARGET
    print(f"\n  Skin Tone Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"  Status: {'PASS' if passed else 'FAIL - NEEDS TUNING'}")
    
    return {'accuracy': accuracy, 'passed': passed, 'correct': correct, 'total': total}


def validate_face_shape():
    """Validate face shape classification."""
    print("\n" + "=" * 60)
    print("FACE SHAPE THRESHOLD VALIDATION")
    print("=" * 60)
    
    test_cases = [
        (1.2, 1.0, 140, "oval"),
        (1.05, 0.98, 135, "round"),
        (1.4, 1.0, 140, "oblong"),
        (1.15, 1.2, 145, "heart"),
        (1.1, 0.85, 140, "triangle"),
        (1.05, 1.0, 160, "square"),
        (1.2, 1.0, 140, "oval"),
    ]
    
    correct = 0
    total = len(test_cases)
    
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
        
        predicted_shape, conf = classify_face_shape(measurements)
        predicted = predicted_shape.value
        is_correct = predicted == expected
        
        if is_correct:
            correct += 1
        
        status = "PASS" if is_correct else "FAIL"
        print(f"  [{status}] LW={lw}, FJ={fj}, JA={ja}: Expected '{expected}', Got '{predicted}'")
    
    accuracy = correct / total
    passed = accuracy >= ACCURACY_TARGET
    print(f"\n  Face Shape Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"  Status: {'PASS' if passed else 'FAIL - NEEDS TUNING'}")
    
    return {'accuracy': accuracy, 'passed': passed, 'correct': correct, 'total': total}


def main():
    print("\n" + "=" * 60)
    print("LOOKCIRCUIT STYLE ANALYSIS VALIDATION")
    print("Target: >=95% Accuracy")
    print("=" * 60)
    
    skin_results = validate_skin_tone()
    shape_results = validate_face_shape()
    
    overall_correct = skin_results['correct'] + shape_results['correct']
    overall_total = skin_results['total'] + shape_results['total']
    overall_accuracy = overall_correct / overall_total
    all_passed = skin_results['passed'] and shape_results['passed']
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"  Skin Tone:  {skin_results['accuracy']:.1%} {'[PASS]' if skin_results['passed'] else '[FAIL]'}")
    print(f"  Face Shape: {shape_results['accuracy']:.1%} {'[PASS]' if shape_results['passed'] else '[FAIL]'}")
    print(f"  Overall:    {overall_accuracy:.1%}")
    print(f"\n  RESULT: {'ALL TESTS PASSED' if all_passed else 'THRESHOLD TUNING REQUIRED'}")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    import sys
    passed = main()
    sys.exit(0 if passed else 1)
