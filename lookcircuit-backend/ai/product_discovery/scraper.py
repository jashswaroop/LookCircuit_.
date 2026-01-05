"""
Product Discovery Web Scraper
Aggregates fashion products from e-commerce platforms.

Note: This is for educational/hackathon purposes only.
For production use, consider official APIs or affiliate partnerships.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
import hashlib
import re


class ProductCategory(Enum):
    """Product categories for discovery."""
    SHIRTS = "shirts"
    TSHIRTS = "t-shirts"
    TROUSERS = "trousers"
    JEANS = "jeans"
    JACKETS = "jackets"
    SUITS = "suits"
    DRESSES = "dresses"
    FOOTWEAR = "footwear"
    ACCESSORIES = "accessories"
    EYEWEAR = "eyewear"


@dataclass
class Product:
    """Represents a fashion product."""
    id: str
    name: str
    brand: str
    price: float
    currency: str
    image_url: str
    product_url: str
    category: str
    colors: List[str]
    source: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class MockProductDatabase:
    """
    Mock product database for development/testing.
    In production, this would be replaced with actual web scraping.
    """
    
    MOCK_PRODUCTS = {
        ProductCategory.SHIRTS: [
            Product(
                id="shirt_001",
                name="Classic Oxford Shirt",
                brand="Arrow",
                price=1499.0,
                currency="INR",
                image_url="https://example.com/images/oxford_shirt.jpg",
                product_url="https://example.com/products/oxford_shirt",
                category="shirts",
                colors=["#FFFFFF", "#87CEEB", "#E6E6FA"],
                source="mock"
            ),
            Product(
                id="shirt_002", 
                name="Slim Fit Formal Shirt",
                brand="Van Heusen",
                price=1999.0,
                currency="INR",
                image_url="https://example.com/images/formal_shirt.jpg",
                product_url="https://example.com/products/formal_shirt",
                category="shirts",
                colors=["#000080", "#FFFFFF", "#D3D3D3"],
                source="mock"
            ),
        ],
        ProductCategory.TSHIRTS: [
            Product(
                id="tshirt_001",
                name="Round Neck Cotton T-Shirt",
                brand="Jockey",
                price=699.0,
                currency="INR",
                image_url="https://example.com/images/cotton_tshirt.jpg",
                product_url="https://example.com/products/cotton_tshirt",
                category="t-shirts",
                colors=["#000000", "#FFFFFF", "#808080", "#000080"],
                source="mock"
            ),
        ],
        ProductCategory.TROUSERS: [
            Product(
                id="trouser_001",
                name="Formal Pleated Trousers",
                brand="Raymond",
                price=2499.0,
                currency="INR",
                image_url="https://example.com/images/formal_trousers.jpg",
                product_url="https://example.com/products/formal_trousers",
                category="trousers",
                colors=["#2F4F4F", "#000000", "#808080"],
                source="mock"
            ),
        ],
        ProductCategory.FOOTWEAR: [
            Product(
                id="shoe_001",
                name="Leather Oxford Shoes",
                brand="Hush Puppies",
                price=4999.0,
                currency="INR",
                image_url="https://example.com/images/oxford_shoes.jpg",
                product_url="https://example.com/products/oxford_shoes",
                category="footwear",
                colors=["#8B4513", "#000000"],
                source="mock"
            ),
        ],
        ProductCategory.EYEWEAR: [
            Product(
                id="glasses_001",
                name="Aviator Sunglasses",
                brand="Ray-Ban",
                price=7990.0,
                currency="INR",
                image_url="https://example.com/images/aviator.jpg",
                product_url="https://example.com/products/aviator",
                category="eyewear",
                colors=["#FFD700", "#C0C0C0"],
                source="mock"
            ),
        ],
    }
    
    def get_products_by_category(self, category: ProductCategory) -> List[Product]:
        """Get all products in a category."""
        return self.MOCK_PRODUCTS.get(category, [])
    
    def get_products_by_color(self, target_color: str, tolerance: int = 50) -> List[Product]:
        """Find products matching a specific color."""
        matching = []
        target_rgb = self._hex_to_rgb(target_color)
        
        for products in self.MOCK_PRODUCTS.values():
            for product in products:
                for color in product.colors:
                    prod_rgb = self._hex_to_rgb(color)
                    if self._color_distance(target_rgb, prod_rgb) < tolerance:
                        matching.append(product)
                        break
        
        return matching
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _color_distance(self, c1: tuple, c2: tuple) -> float:
        """Calculate Euclidean distance between two RGB colors."""
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5


class ProductDiscoveryEngine:
    """
    Main product discovery engine.
    Finds products based on user's style recommendations.
    """
    
    def __init__(self):
        self.mock_db = MockProductDatabase()
    
    def discover_products(
        self,
        color_palette: List[str],
        categories: List[str],
        occasion: Optional[str] = None,
        max_results: int = 20
    ) -> Dict[str, List[Dict]]:
        """
        Discover products matching user preferences.
        
        Args:
            color_palette: List of recommended colors (hex)
            categories: Product categories to search
            occasion: Optional occasion filter
            max_results: Maximum products per category
            
        Returns:
            Dict mapping category to list of products
        """
        results = {}
        
        for cat_name in categories:
            try:
                category = ProductCategory(cat_name.lower().replace(" ", "-"))
            except ValueError:
                continue
            
            products = self.mock_db.get_products_by_category(category)
            
            # Filter by color palette
            color_matched = []
            for product in products:
                for pcolor in product.colors:
                    if pcolor in color_palette:
                        color_matched.append(product)
                        break
            
            # Use all products if no color matches (for demo)
            final_products = color_matched if color_matched else products
            
            results[cat_name] = [p.to_dict() for p in final_products[:max_results]]
        
        return results
    
    def get_outfit_products(
        self,
        outfit_recommendation: Dict,
        color_palette: List[str]
    ) -> Dict[str, List[Dict]]:
        """
        Find products matching an outfit recommendation.
        
        Args:
            outfit_recommendation: Outfit from occasion styling engine
            color_palette: User's color palette
            
        Returns:
            Products organized by outfit component
        """
        categories = []
        
        # Map outfit components to categories
        if 'top' in outfit_recommendation:
            top_type = outfit_recommendation['top'].get('type', '').lower()
            if 'shirt' in top_type:
                categories.append('shirts')
            elif 't-shirt' in top_type or 'tee' in top_type:
                categories.append('t-shirts')
        
        if 'bottom' in outfit_recommendation:
            bottom_type = outfit_recommendation['bottom'].get('type', '').lower()
            if 'jeans' in bottom_type:
                categories.append('jeans')
            elif 'trouser' in bottom_type or 'pant' in bottom_type:
                categories.append('trousers')
        
        if 'footwear' in outfit_recommendation:
            categories.append('footwear')
        
        return self.discover_products(color_palette, categories)


# Quick test
if __name__ == "__main__":
    engine = ProductDiscoveryEngine()
    
    # Test product discovery
    results = engine.discover_products(
        color_palette=["#000080", "#FFFFFF", "#808080"],
        categories=["shirts", "footwear", "eyewear"]
    )
    
    print("=" * 60)
    print("PRODUCT DISCOVERY TEST")
    print("=" * 60)
    for cat, products in results.items():
        print(f"\n{cat.upper()}:")
        for p in products:
            print(f"  - {p['name']} ({p['brand']}) - {p['currency']} {p['price']}")
    print("=" * 60)
