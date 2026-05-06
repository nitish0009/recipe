import React, { useState } from 'react';
import './styles/App.css';
import ExtractRecipe from './pages/ExtractRecipe';
import SavedRecipes from './pages/SavedRecipes';
import MealPlanner from './pages/MealPlanner';

function App() {
  const [activeTab, setActiveTab] = useState('extract');

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="logo-section">
            <h1>Recipe Extractor & Meal Planner</h1>
            <p className="tagline">AI-powered recipe extraction and intelligent meal planning</p>
          </div>
          
          <nav className="tabs">
            <button 
              className={`tab-btn ${activeTab === 'extract' ? 'active' : ''}`}
              onClick={() => setActiveTab('extract')}
              title="Extract recipes from URLs"
            >
              Extract Recipe
            </button>
            <button 
              className={`tab-btn ${activeTab === 'saved' ? 'active' : ''}`}
              onClick={() => setActiveTab('saved')}
              title="View all saved recipes"
            >
              Saved Recipes
            </button>
            <button 
              className={`tab-btn ${activeTab === 'planner' ? 'active' : ''}`}
              onClick={() => setActiveTab('planner')}
              title="Plan meals with multiple recipes"
            >
              Meal Planner
            </button>
          </nav>
        </div>
      </header>

      <main className="App-main">
        {activeTab === 'extract' && <ExtractRecipe />}
        {activeTab === 'saved' && <SavedRecipes />}
        {activeTab === 'planner' && <MealPlanner />}
      </main>

      <footer className="App-footer">
        <p>Recipe Extractor & Meal Planner v2.0 • Powered by Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;