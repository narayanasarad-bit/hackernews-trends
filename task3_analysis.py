import pandas as pd
import numpy as np

# -----------------------------
# STEP 1: LOAD DATA
# -----------------------------
file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# -----------------------------
# STEP 2: BASIC STATS
# -----------------------------
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score:", int(avg_score))
print("Average comments:", int(avg_comments))

# NumPy stats
scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score:", int(np.mean(scores)))
print("Median score:", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))
print("Max score:", int(np.max(scores)))
print("Min score:", int(np.min(scores)))

# -----------------------------
# STEP 3: EXTRA ANALYSIS
# -----------------------------
# Category with most stories
top_category = df["category"].value_counts().idxmax()
count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({count} stories)")

# Most commented story
top_story = df.loc[df["num_comments"].idxmax()]

print(f"\nMost commented story: \"{top_story['title']}\" - {top_story['num_comments']} comments")

# -----------------------------
# STEP 4: ADD NEW COLUMNS
# -----------------------------
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score

# -----------------------------
# STEP 5: SAVE FILE
# -----------------------------
output_path = "data/trends_analysed.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")
