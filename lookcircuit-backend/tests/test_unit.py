"""
Unit Tests for LookCircuit AI Modules
Comprehensive test suite using pytest.
"""

import pytest
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# TEST: Skin Tone Detection
# =============================================================================

class TestSkinToneDetector:
    """Tests for SkinToneDetector module."""
    
    @pytest.fixture
    def detector(self):
        from ai.face_analysis.skin_tone import SkinToneDetector
        return SkinToneDetector()
    
    @pytest.fixture
    def create_skin_image(self):
        import cv2
        import numpy as np
        
        def _create(l_value: float, undertone: str = "neutral"):
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
        
        return _create
    
    def test_type_i_classification(self, detector, create_skin_image):
        """Test Type I (very light) classification."""
        img = create_skin_image(85, "cool")
        result = detector.analyze([img])
        assert result is not None
        assert result.fitzpatrick_type.value == 1
    
    def test_type_iii_classification(self, detector, create_skin_image):
        """Test Type III (medium) classification."""
        img = create_skin_image(60, "neutral")
        result = detector.analyze([img])
        assert result is not None
        assert result.fitzpatrick_type.value == 3
    
    def test_type_vi_classification(self, detector, create_skin_image):
        """Test Type VI (dark) classification."""
        img = create_skin_image(28, "neutral")
        result = detector.analyze([img])
        assert result is not None
        assert result.fitzpatrick_type.value == 6
    
    def test_undertone_detection(self, detector, create_skin_image):
        """Test undertone detection."""
        warm_img = create_skin_image(60, "warm")
        result = detector.analyze([warm_img])
        assert result is not None
        # Undertone detection based on a*/b* ratio
    
    def test_empty_input(self, detector):
        """Test handling of empty input."""
        result = detector.analyze([])
        assert result is None
    
    def test_confidence_range(self, detector, create_skin_image):
        """Test that confidence is within valid range."""
        img = create_skin_image(60, "neutral")
        result = detector.analyze([img])
        assert result is not None
        assert 0.0 <= result.confidence <= 1.0


# =============================================================================
# TEST: Face Shape Classification
# =============================================================================

class TestFaceShapeClassifier:
    """Tests for FaceShapeClassifier module."""
    
    @pytest.fixture
    def classifier(self):
        from ai.face_analysis.face_shape import FaceShapeClassifier
        return FaceShapeClassifier()
    
    def test_oval_classification(self, classifier):
        """Test oval face shape classification."""
        measurements = {
            'length_width_ratio': 1.2,
            'forehead_jaw_ratio': 1.0,
            'jawline_angle': 140,
            'forehead_width': 100,
            'jaw_width': 100,
            'cheekbone_width': 95
        }
        result = classifier.classify(measurements)
        assert result.shape.value == "oval"
    
    def test_round_classification(self, classifier):
        """Test round face shape classification."""
        measurements = {
            'length_width_ratio': 1.05,
            'forehead_jaw_ratio': 0.98,
            'jawline_angle': 135,
            'forehead_width': 100,
            'jaw_width': 102,
            'cheekbone_width': 100
        }
        result = classifier.classify(measurements)
        assert result.shape.value == "round"
    
    def test_oblong_classification(self, classifier):
        """Test oblong face shape classification."""
        measurements = {
            'length_width_ratio': 1.4,
            'forehead_jaw_ratio': 1.0,
            'jawline_angle': 140,
            'forehead_width': 100,
            'jaw_width': 100,
            'cheekbone_width': 95
        }
        result = classifier.classify(measurements)
        assert result.shape.value == "oblong"
    
    def test_heart_classification(self, classifier):
        """Test heart face shape classification."""
        measurements = {
            'length_width_ratio': 1.15,
            'forehead_jaw_ratio': 1.2,
            'jawline_angle': 145,
            'forehead_width': 120,
            'jaw_width': 100,
            'cheekbone_width': 110
        }
        result = classifier.classify(measurements)
        assert result.shape.value == "heart"
    
    def test_square_classification(self, classifier):
        """Test square face shape classification."""
        measurements = {
            'length_width_ratio': 1.05,
            'forehead_jaw_ratio': 1.0,
            'jawline_angle': 160,
            'forehead_width': 100,
            'jaw_width': 100,
            'cheekbone_width': 100
        }
        result = classifier.classify(measurements)
        assert result.shape.value == "square"
    
    def test_confidence_range(self, classifier):
        """Test that confidence is within valid range."""
        measurements = {
            'length_width_ratio': 1.2,
            'forehead_jaw_ratio': 1.0,
            'jawline_angle': 140,
            'forehead_width': 100,
            'jaw_width': 100,
            'cheekbone_width': 95
        }
        result = classifier.classify(measurements)
        assert 0.0 <= result.confidence <= 1.0


