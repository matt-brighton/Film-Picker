from dotenv import load_dotenv
import os
import streamlit as st
import time
import random
from utils import get_films, get_film_info

st.set_page_config(page_title="Film Picker 🎬")

st.title("Welcome to the Film Picker")
st.write("Please use the sidebar to navigate!")

st.button("Reset")

if st.button("Or, let's pick a film!", icon="🎬", type="primary"):
    with st.spinner("Wait for it..."):
        films = get_films()
        film_choice = random.choice(films)
        st.write(film_choice)
        film_info = get_film_info(film_choice["tmdb_id"])
        st.write(film_info)

    if film_info:
        st.header(film_info["title"])
        if film_info["tagline"]:
            st.caption(film_info["tagline"])
        if film_info["poster_url"]:
            st.image(film_info["poster_url"], width=250)
        st.write(film_info["overview"])
        st.write("🎬 Genres:", ", ".join(film_info["genres"]))
        st.write("🗓 Release Date:", film_info["release_date"])
        st.write("⏱ Runtime:", f"{film_info['runtime']} mins")
        st.metric("⭐ Rating", film_info["vote_average"])
        st.write("🏢 Production:", ", ".join(film_info["production_companies"]))
    else:
        st.error("Couldn't fetch movie details from TMDB 😔")
