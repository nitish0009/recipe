# 🍽️ Recipe Extractor & Meal Planner v2.0

An advanced web application that intelligently extracts structured recipe data from blog URLs using AI and provides comprehensive meal planning features with optimized shopping lists.

## ✨ Features

### Core Features
- **AI-Powered Recipe Extraction**: Automatically extract structured recipe data from any recipe blog URL
- **Intelligent Enrichment**: Generate nutritional estimates, ingredient substitutions, categorized shopping lists, and related recipe suggestions
- **Database Management**: Save and organize recipes with full history and search capabilities
- **Advanced Meal Planner**: Select multiple recipes to generate combined, optimized shopping lists
- **Responsive UI**: Beautiful, modern interface that works on desktop and mobile devices

### Advanced Features
- **Smart Shopping List Merging**: Combines ingredients from multiple recipes with merged quantities
- **Difficulty Classification**: Auto-categorized recipes (Easy, Medium, Hard)
- **Nutritional Analysis**: Per-serving nutritional estimates (calories, protein, carbs, fat)
- **Dietary Alternatives**: AI-generated ingredient substitutions for common dietary needs
- **Related Recipes**: Intelligent suggestions for complementary dishes
- **Export Functionality**: Download shopping lists as text files
- **Filter & Search**: Advanced filtering by difficulty and cuisine, full-text search

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.104.1 (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: React 18+ with Axios
- **AI/LLM**: Google Gemini Pro via LangChain
- **Web Scraping**: BeautifulSoup4 + html5lib
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14+ and npm
- PostgreSQL 12+
- Google Gemini API key (free tier available at [Google AI Studio](https://makersuite.google.com/app/apikey))
- Git (for version control, optional)

## 🚀 Installation & Setup

### 1. Clone or Extract the Project

```bash
cd Recipe-Blog-main
```

### 2. Backend Setup

#### Step 1: Create Python Virtual Environment
```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
# Linux/macOS:
nano .env

# Windows:
notepad .env
```

**Environment variables needed:**
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:password@localhost/recipe_extractor`)
- `GOOGLE_API_KEY`: Your Google Gemini API key

#### Step 4: Create PostgreSQL Database
```sql
-- Using psql or your PostgreSQL client
CREATE DATABASE recipe_extractor;
```

#### Step 5: Start the Backend Server
```bash
# Make sure virtual environment is activated
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

#### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

#### Step 2: Start Development Server
```bash
npm start
```

Frontend will open at: `http://localhost:3000`

**Note**: The frontend is configured to communicate with the backend at `http://localhost:8000`. Ensure both servers are running.

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Extract Recipe
**POST** `/extract-recipe`

Extract and process a recipe from a blog URL.

**Request:**
```json
{
  "url": "https://www.example.com/recipe/pasta-carbonara"
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://www.example.com/recipe/pasta-carbonara",
  "title": "Classic Carbonara",
  "cuisine": "Italian",
  "prep_time": "10 mins",
  "cook_time": "20 mins",
  "total_time": "30 mins",
  "servings": 4,
  "difficulty": "medium",
  "ingredients": [
    {
      "quantity": "400",
      "unit": "g",
      "item": "spaghetti"
    }
  ],
  "instructions": [
    "Boil water and cook spaghetti...",
    "Mix eggs with cheese..."
  ],
  "nutrition_estimate": {
    "calories": 450,
    "protein": "18g",
    "carbs": "52g",
    "fat": "22g"
  },
  "substitutions": [
    "Replace guanciale with pancetta for availability",
    "Use Pecorino Romano instead of Parmesan for authentic flavor"
  ],
  "shopping_list": {
    "dairy": ["eggs", "Pecorino Romano cheese"],
    "pantry": ["spaghetti", "salt", "black pepper"],
    "meat": ["guanciale"]
  },
  "related_recipes": [
    "Caesar Salad",
    "Garlic Bread",
    "Tiramisu"
  ],
  "created_at": "2024-05-06T10:30:00"
}
```

#### Get All Recipes
**GET** `/recipes`

Retrieve list of all saved recipes with optional filtering.

**Query Parameters:**
- `skip` (int, default: 0): Pagination offset
- `limit` (int, default: 10, max: 100): Number of recipes to return
- `difficulty` (string, optional): Filter by "easy", "medium", or "hard"
- `cuisine` (string, optional): Filter by cuisine type

**Response:**
```json
{
  "total": 15,
  "recipes": [
    {
      "id": 1,
      "title": "Pasta Carbonara",
      "cuisine": "Italian",
      "difficulty": "medium",
      "prep_time": "10 mins",
      "cook_time": "20 mins",
      "servings": 4,
      "created_at": "2024-05-06T10:30:00"
    }
  ]
}
```

#### Get Recipe Details
**GET** `/recipes/{recipe_id}`

Get full details of a specific recipe.

**Response:**
```json
{
  "id": 1,
  "url": "https://...",
  "title": "...",
  "cuisine": "...",
  "prep_time": "...",
  "cook_time": "...",
  "total_time": "...",
  "servings": 4,
  "difficulty": "medium",
  "ingredients": [...],
  "instructions": [...],
  "nutrition_estimate": {...},
  "substitutions": [...],
  "shopping_list": {...},
  "related_recipes": [...],
  "created_at": "2024-05-06T10:30:00"
}
```

#### Delete Recipe
**DELETE** `/recipes/{recipe_id}`

Delete a recipe from the database.

**Response:**
```json
{
  "message": "Recipe deleted successfully",
  "id": 1
}
```

#### Search Recipes
**GET** `/recipes/search/by-title?q=pasta`

Search recipes by title.

**Query Parameters:**
- `q` (string, required, min length: 1): Search term

**Response:**
```json
[
  {
    "id": 1,
    "title": "Pasta Carbonara",
    "cuisine": "Italian",
    "difficulty": "medium"
  }
]
```

#### Create Meal Plan
**POST** `/meal-plan`

Generate optimized combined shopping list for multiple recipes.

**Request:**
```json
{
  "recipe_ids": [1, 2, 3]
}
```

**Constraints:**
- Minimum 2 recipes
- Maximum 10 recipes per plan

**Response:**
```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Pasta Carbonara",
      "cuisine": "Italian",
      "difficulty": "medium",
      "prep_time": "10 mins",
      "cook_time": "20 mins",
      "servings": 4
    }
  ],
  "shopping_list": {
    "dairy": ["2 eggs", "200g Pecorino Romano"],
    "pantry": ["400g spaghetti", "salt", "black pepper"],
    "meat": ["150g guanciale"]
  }
}
```

#### Get Meal Plan Suggestions
**GET** `/meal-plan/suggestions`

Get suggestions for meal planning based on available recipes.

**Response:**
```json
{
  "total_recipes": 15,
  "by_cuisine": {
    "Italian": [...],
    "Mexican": [...]
  },
  "suggestions": [
    "Try combining 2-3 recipes from the same cuisine",
    "Mix different cuisines for a diverse meal plan"
  ]
}
```

#### Health Check
**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🎨 Frontend Usage

### Tab 1: Extract Recipe
1. Enter a recipe blog URL (e.g., `https://www.allrecipes.com/recipe/...`)
2. Click "Extract Recipe"
3. Wait for processing (may take 30-60 seconds)
4. View extracted recipe with all details

### Tab 2: Saved Recipes
1. Browse all previously extracted recipes
2. Filter by difficulty or search by title
3. Click "View Details" to see full recipe in modal
4. Delete recipes you no longer need

### Tab 3: Meal Planner (Advanced)
1. Select 2-10 recipes from the grid
2. Click "Generate Meal Plan"
3. View combined shopping list organized by category
4. Check off items as you shop
5. Download shopping list as text file

## 📝 Sample Data

Example recipe URLs that work well:
- https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/
- https://www.bbcgoodfood.com/recipes/simple-spaghetti-carbonara
- https://www.tasty.co/article/

## 🧪 Testing

### Backend Testing
```bash
# Navigate to backend
cd backend

# Run with test data
python -m uvicorn app.main:app --reload
```

Test the API using:
- Postman (import from `/backend/API_DOCS.md`)
- cURL commands
- Frontend UI

### Frontend Testing
```bash
# Navigate to frontend
cd frontend

# Run development server with debugging
npm start
```

## 🔐 Environment Variables

Create a `.env` file in the backend directory:

```env
# PostgreSQL Database
DATABASE_URL=postgresql://username:password@localhost:5432/recipe_extractor

# Google Gemini API
GOOGLE_API_KEY=your_api_key_here
```

To get a Google API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy and paste into your `.env` file

## 📁 Project Structure

```
Recipe-Blog-main/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration
│   │   ├── database.py            # Database setup
│   │   ├── main.py                # FastAPI app
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── prompts/               # LLM prompts
│   │   ├── routes/                # API routes
│   │   │   ├── recipes.py         # Recipe endpoints
│   │   │   └── meal_planner.py    # Meal plan endpoints
│   │   └── services/              # Business logic
│   │       ├── llm_service.py     # LLM operations
│   │       └── scraper.py         # Web scraping
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Example env file
│   └── venv/                      # Virtual environment
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── RecipeCard.js      # Recipe display component
│   │   ├── pages/
│   │   │   ├── ExtractRecipe.js   # Recipe extraction page
│   │   │   ├── SavedRecipes.js    # Saved recipes page
│   │   │   └── MealPlanner.js     # Meal planning page
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   ├── ExtractRecipe.css
│   │   │   ├── RecipeCard.css
│   │   │   ├── SavedRecipes.css
│   │   │   └── MealPlanner.css
│   │   ├── App.js                 # Main app component
│   │   └── index.js               # React entry point
│   └── package.json
│
├── sample_data/                   # Example extracted recipes
├── README.md                      # This file
└── API_DOCS.md                    # Additional API documentation
```

## 🚨 Troubleshooting

### Backend Issues

**"database connection failed"**
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Verify database exists: `createdb recipe_extractor`

**"Google API key is invalid"**
- Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Ensure it's correctly set in `.env`

**"Port 8000 is already in use"**
```bash
# Run on different port
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**"Cannot connect to backend"**
- Ensure backend server is running on `http://localhost:8000`
- Check for CORS issues in browser console
- Verify firewall allows localhost connections

**"npm install fails"**
```bash
# Clear npm cache and try again
npm cache clean --force
npm install
```

## 🎯 Performance Tips

- First recipe extraction may take 30-60 seconds (LLM processing)
- Subsequent extractions are faster if URL already exists
- Use PostgreSQL connection pooling for production
- Cache LLM responses for common recipe patterns
- Consider implementing rate limiting for API

## 🔄 Workflow Example

1. **Extract**: User pastes recipe URL → System extracts and enriches → Recipe saved
2. **Browse**: User views all saved recipes in history → Can filter and search
3. **Plan**: User selects 3-5 recipes → System generates combined shopping list
4. **Shop**: User downloads shopping list → Checks off items while shopping

## 📚 LLM Prompts

The system uses optimized prompts for different tasks:
- **Extraction Prompt**: Structured recipe data extraction with validation
- **Nutrition Prompt**: Per-serving nutritional estimates
- **Substitutions Prompt**: Dietary alternative suggestions
- **Shopping List Prompt**: Category-based organization
- **Related Recipes Prompt**: Complementary dish suggestions
- **Meal Plan Prompt**: Smart ingredient merging across recipes

All prompts are designed to minimize hallucination and ground responses in scraped content.

## 🤝 Contributing

Suggestions for improvements:
- Add recipe rating/review system
- Implement user accounts and syncing
- Add recipe scaling (adjust servings)
- Support for more languages
- Mobile app version
- Integration with grocery delivery services

## 📄 License

This project is open source and available for educational and commercial use.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation in `/backend/API_DOCS.md`
3. Check sample data in `/sample_data/`

## 🎉 Getting Started Checklist

- [ ] Python 3.8+ installed
- [ ] PostgreSQL installed and running
- [ ] Node.js 14+ installed
- [ ] Google Gemini API key obtained
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] `.env` file configured
- [ ] Backend server running on port 8000
- [ ] Frontend dependencies installed
- [ ] Frontend server running on port 3000
- [ ] Successfully extracted first recipe
- [ ] Created meal plan with multiple recipes

---

**Version**: 2.0.0  
**Last Updated**: May 2024  
**Status**: Production Ready ✅

5. Create the database:
   ```
   # Make sure PostgreSQL is running and create a database named 'recipe_extractor'
   createdb recipe_extractor
   ```

6. Run the backend:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

The application will be available at `http://localhost:3000` with the backend at `http://localhost:8000`.

## API Endpoints

### Extract Recipe
- **POST** `/api/extract-recipe`
- Body: `{"url": "https://example.com/recipe"}`
- Returns: Full recipe data JSON

### Get Saved Recipes
- **GET** `/api/recipes`
- Returns: List of saved recipes (summary)

### Get Recipe Details
- **GET** `/api/recipes/{id}`
- Returns: Full recipe data for the given ID

### Generate Meal Plan
- **POST** `/api/meal-plan`
- Body: `{"recipe_ids": [1, 2, 3]}`
- Returns: Combined shopping list

## Sample Data

See the `sample_data/` directory for example URLs and their extracted JSON outputs.