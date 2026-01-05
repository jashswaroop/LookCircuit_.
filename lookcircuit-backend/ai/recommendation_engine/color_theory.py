"""
Color Theory and Recommendation Engine for LookCircuit
Provides personalized color palettes and style recommendations based on analysis results.
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


class ColorSeason(Enum):
    """Seasonal color analysis categories."""
    SPRING = "spring"   # Warm + Light
    SUMMER = "summer"   # Cool + Light
    AUTUMN = "autumn"   # Warm + Dark
    WINTER = "winter"   # Cool + Dark


@dataclass
class ColorPalette:
    """A color palette with best and avoid colors."""
    best_colors: List[str]  # Hex colors
    accent_colors: List[str]
    neutral_colors: List[str]
    avoid_colors: List[str]
    metal_preference: str  # gold/silver/rose_gold


@dataclass 
class StyleRecommendation:
    """Complete style recommendation for a user."""
    color_palette: ColorPalette
    season: ColorSeason
    necklines: List[str]
    patterns: List[str]
    fits: List[str]
    accessories: List[str]
    reasoning: Dict[str, str]


class ColorTheoryEngine:
    """
    Color theory engine implementing seasonal color analysis.
    
    Uses Fitzpatrick skin tone + undertone to determine:
    1. Color season (Spring/Summer/Autumn/Winter)
    2. Best color palette
    3. Colors to avoid
    """
    
    # Seasonal color palettes
    SEASONAL_PALETTES = {
        ColorSeason.SPRING: ColorPalette(
            best_colors=[
                "#FFDAB9",  # Peach
                "#FFD700",  # Gold
                "#FF6347",  # Tomato coral
                "#98FB98",  # Pale green
                "#87CEEB",  # Sky blue
                "#FFA07A",  # Light salmon
                "#F0E68C",  # Khaki
                "#DDA0DD",  # Plum light
            ],
            accent_colors=["#FF4500", "#32CD32", "#FF69B4"],
            neutral_colors=["#F5F5DC", "#D2B48C", "#8B7355", "#FFFFF0"],
            avoid_colors=["#000000", "#4A0000", "#2F4F4F", "#800000"],
            metal_preference="gold"
        ),
        ColorSeason.SUMMER: ColorPalette(
            best_colors=[
                "#E6E6FA",  # Lavender
                "#B0C4DE",  # Light steel blue
                "#DDA0DD",  # Plum
                "#FFC0CB",  # Pink
                "#ADD8E6",  # Light blue
                "#D8BFD8",  # Thistle
                "#F0E68C",  # Soft yellow
                "#98FB98",  # Pale green
            ],
            accent_colors=["#9370DB", "#20B2AA", "#DB7093"],
            neutral_colors=["#DCDCDC", "#C0C0C0", "#A9A9A9", "#F5F5F5"],
            avoid_colors=["#FF4500", "#FFD700", "#8B4513", "#FF6347"],
            metal_preference="silver"
        ),
        ColorSeason.AUTUMN: ColorPalette(
            best_colors=[
                "#8B4513",  # Saddle brown
                "#D2691E",  # Chocolate
                "#556B2F",  # Dark olive green
                "#CD853F",  # Peru
                "#B8860B",  # Dark goldenrod
                "#A0522D",  # Sienna
                "#6B8E23",  # Olive drab
                "#DAA520",  # Goldenrod
            ],
            accent_colors=["#FF8C00", "#228B22", "#DC143C"],
            neutral_colors=["#F5DEB3", "#D2B48C", "#8B7355", "#5C4033"],
            avoid_colors=["#FF69B4", "#00FFFF", "#E6E6FA", "#C0C0C0"],
            metal_preference="gold"
        ),
        ColorSeason.WINTER: ColorPalette(
            best_colors=[
                "#000080",  # Navy
                "#800020",  # Burgundy
                "#228B22",  # Forest green
                "#FFFFFF",  # White
                "#DC143C",  # Crimson
                "#4169E1",  # Royal blue
                "#8B008B",  # Dark magenta
                "#2F4F4F",  # Dark slate gray
            ],
            accent_colors=["#FF0000", "#0000FF", "#FF1493"],
            neutral_colors=["#000000", "#FFFFFF", "#808080", "#36454F"],
            avoid_colors=["#FFDAB9", "#F5DEB3", "#DEB887", "#FFE4B5"],
            metal_preference="silver"
        ),
    }
    
    def __init__(self):
        pass
    
    def determine_season(self, fitzpatrick_type: int, undertone: str) -> ColorSeason:
        """
        Determine color season based on skin characteristics.
        
        Args:
            fitzpatrick_type: Fitzpatrick scale 1-6
            undertone: "cool", "warm", or "neutral"
            
        Returns:
            ColorSeason enum value
        """
        is_light = fitzpatrick_type <= 3
        is_warm = undertone.lower() == "warm"
        
        # Neutral undertone: determine based on skin depth
        if undertone.lower() == "neutral":
            # Neutrals can go either way - lean warm for light, cool for dark
            is_warm = is_light
        
        if is_light and is_warm:
            return ColorSeason.SPRING
        elif is_light and not is_warm:
            return ColorSeason.SUMMER
        elif not is_light and is_warm:
            return ColorSeason.AUTUMN
        else:
            return ColorSeason.WINTER
    
    def get_palette(self, season: ColorSeason) -> ColorPalette:
        """Get the color palette for a season."""
        return self.SEASONAL_PALETTES[season]
    
    def get_color_recommendations(self, fitzpatrick_type: int, 
                                   undertone: str) -> Tuple[ColorSeason, ColorPalette]:
        """
        Get complete color recommendations.
        
        Args:
            fitzpatrick_type: Fitzpatrick scale 1-6
            undertone: "cool", "warm", or "neutral"
            
        Returns:
            Tuple of (ColorSeason, ColorPalette)
        """
        season = self.determine_season(fitzpatrick_type, undertone)
        palette = self.get_palette(season)
        return season, palette


class StyleMatchingEngine:
    """
    Style matching engine for clothing and accessory recommendations.
    Based on face shape and body type analysis.
    """
    
    # Neckline recommendations by face shape
    NECKLINE_BY_FACE_SHAPE = {
        "oval": ["v-neck", "crew", "scoop", "boat", "turtleneck"],
        "round": ["v-neck", "deep-v", "asymmetric", "open collar"],
        "square": ["scoop", "round", "cowl", "off-shoulder"],
        "heart": ["v-neck", "sweetheart", "scoop", "boat"],
        "oblong": ["crew", "boat", "cowl", "turtleneck", "square"],
        "diamond": ["boat", "off-shoulder", "v-neck", "scoop"],
        "triangle": ["boat", "off-shoulder", "cowl", "wide scoop"],
    }
    
    # Pattern recommendations by body type
    PATTERN_BY_BODY_TYPE = {
        "ectomorph": ["horizontal stripes", "bold patterns", "large prints"],
        "mesomorph": ["solid colors", "medium patterns", "subtle prints"],
        "endomorph": ["vertical stripes", "small patterns", "solid dark colors"],
    }
    
    # Fit recommendations
    FIT_BY_BODY_TYPE = {
        "ectomorph": ["regular", "relaxed", "layered"],
        "mesomorph": ["slim", "regular", "tailored"],
        "endomorph": ["regular", "structured", "a-line"],
    }
    
    # Accessory recommendations by face shape
    EYEWEAR_BY_FACE_SHAPE = {
        "oval": ["aviator", "wayfarer", "round", "cat-eye"],
        "round": ["rectangular", "square", "angular", "wayfarers"],
        "square": ["round", "oval", "aviator", "cat-eye"],
        "heart": ["aviator", "round", "rimless", "light frames"],
        "oblong": ["oversized", "square", "decorative temples"],
        "diamond": ["oval", "rimless", "cat-eye", "browline"],
        "triangle": ["cat-eye", "semi-rimless", "bold top frames"],
    }
    
    def __init__(self):
        pass
    
    def get_neckline_recommendations(self, face_shape: str) -> List[str]:
        """Get recommended necklines for a face shape."""
        return self.NECKLINE_BY_FACE_SHAPE.get(
            face_shape.lower(), 
            self.NECKLINE_BY_FACE_SHAPE["oval"]
        )
    
    def get_pattern_recommendations(self, body_type: str) -> List[str]:
        """Get recommended patterns for a body type."""
        return self.PATTERN_BY_BODY_TYPE.get(
            body_type.lower(),
            self.PATTERN_BY_BODY_TYPE["mesomorph"]
        )
    
    def get_fit_recommendations(self, body_type: str) -> List[str]:
        """Get recommended fits for a body type."""
        return self.FIT_BY_BODY_TYPE.get(
            body_type.lower(),
            self.FIT_BY_BODY_TYPE["mesomorph"]
        )
    
    def get_eyewear_recommendations(self, face_shape: str) -> List[str]:
        """Get recommended eyewear styles for a face shape."""
        return self.EYEWEAR_BY_FACE_SHAPE.get(
            face_shape.lower(),
            self.EYEWEAR_BY_FACE_SHAPE["oval"]
        )


class GroomingRecommendationEngine:
    """
    Grooming recommendations based on face analysis.
    Includes hairstyles, beard styles, and skincare tips.
    """
    
    HAIRSTYLES_BY_FACE_SHAPE = {
        "oval": ["side part", "pompadour", "textured crop", "slick back", "quiff"],
        "round": ["high fade", "pompadour", "side part", "spiky", "undercut"],
        "square": ["textured top", "side part", "classic taper", "crew cut"],
        "heart": ["side swept", "fringe", "textured crop", "medium length"],
        "oblong": ["side part", "bangs", "textured layers", "medium length"],
        "diamond": ["side swept", "textured fringe", "medium layers"],
        "triangle": ["voluminous top", "side part", "textured quiff"],
    }
    
    BEARD_STYLES_BY_FACE_SHAPE = {
        "oval": ["stubble", "short beard", "full beard", "goatee"],
        "round": ["chin strap", "goatee", "anchor beard", "extended goatee"],
        "square": ["stubble", "circle beard", "short boxed beard"],
        "heart": ["full beard", "balbo", "anchor", "chin curtain"],
        "oblong": ["mutton chops", "stubble", "short sides long chin"],
        "diamond": ["full beard", "chin strap", "anchor"],
        "triangle": ["stubble", "goatee", "soul patch"],
    }
    
    # For bald/thinning users
    BALD_RECOMMENDATIONS = {
        "beard_priority": ["full beard", "sculpted beard", "goatee", "stubble"],
        "accessory_focus": ["statement glasses", "hats/caps", "scarves"],
        "neckline_emphasis": ["v-neck", "open collar", "crew neck"],
        "grooming_tips": [
            "Keep scalp moisturized and protected from sun",
            "Consider a clean shave for a polished look",
            "Invest in quality sunglasses and eyewear",
            "Well-groomed facial hair adds definition"
        ]
    }
    
    def __init__(self):
        pass
    
    def get_hairstyle_recommendations(self, face_shape: str, 
                                       hair_coverage: str = "full") -> List[str]:
        """Get hairstyle recommendations."""
        if hair_coverage.lower() in ["bald", "thinning"]:
            return ["buzz cut", "clean shave", "very short crop"]
        return self.HAIRSTYLES_BY_FACE_SHAPE.get(
            face_shape.lower(),
            self.HAIRSTYLES_BY_FACE_SHAPE["oval"]
        )
    
    def get_beard_recommendations(self, face_shape: str,
                                   hair_coverage: str = "full") -> List[str]:
        """Get beard style recommendations."""
        if hair_coverage.lower() in ["bald", "thinning"]:
            return self.BALD_RECOMMENDATIONS["beard_priority"]
        return self.BEARD_STYLES_BY_FACE_SHAPE.get(
            face_shape.lower(),
            self.BEARD_STYLES_BY_FACE_SHAPE["oval"]
        )
    
    def get_bald_specific_recommendations(self) -> Dict[str, List[str]]:
        """Get special recommendations for bald/thinning users."""
        return self.BALD_RECOMMENDATIONS


class RecommendationEngine:
    """
    Main recommendation engine that combines all recommendation modules.
    """
    
    def __init__(self):
        self.color_engine = ColorTheoryEngine()
        self.style_engine = StyleMatchingEngine()
        self.grooming_engine = GroomingRecommendationEngine()
    
    def generate_recommendations(
        self,
        fitzpatrick_type: int,
        undertone: str,
        face_shape: str,
        body_type: str = "mesomorph",
        hair_coverage: str = "full",
        gender: str = "male"
    ) -> Dict:
        """
        Generate complete personalized recommendations.
        
        Args:
            fitzpatrick_type: Fitzpatrick scale 1-6
            undertone: "cool", "warm", or "neutral"
            face_shape: Face shape classification
            body_type: Body type classification
            hair_coverage: "full", "thinning", or "bald"
            gender: "male" or "female"
            
        Returns:
            Complete recommendation dictionary
        """
        # Color recommendations
        season, palette = self.color_engine.get_color_recommendations(
            fitzpatrick_type, undertone
        )
        
        # Style recommendations
        necklines = self.style_engine.get_neckline_recommendations(face_shape)
        patterns = self.style_engine.get_pattern_recommendations(body_type)
        fits = self.style_engine.get_fit_recommendations(body_type)
        eyewear = self.style_engine.get_eyewear_recommendations(face_shape)
        
        # Grooming recommendations
        hairstyles = self.grooming_engine.get_hairstyle_recommendations(
            face_shape, hair_coverage
        )
        beard_styles = self.grooming_engine.get_beard_recommendations(
            face_shape, hair_coverage
        ) if gender.lower() == "male" else []
        
        # Build recommendation response
        recommendations = {
            "color_analysis": {
                "season": season.value,
                "best_colors": palette.best_colors,
                "accent_colors": palette.accent_colors,
                "neutral_colors": palette.neutral_colors,
                "avoid_colors": palette.avoid_colors,
                "metal_preference": palette.metal_preference
            },
            "style": {
                "recommended_necklines": necklines,
                "patterns": patterns,
                "fits": fits,
                "eyewear": eyewear
            },
            "grooming": {
                "hairstyles": hairstyles,
                "beard_styles": beard_styles
            },
            "reasoning": {
                "color": f"Your {undertone} undertone and Type {fitzpatrick_type} skin place you in the {season.value.upper()} color season.",
                "necklines": f"Your {face_shape} face shape is complemented by {', '.join(necklines[:3])} necklines.",
                "patterns": f"Your {body_type} body type works well with {', '.join(patterns[:2])}.",
            }
        }
        
        # Add bald-specific recommendations if applicable
        if hair_coverage.lower() in ["bald", "thinning"]:
            recommendations["alternative_styling"] = self.grooming_engine.get_bald_specific_recommendations()
            recommendations["reasoning"]["hair"] = "Focus on complementary accessories and well-groomed facial hair to create a polished look."
        
        return recommendations


# Quick test
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    # Test case: Type III warm, oval face
    result = engine.generate_recommendations(
        fitzpatrick_type=3,
        undertone="warm",
        face_shape="oval",
        body_type="mesomorph",
        hair_coverage="full",
        gender="male"
    )
    
    print("=" * 60)
    print("RECOMMENDATION ENGINE TEST")
    print("=" * 60)
    print(f"Season: {result['color_analysis']['season']}")
    print(f"Best Colors: {result['color_analysis']['best_colors'][:4]}")
    print(f"Necklines: {result['style']['recommended_necklines'][:3]}")
    print(f"Hairstyles: {result['grooming']['hairstyles'][:3]}")
    print(f"\nReasoning: {result['reasoning']['color']}")
    print("=" * 60)
