import basic
import eda1
import eda2
import eda3
import streamlit as st

PAGES = {
    "Goals": basic,
    "Basic Analytics": basic,
    "Exploratory Data Analysis": eda2,
    "Data Analysis at School Distric level": eda2,
    "Further Data Analysis at School level": eda2
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()