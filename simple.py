import streamlit as st
from streamlit_option_menu import option_menu
from home import home_page
from portfolio import portfolio_page
from simulation import simulation_page
from login import main as login_main

st.set_page_config(layout="wide")

# Initialize user authentication
login_main()




# Initialize session state if not already done
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = None

# Horizontal side bar
selected = option_menu(
    menu_title='',
    options=['Home', 'Portfolio', 'Simulation'],
    default_index=0,
    orientation='horizontal',
)

if selected == "Home":
    home_page()
elif selected == "Portfolio":
    portfolio_page()
elif selected == "Simulation":
    simulation_page()
