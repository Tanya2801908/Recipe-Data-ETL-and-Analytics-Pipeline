import json
import csv
import os

# ---------------------- Helper Functions ----------------------
def load_json(file_name):
    """
    Load JSON file from current folder.
    """
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_csv(file_name, fieldnames, rows):
    """
    Save list of dictionaries to CSV.
    """
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ '{file_name}' created with {len(rows)} records.")


# ---------------------- Transform Recipes ----------------------
def transform_recipes(recipes):
    recipes_rows = []
    ingredients_rows = []
    steps_rows = []

    for recipe in recipes:
        recipe_id = recipe.get("id", "")

        # Recipes table
        recipes_rows.append({
            "recipe_id": recipe_id,
            "name": recipe.get("name", ""),
            "category": recipe.get("category", ""),
            "prep_time": recipe.get("prep_time", ""),   # Included
            "cook_time": recipe.get("cook_time", ""),   # Included
            "servings": recipe.get("servings", ""),
            "difficulty": recipe.get("difficulty", "")
        })

        # Ingredients (nested)
        for i, ing in enumerate(recipe.get("ingredients", []), start=1):
            ingredients_rows.append({
                "ingredient_id": f"{recipe_id}_ing{i}",
                "recipe_id": recipe_id,
                "ingredient_name": ing.get("name", ""),
                "quantity": ing.get("quantity", "")
            })

        # Steps (nested)
        for i, step in enumerate(recipe.get("steps", []), start=1):
            steps_rows.append({
                "step_id": f"{recipe_id}_step{i}",
                "recipe_id": recipe_id,
                "step_number": i,
                "instruction": step
            })

    return recipes_rows, ingredients_rows, steps_rows


# ---------------------- Transform Interactions ----------------------
def transform_interactions(interactions):
    rows = []
    for inter in interactions:
        rows.append({
            "interaction_id": inter.get("id", ""),
            "user_id": inter.get("user_id", ""),
            "recipe_id": inter.get("recipe_id", ""),
            "views": inter.get("views", 0),
            "likes": inter.get("likes", 0),
            "rating": inter.get("rating", ""),
            "cook_attempts": inter.get("cook_attempts", 0)
        })
    return rows


# ---------------------- Main ETL (no users.json) ----------------------
def run_etl():
    print("🔄 Loading JSON files...")

    recipes = load_json("recipes.json")
    interactions = load_json("interactions.json")

    # ---- Transform Recipes ----
    recipes_rows, ingredients_rows, steps_rows = transform_recipes(recipes)

    save_csv(
        "recipes.csv",
        ["recipe_id", "name", "category", "prep_time", "cook_time", "servings", "difficulty"],
        recipes_rows
    )

    save_csv(
        "ingredients.csv",
        ["ingredient_id", "recipe_id", "ingredient_name", "quantity"],
        ingredients_rows
    )

    save_csv(
        "steps.csv",
        ["step_id", "recipe_id", "step_number", "instruction"],
        steps_rows
    )

    # ---- Transform Interactions ----
    interactions_rows = transform_interactions(interactions)

    save_csv(
        "interactions.csv",
        ["interaction_id", "user_id", "recipe_id", "views", "likes", "rating", "cook_attempts"],
        interactions_rows
    )

    print("🎉 ETL completed successfully (users.json excluded).")


# ---------------------- Run ----------------------
if __name__ == "__main__":
    run_etl()