# =============================================================================
# TEST: Color Theory Engine
# =============================================================================

class TestColorTheoryEngine:
    """Tests for ColorTheoryEngine module."""
    
    @pytest.fixture
    def engine(self):
        from ai.recommendation_engine.color_theory import ColorTheoryEngine
        return ColorTheoryEngine()
    
    def test_spring_season(self, engine):
        """Test Spring season determination."""
        from ai.recommendation_engine.color_theory import ColorSeason
        season = engine.determine_season(2, "warm")
        assert season == ColorSeason.SPRING
    
    def test_summer_season(self, engine):
        """Test Summer season determination."""
        from ai.recommendation_engine.color_theory import ColorSeason
        season = engine.determine_season(2, "cool")
        assert season == ColorSeason.SUMMER
    
    def test_autumn_season(self, engine):
        """Test Autumn season determination."""
        from ai.recommendation_engine.color_theory import ColorSeason
        season = engine.determine_season(4, "warm")
        assert season == ColorSeason.AUTUMN
    
    def test_winter_season(self, engine):
        """Test Winter season determination."""
        from ai.recommendation_engine.color_theory import ColorSeason
        season = engine.determine_season(5, "cool")
        assert season == ColorSeason.WINTER
    
    def test_palette_contains_colors(self, engine):
        """Test that palette contains color lists."""
        from ai.recommendation_engine.color_theory import ColorSeason
        palette = engine.get_palette(ColorSeason.SPRING)
        assert len(palette.best_colors) > 0
        assert len(palette.avoid_colors) > 0


# =============================================================================
# TEST: Recommendation Engine
# =============================================================================

class TestRecommendationEngine:
    """Tests for RecommendationEngine module."""
    
    @pytest.fixture
    def engine(self):
        from ai.recommendation_engine.color_theory import RecommendationEngine
        return RecommendationEngine()
    
    def test_generate_recommendations_structure(self, engine):
        """Test that recommendations contain all required sections."""
        result = engine.generate_recommendations(
            fitzpatrick_type=3,
            undertone="warm",
            face_shape="oval",
            body_type="mesomorph",
            hair_coverage="full",
            gender="male"
        )
        
        assert "color_analysis" in result
        assert "style" in result
        assert "grooming" in result
        assert "reasoning" in result
    
    def test_color_analysis_content(self, engine):
        """Test color analysis section content."""
        result = engine.generate_recommendations(
            fitzpatrick_type=3,
            undertone="warm",
            face_shape="oval"
        )
        
        assert "season" in result["color_analysis"]
        assert "best_colors" in result["color_analysis"]
        assert len(result["color_analysis"]["best_colors"]) > 0
    
    def test_bald_specific_recommendations(self, engine):
        """Test recommendations for bald users."""
        result = engine.generate_recommendations(
            fitzpatrick_type=3,
            undertone="warm",
            face_shape="oval",
            hair_coverage="bald",
            gender="male"
        )
        
        assert "alternative_styling" in result


# =============================================================================
# TEST: Product Discovery
# =============================================================================

class TestProductDiscovery:
    """Tests for ProductDiscoveryEngine module."""
    
    @pytest.fixture
    def engine(self):
        from ai.product_discovery.scraper import ProductDiscoveryEngine
        return ProductDiscoveryEngine()
    
    def test_discover_products(self, engine):
        """Test product discovery returns products."""
        result = engine.discover_products(
            color_palette=["#000080", "#FFFFFF"],
            categories=["shirts", "footwear"]
        )
        
        assert isinstance(result, dict)
    
    def test_product_structure(self, engine):
        """Test individual product structure."""
        result = engine.discover_products(
            color_palette=["#FFFFFF"],
            categories=["shirts"]
        )
        
        if "shirts" in result and len(result["shirts"]) > 0:
            product = result["shirts"][0]
            assert "name" in product
            assert "brand" in product
            assert "price" in product


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
