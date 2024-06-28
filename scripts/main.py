import streamlit as st
from scripts.home_page import introduction_page
from scripts.portfolio_creation import portfolio_creation_page
from scripts.portfolio import portfolio_page
from scripts.simulation import simulation_page

# Sidebar for navigation
st.sidebar.markdown(
    """
    <h2 style="text-align: left;">
        Retire<span style="color: #538786;">Wise</span>
    </h2>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
page = st.sidebar.selectbox(
    " ",
    ("🏡 Home", "🛠️ Portfolio Creation", "📊 Portfolio", "📈 Simulation")
)

# Render selected page
if page == "🏡 Home":
    introduction_page()
elif page == "🛠️ Portfolio Creation":
    portfolio_creation_page()
elif page == "📊 Portfolio":
    portfolio_page()
elif page == "📈 Simulation":
    simulation_page()
