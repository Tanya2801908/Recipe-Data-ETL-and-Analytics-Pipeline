#!/usr/bin/env python3
"""
Seed Firestore with:
- 30 users (user1 ... user30)
- 21 recipes (recipe1_<slug> ... recipe21_<slug>), primary is Paneer Curry with Chapati
- Interactions: interaction1 ... interactionN (at least 2 per recipe)

Requirements:
- Place ServiceAccountKey.json in same folder
- pip install firebase-admin
"""

import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore
from datetime import datetime
import time
import random
import re

# ---------------------------
# CONFIG
# ---------------------------
SERVICE_ACCOUNT_FILE = "ServiceAccountKey.json"
NUM_USERS = 30
NUM_SYNTHETIC_RECIPES = 20   # + 1 primary => total 21
MIN_INTERACTIONS_PER_RECIPE = 2

# ---------------------------
# INITIALIZE FIRESTORE
# ---------------------------
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------------------
# HELPERS
# ---------------------------
def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def slugify(s: str) -> str:
    """Return a lower-case slug safe for document IDs: letters, digits, underscore."""
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)        # remove non-word chars
    s = re.sub(r"[\s-]+", "_", s)         # spaces/dashes -> underscore
    return s

def recipe_doc_id(index:int, name:str):
    return f"recipe{index}_{slugify(name)}"

def interaction_doc_id(seq:int):
    return f"interaction{seq}"

def user_doc_id(index:int):
    return f"user{index}"

# ---------------------------
# 1) Create Users: user1 .. user30
# ---------------------------
def create_users():
    print("Creating users...")
    for i in range(1, NUM_USERS + 1):
        uid = user_doc_id(i)
        user_doc = {
            "user_id": uid,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "joined_at": now_iso()
        }
        db.collection("users").document(uid).set(user_doc)
    print(f"Created {NUM_USERS} users (user1 .. user{NUM_USERS})\n")

# ---------------------------
# 2) Primary recipe: Paneer Curry with Chapati
# ---------------------------
def get_primary_recipe():
    name = "Paneer Curry with Chapati"
    return {
        "recipe_id": recipe_doc_id(1, name),
        "name": name,
        "description": "A rich and aromatic paneer curry served with fresh chapatis — classic home-style Indian meal.",
        "category": "Indian",
        "difficulty": "Medium",
        "prep_time": 25,
        "cook_time": 30,
        "servings": 2,
        "ingredients": [
            {"name":"Paneer","quantity":"200 g"},
            {"name":"Onion","quantity":"3 to 4, chopped"},
            {"name":"Tomato","quantity":"2, pureed"},
            {"name":"Green Chillies","quantity":"2, slit"},
            {"name":"Ginger-Garlic Paste","quantity":"1 tbsp"},
            {"name":"Turmeric Powder","quantity":"1/4 tsp"},
            {"name":"Red Chilli Powder","quantity":"1/2 tsp"},
            {"name":"Coriander Powder","quantity":"1 tbsp"},
            {"name":"Garam Masala","quantity":"1/2 tsp"},
            {"name":"Kasuri Methi","quantity":"1 tsp"},
            {"name":"Curd","quantity":"30 g"},
            {"name":"Fresh Cream","quantity":"1 tbsp (optional)"},
            {"name":"Oil","quantity":"2 tbsp"},
            {"name":"Salt","quantity":"to taste"},
            {"name":"Coriander Leaves","quantity":"3-4 sprigs"},
            {"name":"Whole Wheat Flour (for chapati)","quantity":"3-4 cups"},
            {"name":"Water","quantity":"2-3 cups (for dough)"},
            {"name":"Ghee / Oil (for cooking)","quantity":"1 tsp optional"},
            {"name":"Wet cotton cloth","quantity":"for covering dough"}
        ],
        "steps": [
            "Turn the burner ON and place a heavy-bottomed pan on the burner.",
            "Pour 2 tbsp oil into the pan and let it heat for 30-45 seconds.",
            "Add 1 tsp cumin seeds and wait for them to crackle.",
            "Add chopped onions and sauté on medium flame until they turn golden brown (about 6-8 minutes).",
            "Add 1 tbsp ginger-garlic paste and sauté for 1 minute until raw smell disappears.",
            "Add tomato puree, mix, and cook until oil starts separating from the masala (approx 6-8 minutes).",
            "Add turmeric (1/4 tsp), red chilli (1/2 tsp), coriander powder (1 tbsp) and salt; stir and cook 1-2 minutes.",
            "Turn the burner to LOW, add 30 g curd and stir continuously to avoid curdling.",
            "Add 200 g paneer cubes, mix gently so paneer doesn’t break. Add 1/2 tsp garam masala and kasuri methi; simmer for 4-5 minutes on LOW.",
            "Optional: add 1 tbsp fresh cream, mix and cook for 1 minute.",
            "Turn the burner OFF and garnish with coriander leaves. Keep curry covered and warm.",
            "For chapati: place a mixing bowl, add 3-4 cups whole wheat flour, a pinch of salt and 2-3 cups water gradually. Knead into a soft pliable dough.",
            "Cover the dough with a wet cotton cloth and let it rest for 10 minutes.",
            "After resting, divide dough into equal small balls, roll into flat discs using a rolling pin on a lightly floured surface.",
            "Turn the burner ON and heat a tawa (flat griddle). Place the rolled chapati on the hot tawa.",
            "Cook until small bubbles form, flip and cook the other side until brown spots appear. Apply a little ghee or oil if desired.",
            "Remove chapati, keep covered in a cloth to keep soft. Repeat for remaining dough.",
            "Serve hot paneer curry with freshly made chapatis."
        ],
        "created_at": now_iso()
    }

