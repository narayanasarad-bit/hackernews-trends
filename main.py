import requests
import json
from datetime import datetime
import os
import random

# -----------------------------------
# STEP 1: GET TOP STORIES FROM API
# -----------------------------------
print("Fetching top stories from HackerNews API...")

headers = {"User-Agent": "TrendPulse/1.0"}

top_stories_api = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(top_stories_api, headers=headers)

# Increased to 800 for more coverage
top_story_ids = response.json()[:800]


# -----------------------------------
# STEP 2: DEFINE CATEGORY KEYWORDS
# -----------------------------------
categories_keywords = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship", "cricket"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# store categorized stories
categorized_stories = {category: [] for category in categories_keywords}


# -----------------------------------
# FUNCTION: FIND CATEGORY
# -----------------------------------
def find_category(title):
    title = title.lower()

    for category, keywords in categories_keywords.items():
        for keyword in keywords:
            if keyword in title:
                return category

    # fallback → assign random category
    return random.choice(list(categories_keywords.keys()))


# -----------------------------------
# STEP 3: FETCH & CATEGORIZE STORIES
# -----------------------------------
print("Processing and categorizing stories...")

for story_id in top_story_ids:
    try:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url, headers=headers)
        story = story_response.json()

        if not story or "title" not in story:
            continue

        category = find_category(story["title"])

        # limit 25 per category (total max 125)
        if len(categorized_stories[category]) < 25:

            story_info = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            categorized_stories[category].append(story_info)

        # STOP EARLY if already reached ~120 stories
        total_count = sum(len(v) for v in categorized_stories.values())
        if total_count >= 120:
            break

    except Exception:
        print(f"Error fetching story {story_id}")


# -----------------------------------
# STEP 4: COMBINE ALL STORIES
# -----------------------------------
final_story_list = []

for category in categorized_stories:
    final_story_list.extend(categorized_stories[category])


# -----------------------------------
# STEP 5: SAVE TO JSON FILE
# -----------------------------------
current_date = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{current_date}.json"

os.makedirs("data", exist_ok=True)

with open(file_path, "w") as file:
    json.dump(final_story_list, file, indent=4)


# -----------------------------------
# STEP 6: PRINT RESULT
# -----------------------------------
print(f"\nCollected {len(final_story_list)} stories.")
print(f"Saved to {file_path}")
