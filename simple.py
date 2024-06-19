import streamlit as st
from streamlit_option_menu import option_menu
from home import home_page
from portfolio import portfolio_page
from profile_page import profile_page

# Initialize session state if not already done
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = None

# Horizontal side bar
selected = option_menu(
    menu_title='',
    options=['Home', 'Portfolio', 'Profile'],
    default_index=0,
    orientation='horizontal'
)

if selected == "Home":
    home_page()
elif selected == "Portfolio":
    portfolio_page()
elif selected == "Profile":
    profile_page()
