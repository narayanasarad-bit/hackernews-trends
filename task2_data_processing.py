import pandas as pd
import os

# -----------------------------------
# STEP 1: LOAD JSON FILE
# -----------------------------------
file_path = "data/trends_20260413.json"

if not os.path.exists(file_path):
    print("Error: JSON file not found!")
    exit()

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")


# -----------------------------------
# STEP 2: CLEAN DATA
# -----------------------------------

df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

df = df.dropna(subset=["post_id", "title", "score", "num_comments"])
print(f"After removing nulls: {len(df)}")

df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

df["title"] = df["title"].astype(str).str.strip()


# -----------------------------------
# STEP 3: SAVE CSV
# -----------------------------------
os.makedirs("data", exist_ok=True)

output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")


# -----------------------------------
# STEP 4: SUMMARY
# -----------------------------------
print("\nStories per category:")
print(df["category"].value_counts())
