"""
Simple Integration Test - Self Contained
Runs directly from lookcircuit-backend directory
"""

import sys
import os

# Absolute path setup
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR.endswith('tests'):
    BACKEND_DIR = os.path.dirname(BACKEND_DIR)
sys.path.insert(0, BACKEND_DIR)

print("Backend Dir:", BACKEND_DIR)
print("=" * 60)
print("LOOKCIRCUIT SIMPLE TEST")
print("=" * 60)

# Test 1: Import check
print("\n[1] Import Test")
try:
    from ai.face_analysis.skin_tone import SkinToneDetector, FitzpatrickType
    from ai.face_analysis.face_shape import FaceShapeClassifier, FaceShape
    from ai.recommendation_engine.color_theory import (
        ColorTheoryEngine, RecommendationEngine, StyleMatchingEngine, 
        GroomingRecommendationEngine, ColorSeason
    )
    from ai.recommendation_engine.occasion_styling import OccasionStylingEngine
    print("    [OK] All modules imported successfully")
    import_ok = True
except Exception as e:
    print(f"    [FAIL] Import error: {e}")
    import_ok = False
    sys.exit(1)

# Test 2: Color Theory
print("\n[2] Color Theory Test")
ct = ColorTheoryEngine()
season = ct.determine_season(3, "warm")
if season == ColorSeason.SPRING:
    print(f"    [OK] Type 3 + warm = {season.value}")
else:
    print(f"    [FAIL] Expected SPRING, got {season.value}")

season2 = ct.determine_season(5, "cool")
if season2 == ColorSeason.WINTER:
    print(f"    [OK] Type 5 + cool = {season2.value}")
else:
    print(f"    [FAIL] Expected WINTER, got {season2.value}")

# Test 3: Face Shape
print("\n[3] Face Shape Test")
fs = FaceShapeClassifier()
result = fs.classify({
    'length_width_ratio': 1.2,
    'forehead_jaw_ratio': 1.0,
    'jawline_angle': 140,
    'forehead_width': 100,
    'jaw_width': 100,
    'cheekbone_width': 95
})
if result.shape == FaceShape.OVAL:
    print(f"    [OK] Oval detected (conf: {result.confidence:.2f})")
else:
    print(f"    [FAIL] Expected OVAL, got {result.shape.value}")

# Test 4: Recommendations
print("\n[4] Recommendation Engine Test")
rec = RecommendationEngine()
recs = rec.generate_recommendations(
    fitzpatrick_type=3,
    undertone="warm",
    face_shape="oval",
    body_type="mesomorph"
)
if "color_analysis" in recs and "style" in recs:
    print(f"    [OK] Recommendations generated")
    print(f"        Season: {recs['color_analysis']['season']}")
    print(f"        Colors: {recs['color_analysis']['best_colors'][:3]}")
    print(f"        Necklines: {recs['style']['recommended_necklines'][:3]}")
else:
    print(f"    [FAIL] Missing recommendation components")

# Test 5: Occasions
print("\n[5] Occasion Styling Test")
occ = OccasionStylingEngine()
outfit = occ.get_occasion_outfit("interview", "male", ["#000080"], "oval")
if outfit.top and outfit.bottom:
    print(f"    [OK] Interview outfit: {outfit.top['type']}, {outfit.bottom['type']}")
else:
    print(f"    [FAIL] Missing outfit components")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
