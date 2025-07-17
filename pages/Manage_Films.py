import streamlit as st
import pandas as pd
import json

with open("films.json") as films:
    data = json.load(films)

films = data["films"]
df = pd.DataFrame(films)

st.title("Manage Films")
st.dataframe(df)




