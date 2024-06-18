import streamlit as st
import pandas as pd
import numpy as np
import os
from AI_call import Groq

groq_api = "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"

client = Groq(api_key=groq_api)


# Mock function to generate AI-driven recommendations
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

