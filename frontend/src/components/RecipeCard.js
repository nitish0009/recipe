import React from 'react';
import '../styles/RecipeCard.css';

function RecipeCard({ recipe, onClose, showDetails = true }) {
  if (!recipe) return null;

  return (
    <div className="recipe-card-container">
      <div className="recipe-card">
        {onClose && (
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        )}

        {/* Header */}
        <div className="recipe-header">
          <h2>{recipe.title || 'Untitled Recipe'}</h2>
          <div className="recipe-meta">
            <span className={`difficulty ${recipe.difficulty}`}>
              {recipe.difficulty?.toUpperCase() || 'N/A'}
            </span>
            <span className="cuisine">{recipe.cuisine || 'N/A'}</span>
          </div>
        </div>

        {/* Timing Info */}
        <div className="timing-info">
          <div className="timing-item">
            <span className="label">Prep</span>
            <span className="value">{recipe.prep_time || 'N/A'}</span>
          </div>
          <div className="timing-item">
            <span className="label">Cook</span>
            <span className="value">{recipe.cook_time || 'N/A'}</span>
          </div>
          <div className="timing-item">
            <span className="label">Total</span>
            <span className="value">{recipe.total_time || 'N/A'}</span>
          </div>
          <div className="timing-item">
            <span className="label">Servings</span>
            <span className="value">{recipe.servings || 'N/A'}</span>
          </div>
        </div>

        {showDetails && (
          <>
            {/* Ingredients */}
            {recipe.ingredients && recipe.ingredients.length > 0 && (
              <section className="recipe-section">
                <h3>Ingredients</h3>
                <ul className="ingredients-list">
                  {recipe.ingredients.map((ing, idx) => (
                    <li key={idx}>
                      <span className="quantity">{ing.quantity}</span>
                      <span className="unit">{ing.unit}</span>
                      <span className="item">{ing.item}</span>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* Instructions */}
            {recipe.instructions && recipe.instructions.length > 0 && (
              <section className="recipe-section">
                <h3>Instructions</h3>
                <ol className="instructions-list">
                  {recipe.instructions.map((instruction, idx) => (
                    <li key={idx}>{instruction}</li>
                  ))}
                </ol>
              </section>
            )}

            {/* Nutrition */}
            {recipe.nutrition_estimate && (
              <section className="recipe-section">
                <h3>Nutrition (per serving)</h3>
                <div className="nutrition-grid">
                  <div className="nutrition-item">
                    <span className="nutrient">Calories</span>
                    <span className="value">{recipe.nutrition_estimate.calories || 'N/A'}</span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrient">Protein</span>
                    <span className="value">{recipe.nutrition_estimate.protein || 'N/A'}</span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrient">Carbs</span>
                    <span className="value">{recipe.nutrition_estimate.carbs || 'N/A'}</span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrient">Fat</span>
                    <span className="value">{recipe.nutrition_estimate.fat || 'N/A'}</span>
                  </div>
                </div>
              </section>
            )}

            {/* Substitutions */}
            {recipe.substitutions && recipe.substitutions.length > 0 && (
              <section className="recipe-section">
                <h3>Ingredient Substitutions</h3>
                <ul className="substitutions-list">
                  {recipe.substitutions.map((sub, idx) => (
                    <li key={idx}>{sub}</li>
                  ))}
                </ul>
              </section>
            )}

            {/* Shopping List */}
            {recipe.shopping_list && (
              <section className="recipe-section">
                <h3>Shopping List</h3>
                <div className="shopping-list">
                  {Object.entries(recipe.shopping_list).map(([category, items]) => (
                    <div key={category} className="shopping-category">
                      <h4>{category.charAt(0).toUpperCase() + category.slice(1)}</h4>
                      <ul>
                        {Array.isArray(items) && items.map((item, idx) => (
                          <li key={idx}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Related Recipes */}
            {recipe.related_recipes && recipe.related_recipes.length > 0 && (
              <section className="recipe-section">
                <h3>Related Recipes</h3>
                <ul className="related-recipes">
                  {recipe.related_recipes.map((rel, idx) => (
                    <li key={idx}>{rel}</li>
                  ))}
                </ul>
              </section>
            )}

            {/* Recipe URL */}
            {recipe.url && (
              <section className="recipe-section">
                <p className="recipe-url">
                  <small>Source: <a href={recipe.url} target="_blank" rel="noopener noreferrer">
                    {recipe.url.substring(0, 50)}...
                  </a></small>
                </p>
              </section>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default RecipeCard;
