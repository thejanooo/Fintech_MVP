import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from auth import login_widget, registration_widget, landing_page

# Loading config file
with open('/Users/thomas/Documents/GitHub/Fintech_MVP/user.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Main app logic
if 'page' not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "login":
    login_widget(authenticator)
elif st.session_state.page == "register":
    registration_widget(authenticator)

# Saving config file
with open('/Users/thomas/Documents/GitHub/Fintech_MVP/user.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)
