# Recipe Extraction Prompt
extraction_prompt = """
You are a professional recipe extraction expert. Extract structured recipe data from the following HTML-scraped text.
Return ONLY valid JSON with no additional text, markdown formatting, or commentary.

REQUIRED FIELDS (All must be present):
- title: string (exact recipe name from the page)
- cuisine: string (type of cuisine: Italian, Mexican, Asian, American, French, Indian, Mediterranean, etc.)
- prep_time: string (format: "15 mins" or "1 hour" or "1 hour 30 mins")
- cook_time: string (format same as prep_time)
- total_time: string (format same as prep_time)
- servings: integer (number of servings)
- difficulty: string (exactly one of: "easy", "medium", "hard")
- ingredients: array of objects with structure {{"quantity": "number as string", "unit": "cup/tbsp/tsp/oz/g/lb/ml/L/pinch/to taste", "item": "ingredient name"}}
- instructions: array of strings (each string is one step, clear and actionable)

EXTRACTION RULES:
1. Extract ONLY information explicitly found in the text
2. For missing times, estimate reasonably (e.g., grilled items: 10-20 mins cook time)
3. For missing servings, default to 4
4. Normalize units (convert all to standard: cups, tbsp, tsp, oz, g, lb, ml, L)
5. Each instruction should be a single step
6. Difficulty: "easy" (≤30 mins, simple steps), "medium" (30-60 mins, moderate skills), "hard" (>60 mins or complex techniques)
7. Ground all answers strictly in the provided text

SCRAPED TEXT:
{scraped_text}

RESPOND WITH ONLY VALID JSON:
"""

# Nutrition Estimation Prompt
nutrition_prompt = """
You are a nutritionist. Estimate realistic nutritional information PER SERVING based on this recipe ingredients.
Use standard USDA nutritional databases as reference. Return ONLY valid JSON with no explanations.

Ingredients:
{ingredients}

Return ONLY this JSON structure (per serving):
{{
  "calories": "<number>",
  "protein": "<number>g",
  "carbs": "<number>g",
  "fat": "<number>g"
}}

Make reasonable estimates based on ingredients and quantities.
"""

# Ingredient Substitutions Prompt
substitutions_prompt = """
Generate 3 useful ingredient substitutions for this recipe. Focus on common dietary needs (dairy-free, vegan, gluten-free, healthier alternatives).
Return ONLY valid JSON array with no explanations.

Ingredients:
{ingredients}

Return exactly 3 substitutions as JSON strings. Each should be a specific, actionable suggestion.

Return ONLY the JSON array:
["substitution 1", "substitution 2", "substitution 3"]
"""

# Shopping List Prompt
shopping_list_prompt = """
Create a shopping list grouped by category from these ingredients.
Return ONLY valid JSON with no explanations.

Ingredients:
{ingredients}

Organize ingredients into logical categories.
Categories: dairy, produce, meat, pantry, spices, bakery, frozen, other

Return JSON object:
{{
  "dairy": ["item1", "item2"],
  "produce": ["item3", "item4"],
  "pantry": ["item5"]
}}

Return ONLY the JSON object:
"""

# Related Recipes Prompt
related_recipes_prompt = """
Suggest 3 related recipes that pair well with a {title} recipe from {cuisine} cuisine.
These should be actual well-known recipes that go well with the given dish.
Return ONLY valid JSON array with no explanations.

Think about complementary flavors, courses (appetizer, main, dessert, side), and cuisines.
Return exactly 3 recipe names as JSON array of strings.

Example:
["Garlic Bread", "Caesar Salad", "Tiramisu"]

Return ONLY the JSON array:
"""

# Meal Plan Combined Shopping List Prompt
meal_plan_shopping_prompt = """
You are a smart grocery shopper. Combine ingredients from multiple recipes into one optimized shopping list.
Merge quantities of duplicate ingredients.
Return ONLY valid JSON with no explanations.

Ingredients from multiple recipes:
{ingredients}

Return JSON object with categories:
{{
  "dairy": ["2 cups milk", "1 lb butter"],
  "produce": ["3 onions", "6 cloves garlic"],
  "pantry": ["3 cups flour"],
  "other": []
}}

Smart rules:
- Combine quantities for identical ingredients
- Use sensible units (pounds for bulk items)
- Keep list concise and practical

Return ONLY the JSON object:
"""