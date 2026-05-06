import React, { useState } from 'react';
import axios from 'axios';
import RecipeCard from '../components/RecipeCard';
import '../styles/ExtractRecipe.css';

function ExtractRecipe() {
  const [url, setUrl] = useState('');
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    setRecipe(null);

    try {
      if (!url.trim()) {
        throw new Error('Please enter a valid URL');
      }

      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        throw new Error('URL must start with http:// or https://');
      }

      const response = await axios.post('http://localhost:8000/api/extract-recipe', { 
        url: url.trim() 
      }, {
        timeout: 60000 // 60 second timeout for extraction
      });

      setRecipe(response.data);
      setSuccess(`Successfully extracted recipe: "${response.data.title}"`);
      setUrl('');
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred while extracting the recipe. Please check the URL and try again.';
      setError(errorMessage);
      console.error('Extraction error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="extract-recipe-container">
      <div className="extract-form-section">
        <h2>Extract Recipe from URL</h2>
        <p className="subtitle">Enter a recipe blog URL and our AI will extract all the information</p>

        <form onSubmit={handleSubmit} className="extract-form">
          <div className="form-group">
            <label htmlFor="url">Recipe Blog URL</label>
            <input
              id="url"
              type="url"
              placeholder="https://www.example.com/recipe/..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
              className="url-input"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading} 
            className="submit-btn"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Extracting...
              </>
            ) : (
              'Extract Recipe'
            )}
          </button>
        </form>

        {error && (
          <div className="alert alert-error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            <strong>Success!</strong> {success}
          </div>
        )}

        {/* Example URLs */}
        <div className="examples-section">
          <h4>Try these recipe URLs:</h4>
          <ul className="example-urls">
            <li>https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/</li>
            <li>https://www.recipetineats.com/bolognese-pasta-sauce-recipe/</li>
            <li>https://www.bbcgoodfood.com/recipes</li>
          </ul>
        </div>
      </div>

      {recipe && (
        <div className="recipe-result-section">
          <RecipeCard recipe={recipe} showDetails={true} />
        </div>
      )}
    </div>
  );
}

export default ExtractRecipe;