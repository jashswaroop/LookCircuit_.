"""
Face Analyzer - Main Orchestrator
Combines all face analysis modules into a unified analysis pipeline.
"""

import cv2
import numpy as np
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from .detector import FaceDetector, FaceDetectionResult
from .skin_tone import SkinToneDetector, SkinToneResult
from .face_shape import FaceShapeClassifier, FaceShapeResult
from .baldness import BaldnessDetector, BaldnessResult


@dataclass
class FaceAnalysisResult:
    """Complete face analysis result combining all modules."""
    detected: bool
    skin_tone: Optional[SkinToneResult]
    face_shape: Optional[FaceShapeResult]
    hair_coverage: Optional[BaldnessResult]
    color_season: Optional[str]
    overall_confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for API response."""
        result = {
            'detected': self.detected,
            'overall_confidence': self.overall_confidence
        }
        
        if self.skin_tone:
            result['skin_tone'] = {
                'fitzpatrick_type': self.skin_tone.fitzpatrick_type.name,
                'fitzpatrick_value': self.skin_tone.fitzpatrick_type.value,
                'undertone': self.skin_tone.undertone.value,
                'confidence': self.skin_tone.confidence,
                'hex_color': self.skin_tone.hex_color
            }
        
        if self.face_shape:
            result['face_shape'] = {
                'shape': self.face_shape.shape.value,
                'confidence': self.face_shape.confidence,
                'reasoning': self.face_shape.reasoning
            }
        
        if self.hair_coverage:
            result['hair_coverage'] = {
                'level': self.hair_coverage.coverage_level.value,
                'percentage': self.hair_coverage.coverage_percentage,
                'confidence': self.hair_coverage.confidence,
                'requires_alternative_styling': self.hair_coverage.requires_alternative_styling
            }
        
        if self.color_season:
            result['color_season'] = self.color_season
        
        return result


class FaceAnalyzer:
    """
    Main face analysis orchestrator.
    
    Combines:
    - Face Detection (MediaPipe)
    - Skin Tone Detection (Fitzpatrick Scale + Undertone)
    - Face Shape Classification
    - Baldness/Hair Coverage Detection
    
    Usage:
        analyzer = FaceAnalyzer()
        result = analyzer.analyze(image)
        print(result.to_dict())
    """
    
    def __init__(self):
        """Initialize all analysis modules."""
        self.face_detector = FaceDetector()
        self.skin_tone_detector = SkinToneDetector()
        self.face_shape_classifier = FaceShapeClassifier()
        self.baldness_detector = BaldnessDetector()
    
    def analyze(self, image: np.ndarray) -> FaceAnalysisResult:
        """
        Perform complete face analysis on an image.
        
        Args:
            image: BGR image as numpy array (from cv2.imread or camera)
            
        Returns:
            FaceAnalysisResult with all analysis components
        """
        # Step 1: Detect face and extract landmarks
        detection = self.face_detector.detect(image)
        
        if detection is None:
            return FaceAnalysisResult(
                detected=False,
                skin_tone=None,
                face_shape=None,
                hair_coverage=None,
                color_season=None,
                overall_confidence=0.0
            )
        
        # Step 2: Analyze skin tone from cheek and forehead regions
        skin_regions = []
        left_cheek, right_cheek = self.face_detector.get_cheek_regions(image, detection.landmarks)
        forehead = self.face_detector.get_forehead_region(image, detection.landmarks)
        
        if left_cheek.size > 0:
            skin_regions.append(left_cheek)
        if right_cheek.size > 0:
            skin_regions.append(right_cheek)
        if forehead.size > 0:
            skin_regions.append(forehead)
        
        skin_tone_result = self.skin_tone_detector.analyze(skin_regions)
        
        # Step 3: Classify face shape from measurements
        measurements = self.face_detector.get_face_measurements(detection.landmarks)
        face_shape_result = self.face_shape_classifier.classify(measurements)
        
        # Step 4: Analyze hair coverage
        baldness_result = self.baldness_detector.analyze(image, detection.bbox)
        
        # Step 5: Determine color season
        color_season = None
        if skin_tone_result:
            color_season = self.skin_tone_detector.get_season(
                skin_tone_result.fitzpatrick_type,
                skin_tone_result.undertone
            )
        
        # Calculate overall confidence
        confidences = []
        if skin_tone_result:
            confidences.append(skin_tone_result.confidence)
        if face_shape_result:
            confidences.append(face_shape_result.confidence)
        if baldness_result:
            confidences.append(baldness_result.confidence)
        
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return FaceAnalysisResult(
            detected=True,
            skin_tone=skin_tone_result,
            face_shape=face_shape_result,
            hair_coverage=baldness_result,
            color_season=color_season,
            overall_confidence=overall_confidence
        )
    
    def analyze_from_path(self, image_path: str) -> FaceAnalysisResult:
        """
        Analyze face from an image file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            FaceAnalysisResult
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        return self.analyze(image)
