"""
Occasion-Based Styling Recommendations
Provides complete outfit suggestions for different occasions.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class OccasionOutfit:
    """Complete outfit recommendation for an occasion."""
    occasion: str
    top: Dict[str, str]
    bottom: Dict[str, str]  
    footwear: Dict[str, str]
    accessories: List[str]
    grooming_notes: str
    color_suggestions: List[str]


class OccasionStylingEngine:
    """
    Generates complete outfit recommendations for various occasions.
    Takes into account user's color season and style preferences.
    """
    
    # Base outfit templates by occasion
    OCCASION_TEMPLATES = {
        "casual": {
            "male": {
                "tops": ["t-shirt", "polo", "casual shirt", "henley"],
                "bottoms": ["jeans", "chinos", "shorts"],
                "footwear": ["sneakers", "loafers", "sandals"],
                "accessories": ["watch", "sunglasses", "cap"],
            },
            "female": {
                "tops": ["blouse", "t-shirt", "tank top", "crop top"],
                "bottoms": ["jeans", "skirt", "shorts", "culottes"],
                "footwear": ["sneakers", "flats", "sandals"],
                "accessories": ["tote bag", "sunglasses", "minimal jewelry"],
            }
        },
        "formal": {
            "male": {
                "tops": ["dress shirt", "blazer", "suit jacket"],
                "bottoms": ["dress pants", "suit trousers"],
                "footwear": ["oxford shoes", "derby shoes", "loafers"],
                "accessories": ["tie", "pocket square", "cufflinks", "dress watch"],
            },
            "female": {
                "tops": ["blouse", "blazer", "dress shirt"],
                "bottoms": ["dress pants", "pencil skirt", "formal dress"],
                "footwear": ["heels", "pumps", "loafers"],
                "accessories": ["structured bag", "pearl jewelry", "elegant watch"],
            }
        },
        "business_casual": {
            "male": {
                "tops": ["button-down shirt", "polo", "sweater", "light blazer"],
                "bottoms": ["chinos", "dress pants", "dark jeans"],
                "footwear": ["loafers", "brogues", "clean sneakers"],
                "accessories": ["leather belt", "watch", "minimal jewelry"],
            },
            "female": {
                "tops": ["blouse", "cardigan", "blazer", "knit top"],
                "bottoms": ["dress pants", "midi skirt", "tailored jeans"],
                "footwear": ["flats", "low heels", "loafers"],
                "accessories": ["tote bag", "simple jewelry", "scarf"],
            }
        },
        "date_night": {
            "male": {
                "tops": ["fitted shirt", "smart casual blazer", "dark sweater"],
                "bottoms": ["dark jeans", "chinos", "smart trousers"],
                "footwear": ["chelsea boots", "loafers", "clean sneakers"],
                "accessories": ["nice watch", "subtle cologne", "leather belt"],
            },
            "female": {
                "tops": ["elegant blouse", "bodysuit", "dressy top"],
                "bottoms": ["fitted jeans", "skirt", "dress"],
                "footwear": ["heels", "ankle boots", "elegant flats"],
                "accessories": ["statement jewelry", "clutch", "light fragrance"],
            }
        },
        "fitness": {
            "male": {
                "tops": ["performance t-shirt", "tank top", "compression shirt"],
                "bottoms": ["shorts", "joggers", "compression pants"],
                "footwear": ["running shoes", "training shoes"],
                "accessories": ["fitness tracker", "sweatband", "gym bag"],
            },
            "female": {
                "tops": ["sports bra", "tank top", "workout tee"],
                "bottoms": ["leggings", "shorts", "joggers"],
                "footwear": ["running shoes", "cross-trainers"],
                "accessories": ["hair tie", "fitness tracker", "gym bag"],
            }
        },
        "festive": {
            "male": {
                "tops": ["kurta", "sherwani", "bandhgala", "ethnic jacket"],
                "bottoms": ["churidar", "dhoti pants", "formal trousers"],
                "footwear": ["mojari", "juttis", "formal leather shoes"],
                "accessories": ["dupatta/stole", "brooch", "ethnic jewelry"],
            },
            "female": {
                "tops": ["saree blouse", "lehenga choli", "anarkali"],
                "bottoms": ["saree", "lehenga", "palazzo"],
                "footwear": ["heels", "juttis", "embellished sandals"],
                "accessories": ["statement jewelry", "clutch", "bindi", "bangles"],
            }
        },
        "interview": {
            "male": {
                "tops": ["white/light dress shirt", "conservative blazer"],
                "bottoms": ["dark dress pants", "suit trousers"],
                "footwear": ["oxford shoes", "polished leather shoes"],
                "accessories": ["conservative tie", "minimal watch", "leather portfolio"],
            },
            "female": {
                "tops": ["professional blouse", "blazer"],
                "bottoms": ["dress pants", "pencil skirt", "professional dress"],
                "footwear": ["closed-toe heels", "flats"],
                "accessories": ["minimal jewelry", "professional bag", "portfolio"],
            }
        },
    }
    
    def __init__(self):
        pass
    
    def get_occasion_outfit(
        self,
        occasion: str,
        gender: str,
        color_palette: List[str],
        face_shape: str = "oval"
    ) -> OccasionOutfit:
        """
        Generate complete outfit recommendation for an occasion.
        
        Args:
            occasion: Type of occasion
            gender: "male" or "female"
            color_palette: User's recommended colors
            face_shape: For accessory recommendations
            
        Returns:
            OccasionOutfit with complete recommendations
        """
        occasion_key = occasion.lower().replace(" ", "_")
        gender_key = gender.lower()
        
        if occasion_key not in self.OCCASION_TEMPLATES:
            occasion_key = "casual"
        
        template = self.OCCASION_TEMPLATES[occasion_key][gender_key]
        
        # Select primary and accent colors from palette
        primary_colors = color_palette[:3] if color_palette else ["#000000", "#FFFFFF"]
        
        return OccasionOutfit(
            occasion=occasion,
            top={
                "type": template["tops"][0],
                "alternatives": template["tops"][1:],
                "color_suggestion": primary_colors[0] if primary_colors else "#FFFFFF"
            },
            bottom={
                "type": template["bottoms"][0],
                "alternatives": template["bottoms"][1:],
                "color_suggestion": primary_colors[1] if len(primary_colors) > 1 else "#000000"
            },
            footwear={
                "type": template["footwear"][0],
                "alternatives": template["footwear"][1:],
                "color_suggestion": "neutral"
            },
            accessories=template["accessories"],
            grooming_notes=self._get_grooming_notes(occasion_key, gender_key),
            color_suggestions=primary_colors
        )
    
    def _get_grooming_notes(self, occasion: str, gender: str) -> str:
        """Get grooming tips for the occasion."""
        notes = {
            "formal": "Clean-shaven or well-groomed facial hair. Neat hairstyle.",
            "casual": "Relaxed grooming, but maintain cleanliness.",
            "interview": "Conservative, polished appearance. Minimal fragrance.",
            "date_night": "Well-groomed, subtle fragrance, attention to detail.",
            "fitness": "Hair tied back if long, minimal products.",
            "festive": "Traditional grooming appropriate for the occasion.",
            "business_casual": "Professional but relaxed grooming.",
        }
        return notes.get(occasion, "Maintain a clean, well-groomed appearance.")
    
    def get_all_occasions(self) -> List[str]:
        """Get list of all supported occasions."""
        return list(self.OCCASION_TEMPLATES.keys())


# Quick test
if __name__ == "__main__":
    engine = OccasionStylingEngine()
    
    outfit = engine.get_occasion_outfit(
        occasion="interview",
        gender="male",
        color_palette=["#000080", "#FFFFFF", "#808080"],
        face_shape="oval"
    )
    
    print(f"Occasion: {outfit.occasion}")
    print(f"Top: {outfit.top}")
    print(f"Bottom: {outfit.bottom}")
    print(f"Footwear: {outfit.footwear}")
    print(f"Accessories: {outfit.accessories}")
    print(f"Grooming: {outfit.grooming_notes}")
