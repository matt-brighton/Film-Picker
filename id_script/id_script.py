import requests
import json
import time
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY") or st.secrets["TMDB_API_KEY"]


SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

with open("films_without_ids.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output = []

x=1

for film in data["films"]:
    print(x)
    x += 1
    title = film["title"]
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "include_adult": False
    }

    try:
        response = requests.get(SEARCH_URL, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])

        if results:
            best_match = results[0]
            output.append({
                "title": title,
                "tmdb_id": best_match["id"]
            })
        else:
            print(f"No result for: {title}")
            output.append({
                "title": title,
                "tmdb_id": None
            })

        time.sleep(0.25)

    except Exception as e:
        print(f"Error searching for {title}: {e}")
        output.append({
            "title": title,
            "tmdb_id": None
        })

with open("films_with_ids.json", "w", encoding="utf-8") as f:
    json.dump({"films": output}, f, indent=2)

print("Done. Results saved to 'films_with_ids.json'.")
