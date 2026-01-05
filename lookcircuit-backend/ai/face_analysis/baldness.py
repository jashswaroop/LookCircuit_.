"""
Baldness/Hair Coverage Detection Module
Detects hair coverage level to provide appropriate grooming recommendations.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class HairCoverageLevel(Enum):
    """Hair coverage classification levels."""
    FULL = "full"           # >80% coverage
    THINNING = "thinning"   # 40-80% coverage
    BALD = "bald"           # <40% coverage


@dataclass
class BaldnessResult:
    """Result of baldness/hair coverage detection."""
    coverage_level: HairCoverageLevel
    coverage_percentage: float
    confidence: float
    requires_alternative_styling: bool


class BaldnessDetector:
    """
    Hair coverage detection using color and texture analysis.
    
    Approach:
    1. Segment the head region above the face
    2. Detect hair vs skin pixels using color thresholds
    3. Calculate coverage percentage
    4. Classify into Full/Thinning/Bald
    """
    
    # Coverage thresholds
    FULL_COVERAGE_THRESHOLD = 0.80
    THINNING_THRESHOLD = 0.40
    
    def __init__(self):
        """Initialize the Baldness Detector."""
        pass
    
    def analyze(self, image: np.ndarray, face_bbox: Tuple[int, int, int, int]) -> Optional[BaldnessResult]:
        """
        Analyze hair coverage from image.
        
        Args:
            image: BGR image
            face_bbox: Face bounding box (x, y, width, height)
            
        Returns:
            BaldnessResult with coverage level and percentage
        """
        x, y, w, h = face_bbox
        img_height, img_width = image.shape[:2]
        
        # Extract region above the face (scalp area)
        scalp_region = self._extract_scalp_region(image, face_bbox)
        
        if scalp_region is None or scalp_region.size == 0:
            return BaldnessResult(
                coverage_level=HairCoverageLevel.FULL,
                coverage_percentage=100.0,
                confidence=0.5,
                requires_alternative_styling=False
            )
        
        # Analyze hair coverage
        coverage_percentage, confidence = self._calculate_hair_coverage(scalp_region)
        
        # Classify coverage level
        if coverage_percentage >= self.FULL_COVERAGE_THRESHOLD * 100:
            level = HairCoverageLevel.FULL
        elif coverage_percentage >= self.THINNING_THRESHOLD * 100:
            level = HairCoverageLevel.THINNING
        else:
            level = HairCoverageLevel.BALD
        
        return BaldnessResult(
            coverage_level=level,
            coverage_percentage=coverage_percentage,
            confidence=confidence,
            requires_alternative_styling=level != HairCoverageLevel.FULL
        )
    
    def _extract_scalp_region(self, image: np.ndarray, 
                               face_bbox: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        """
        Extract the scalp region above the face.
        
        Args:
            image: BGR image
            face_bbox: Face bounding box
            
        Returns:
            Cropped scalp region image
        """
        x, y, w, h = face_bbox
        img_height, img_width = image.shape[:2]
        
        # Calculate scalp region (above forehead)
        scalp_height = int(h * 0.5)  # Estimate scalp as 50% of face height
        scalp_y = max(0, y - scalp_height)
        scalp_h = y - scalp_y
        
        # Widen the region slightly to capture sides
        scalp_x = max(0, x - int(w * 0.1))
        scalp_w = min(img_width - scalp_x, int(w * 1.2))
        
        if scalp_h < 10 or scalp_w < 10:
            return None
        
        return image[scalp_y:scalp_y + scalp_h, scalp_x:scalp_x + scalp_w]
    
    def _calculate_hair_coverage(self, region: np.ndarray) -> Tuple[float, float]:
        """
        Calculate hair coverage percentage in the region.
        
        Uses color-based detection to differentiate hair from skin/background.
        
        Args:
            region: BGR image of scalp region
            
        Returns:
            Tuple of (coverage_percentage, confidence)
        """
        if region.size == 0:
            return 100.0, 0.5
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        # Hair detection using multiple criteria
        
        # Criterion 1: Dark pixels (hair is usually darker than skin)
        # Use adaptive thresholding based on image statistics
        mean_brightness = np.mean(gray)
        dark_threshold = max(50, mean_brightness * 0.6)
        dark_mask = gray < dark_threshold
        
        # Criterion 2: Low saturation for dark hair, or specific hues for colored hair
        # Hair typically has lower saturation than skin
        low_sat_mask = hsv[:, :, 1] < 80
        
        # Criterion 3: Texture analysis using edge detection
        # Hair has more texture than bald skin
        edges = cv2.Canny(gray, 50, 150)
        texture_mask = edges > 0
        
        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        
        # Combine masks: hair is dark AND (low saturation OR has texture)
        hair_mask = dark_mask & (low_sat_mask | cv2.dilate(texture_mask, kernel, iterations=2))
        
        # Clean up mask
        hair_mask = cv2.morphologyEx(hair_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
        hair_mask = cv2.morphologyEx(hair_mask, cv2.MORPH_OPEN, kernel)
        
        # Calculate coverage
        total_pixels = region.shape[0] * region.shape[1]
        hair_pixels = np.sum(hair_mask > 0)
        
        coverage_percentage = (hair_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        
        # Confidence based on mask quality
        edge_ratio = np.sum(texture_mask) / total_pixels
        confidence = min(0.95, 0.7 + edge_ratio * 0.5)
        
        return coverage_percentage, confidence
