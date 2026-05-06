import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock LLM Service - Returns sample data without API calls
# Perfect for testing and development

def extract_recipe_data(scraped_text: str) -> dict:
    """Extract structured recipe data from scraped text (MOCK)."""
    try:
        if not scraped_text or len(scraped_text.strip()) < 50:
            raise ValueError("Scraped text is too short or empty")
        
        # Return mock recipe data
        recipe_data = {
            "title": "Delicious Homemade Recipe",
            "cuisine": "American",
            "prep_time": "15 mins",
            "cook_time": "30 mins",
            "total_time": "45 mins",
            "servings": 4,
            "difficulty": "medium",
            "ingredients": [
                {"quantity": "2", "unit": "cups", "item": "all-purpose flour"},
                {"quantity": "1", "unit": "cup", "item": "sugar"},
                {"quantity": "2", "unit": "eggs", "item": "large"},
                {"quantity": "0.5", "unit": "cup", "item": "butter"},
                {"quantity": "1", "unit": "tsp", "item": "vanilla extract"},
                {"quantity": "1.5", "unit": "tsp", "item": "baking powder"},
                {"quantity": "0.25", "unit": "tsp", "item": "salt"}
            ],
            "instructions": [
                "Preheat oven to 350°F (175°C).",
                "In a large bowl, cream together butter and sugar until light and fluffy.",
                "Beat in eggs one at a time, then stir in vanilla extract.",
                "In a separate bowl, whisk together flour, baking powder, and salt.",
                "Gradually blend the dry ingredients into the creamed mixture.",
                "Pour batter into a greased 9x13 inch pan.",
                "Bake for 30 minutes or until a toothpick inserted in center comes out clean.",
                "Cool in pan for 10 minutes before serving."
            ]
        }
        
        logger.info(f"Mock extraction returned recipe: {recipe_data['title']}")
        return recipe_data
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise ValueError(f"Recipe extraction failed: {str(e)}")

def get_nutrition_estimate(recipe_data: dict) -> dict:
    """Generate nutritional estimates (MOCK)."""
    try:
        # Return mock nutrition data
        nutrition = {
            "calories": "245",
            "protein": "4g",
            "carbs": "38g",
            "fat": "8g"
        }
        logger.info(f"Mock nutrition estimate generated")
        return nutrition
    except Exception as e:
        logger.error(f"Nutrition estimation error: {str(e)}")
        return {"calories": "0", "protein": "0g", "carbs": "0g", "fat": "0g"}

def get_substitutions(recipe_data: dict) -> list:
    """Generate ingredient substitutions (MOCK)."""
    try:
        # Return mock substitutions
        substitutions = [
            "Use almond flour instead of all-purpose flour for a gluten-free version",
            "Replace butter with coconut oil for a dairy-free option",
            "Substitute eggs with applesauce (1:1 ratio) for a vegan alternative"
        ]
        logger.info(f"Mock substitutions generated")
        return substitutions
    except Exception as e:
        logger.error(f"Substitutions error: {str(e)}")
        return [
            "Use dairy-free butter as alternative",
            "Try plant-based milk substitutes",
            "Use egg replacers for vegan baking"
        ]

def get_shopping_list(recipe_data: dict) -> dict:
    """Generate categorized shopping list (MOCK)."""
    try:
        # Return mock shopping list
        shopping_list = {
            "dairy": ["1 cup butter", "2 eggs"],
            "produce": [],
            "pantry": ["2 cups flour", "1 cup sugar", "1.5 tsp baking powder", "0.25 tsp salt"],
            "spices": ["1 tsp vanilla extract"],
            "bakery": [],
            "frozen": [],
            "meat": [],
            "other": []
        }
        logger.info(f"Mock shopping list generated")
        return shopping_list
    except Exception as e:
        logger.error(f"Shopping list error: {str(e)}")
        return {
            "dairy": [],
            "produce": [],
            "pantry": [],
            "other": []
        }

def get_related_recipes(recipe_data: dict) -> list:
    """Get related recipe suggestions (MOCK)."""
    try:
        # Return mock related recipes
        related = [
            "Chocolate Chip Cookies",
            "Vanilla Frosting",
            "Whipped Cream Topping"
        ]
        logger.info(f"Mock related recipes generated")
        return related
    except Exception as e:
        logger.error(f"Related recipes error: {str(e)}")
        return [
            "Similar Dessert Recipe",
            "Complementary Side Dish",
            "Popular Variation"
        ]

def generate_meal_plan_shopping_list(recipes_data: list) -> dict:
    """Generate merged shopping list for multiple recipes (MOCK)."""
    try:
        # Return mock merged shopping list
        shopping_list = {
            "dairy": ["2 cups butter", "4 eggs"],
            "produce": ["2 onions", "3 cloves garlic"],
            "pantry": ["4 cups flour", "2 cups sugar", "3 tsp baking powder", "0.5 tsp salt"],
            "spices": ["2 tsp vanilla extract", "1 tsp cinnamon"],
            "bakery": [],
            "frozen": [],
            "meat": [],
            "other": []
        }
        logger.info(f"Mock meal plan shopping list generated for {len(recipes_data)} recipes")
        return shopping_list
    except Exception as e:
        logger.error(f"Meal plan shopping list error: {str(e)}")
        return {}
