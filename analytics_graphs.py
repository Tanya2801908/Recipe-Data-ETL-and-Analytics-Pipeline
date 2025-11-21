import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------- Create Output Folder ----------------------
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# ---------------------- Load CSV Files ----------------------
recipes = pd.read_csv("recipes.csv")
ingredients = pd.read_csv("ingredients.csv")
interactions = pd.read_csv("interactions.csv")

# Convert numeric columns safely
recipes["prep_time"] = pd.to_numeric(recipes.get("prep_time"), errors="coerce")
recipes["cook_time"] = pd.to_numeric(recipes.get("cook_time"), errors="coerce")
interactions["views"] = pd.to_numeric(interactions.get("views"), errors="coerce")
interactions["likes"] = pd.to_numeric(interactions.get("likes"), errors="coerce")
interactions["rating"] = pd.to_numeric(interactions.get("rating"), errors="coerce")

# Merge for relationship-based insights
merged = pd.merge(recipes, interactions, on="recipe_id", how="left")

# ---------------------- 1. Most Common Ingredients ----------------------
top_ing = (
    ingredients["ingredient_name"].str.lower()
    .value_counts()
    .head(10)
)

plt.figure()
top_ing.plot(kind="bar")
plt.title("Top 10 Most Common Ingredients")
plt.xlabel("Ingredient")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("graphs/most_common_ingredients.png")
plt.close()

# ---------------------- 2. Average Preparation Time ----------------------
plt.figure()
recipes["prep_time"].dropna().plot(kind="hist", bins=10)
plt.title("Distribution of Preparation Time")
plt.xlabel("Prep Time (min)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("graphs/prep_time_distribution.png")
plt.close()

# ---------------------- 3. Average Cooking Time ----------------------
plt.figure()
recipes["cook_time"].dropna().plot(kind="hist", bins=10)
plt.title("Distribution of Cooking Time")
plt.xlabel("Cook Time (min)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("graphs/cook_time_distribution.png")
plt.close()

# ---------------------- 4. Difficulty Distribution ----------------------
difficulty_dist = recipes["difficulty"].value_counts()

plt.figure()
difficulty_dist.plot(kind="bar")
plt.title("Difficulty Distribution")
plt.xlabel("Difficulty Level")
plt.ylabel("Number of Recipes")
plt.tight_layout()
plt.savefig("graphs/difficulty_distribution.png")
plt.close()

# ---------------------- 5. Correlation Between Prep Time & Likes ----------------------
plt.figure()
plt.scatter(merged["prep_time"], merged["likes"])
plt.title("Prep Time vs Likes")
plt.xlabel("Prep Time")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig("graphs/prep_vs_likes.png")
plt.close()

# ---------------------- 6. Most Viewed Recipes ----------------------
most_viewed = (
    merged.groupby("name")["views"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
most_viewed.plot(kind="bar")
plt.title("Most Viewed Recipes (Top 10)")
plt.xlabel("Recipe")
plt.ylabel("Views")
plt.tight_layout()
plt.savefig("graphs/most_viewed_recipes.png")
plt.close()

# ---------------------- 7. Ingredients Associated with High Engagement ----------------------
merged_ing = pd.merge(ingredients, interactions, on="recipe_id", how="left")

top_eng_ing = (
    merged_ing.groupby("ingredient_name")["likes"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
top_eng_ing.plot(kind="bar")
plt.title("Top Ingredients by Average Likes")
plt.xlabel("Ingredient")
plt.ylabel("Avg Likes")
plt.tight_layout()
plt.savefig("graphs/high_engagement_ingredients.png")
plt.close()

# ---------------------- 8. Top Rated Recipes ----------------------
top_rated = (
    merged.groupby("name")["rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
top_rated.plot(kind="bar")
plt.title("Top Rated Recipes")
plt.xlabel("Recipe")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.savefig("graphs/top_rated_recipes.png")
plt.close()

# ---------------------- 9. Most Liked Recipes ----------------------
most_liked = (
    merged.groupby("name")["likes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
most_liked.plot(kind="bar")
plt.title("Most Liked Recipes")
plt.xlabel("Recipe")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig("graphs/most_liked_recipes.png")
plt.close()

# ---------------------- 10. Average Ingredients Per Recipe ----------------------
ingredients_count = (
    ingredients.groupby("recipe_id")["ingredient_name"]
    .count()
)

plt.figure()
ingredients_count.plot(kind="hist", bins=10)
plt.title("Ingredient Count Distribution")
plt.xlabel("Ingredients per Recipe")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("graphs/ingredient_count_distribution.png")
plt.close()

# ---------------------- 11. Recipes With Most Ingredients ----------------------
recipes_most_ing = ingredients_count.sort_values(ascending=False).head(10)

plt.figure()
recipes_most_ing.plot(kind="bar")
plt.title("Recipes with Most Ingredients (Top 10)")
plt.xlabel("Recipe ID")
plt.ylabel("Ingredient Count")
plt.tight_layout()
plt.savefig("graphs/recipes_most_ingredients.png")
plt.close()

# ---------------------- 12. Highest Total Engagement ----------------------
merged["total_engagement"] = (
    merged["views"].fillna(0) +
    merged["likes"].fillna(0) +
    merged["cook_attempts"].fillna(0)
)

top_engagement = (
    merged.groupby("name")["total_engagement"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
top_engagement.plot(kind="bar")
plt.title("Recipes With Highest Engagement")
plt.xlabel("Recipe")
plt.ylabel("Total Engagement")
plt.tight_layout()
plt.savefig("graphs/highest_engagement_recipes.png")
plt.close()

print("🎉 All graphs successfully generated in the 'graphs/' folder!")



