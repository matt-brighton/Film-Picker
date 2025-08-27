import json
import requests
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path
import os

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY") or st.secrets["TMDB_API_KEY"]

FILM_LIST_DIRECTORY =  Path("film_lists")



def get_film_directory():
    film_files = []
    for film_file in FILM_LIST_DIRECTORY.glob("*.json"):
        film_files.append(film_file.name)
    film_files.sort()
    
    formatted_film_files = [] 
    for film_file in film_files:
        name = film_file.replace(".json", "")
        name = name.replace("_", " ").replace("-", " ")
        formatted_film_files.append(name.title())
    
    return film_files, formatted_film_files

def get_films(selected_file):
    filepath = FILM_LIST_DIRECTORY / selected_file
    with open(filepath, "r", encoding="utf-8") as films:
        data=json.load(films)

    return data.get("films", [])


def get_film_info(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)

    if not response.ok:
        print(f"TMDB API Error {response.status_code}: {response.text}")
        return None

    data = response.json()

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


def get_watch_providers(tmdb_id, region: str="GB"):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    
    if not response.ok:
        print(f"TMDB API Error {response.status_code}: {response.text}")
        return None
    
    data = response.json().get("results", {})
    base = "https://image.tmdb.org/t/p/"
    
    return {
            "link": data.get("link"),
            "flatrate": [
                {
                    "provider_id": p["provider_id"],
                    "provider_name": p["provider_name"],
                    "logo_url": f"{base}w45{p['logo_path']}" if p.get("logo_path") else None,
                    "display_priority": p.get("display_priority"),
                }
                for p in sorted(data.get("flatrate", []), key=lambda x: x.get("display_priority", 999))
            ],
        "rent": [
            {
                "provider_id": p["provider_id"],
                "provider_name": p["provider_name"],
                "logo_url": f"{base}w45{p['logo_path']}" if p.get("logo_path") else None,
                "display_priority": p.get("display_priority"),
            }
            for p in sorted(data.get("rent", []), key=lambda x: x.get("display_priority", 999))
        ],
        "buy": [
            {
                "provider_id": p["provider_id"],
                "provider_name": p["provider_name"],
                "logo_url": f"{base}w45{p['logo_path']}" if p.get("logo_path") else None,
                "display_priority": p.get("display_priority"),
            }
            for p in sorted(data.get("buy", []), key=lambda x: x.get("display_priority", 999))
        ],
        "ads": [
            {
                "provider_id": p["provider_id"],
                "provider_name": p["provider_name"],
                "logo_url": f"{base}w45{p['logo_path']}" if p.get("logo_path") else None,
                "display_priority": p.get("display_priority"),
            }
            for p in sorted(data.get("ads", []), key=lambda x: x.get("display_priority", 999))
        ],
        "free": [
            {
                "provider_id": p["provider_id"],
                "provider_name": p["provider_name"],
                "logo_url": f"{base}w45{p['logo_path']}" if p.get("logo_path") else None,
                "display_priority": p.get("display_priority"),
            }
            for p in sorted(data.get("free", []), key=lambda x: x.get("display_priority", 999))
        ],
        }
