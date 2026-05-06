import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RecipeCard from '../components/RecipeCard';
import '../styles/MealPlanner.css';

function MealPlanner() {
  const [recipes, setRecipes] = useState([]);
  const [selectedRecipes, setSelectedRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [mealPlan, setMealPlan] = useState(null);
  const [generatingPlan, setGeneratingPlan] = useState(false);
  const [showRecipeDetails, setShowRecipeDetails] = useState(null);

  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('http://localhost:8001/api/recipes');
      setRecipes(response.data.recipes || response.data);
    } catch (err) {
      setError('Failed to fetch recipes. Make sure the backend is running.');
      console.error('Error fetching recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleRecipeSelection = (id) => {
    setSelectedRecipes(prev => 
      prev.includes(id) 
        ? prev.filter(rid => rid !== id)
        : [...prev, id]
    );
  };

  const generateMealPlan = async () => {
    if (selectedRecipes.length < 2) {
      setError('Select at least 2 recipes to create a meal plan');
      return;
    }

    if (selectedRecipes.length > 10) {
      setError('Maximum 10 recipes per meal plan');
      return;
    }

    setGeneratingPlan(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:8001/api/meal-plan', {
        recipe_ids: selectedRecipes
      });
      setMealPlan(response.data);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate meal plan');
      console.error('Error generating meal plan:', err);
    } finally {
      setGeneratingPlan(false);
    }
  };

  const clearSelection = () => {
    setSelectedRecipes([]);
    setMealPlan(null);
    setError('');
  };

  const exportShoppingList = () => {
    if (!mealPlan) return;

    let text = 'MEAL PLAN SHOPPING LIST\n';
    text += '='.repeat(50) + '\n\n';

    text += 'RECIPES:\n';
    mealPlan.recipes.forEach(recipe => {
      text += `- ${recipe.title} (${recipe.cuisine}, ${recipe.difficulty})\n`;
    });

    text += '\n' + '='.repeat(50) + '\nSHOPPING LIST:\n';
    text += '='.repeat(50) + '\n\n';

    Object.entries(mealPlan.shopping_list).forEach(([category, items]) => {
      text += `${category.toUpperCase()}:\n`;
      if (Array.isArray(items)) {
        items.forEach(item => text += `  [ ] ${item}\n`);
      }
      text += '\n';
    });

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', 'meal_plan_shopping_list.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (loading) {
    return <div className="meal-planner-container"><div className="loading">Loading recipes...</div></div>;
  }

  if (recipes.length === 0) {
    return (
      <div className="meal-planner-container">
        <div className="empty-state">
          <h2>No Recipes Available</h2>
          <p>Go to the "Extract Recipe" tab to add recipes first!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="meal-planner-container">
      <h2>Meal Planner</h2>
      <p className="subtitle">Select 2-10 recipes to create an optimized shopping list</p>

      {error && <div className="alert alert-error"><strong>Error:</strong> {error}</div>}

      {/* Meal Plan Results */}
      {mealPlan && (
        <div className="meal-plan-results">
          <div className="results-header">
            <h3>Your Meal Plan</h3>
            <button className="btn-export" onClick={exportShoppingList}>
              📥 Download Shopping List
            </button>
          </div>

          {/* Selected Recipes */}
          <div className="plan-recipes">
            <h4>Selected Recipes ({mealPlan.recipes.length})</h4>
            <div className="recipes-grid">
              {mealPlan.recipes.map(recipe => (
                <div key={recipe.id} className="plan-recipe-card">
                  <h5>{recipe.title}</h5>
                  <p><span className="label">Cuisine:</span> {recipe.cuisine}</p>
                  <p><span className="label">Time:</span> {recipe.prep_time} + {recipe.cook_time}</p>
                  <p><span className="label">Servings:</span> {recipe.servings}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Combined Shopping List */}
          <div className="combined-shopping-list">
            <h4>Combined Shopping List</h4>
            <div className="shopping-categories">
              {Object.entries(mealPlan.shopping_list).map(([category, items]) => (
                <div key={category} className="shopping-category">
                  <h5>{category.charAt(0).toUpperCase() + category.slice(1)}</h5>
                  <ul>
                    {Array.isArray(items) && items.map((item, idx) => (
                      <li key={idx}>
                        <input type="checkbox" id={`item-${idx}`} />
                        <label htmlFor={`item-${idx}`}>{item}</label>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          <button className="btn-new-plan" onClick={clearSelection}>
            Plan Another Meal
          </button>
        </div>
      )}

      {/* Recipe Selection */}
      {!mealPlan && (
        <div className="recipe-selection">
          <div className="selection-controls">
            <div className="selection-info">
              <strong>Selected: {selectedRecipes.length} recipes</strong>
              {selectedRecipes.length > 0 && (
                <button className="btn-clear-selection" onClick={clearSelection}>Clear</button>
              )}
            </div>
            
            <button
              className="btn-generate"
              onClick={generateMealPlan}
              disabled={selectedRecipes.length < 2 || generatingPlan}
            >
              {generatingPlan ? 'Generating...' : `Generate Meal Plan (${selectedRecipes.length})`}
            </button>
          </div>

          <div className="recipes-selection-grid">
            {recipes.map(recipe => (
              <div 
                key={recipe.id} 
                className={`recipe-selection-card ${selectedRecipes.includes(recipe.id) ? 'selected' : ''}`}
                onClick={() => toggleRecipeSelection(recipe.id)}
              >
                <div className="selection-checkbox">
                  <input 
                    type="checkbox" 
                    checked={selectedRecipes.includes(recipe.id)}
                    onChange={() => {}}
                    onClick={(e) => e.stopPropagation()}
                  />
                </div>
                <h4>{recipe.title}</h4>
                <p><strong>{recipe.cuisine}</strong></p>
                <p className="difficulty"><span className={`badge ${recipe.difficulty}`}>{recipe.difficulty}</span></p>
                <p className="timing">{recipe.prep_time || 'N/A'} prep • {recipe.cook_time || 'N/A'} cook</p>
                <p className="servings">{recipe.servings || '?'} servings</p>
                <button 
                  className="btn-view"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowRecipeDetails(recipe);
                  }}
                >
                  View Details
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recipe Details Modal */}
      {showRecipeDetails && (
        <div className="modal-overlay" onClick={() => setShowRecipeDetails(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <RecipeCard 
              recipe={showRecipeDetails} 
              onClose={() => setShowRecipeDetails(null)}
              showDetails={false}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default MealPlanner;
