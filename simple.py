import streamlit as st
from streamlit_option_menu import option_menu

# Horizontal side bar
selected = option_menu(
    menu_title='',
    options=['Home', 'About', 'Contact'],
    icons=['🏠', '📚', '📧'],
    default_index=0,
    orientation='horizontal'
)

if selected =="Home":
    st.title(f"You have selected {selected}")
if selected == "About":
    st.title(f"You have selected {selected}")
if selected =="Contact":
    st.title(f"You have selected {selected}")

