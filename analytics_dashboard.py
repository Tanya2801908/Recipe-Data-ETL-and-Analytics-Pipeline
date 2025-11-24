import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# --------------------------
# REMOVE ALL WARNINGS CLEANLY
# --------------------------
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Recipe Analytics Dashboard", layout="wide")


# Hide Streamlit warnings on UI (yellow bars)
st.markdown("""
<style>
.stAlert {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# --------------------------
# LOAD DATA
# --------------------------
BASE = os.getcwd()
DATA = os.path.join(BASE, "csvoutputs")
IMAGE_DIR = os.path.join(BASE, "images")

recipes = pd.read_csv(os.path.join(DATA, "recipes.csv"))
ingredients = pd.read_csv(os.path.join(DATA, "ingredients.csv"))
interactions = pd.read_csv(os.path.join(DATA, "interactions.csv"))

header_image_path = os.path.join(IMAGE_DIR, "header_image.png")


# --------------------------
# INSIGHT FUNCTIONS
# --------------------------

def most_common_ingredients():
    top10 = ingredients["ingredient_name"].value_counts().head(10)
    return top10.to_frame("Count")

def avg_prep_time():
    return pd.DataFrame({"Average Prep Time (min)": [round(recipes["prep_time"].mean(), 2)]})

def avg_cooking_time():
    return pd.DataFrame({"Average Cooking Time (min)": [round(recipes["cook_time"].mean(), 2)]})

def difficulty_distribution():
    return recipes["difficulty"].value_counts().to_frame("Number of Recipes")

def correlation_prep_likes():
    merged = interactions.merge(recipes, on="recipe_id")
    corr = merged["prep_time"].corr(merged["likes"])
    return pd.DataFrame({"Correlation (prep_time vs likes)": [round(corr, 4)]})

def most_viewed_recipes():
    return interactions.groupby("recipe_id")["views"].sum().sort_values(ascending=False).head(10).to_frame("Total Views")

def high_engagement_ingredients():
    merged = interactions.merge(recipes, on="recipe_id").merge(ingredients, on="recipe_id")
    merged["engagement"] = merged["views"] + merged["likes"] + merged["cook_attempts"]
    return merged.groupby("ingredient_name")["engagement"].sum().sort_values(ascending=False).head(10).to_frame("Engagement")

def top_rated_recipes():
    return interactions.groupby("recipe_id")["rating"].mean().sort_values(ascending=False).head(10).to_frame("Avg Rating")

def most_liked_recipes():
    return interactions.groupby("recipe_id")["likes"].sum().sort_values(ascending=False).head(10).to_frame("Likes")

def avg_ingredients_per_recipe():
    avg_ing = ingredients.groupby("recipe_id").size().mean()
    return pd.DataFrame({"Avg Ingredients per Recipe": [round(avg_ing, 2)]})

def highest_engagement_recipe():
    inter = interactions.copy()
    inter["engagement"] = inter["views"] + inter["likes"] + inter["cook_attempts"]
    result = inter.groupby("recipe_id")["engagement"].sum().sort_values(ascending=False).head(1)
    return result.to_frame("Total Engagement")


# mapping insight name → function
INSIGHTS = {
    "Most Common Ingredients": most_common_ingredients,
    "Average Preparation Time": avg_prep_time,
    "Average Cooking Time": avg_cooking_time,
    "Difficulty Distribution": difficulty_distribution,
    "Correlation (Prep_time vs Likes)": correlation_prep_likes,
    "Most Viewed Recipes": most_viewed_recipes,
    "High Engagement Ingredients": high_engagement_ingredients,
    "Top Rated Recipes": top_rated_recipes,
    "Most Liked Recipes": most_liked_recipes,
    "Average Ingredients Per Recipe": avg_ingredients_per_recipe,
    "Highest Engagement Recipe": highest_engagement_recipe
}


# --------------------------
# DASHBOARD LAYOUT
# --------------------------

# Page Title ABOVE the header image
st.markdown(
    "<h1 style='text-align:center; color:white;'>Recipe Data ETL & Analytics Pipeline</h1>",
    unsafe_allow_html=True
)

# Header Image
if os.path.exists(header_image_path):
    st.image(header_image_path, use_container_width=True)
else:
    st.error(f"Header image not found: {header_image_path}")


# Section Title
st.markdown(
    "<h2 style='text-align:center; color:white; margin-top:40px;'>📊 Analytical Insights</h2>",
    unsafe_allow_html=True
)

st.write("---")

# Two-column layout
col1, col2 = st.columns([1.2, 2.2])


# -------- LEFT PANEL → Select Insight + Table --------
with col1:
    st.markdown("### 🔍 Select Insight")

    insight = st.selectbox(
        "Choose an insight:",
        list(INSIGHTS.keys()),
        index=0,
        key="insight_select",
        help="Scroll to see all insights."
    )

    df = INSIGHTS[insight]()

    st.markdown("### 📄 Insight Table")
    st.dataframe(df, use_container_width=True)


# -------- RIGHT PANEL → Graph --------
with col2:
    st.markdown("### 📈 Insight Graph")

    # Create graph
    fig, ax = plt.subplots(figsize=(8, 4))
    df.plot(kind="bar", ax=ax, legend=True)
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig)


st.write("---")
