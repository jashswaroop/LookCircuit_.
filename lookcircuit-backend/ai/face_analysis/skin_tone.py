"""
Skin Tone Detection Module
Classifies skin tone using Fitzpatrick Scale (I-VI) and detects undertone (Cool/Warm/Neutral).
"""

import cv2
import numpy as np
from typing import Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class FitzpatrickType(Enum):
    """Fitzpatrick Skin Type Scale (I-VI)"""
    TYPE_I = 1    # Very light, always burns
    TYPE_II = 2   # Light, burns easily
    TYPE_III = 3  # Medium, sometimes burns
    TYPE_IV = 4   # Olive, rarely burns
    TYPE_V = 5    # Brown, very rarely burns
    TYPE_VI = 6   # Dark brown/black, never burns


class Undertone(Enum):
    """Skin undertone classification"""
    COOL = "cool"
    WARM = "warm"
    NEUTRAL = "neutral"


@dataclass
class SkinToneResult:
    """Result of skin tone analysis."""
    fitzpatrick_type: FitzpatrickType
    undertone: Undertone
    confidence: float
    lab_values: Tuple[float, float, float]  # L*, a*, b* average values
    hex_color: str  # Representative skin color in hex


class SkinToneDetector:
    """
    Skin tone detection using LAB color space analysis.
    
    Approach:
    1. Extract skin regions (cheeks, forehead) using face landmarks
    2. Convert to LAB color space for perceptually uniform analysis
    3. Analyze L* (luminance) for Fitzpatrick classification
    4. Analyze a*/b* ratio for undertone detection
    """
    
    # Fitzpatrick thresholds based on L* values (luminance in LAB)
    # These are calibrated thresholds - may need adjustment based on validation
    FITZPATRICK_L_THRESHOLDS = {
        FitzpatrickType.TYPE_I: (75, 100),   # Very light
        FitzpatrickType.TYPE_II: (65, 75),   # Light
        FitzpatrickType.TYPE_III: (55, 65),  # Medium
        FitzpatrickType.TYPE_IV: (45, 55),   # Olive
        FitzpatrickType.TYPE_V: (35, 45),    # Brown
        FitzpatrickType.TYPE_VI: (0, 35),    # Dark
    }
    
    # Undertone thresholds based on a*/b* relationship
    # Positive a* = more red/pink (cool), Positive b* = more yellow (warm)
    UNDERTONE_THRESHOLD = 0.8  # b*/a* ratio threshold
    
    def __init__(self):
        """Initialize the Skin Tone Detector."""
        pass
    
    def analyze(self, skin_regions: list[np.ndarray]) -> Optional[SkinToneResult]:
        """
        Analyze skin tone from multiple skin region images.
        
        Args:
            skin_regions: List of BGR images containing skin regions
            
        Returns:
            SkinToneResult with Fitzpatrick type and undertone
        """
        if not skin_regions or all(r.size == 0 for r in skin_regions):
            return None
        
        # Collect LAB values from all regions
        all_lab_values = []
        
        for region in skin_regions:
            if region.size == 0:
                continue
                
            lab_values = self._extract_skin_lab_values(region)
            if lab_values is not None:
                all_lab_values.extend(lab_values)
        
        if not all_lab_values:
            return None
        
        # Calculate average LAB values
        lab_array = np.array(all_lab_values)
        avg_l = np.mean(lab_array[:, 0])
        avg_a = np.mean(lab_array[:, 1])
        avg_b = np.mean(lab_array[:, 2])
        
        # Classify Fitzpatrick type
        fitzpatrick_type, fitz_confidence = self._classify_fitzpatrick(avg_l)
        
        # Classify undertone
        undertone, undertone_confidence = self._classify_undertone(avg_a, avg_b)
        
        # Calculate overall confidence
        confidence = (fitz_confidence + undertone_confidence) / 2
        
        # Generate representative hex color
        hex_color = self._lab_to_hex(avg_l, avg_a, avg_b)
        
        return SkinToneResult(
            fitzpatrick_type=fitzpatrick_type,
            undertone=undertone,
            confidence=confidence,
            lab_values=(avg_l, avg_a, avg_b),
            hex_color=hex_color
        )
    
    def _extract_skin_lab_values(self, region: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract LAB values from skin pixels, filtering non-skin areas.
        
        Args:
            region: BGR image of skin region
            
        Returns:
            Array of LAB values for skin pixels
        """
        if region.size == 0:
            return None
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(region, cv2.COLOR_BGR2LAB)
        
        # Create skin mask using HSV thresholds
        # This helps filter out hair, shadows, and non-skin areas
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask1 = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Additional range for darker skin tones
        lower_skin2 = np.array([0, 10, 60], dtype=np.uint8)
        upper_skin2 = np.array([25, 255, 255], dtype=np.uint8)
        mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
        
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Apply morphological operations to clean mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Extract LAB values where mask is valid
        skin_pixels = lab[mask > 0]
        
        if len(skin_pixels) < 10:  # Need minimum pixels for reliable analysis
            # Fall back to center region sampling
            h, w = region.shape[:2]
            center_region = lab[h//4:3*h//4, w//4:3*w//4]
            skin_pixels = center_region.reshape(-1, 3)
        
        return skin_pixels if len(skin_pixels) > 0 else None
    
    def _classify_fitzpatrick(self, l_value: float) -> Tuple[FitzpatrickType, float]:
        """
        Classify Fitzpatrick type based on L* value.
        
        Args:
            l_value: Average L* value from LAB color space
            
        Returns:
            Tuple of (FitzpatrickType, confidence)
        """
        for fitz_type, (low, high) in self.FITZPATRICK_L_THRESHOLDS.items():
            if low <= l_value < high:
                # Calculate confidence based on distance from threshold edges
                range_size = high - low
                center = (low + high) / 2
                distance_from_center = abs(l_value - center)
                confidence = 1.0 - (distance_from_center / (range_size / 2))
                return fitz_type, max(0.7, min(0.98, confidence))
        
        # Edge cases
        if l_value >= 75:
            return FitzpatrickType.TYPE_I, 0.85
        else:
            return FitzpatrickType.TYPE_VI, 0.85
    
    def _classify_undertone(self, a_value: float, b_value: float) -> Tuple[Undertone, float]:
        """
        Classify undertone based on a* and b* values.
        
        a* axis: green (-) to red (+)
        b* axis: blue (-) to yellow (+)
        
        Warm undertones: higher b* (more yellow)
        Cool undertones: higher a* relative to b* (more pink/red)
        Neutral: balanced a* and b*
        
        Args:
            a_value: Average a* value
            b_value: Average b* value
            
        Returns:
            Tuple of (Undertone, confidence)
        """
        # Normalize values (a* and b* typically range from -128 to 127)
        # Shift to positive range for ratio calculation
        a_shifted = a_value + 128
        b_shifted = b_value + 128
        
        if a_shifted == 0:
            a_shifted = 0.01  # Avoid division by zero
        
        ratio = b_shifted / a_shifted
        
        # Classification based on b*/a* ratio
        if ratio > 1.1:
            undertone = Undertone.WARM
            confidence = min(0.95, 0.7 + (ratio - 1.1) * 0.1)
        elif ratio < 0.9:
            undertone = Undertone.COOL
            confidence = min(0.95, 0.7 + (0.9 - ratio) * 0.1)
        else:
            undertone = Undertone.NEUTRAL
            # Confidence is higher when closer to 1.0
            confidence = 0.8 + (1.0 - abs(ratio - 1.0)) * 0.15
        
        return undertone, confidence
    
    def _lab_to_hex(self, l: float, a: float, b: float) -> str:
        """
        Convert LAB values to hex color string.
        
        Args:
            l, a, b: LAB color values
            
        Returns:
            Hex color string (e.g., "#F5DEB3")
        """
        # Create a 1x1 image with LAB values
        lab_pixel = np.array([[[l, a, b]]], dtype=np.float32)
        
        # Normalize to OpenCV LAB range
        lab_pixel[:, :, 0] = lab_pixel[:, :, 0] * 255 / 100  # L: 0-100 -> 0-255
        lab_pixel[:, :, 1] = lab_pixel[:, :, 1] + 128  # a: -128 to 127 -> 0-255
        lab_pixel[:, :, 2] = lab_pixel[:, :, 2] + 128  # b: -128 to 127 -> 0-255
        
        lab_pixel = lab_pixel.astype(np.uint8)
        
        # Convert to BGR
        bgr_pixel = cv2.cvtColor(lab_pixel, cv2.COLOR_LAB2BGR)
        
        # Extract RGB values
        b_val, g_val, r_val = bgr_pixel[0, 0]
        
        return f"#{r_val:02X}{g_val:02X}{b_val:02X}"
    
    def get_season(self, fitzpatrick: FitzpatrickType, undertone: Undertone) -> str:
        """
        Determine color season based on Fitzpatrick type and undertone.
        
        Returns:
            Season string: "spring", "summer", "autumn", "winter"
        """
        is_light = fitzpatrick.value <= 3
        is_warm = undertone == Undertone.WARM
        
        if is_light and is_warm:
            return "spring"
        elif is_light and not is_warm:
            return "summer"
        elif not is_light and is_warm:
            return "autumn"
        else:
            return "winter"
