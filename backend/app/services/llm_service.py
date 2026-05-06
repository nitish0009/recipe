from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json
import logging
from ..config import GOOGLE_API_KEY
from .. import prompts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLMs with different temperatures
llm_extraction = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.1
)

llm_creative = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

def extract_recipe_data(scraped_text: str) -> dict:
    """Extract structured recipe data from scraped text."""
    try:
        if not scraped_text or len(scraped_text.strip()) < 50:
            raise ValueError("Scraped text is too short or empty")
        
        prompt_text = prompts.extraction_prompt.format(scraped_text=scraped_text[:5000])
        result = llm_extraction.invoke(prompt_text)
        
        # Clean up JSON response (remove markdown, extra text)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        recipe_data = json.loads(result)
        
        # Validate required fields
        required_fields = ["title", "cuisine", "prep_time", "cook_time", "total_time", 
                          "servings", "difficulty", "ingredients", "instructions"]
        for field in required_fields:
            if field not in recipe_data:
                recipe_data[field] = None
        
        return recipe_data
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise ValueError("Failed to parse extraction result - invalid JSON format")
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise ValueError(f"Recipe extraction failed: {str(e)}")

def get_nutrition_estimate(recipe_data: dict) -> dict:
    """Generate nutritional estimates based on recipe data."""
    try:
        ingredients_text = str(recipe_data.get("ingredients", []))
        prompt_text = prompts.nutrition_prompt.format(ingredients=ingredients_text)
        result = llm_extraction.invoke(prompt_text)
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        nutrition = json.loads(result)
        return nutrition
    except Exception as e:
        logger.error(f"Nutrition estimation error: {str(e)}")
        return {"calories": "0", "protein": "0g", "carbs": "0g", "fat": "0g"}

def get_substitutions(recipe_data: dict) -> list:
    """Generate ingredient substitutions."""
    try:
        ingredients_text = str(recipe_data.get("ingredients", []))
        prompt_text = prompts.substitutions_prompt.format(ingredients=ingredients_text)
        result = llm_creative.invoke(prompt_text)
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        substitutions = json.loads(result)
        if isinstance(substitutions, dict) and "substitutions" in substitutions:
            return substitutions["substitutions"][:3]
        return substitutions[:3] if isinstance(substitutions, list) else []
    except Exception as e:
        logger.error(f"Substitutions error: {str(e)}")
        return [
            {"type": "Dairy-Free", "options": "Use plant-based milk and butter alternatives"},
            {"type": "Vegan", "options": "Replace eggs with flax eggs and dairy with plant-based options"},
            {"type": "Gluten-Free", "options": "Use gluten-free flour blends"}
        ]

def get_shopping_list(recipe_data: dict) -> dict:
    """Generate categorized shopping list."""
    try:
        ingredients_text = str(recipe_data.get("ingredients", []))
        prompt_text = prompts.shopping_list_prompt.format(ingredients=ingredients_text)
        result = llm_extraction.invoke(prompt_text)
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        shopping_list = json.loads(result)
        if isinstance(shopping_list, dict):
            return shopping_list
        return {}
    except Exception as e:
        logger.error(f"Shopping list error: {str(e)}")
        return {
            "produce": [],
            "dairy": [],
            "pantry": [],
            "other": []
        }

def get_related_recipes(recipe_data: dict) -> list:
    """Get related recipe suggestions."""
    try:
        title = recipe_data.get("title", "Recipe")
        cuisine = recipe_data.get("cuisine", "")
        prompt_text = prompts.related_recipes_prompt.format(
            title=title,
            cuisine=cuisine
        )
        result = llm_creative.invoke(prompt_text)
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        related = json.loads(result)
        if isinstance(related, dict) and "recipes" in related:
            return related["recipes"][:3]
        return related[:3] if isinstance(related, list) else []
    except Exception as e:
        logger.error(f"Related recipes error: {str(e)}")
        return [
            {"name": "Appetizer", "description": "Perfect starter for this meal"},
            {"name": "Side Dish", "description": "Complements well with this dish"},
            {"name": "Dessert", "description": "Great finale to this meal"}
        ]

def generate_meal_plan_shopping_list(recipes_data: list) -> dict:
    """Generate merged shopping list for multiple recipes."""
    try:
        all_ingredients = []
        for recipe in recipes_data:
            ingredients = recipe.get("ingredients", [])
            if isinstance(ingredients, list):
                all_ingredients.extend(ingredients)
        
        ingredients_text = str(all_ingredients)
        prompt_text = prompts.meal_plan_shopping_prompt.format(ingredients=ingredients_text)
        result = llm_extraction.invoke(prompt_text)
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        shopping_list = json.loads(result)
        return shopping_list if isinstance(shopping_list, dict) else {}
    except Exception as e:
        logger.error(f"Meal plan shopping list error: {str(e)}")
        return {}
