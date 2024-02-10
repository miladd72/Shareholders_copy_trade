import pandas as pd
import streamlit as st
# from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",  # Set layout to wide mode
    initial_sidebar_state="expanded",  # Optionally, expand the sidebar by default
)

st.write("# Welcome to Share holders  Dashboard! 👋")

# st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is a dashboard for stock shareholders project \n
    **👈 Select pages from the sidebar** to see other pages

"""
)

