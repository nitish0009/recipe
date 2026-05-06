from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models import Recipe
from ..services.scraper import scrape_recipe
from ..services.llm_service import (
    extract_recipe_data,
    get_nutrition_estimate,
    get_substitutions,
    get_shopping_list,
    get_related_recipes
)
from pydantic import BaseModel
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class RecipeURL(BaseModel):
    url: str

class RecipeResponse(BaseModel):
    id: int
    title: str
    cuisine: str
    difficulty: str
    created_at: Optional[str] = None

@router.post("/extract-recipe")
def extract_recipe(recipe_url: RecipeURL, db: Session = Depends(get_db)):
    """Extract recipe from URL and store in database."""
    try:
        # Validate URL
        if not recipe_url.url or not recipe_url.url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format")
        
        # Check if recipe already exists
        existing = db.query(Recipe).filter(Recipe.url == recipe_url.url).first()
        if existing:
            logger.info(f"Recipe already exists: {existing.id}")
            response = existing.__dict__
            response['_sa_instance_state'] = None  # Remove SQLAlchemy state
            return response
        
        logger.info(f"Scraping URL: {recipe_url.url}")
        # Scrape
        scraped_text = scrape_recipe(recipe_url.url)
        
        logger.info("Extracting recipe data...")
        # Extract core recipe data
        recipe_data = extract_recipe_data(scraped_text)
        
        if not recipe_data.get("title"):
            raise ValueError("Could not extract recipe title from page")
        
        logger.info("Generating nutrition, substitutions, shopping list, and related recipes...")
        # Enrich with additional data
        recipe_data["nutrition_estimate"] = get_nutrition_estimate(recipe_data)
        recipe_data["substitutions"] = get_substitutions(recipe_data)
        recipe_data["shopping_list"] = get_shopping_list(recipe_data)
        recipe_data["related_recipes"] = get_related_recipes(recipe_data)
        recipe_data["url"] = recipe_url.url
        
        # Create database record
        recipe = Recipe(**recipe_data)
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        
        logger.info(f"Recipe saved with ID: {recipe.id}")
        response = recipe.__dict__
        response.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
        return response
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to extract recipe: {str(e)}")

@router.get("/recipes")
def get_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    difficulty: Optional[str] = None,
    cuisine: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of all recipes with optional filtering."""
    try:
        query = db.query(Recipe).order_by(desc(Recipe.created_at))
        
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)
        
        if cuisine:
            query = query.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))
        
        total = query.count()
        recipes = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "recipes": [
                {
                    "id": r.id,
                    "title": r.title,
                    "cuisine": r.cuisine,
                    "difficulty": r.difficulty,
                    "prep_time": r.prep_time,
                    "cook_time": r.cook_time,
                    "servings": r.servings,
                    "created_at": r.created_at.isoformat() if r.created_at else None
                }
                for r in recipes
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching recipes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch recipes")

@router.get("/recipes/{recipe_id}")
def get_recipe_details(recipe_id: int, db: Session = Depends(get_db)):
    """Get full details of a specific recipe."""
    try:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        response = recipe.__dict__
        response.pop('_sa_instance_state', None)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching recipe: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch recipe")

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe from the database."""
    try:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        db.delete(recipe)
        db.commit()
        
        logger.info(f"Recipe {recipe_id} deleted")
        return {"message": "Recipe deleted successfully", "id": recipe_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting recipe: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete recipe")

@router.get("/recipes/search/by-title")
def search_recipes(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Search recipes by title."""
    try:
        recipes = db.query(Recipe).filter(Recipe.title.ilike(f"%{q}%")).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "cuisine": r.cuisine,
                "difficulty": r.difficulty
            }
            for r in recipes
        ]
    except Exception as e:
        logger.error(f"Error searching recipes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search recipes")