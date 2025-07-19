import streamlit as st
import pandas as pd
import json
from utils import get_films

films = get_films()

df = pd.DataFrame(films)

st.title("Manage Lists")
st.dataframe(df)




