import pandas as pd

# ---------------------- Load CSV Files ----------------------
recipes = pd.read_csv("recipes.csv")
ingredients = pd.read_csv("ingredients.csv")
interactions = pd.read_csv("interactions.csv")

analytics_output = []   # list to store final CSV rows


# ---------------------- INSIGHT 1: Most Common Ingredients ----------------------
most_common_ingredients = (
    ingredients["ingredient_name"]
    .str.lower()
    .value_counts()
    .head(10)
)

analytics_output.append({
    "insight_name": "Most Common Ingredients (Top 10)",
    "insight_value": most_common_ingredients.to_string()
})

print("\n1️⃣ MOST COMMON INGREDIENTS:")
print(most_common_ingredients)


# ---------------------- INSIGHT 2: Average Preparation Time ----------------------
recipes["prep_time"] = pd.to_numeric(recipes["prep_time"], errors="ignore")
avg_prep_time = recipes["prep_time"].mean()

analytics_output.append({
    "insight_name": "Average Preparation Time",
    "insight_value": f"{avg_prep_time:.2f} minutes"
})

print("\n2️⃣ AVERAGE PREPARATION TIME:")
print(f"{avg_prep_time:.2f} minutes")


# ---------------------- INSIGHT 3: Average Cooking Time ----------------------
recipes["cook_time"] = pd.to_numeric(recipes["cook_time"], errors="ignore")
avg_cook_time = recipes["cook_time"].mean()

analytics_output.append({
    "insight_name": "Average Cooking Time",
    "insight_value": f"{avg_cook_time:.2f} minutes"
})

print("\n3️⃣ AVERAGE COOK TIME:")
print(f"{avg_cook_time:.2f} minutes")


# ---------------------- INSIGHT 4: Difficulty Distribution ----------------------
difficulty_distribution = recipes["difficulty"].value_counts()

analytics_output.append({
    "insight_name": "Difficulty Distribution",
    "insight_value": difficulty_distribution.to_string()
})

print("\n4️⃣ DIFFICULTY DISTRIBUTION:")
print(difficulty_distribution)


# ---------------------- INSIGHT 5: Correlation Between Prep Time & Likes ----------------------
interactions["likes"] = pd.to_numeric(interactions["likes"], errors="coerce")
merged = pd.merge(recipes, interactions, on="recipe_id")

correlation = merged["prep_time"].corr(merged["likes"])

analytics_output.append({
    "insight_name": "Correlation (Prep Time vs Likes)",
    "insight_value": f"{correlation:.3f}"
})

print("\n5️⃣ CORRELATION: Prep Time vs Likes:")
print(f"Correlation score: {correlation:.3f}")


# ---------------------- INSIGHT 6: Most Viewed Recipes ----------------------
interactions["views"] = pd.to_numeric(interactions["views"], errors="coerce")

most_viewed = (
    merged.groupby("name")["views"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

analytics_output.append({
    "insight_name": "Most Viewed Recipes (Top 10)",
    "insight_value": most_viewed.to_string()
})

print("\n6️⃣ MOST VIEWED RECIPES:")
print(most_viewed)


# ---------------------- INSIGHT 7: Ingredients With High Engagement ----------------------
merged_ing = pd.merge(ingredients, interactions, on="recipe_id")

high_engagement_ingredients = (
    merged_ing.groupby("ingredient_name")["likes"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

analytics_output.append({
    "insight_name": "High Engagement Ingredients (Top 10)",
    "insight_value": high_engagement_ingredients.to_string()
})

print("\n7️⃣ INGREDIENTS WITH HIGHEST AVERAGE LIKES:")
print(high_engagement_ingredients)


# ---------------------- INSIGHT 8: Top Rated Recipes ----------------------
interactions["rating"] = pd.to_numeric(interactions["rating"], errors="coerce")

top_rated = (
    merged.groupby("name")["rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

analytics_output.append({
    "insight_name": "Top Rated Recipes (Top 10)",
    "insight_value": top_rated.to_string()
})

print("\n8️⃣ TOP RATED RECIPES:")
print(top_rated)


# ---------------------- INSIGHT 9: Most Liked Recipes ----------------------
most_liked = (
    merged.groupby("name")["likes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

analytics_output.append({
    "insight_name": "Most Liked Recipes (Top 10)",
    "insight_value": most_liked.to_string()
})

print("\n9️⃣ MOST LIKED RECIPES:")
print(most_liked)


# ---------------------- INSIGHT 10: Avg Ingredients Per Recipe ----------------------
ingredients_per_recipe = (
    ingredients.groupby("recipe_id")["ingredient_name"]
    .count()
    .mean()
)

analytics_output.append({
    "insight_name": "Average Ingredients Per Recipe",
    "insight_value": f"{ingredients_per_recipe:.2f}"
})

print("\n🔟 AVERAGE INGREDIENT COUNT:")
print(f"{ingredients_per_recipe:.2f}")


# ---------------------- INSIGHT 11: Recipes With Most Ingredients ----------------------
most_ingredients = (
    ingredients.groupby("recipe_id")["ingredient_name"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

analytics_output.append({
    "insight_name": "Recipes With Most Ingredients (Top 10)",
    "insight_value": most_ingredients.to_string()
})

print("\n1️⃣1️⃣ RECIPES WITH MOST INGREDIENTS:")
print(most_ingredients)


# ---------------------- INSIGHT 12: Highest Total Engagement ----------------------
merged["total_engagement"] = (
    merged["likes"] +
    merged["views"] +
    merged["cook_attempts"]
)

top_engagement = (
    merged.groupby("name")["total_engagement"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

analytics_output.append({
    "insight_name": "Highest Engagement Recipes (Top 10)",
    "insight_value": top_engagement.to_string()
})

print("\n1️⃣2️⃣ HIGHEST ENGAGEMENT RECIPES:")
print(top_engagement)


# ---------------------- SAVE OUTPUT TO CSV ----------------------
output_df = pd.DataFrame(analytics_output)
output_df.to_csv("analytics_output.csv", index=False)

print("\n📁 'analytics_output.csv' has been created successfully!")


