import streamlit as st
import pandas as pd
import json
from utils import get_films, get_film_directory

raw_files, formatted_files = get_film_directory()
file_map = dict(zip(formatted_files, raw_files))

st.title("Manage Lists")
selected_film_list = st.selectbox("Choose a List", (formatted_files))
selected_file = file_map[selected_film_list]
if st.button("Select List", type="primary"):
    films = get_films(selected_file)
    data = pd.DataFrame(films)
    st.dataframe(data)
