"""
Face Shape Classification Module
Classifies face shapes into: Oval, Round, Square, Heart, Oblong, Diamond
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class FaceShape(Enum):
    """Face shape classification categories."""
    OVAL = "oval"
    ROUND = "round"
    SQUARE = "square"
    HEART = "heart"
    OBLONG = "oblong"
    DIAMOND = "diamond"
    TRIANGLE = "triangle"


@dataclass
class FaceShapeResult:
    """Result of face shape classification."""
    shape: FaceShape
    confidence: float
    measurements: Dict[str, float]
    reasoning: str


class FaceShapeClassifier:
    """
    Face shape classification using geometric ratios from facial landmarks.
    
    Classification Logic:
    - Oval: Balanced proportions, length slightly greater than width
    - Round: Length ≈ Width, soft jawline
    - Square: Length ≈ Width, angular jawline
    - Heart: Wide forehead, narrow jaw
    - Oblong: Length >> Width
    - Diamond: Wide cheekbones, narrow forehead and jaw
    - Triangle: Narrow forehead, wide jaw
    """
    
    # Threshold constants (tuned for accuracy)
    ROUND_LENGTH_WIDTH_THRESHOLD = 1.1
    OBLONG_LENGTH_WIDTH_THRESHOLD = 1.3
    HEART_FOREHEAD_JAW_THRESHOLD = 1.1
    TRIANGLE_FOREHEAD_JAW_THRESHOLD = 0.9
    SQUARE_JAWLINE_ANGLE_THRESHOLD = 150  # degrees
    DIAMOND_CHEEKBONE_THRESHOLD = 1.05  # cheekbone > forehead and jaw
    
    def __init__(self):
        """Initialize the Face Shape Classifier."""
        pass
    
    def classify(self, measurements: Dict[str, float]) -> FaceShapeResult:
        """
        Classify face shape based on facial measurements.
        
        Args:
            measurements: Dictionary containing:
                - face_length: Top to chin distance
                - face_width: Cheekbone width
                - forehead_width: Forehead width
                - jaw_width: Jaw width
                - cheekbone_width: Cheekbone width
                - jawline_angle: Angle at chin
                - length_width_ratio: face_length / face_width
                - forehead_jaw_ratio: forehead_width / jaw_width
                
        Returns:
            FaceShapeResult with shape, confidence, and reasoning
        """
        length_width = measurements.get('length_width_ratio', 1.0)
        forehead_jaw = measurements.get('forehead_jaw_ratio', 1.0)
        jawline_angle = measurements.get('jawline_angle', 140)
        
        # Calculate additional ratios for diamond detection
        forehead_width = measurements.get('forehead_width', 1)
        jaw_width = measurements.get('jaw_width', 1)
        cheekbone_width = measurements.get('cheekbone_width', 1)
        
        cheekbone_forehead_ratio = cheekbone_width / forehead_width if forehead_width > 0 else 1
        cheekbone_jaw_ratio = cheekbone_width / jaw_width if jaw_width > 0 else 1
        
        # Classification logic with confidence scoring
        shape, confidence, reasoning = self._apply_classification_rules(
            length_width=length_width,
            forehead_jaw=forehead_jaw,
            jawline_angle=jawline_angle,
            cheekbone_forehead_ratio=cheekbone_forehead_ratio,
            cheekbone_jaw_ratio=cheekbone_jaw_ratio
        )
        
        return FaceShapeResult(
            shape=shape,
            confidence=confidence,
            measurements=measurements,
            reasoning=reasoning
        )
    
    def _apply_classification_rules(
        self,
        length_width: float,
        forehead_jaw: float,
        jawline_angle: float,
        cheekbone_forehead_ratio: float,
        cheekbone_jaw_ratio: float
    ) -> Tuple[FaceShape, float, str]:
        """
        Apply classification rules with confidence scoring.
        
        Returns:
            Tuple of (FaceShape, confidence, reasoning)
        """
        scores = {}
        
        # Score each face shape based on how well measurements match
        
        # ROUND: Short face, similar width and length
        round_score = 0.0
        if length_width < self.ROUND_LENGTH_WIDTH_THRESHOLD:
            round_score += 0.4
        if 0.95 < forehead_jaw < 1.05:  # Balanced forehead and jaw
            round_score += 0.3
        if jawline_angle < 145:  # Softer jawline
            round_score += 0.3
        scores[FaceShape.ROUND] = round_score
        
        # OBLONG: Long face
        oblong_score = 0.0
        if length_width > self.OBLONG_LENGTH_WIDTH_THRESHOLD:
            oblong_score += 0.6
            oblong_score += min(0.4, (length_width - 1.3) * 0.5)
        if 0.9 < forehead_jaw < 1.1:
            oblong_score += 0.2
        scores[FaceShape.OBLONG] = oblong_score
        
        # HEART: Wide forehead, narrow jaw
        heart_score = 0.0
        if forehead_jaw > self.HEART_FOREHEAD_JAW_THRESHOLD:
            heart_score += 0.5
            heart_score += min(0.3, (forehead_jaw - 1.1) * 0.3)
        if length_width > 1.0:
            heart_score += 0.2
        scores[FaceShape.HEART] = heart_score
        
        # TRIANGLE: Narrow forehead, wide jaw
        triangle_score = 0.0
        if forehead_jaw < self.TRIANGLE_FOREHEAD_JAW_THRESHOLD:
            triangle_score += 0.5
            triangle_score += min(0.3, (0.9 - forehead_jaw) * 0.3)
        scores[FaceShape.TRIANGLE] = triangle_score
        
        # SQUARE: Angular jawline, balanced proportions
        square_score = 0.0
        if jawline_angle > self.SQUARE_JAWLINE_ANGLE_THRESHOLD:
            square_score += 0.4
        if length_width < 1.15:
            square_score += 0.3
        if 0.9 < forehead_jaw < 1.1:
            square_score += 0.3
        scores[FaceShape.SQUARE] = square_score
        
        # DIAMOND: Prominent cheekbones
        diamond_score = 0.0
        if cheekbone_forehead_ratio > self.DIAMOND_CHEEKBONE_THRESHOLD:
            diamond_score += 0.4
        if cheekbone_jaw_ratio > self.DIAMOND_CHEEKBONE_THRESHOLD:
            diamond_score += 0.4
        if 1.1 < length_width < 1.3:
            diamond_score += 0.2
        scores[FaceShape.DIAMOND] = diamond_score
        
        # OVAL: Balanced proportions (default/fallback)
        oval_score = 0.0
        if 1.1 < length_width < 1.3:
            oval_score += 0.4
        if 0.9 < forehead_jaw < 1.1:
            oval_score += 0.3
        if 130 < jawline_angle < 150:
            oval_score += 0.3
        scores[FaceShape.OVAL] = oval_score
        
        # Find best match
        best_shape = max(scores, key=scores.get)
        best_score = scores[best_shape]
        
        # Calculate confidence based on score difference from second best
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            score_gap = sorted_scores[0] - sorted_scores[1]
            confidence = min(0.98, 0.7 + score_gap * 0.5)
        else:
            confidence = 0.85
        
        # If no clear winner, default to oval
        if best_score < 0.3:
            best_shape = FaceShape.OVAL
            confidence = 0.6
        
        # Generate reasoning
        reasoning = self._generate_reasoning(best_shape, length_width, forehead_jaw, jawline_angle)
        
        return best_shape, confidence, reasoning
    
    def _generate_reasoning(
        self,
        shape: FaceShape,
        length_width: float,
        forehead_jaw: float,
        jawline_angle: float
    ) -> str:
        """Generate human-readable reasoning for the classification."""
        
        reasons = {
            FaceShape.OVAL: f"Balanced proportions with length-to-width ratio of {length_width:.2f}",
            FaceShape.ROUND: f"Face length approximately equals width (ratio: {length_width:.2f})",
            FaceShape.SQUARE: f"Angular jawline ({jawline_angle:.0f}°) with balanced proportions",
            FaceShape.HEART: f"Forehead wider than jaw (ratio: {forehead_jaw:.2f})",
            FaceShape.OBLONG: f"Face length significantly exceeds width (ratio: {length_width:.2f})",
            FaceShape.DIAMOND: f"Prominent cheekbones with narrower forehead and jaw",
            FaceShape.TRIANGLE: f"Jaw wider than forehead (ratio: {forehead_jaw:.2f})"
        }
        
        return reasons.get(shape, "Classification based on facial measurements")
