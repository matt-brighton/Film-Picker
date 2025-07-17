import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def get_films():
    with open("films.json") as films:
        data=json.load(films)

    return data.get("films", [])


def get_film_info(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)

    if not response.ok:
        print(f"TMDB API Error {response.status_code}: {response.text}")
        return None

    data = response.json()
    print(data)

    return {
        "title": data.get("title"),
        "tagline": data.get("tagline"),
        "overview": data.get("overview"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "release_date": data.get("release_date"),
        "runtime": data.get("runtime"),
        "vote_average": data.get("vote_average"),
        "poster_url": f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
        "backdrop_url": f"https://image.tmdb.org/t/p/w780{data['backdrop_path']}" if data.get("backdrop_path") else None,
        "status": data.get("status"),
        "language": data.get("original_language"),
        "country": [c["name"] for c in data.get("production_countries", [])],
        "production_companies": [p["name"] for p in data.get("production_companies", [])],
        "revenue": data.get("revenue"),
        "budget": data.get("budget"),
        "imdb_id": data.get("imdb_id"),
        "homepage": data.get("homepage")
        
    }
