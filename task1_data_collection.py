import requests
import json
import os
import time
from datetime import datetime



get_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}



response = requests.get(
    get_url,
    headers=headers,
    timeout=10
)

story_ids = response.json()


story_ids = story_ids[:500]

print("Got", len(story_ids), "story IDs")


categories = {

    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}




stories = []


category_counts = {

    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}


used_ids = set()



for story_id in story_ids:

    
    if len(stories) >= 100:
        break


    story_url = (
        f"https://hacker-news.firebaseio.com/"
        f"v0/item/{story_id}.json"
    )


    try:

        response = requests.get(
            story_url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        story = response.json()


    except requests.RequestException:

        print("Failed to fetch story", story_id)

        continue




    title = story.get("title", "")


    if not title:
        continue


    matching_categories = []


    for name, keywords in categories.items():

        
        if category_counts[name] >= 25:
            continue


        for keyword in keywords:

            if keyword.lower() in title.lower():

                matching_categories.append(name)

                break


    if not matching_categories:
        continue




    category = min(
        matching_categories,
        key=lambda name: category_counts[name]
    )




    if story_id in used_ids:
        continue




    story_data = {

        "post_id": story.get("id"),

        "title": title,

        "category": category,

        "score": story.get("score", 0),

        "num_comments": story.get(
            "descendants",
            0
        ),

        "author": story.get("by"),

        "collected_at": datetime.now().isoformat()
    }


  
    stories.append(story_data)

    used_ids.add(story_id)


  
    category_counts[category] += 1


    print(
        category,
        category_counts[category],
        "/25:",
        title
    )




print()

for category in categories:

    print(
        "Finished",
        category,
        "-",
        category_counts[category]
    )

    time.sleep(2)




os.makedirs(
    "data",
    exist_ok=True
)




data = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{data}.json"



with open(
    filename,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        stories,
        file,
        indent=4
    )



print()

print(
    "Collected",
    len(stories),
    "stories."
)

print(
    "Saved to",
    filename
)


print()

print("Category totals:")


for category, count in category_counts.items():

    print(
        category,
        ":",
        count
    )