import streamlit as st
from streamlit_authenticator.utilities.exceptions import (LoginError, RegisterError)
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np


def generate_recommendations(salary, spending, savings_goal, age, retirement_age, risk_aversion):
    # This function is a placeholder for the AI model
    # Here we generate a simple mock portfolio
    np.random.seed(42)
    years_to_invest = retirement_age - age
    recommendations = {
        'Stocks': np.random.uniform(0.5, 0.7),
        'Bonds': np.random.uniform(0.2, 0.4),
        'ETFs': np.random.uniform(0.1, 0.3),
        'Cash': np.random.uniform(0.0, 0.1)
    }
    return recommendations

# Function to display login widget
def login_widget(authenticator):
    st.header("Login")
    try:
        name, authentication_status, username = authenticator.login('main')
        if authentication_status:
            st.session_state["authentication_status"] = True
            st.session_state["name"] = name
            st.session_state["username"] = username
            st.success(f'Welcome {name}')
        elif authentication_status == False:
            st.session_state["authentication_status"] = False
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.session_state["authentication_status"] = None
            st.warning('Please enter your username and password')
    except LoginError as e:
        st.error(e)

    if st.session_state.get("authentication_status"):
        authenticator.logout('Logout', 'sidebar')
        st.write(f'Welcome *{st.session_state["name"]}*')
        # Mock function to generate AI-driven recommendations


        # Title of the app
        st.title("RetireWise: Your Personalized Path to a Secure Future")

        # User input for generating recommendations
        st.header("Provide Your Information")
        salary = st.number_input("Annual Salary ($)", min_value=0, value=50000, step=1000)
        spending = st.number_input("Annual Spending ($)", min_value=0, value=30000, step=1000)
        savings_goal = st.number_input("Savings Goal ($)", min_value=0, value=500000, step=10000)
        age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
        retirement_age = st.number_input("Planned Retirement Age", min_value=50, max_value=100, value=65)
        risk_aversion = st.slider("Risk Aversion (0 = Low, 100 = High)", min_value=0, max_value=100, value=50)

        # Button to generate recommendations
        if st.button("Generate Investment Plan"):
            recommendations = generate_recommendations(salary, spending, savings_goal, age, retirement_age, risk_aversion)
            st.subheader("Your Personalized Investment Plan")
            st.write("Based on the information you provided, here is your recommended portfolio allocation:")
            
            for asset, allocation in recommendations.items():
                st.write(f"{asset}: {allocation:.2%}")

            # Mock data for portfolio projection
            years = list(range(1, retirement_age - age + 1))
            portfolio_value = np.cumsum([salary - spending] * len(years)) * (1 + np.random.normal(0.05, 0.02, len(years)))

            # Visualization of portfolio growth
            st.subheader("Projected Portfolio Growth")
            df = pd.DataFrame({'Year': years, 'Portfolio Value ($)': portfolio_value})
            st.line_chart(df.set_index('Year'))

# Function to display registration widget
def registration_widget(authenticator):
    st.header("Register")
    try:
        (email_of_registered_user,
            username_of_registered_user,
            name_of_registered_user) = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except RegisterError as e:
        st.error(e)

# Landing page with welcome message and buttons
def landing_page():
    st.title("Hello, welcome to the app")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            st.session_state.page = "login"
    with col2:
        if st.button("Register"):
            st.session_state.page = "register"
