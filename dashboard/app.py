import eda1
import eda2
import eda3
import streamlit as st

PAGES = {
    "EDA1": eda1,
    "EDA2": eda2,
    "EDA3": eda2
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()