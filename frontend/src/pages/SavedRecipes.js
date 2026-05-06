import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RecipeCard from '../components/RecipeCard';
import '../styles/SavedRecipes.css';

function SavedRecipes() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [filterDifficulty, setFilterDifficulty] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

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

  const viewDetails = async (id) => {
    try {
      const response = await axios.get(`http://localhost:8001/api/recipes/${id}`);
      setSelectedRecipe(response.data);
      setShowModal(true);
    } catch (err) {
      setError('Failed to fetch recipe details');
      console.error('Error fetching recipe details:', err);
    }
  };

  const deleteRecipe = async (id) => {
    if (!window.confirm('Are you sure you want to delete this recipe?')) return;
    
    try {
      await axios.delete(`http://localhost:8001/api/recipes/${id}`);
      setRecipes(recipes.filter(r => r.id !== id));
      setShowModal(false);
      setSelectedRecipe(null);
    } catch (err) {
      setError('Failed to delete recipe');
      console.error('Error deleting recipe:', err);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedRecipe(null);
  };

  // Filter recipes
  const filteredRecipes = recipes.filter(recipe => {
    const matchesDifficulty = !filterDifficulty || recipe.difficulty === filterDifficulty;
    const matchesSearch = !searchTerm || 
      recipe.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      recipe.cuisine.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesDifficulty && matchesSearch;
  });

  if (loading) {
    return (
      <div className="saved-recipes-container">
        <div className="loading">Loading recipes...</div>
      </div>
    );
  }

  return (
    <div className="saved-recipes-container">
      <h2>Saved Recipes</h2>
      
      {error && (
        <div className="alert alert-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {recipes.length === 0 ? (
        <div className="empty-state">
          <p>No recipes saved yet. Go to the "Extract Recipe" tab to add your first recipe!</p>
        </div>
      ) : (
        <>
          {/* Filters */}
          <div className="filters-section">
            <div className="filter-group">
              <label htmlFor="search">Search</label>
              <input
                id="search"
                type="text"
                placeholder="Search by title or cuisine..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="filter-input"
              />
            </div>

            <div className="filter-group">
              <label htmlFor="difficulty">Difficulty</label>
              <select
                id="difficulty"
                value={filterDifficulty}
                onChange={(e) => setFilterDifficulty(e.target.value)}
                className="filter-select"
              >
                <option value="">All</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <div className="filter-info">
              Showing {filteredRecipes.length} of {recipes.length} recipes
            </div>
          </div>

          {/* Recipes Table */}
          <div className="recipes-table-container">
            <table className="recipes-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Cuisine</th>
                  <th>Difficulty</th>
                  <th>Prep Time</th>
                  <th>Servings</th>
                  <th>Date Saved</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredRecipes.map(recipe => (
                  <tr key={recipe.id}>
                    <td className="recipe-title">{recipe.title}</td>
                    <td>{recipe.cuisine || 'N/A'}</td>
                    <td>
                      <span className={`difficulty-badge ${recipe.difficulty}`}>
                        {recipe.difficulty}
                      </span>
                    </td>
                    <td>{recipe.prep_time || 'N/A'}</td>
                    <td>{recipe.servings || 'N/A'}</td>
                    <td className="date">
                      {recipe.created_at ? new Date(recipe.created_at).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="actions">
                      <button 
                        className="btn-details"
                        onClick={() => viewDetails(recipe.id)}
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Recipe Details Modal */}
      {showModal && selectedRecipe && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <RecipeCard 
              recipe={selectedRecipe} 
              onClose={closeModal}
              showDetails={true}
            />
            <div className="modal-actions">
              <button className="btn-delete" onClick={() => deleteRecipe(selectedRecipe.id)}>
                Delete Recipe
              </button>
              <button className="btn-close" onClick={closeModal}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SavedRecipes;