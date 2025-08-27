import os
import streamlit as st
import random
from utils import get_films, get_film_info, get_film_directory, get_watch_providers

# ----- Setup & list selection -----
raw_files, formatted_files = get_film_directory()
file_map = dict(zip(formatted_files, raw_files))

st.set_page_config(page_title="Film Picker 🎬")
st.title("Film Picker")

selected_film_list = st.selectbox("Choose a List", (formatted_files))
selected_file = file_map[selected_film_list]

# Region picker for watch providers (TMDB uses ISO country codes)
region = st.selectbox(
    "Watch region", ["GB", "US", "CA", "AU", "DE", "FR", "IT", "ES"], index=0)

# ----- UI helpers -----


def render_provider_bucket(title: str, items: list):
    if not items:
        return
    st.write(title + ":")
    cols = st.columns(min(len(items), 6))
    for i, p in enumerate(items):
        with cols[i % len(cols)]:
            logo = p.get("logo_url")
            name = p.get("provider_name", "Unknown")
            if logo:
                st.image(logo, width=32)
            st.caption(name)


# ----- Main action -----
if st.button("Time to Pick!", icon="🎬", type="primary"):
    with st.spinner("Wait for it..."):
        films = get_films(selected_file)
        if not films:
            st.warning("That list is empty. Add some films first.")
            st.stop()

        film_choice = random.choice(films)
        film_info = get_film_info(film_choice.get("tmdb_id"))
        providers = get_watch_providers(
            film_choice.get("tmdb_id"), region=region)

    if film_info:
        # Title & basics
        st.header(film_info.get("title") or "Untitled")
        if film_info.get("tagline"):
            st.caption(film_info["tagline"])
        if film_info.get("poster_url"):
            st.image(film_info["poster_url"], width=250)

        if film_info.get("overview"):
            st.write(film_info["overview"])
        if film_info.get("genres"):
            st.write("🎬 Genres:", ", ".join(film_info["genres"]))
        if film_info.get("release_date"):
            st.write("🗓 Release Date:", film_info["release_date"])
        if isinstance(film_info.get("runtime"), int):
            st.write("⏱ Runtime:", f"{film_info['runtime']} mins")
        if film_info.get("vote_average") is not None:
            st.metric("⭐ Rating", round(film_info["vote_average"], 1))
        if film_info.get("production_companies"):
            st.write("🏢 Production:", ", ".join(
                film_info["production_companies"]))

        # Watch providers (sorted + logos)
        st.subheader("Where to watch")
        if providers:
            render_provider_bucket(
                "Included with subscription", providers.get("flatrate", []))
            render_provider_bucket("Rent", providers.get("rent", []))
            render_provider_bucket("Buy", providers.get("buy", []))
            render_provider_bucket("Free (ads)", providers.get("ads", []))
            render_provider_bucket("Free", providers.get("free", []))

            if providers.get("link"):
                st.link_button("More ways to watch (TMDB)",
                               providers["link"], type="secondary")
        else:
            st.info(f"No {region} streaming options found.")
    else:
        st.error("Couldn't fetch movie details from TMDB 😔")
