import pandas as pd

#append two csvs
# csv1 = pd.read_csv("/Users/richasirwani/Downloads/dishes_seed.csv")
# csv2 = pd.read_csv("/Users/richasirwani/Downloads/dishes_extended_50.csv")
# final_df = pd.concat([csv1, csv2]).to_csv("data/dishes_combined.csv", index=False)
#convert to csv and save in data folder
def score_by_calories(df, target_calories):
    """Return dishes sorted by closeness to target_calories, with a distance column."""
    df = df.copy()
    # Done: compute abs distance for every row
    df["calorie_distance"] = abs(target_calories - df["calories"])
    return df.sort_values("calorie_distance")

def score_by_ingredients(df, user_ingredients):
    """Return dishes sorted by how well they match user_ingredients, with a match_score column."""
    df = df.copy()
    user_set = set(i.strip().lower() for i in user_ingredients)

    def overlap_score(dish_ingredients_str):
        dish_set = set(i.strip().lower() for i in dish_ingredients_str.split(","))
        # Done: compute intersection-over-dish-size score using dish_set and user_set
        return len(user_set & dish_set) / len(user_set)

    df["match_score"] = df["ingredients"].apply(overlap_score)
    return df.sort_values("match_score", ascending=False)

def recommend(df, target_calories=None, user_ingredients=None, allergens_to_avoid=None):
    df = df.copy()

    # 1. Hard filter: allergies (runs first, no exceptions)
    if allergens_to_avoid:
        for allergen in allergens_to_avoid:
            # TODO: filter out rows where df["allergens"] contains this allergen
            df = df[~df["allergens"].str.contains(allergen, na=False)]

    # 2. Soft scoring: whichever mode applies
    if target_calories is not None:
        df = score_by_calories(df, target_calories)
    if user_ingredients is not None:
        df = score_by_ingredients(df, user_ingredients)

    return df.head(3)

# --- test cases, should pass once you fill in the TODOs ---
df = pd.read_csv("data/dishes_combined.csv")

# result1 = score_by_calories(df, target_calories=500)
# assert result1.iloc[0]["calorie_distance"] >= 0, "distance should never be negative"
# print(result1[["dish", "calories", "calorie_distance"]].head(3))
#
# result2 = score_by_ingredients(df, user_ingredients=["rice", "tur dal", "tomato"])
# assert 0 <= result2.iloc[0]["match_score"] <= 1, "score should be between 0 and 1"
# print(result2[["dish", "ingredients", "match_score"]].head(3))

top3_df = recommend(df, target_calories=500, user_ingredients=["sabudana", "peanuts", "potato", "cumin"], allergens_to_avoid=["dairy"])
print(top3_df[["dish","allergens","calories","ingredients"]].head())