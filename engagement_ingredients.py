import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------ Load CSV Files ------------------
recipes = pd.read_csv("recipes.csv")
ingredients = pd.read_csv("ingredients.csv")
interactions = pd.read_csv("interactions.csv")

# ------------------ Fix ingredient column ------------------
# Your file has: ingredient_name → rename it
ingredients = ingredients.rename(columns={"ingredient_name": "ingredient"})

# ------------------ Compute Engagement Score ------------------
interactions["engagement"] = (
    interactions["likes"].fillna(0) +
    interactions["views"].fillna(0) +
    interactions["cook_attempts"].fillna(0)
)

# ------------------ Total Engagement per Recipe ------------------
recipe_engagement = interactions.groupby("recipe_id")["engagement"].sum().reset_index()

# ------------------ Merge Ingredients with Recipe Engagement ------------------
merged_df = pd.merge(ingredients, recipe_engagement, on="recipe_id", how="inner")

# ------------------ Engagement per Ingredient ------------------
ingredient_engagement = (
    merged_df.groupby("ingredient")["engagement"]
    .sum()
    .reset_index()
    .sort_values("engagement", ascending=False)
    .head(15)
)

# ------------------ Make folder for charts ------------------
os.makedirs("charts", exist_ok=True)

# ------------------ Plot Graph ------------------
plt.figure(figsize=(12, 6))
plt.barh(ingredient_engagement["ingredient"], ingredient_engagement["engagement"])
plt.xlabel("Engagement Score")
plt.ylabel("Ingredient")
plt.title("Ingredients Associated With High Engagement")
plt.gca().invert_yaxis()  # Highest on top
plt.tight_layout()

# Save graph
plt.savefig("charts/high_engagement_ingredients.png", dpi=300)
plt.close()

print("✅ Graph saved successfully: charts/high_engagement_ingredients.png")