# ---------------------------
# 3) Synthetic recipes (20)
# ---------------------------
SYNTHETIC_NAMES = [
    "Veg Fried Rice", "Masala Dosa", "Aloo Paratha", "Chicken Curry", "Egg Bhurji",
    "Dal Tadka", "Chole Bhature", "Pasta Alfredo", "Veg Biryani", "Sambar Rice",
    "Poha", "Upma", "Roti Sabzi", "Paneer Butter Masala", "Mixed Veg Curry",
    "Tomato Soup", "Veg Sandwich", "Fruit Salad", "Jeera Rice", "Curd Rice"
]

def make_synthetic_recipe(idx, name):
    recipe_index = idx
    return {
        "recipe_id": recipe_doc_id(recipe_index, name),
        "name": name,
        "description": f"Synthetic recipe for {name} used for testing and analytics.",
        "category": random.choice(["Indian", "Indian/International", "International"]),
        "difficulty": random.choice(["Easy", "Medium", "Hard"]),
        "prep_time": random.randint(8, 40),
        "cook_time": random.randint(5, 60),
        "servings": random.randint(1, 6),
        "ingredients": [
            {"name": f"{name} Ingredient A", "quantity": "1 unit"},
            {"name": f"{name} Ingredient B", "quantity": "2 units"},
            {"name": "Salt", "quantity": "to taste"},
            {"name": "Oil", "quantity": "1 tbsp"}
        ],
        "steps": [
            "Turn burner ON and place pan.",
            f"Add oil and sauté the base for {name}.",
            "Add main ingredients and cook thoroughly.",
            "Turn burner OFF and let rest",
            "Serve hot."
        ],
        "created_at": now_iso()
    }

# ---------------------------
# 4) Insert recipes (primary first, then synthetic)
# ---------------------------
def create_recipes():
    print("Creating recipes (primary first, then synthetic)...")
    # Primary:
    primary = get_primary_recipe()
    db.collection("recipes").document(primary["recipe_id"]).set(primary)
    # Synthetic: recipe2 ... recipe21
    idx = 2
    for name in SYNTHETIC_NAMES[:NUM_SYNTHETIC_RECIPES]:
        rec = make_synthetic_recipe(idx, name)
        db.collection("recipes").document(rec["recipe_id"]).set(rec)
        idx += 1
    print(f"Created {1 + NUM_SYNTHETIC_RECIPES} recipes (recipe1..recipe{1+NUM_SYNTHETIC_RECIPES})\n")

# ---------------------------
# 5) Create interactions (interaction1, interaction2, ...)
#    At least 2 per recipe; deterministic ascending order
# ---------------------------
def create_interactions():
    print("Creating interactions (ascending interaction IDs)...")
    # deterministic lists
    recipe_ids = []
    # primary (recipe1...) then recipe2..recipe21
    # Build list exactly in ascending order
    recipe_ids.append(recipe_doc_id(1, "Paneer Curry with Chapati"))
    idx = 2
    for name in SYNTHETIC_NAMES[:NUM_SYNTHETIC_RECIPES]:
        recipe_ids.append(recipe_doc_id(idx, name))
        idx += 1

    user_ids = [user_doc_id(i) for i in range(1, NUM_USERS + 1)]

    interaction_seq = 1
    # For each recipe, create exactly MIN_INTERACTIONS_PER_RECIPE interactions (you can expand later)
    for rid in recipe_ids:
        # create 2 deterministic interactions using different users
        # choose users in round-robin for deterministic distribution
        for k in range(MIN_INTERACTIONS_PER_RECIPE):
            uid = user_ids[(interaction_seq - 1) % len(user_ids)]
            inter_doc = {
                "interaction_id": interaction_doc_id(interaction_seq),
                "recipe_id": rid,
                "user_id": uid,
                "views": random.randint(1, 200),
                "likes": random.choice([0, 1]),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "cook_attempts": random.randint(0, 4),
                "timestamp": now_iso()
            }
            # Write with the requested sequential interaction ID
            db.collection("interactions").document(inter_doc["interaction_id"]).set(inter_doc)
            interaction_seq += 1

    print(f"Created {interaction_seq - 1} interactions (at least {MIN_INTERACTIONS_PER_RECIPE} per recipe)\n")

# ---------------------------
# MAIN
# ---------------------------
def run_all():
    t0 = time.time()
    create_users()
    create_recipes()
    create_interactions()
    elapsed = time.time() - t0
    print("Seeding completed in {:.2f}s".format(elapsed))

if __name__ == "__main__":
    run_all()
