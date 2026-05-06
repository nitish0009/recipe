from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
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
        
        chain = LLMChain(llm=llm_extraction, prompt=prompts.extraction_prompt)
        result = chain.run(scraped_text=scraped_text[:5000])  # Limit text length
        
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
        chain = LLMChain(llm=llm_extraction, prompt=prompts.nutrition_prompt)
        result = chain.run(recipe_data=json.dumps(recipe_data))
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        nutrition = json.loads(result)
        
        # Validate nutrition data
        if not all(k in nutrition for k in ["calories", "protein", "carbs", "fat"]):
            return {
                "calories": 0,
                "protein": "0g",
                "carbs": "0g",
                "fat": "0g"
            }
        return nutrition
    except Exception as e:
        logger.error(f"Nutrition estimation error: {str(e)}")
        return {
            "calories": 0,
            "protein": "0g",
            "carbs": "0g",
            "fat": "0g"
        }

def get_substitutions(recipe_data: dict) -> list:
    """Generate ingredient substitution suggestions."""
    try:
        chain = LLMChain(llm=llm_creative, prompt=prompts.substitutions_prompt)
        result = chain.run(recipe_data=json.dumps(recipe_data))
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        substitutions = json.loads(result)
        
        # Ensure it's a list
        if isinstance(substitutions, list):
            return substitutions[:3]  # Limit to 3 suggestions
        return []
    except Exception as e:
        logger.error(f"Substitutions generation error: {str(e)}")
        return [
            "Adjust cooking time or temperature for dietary preferences",
            "Try alternative protein sources for dietary needs",
            "Use herbs and spices as flavor alternatives"
        ]

def get_shopping_list(recipe_data: dict) -> dict:
    """Generate categorized shopping list."""
    try:
        chain = LLMChain(llm=llm_extraction, prompt=prompts.shopping_list_prompt)
        result = chain.run(recipe_data=json.dumps(recipe_data))
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        shopping_list = json.loads(result)
        
        # Validate it's a dict
        if isinstance(shopping_list, dict):
            return shopping_list
        return {"other": []}
    except Exception as e:
        logger.error(f"Shopping list generation error: {str(e)}")
        # Fallback: group ingredients by basic categories
        fallback = {
            "produce": [],
            "dairy": [],
            "pantry": [],
            "other": []
        }
        if "ingredients" in recipe_data and isinstance(recipe_data["ingredients"], list):
            for ing in recipe_data["ingredients"][:5]:  # Limit to 5
                if isinstance(ing, dict) and "item" in ing:
                    fallback["other"].append(ing["item"])
        return fallback

def get_related_recipes(recipe_data: dict) -> list:
    """Generate suggestions for related recipes."""
    try:
        chain = LLMChain(llm=llm_creative, prompt=prompts.related_recipes_prompt)
        result = chain.run(recipe_data=json.dumps(recipe_data))
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        related = json.loads(result)
        
        # Ensure it's a list
        if isinstance(related, list):
            return related[:3]  # Limit to 3 suggestions
        return []
    except Exception as e:
        logger.error(f"Related recipes generation error: {str(e)}")
        return [
            "Complementary side dish",
            "Matching appetizer",
            "Suitable dessert"
        ]

def generate_meal_plan_shopping_list(recipes_data: list) -> dict:
    """Generate combined shopping list for multiple recipes with merged quantities."""
    try:
        chain = LLMChain(llm=llm_extraction, prompt=prompts.meal_plan_shopping_prompt)
        result = chain.run(recipes_data=json.dumps(recipes_data))
        
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        shopping_list = json.loads(result)
        
        # Validate it's a dict
        if isinstance(shopping_list, dict):
            return shopping_list
        return {"other": []}
    except Exception as e:
        logger.error(f"Meal plan shopping list error: {str(e)}")
        return {"other": ["Unable to generate combined shopping list"]}
        return ["Unable to generate suggestions"]