from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Recipe
from ..services.llm_service import generate_meal_plan_shopping_list
from pydantic import BaseModel
from typing import List
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class MealPlan(BaseModel):
    recipe_ids: List[int]

class MealPlanResponse(BaseModel):
    recipes: List[dict]
    shopping_list: dict

@router.post("/meal-plan")
def create_meal_plan(meal_plan: MealPlan, db: Session = Depends(get_db)):
    """Generate a combined shopping list for multiple recipes."""
    try:
        if not meal_plan.recipe_ids:
            raise ValueError("At least one recipe is required")
        
        if len(meal_plan.recipe_ids) > 10:
            raise ValueError("Maximum 10 recipes allowed in a meal plan")
        
        # Fetch recipes
        recipes = db.query(Recipe).filter(Recipe.id.in_(meal_plan.recipe_ids)).all()
        
        if len(recipes) != len(meal_plan.recipe_ids):
            raise HTTPException(status_code=404, detail="Some recipes not found")
        
        # Prepare recipes data for LLM
        recipes_data = [
            {
                "title": r.title,
                "ingredients": r.ingredients,
                "shopping_list": r.shopping_list
            }
            for r in recipes
        ]
        
        logger.info(f"Generating combined shopping list for {len(recipes)} recipes")
        
        # Generate combined shopping list using LLM
        combined_shopping_list = generate_meal_plan_shopping_list(recipes_data)
        
        # Prepare response
        response = {
            "recipes": [
                {
                    "id": r.id,
                    "title": r.title,
                    "cuisine": r.cuisine,
                    "difficulty": r.difficulty,
                    "prep_time": r.prep_time,
                    "cook_time": r.cook_time,
                    "servings": r.servings
                }
                for r in recipes
            ],
            "shopping_list": combined_shopping_list
        }
        
        return response
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Meal plan generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate meal plan: {str(e)}")

@router.get("/meal-plan/suggestions")
def get_meal_plan_suggestions(db: Session = Depends(get_db)):
    """Get suggestions for meal planning based on available recipes."""
    try:
        recipes = db.query(Recipe).all()
        
        if len(recipes) < 3:
            return {
                "message": "Add more recipes to get meal planning suggestions",
                "recipes_available": len(recipes)
            }
        
        # Group by cuisine for suggestions
        cuisine_groups = {}
        for recipe in recipes:
            cuisine = recipe.cuisine or "Other"
            if cuisine not in cuisine_groups:
                cuisine_groups[cuisine] = []
            cuisine_groups[cuisine].append({
                "id": recipe.id,
                "title": recipe.title,
                "prep_time": recipe.prep_time,
                "cook_time": recipe.cook_time
            })
        
        return {
            "total_recipes": len(recipes),
            "by_cuisine": cuisine_groups,
            "suggestions": [
                "Try combining 2-3 recipes from the same cuisine",
                "Mix different cuisines for a diverse meal plan",
                "Consider prep time when planning meals"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get suggestions")