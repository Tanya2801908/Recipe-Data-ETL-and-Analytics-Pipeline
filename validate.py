import csv
import os

# ---------------------- Helper: Load CSV ----------------------
def load_csv(file_name):
    rows = []
    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

# ---------------------- Validation Functions ----------------------

def validate_recipes(rows):
    required = ["recipe_id", "name", "category", "prep_time", "cook_time", "servings", "difficulty"]

    valid = 0
    invalid = 0

    for r in rows:
        if any(r[field] in ("", None) for field in required):
            invalid += 1
        else:
            valid += 1

    return valid, invalid


def validate_ingredients(rows):
    required = ["ingredient_id", "recipe_id", "ingredient_name", "quantity"]

    valid = 0
    invalid = 0

    for r in rows:
        if any(r[field] in ("", None) for field in required):
            invalid += 1
        else:
            valid += 1

    return valid, invalid


def validate_steps(rows):
    required = ["step_id", "recipe_id", "step_number", "instruction"]

    valid = 0
    invalid = 0

    for r in rows:
        # step_number should be numeric
        if any(r[field] in ("", None) for field in required):
            invalid += 1
            continue

        try:
            int(r["step_number"])
            valid += 1
        except:
            invalid += 1

    return valid, invalid


def validate_interactions(rows):
    required = ["interaction_id", "user_id", "recipe_id", "views", "likes", "rating", "cook_attempts"]

    valid = 0
    invalid = 0

    for r in rows:
        if any(r[field] in ("", None) for field in required):
            invalid += 1
            continue

        # Validate numeric fields
        try:
            int(r["views"])
            int(r["likes"])
            float(r["rating"])
            int(r["cook_attempts"])
            valid += 1
        except:
            invalid += 1

    return valid, invalid


# ---------------------- Write Final Validation CSV ----------------------
def write_validation_report(results):
    output_file = "validation_report.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["collection", "valid", "invalid"])

        for collection, (valid_count, invalid_count) in results.items():
            writer.writerow([collection, valid_count, invalid_count])

    print(f"✅ Validation completed. Report saved as '{output_file}'")


# ---------------------- Main ----------------------
def run_validation():

    print("🔍 Validating CSV files...\n")

    # Load CSVs
    recipes = load_csv("recipes.csv")
    ingredients = load_csv("ingredients.csv")
    steps = load_csv("steps.csv")
    interactions = load_csv("interactions.csv")

    # Run validations
    results = {
        "recipes": validate_recipes(recipes),
        "ingredients": validate_ingredients(ingredients),
        "steps": validate_steps(steps),
        "interactions": validate_interactions(interactions)
    }

    # Create final CSV
    write_validation_report(results)

    print("\n🎉 Validation completed successfully!")


# ---------------------- Run ----------------------
if __name__ == "__main__":
    run_validation()







