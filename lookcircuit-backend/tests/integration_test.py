"""
Integration Test Suite for LookCircuit
Tests the complete pipeline from analysis to recommendations.
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 70)
print("LOOKCIRCUIT INTEGRATION TEST SUITE")
print("=" * 70)

# ============================================================================
# TEST 1: Skin Tone Classification
# ============================================================================
print("\n[TEST 1] SKIN TONE CLASSIFICATION")
print("-" * 40)

import cv2
import numpy as np

def create_skin_image(l_value, undertone="neutral"):
    """Create synthetic skin image."""
    if undertone == "warm":
        a, b = 15, 25
    elif undertone == "cool":
        a, b = 18, 10
    else:
        a, b = 16, 18
    
    lab = np.zeros((100, 100, 3), dtype=np.float32)
    lab[:, :, 0] = l_value * 255 / 100
    lab[:, :, 1] = a + 128
    lab[:, :, 2] = b + 128
    return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)

try:
    from ai.face_analysis.skin_tone import SkinToneDetector
    detector = SkinToneDetector()
    
    test_cases = [
        (85, 1), (70, 2), (60, 3), (50, 4), (40, 5), (28, 6)
    ]
    
    passed = 0
    for l_val, expected in test_cases:
        img = create_skin_image(l_val, "neutral")
        result = detector.analyze([img])
        if result and result.fitzpatrick_type.value == expected:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"
        print(f"  [{status}] L*={l_val} -> Type {expected}")
    
    skin_accuracy = passed / len(test_cases)
    print(f"\n  Skin Tone Accuracy: {skin_accuracy:.0%} ({passed}/{len(test_cases)})")
    skin_test_pass = skin_accuracy >= 0.9
except Exception as e:
    print(f"  ERROR: {e}")
    skin_test_pass = False

# ============================================================================
# TEST 2: Face Shape Classification
# ============================================================================
print("\n[TEST 2] FACE SHAPE CLASSIFICATION")
print("-" * 40)

try:
    from ai.face_analysis.face_shape import FaceShapeClassifier
    classifier = FaceShapeClassifier()
    
    shape_tests = [
        (1.2, 1.0, 140, "oval"),
        (1.05, 0.98, 135, "round"),
        (1.4, 1.0, 140, "oblong"),
        (1.15, 1.2, 145, "heart"),
        (1.05, 1.0, 160, "square"),
    ]
    
    passed = 0
    for lw, fj, ja, expected in shape_tests:
        measurements = {
            'face_length': 200, 'face_width': 200/lw,
            'forehead_width': 100, 'jaw_width': 100/fj,
            'cheekbone_width': 95, 'jawline_angle': ja,
            'length_width_ratio': lw, 'forehead_jaw_ratio': fj
        }
        result = classifier.classify(measurements)
        if result.shape.value == expected:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"
        print(f"  [{status}] LW={lw}, FJ={fj} -> {expected} (got: {result.shape.value})")
    
    shape_accuracy = passed / len(shape_tests)
    print(f"\n  Face Shape Accuracy: {shape_accuracy:.0%} ({passed}/{len(shape_tests)})")
    shape_test_pass = shape_accuracy >= 0.9
except Exception as e:
    print(f"  ERROR: {e}")
    shape_test_pass = False

# ============================================================================
# TEST 3: Color Theory Engine
# ============================================================================
print("\n[TEST 3] COLOR THEORY ENGINE")
print("-" * 40)

try:
    from ai.recommendation_engine.color_theory import ColorTheoryEngine, ColorSeason
    engine = ColorTheoryEngine()
    
    color_tests = [
        (1, "warm", ColorSeason.SPRING),
        (2, "cool", ColorSeason.SUMMER),
        (4, "warm", ColorSeason.AUTUMN),
        (5, "cool", ColorSeason.WINTER),
    ]
    
    passed = 0
    for fitz, undertone, expected_season in color_tests:
        season = engine.determine_season(fitz, undertone)
        if season == expected_season:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"
        print(f"  [{status}] Type {fitz} + {undertone} -> {expected_season.value} (got: {season.value})")
    
    color_accuracy = passed / len(color_tests)
    print(f"\n  Color Season Accuracy: {color_accuracy:.0%} ({passed}/{len(color_tests)})")
    color_test_pass = color_accuracy >= 0.9
except Exception as e:
    print(f"  ERROR: {e}")
    color_test_pass = False

# ============================================================================
# TEST 4: Full Recommendation Engine
# ============================================================================
print("\n[TEST 4] RECOMMENDATION ENGINE INTEGRATION")
print("-" * 40)

try:
    from ai.recommendation_engine.color_theory import RecommendationEngine
    engine = RecommendationEngine()
    
    result = engine.generate_recommendations(
        fitzpatrick_type=3,
        undertone="warm",
        face_shape="oval",
        body_type="mesomorph",
        hair_coverage="full",
        gender="male"
    )
    
    checks = [
        ("color_analysis" in result, "Color analysis present"),
        ("style" in result, "Style recommendations present"),
        ("grooming" in result, "Grooming recommendations present"),
        ("reasoning" in result, "Reasoning present"),
        (len(result["color_analysis"]["best_colors"]) > 0, "Best colors provided"),
        (len(result["style"]["recommended_necklines"]) > 0, "Necklines provided"),
        (len(result["grooming"]["hairstyles"]) > 0, "Hairstyles provided"),
    ]
    
    passed = 0
    for check, name in checks:
        if check:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
    
    rec_accuracy = passed / len(checks)
    print(f"\n  Recommendation Engine: {rec_accuracy:.0%} ({passed}/{len(checks)})")
    rec_test_pass = rec_accuracy >= 0.9
except Exception as e:
    print(f"  ERROR: {e}")
    rec_test_pass = False

# ============================================================================
# TEST 5: Occasion Styling
# ============================================================================
print("\n[TEST 5] OCCASION STYLING ENGINE")
print("-" * 40)

try:
    from ai.recommendation_engine.occasion_styling import OccasionStylingEngine
    engine = OccasionStylingEngine()
    
    occasions = ["casual", "formal", "interview", "date_night"]
    passed = 0
    
    for occasion in occasions:
        outfit = engine.get_occasion_outfit(
            occasion=occasion,
            gender="male",
            color_palette=["#000080", "#FFFFFF"],
            face_shape="oval"
        )
        if outfit.top and outfit.bottom and outfit.footwear:
            passed += 1
            print(f"  [PASS] {occasion}: {outfit.top['type']}, {outfit.bottom['type']}")
        else:
            print(f"  [FAIL] {occasion}: Missing outfit components")
    
    occasion_accuracy = passed / len(occasions)
    print(f"\n  Occasion Styling: {occasion_accuracy:.0%} ({passed}/{len(occasions)})")
    occasion_test_pass = occasion_accuracy >= 0.9
except Exception as e:
    print(f"  ERROR: {e}")
    occasion_test_pass = False

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

tests = [
    ("Skin Tone Classification", skin_test_pass),
    ("Face Shape Classification", shape_test_pass),
    ("Color Theory Engine", color_test_pass),
    ("Recommendation Engine", rec_test_pass),
    ("Occasion Styling", occasion_test_pass),
]

all_passed = True
for name, passed in tests:
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_passed = False
    print(f"  [{status}] {name}")

print("\n" + "=" * 70)
if all_passed:
    print("OVERALL RESULT: ALL TESTS PASSED")
    exit_code = 0
else:
    print("OVERALL RESULT: SOME TESTS FAILED")
    exit_code = 1
print("=" * 70)

sys.exit(exit_code)
