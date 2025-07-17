from dotenv import load_dotenv
import os
import streamlit as st
# https://jnbk3wnuzk2wpvtczpuwmc.streamlit.app

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(
    page_title="Film Picker"
)

st.title("Welcome to the Film Picker")
st.write("Please use the sidebar to navigate!")
