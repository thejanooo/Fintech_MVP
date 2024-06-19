import streamlit as st
from groq import Groq
import os
import json
import plotly.express as px

groq_api = "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"
client = Groq(api_key=groq_api)

def home_page():
    st.title("Home")
    st.write("Welcome to the Home page!")

    with st.form(key='user_form'):
        age = st.number_input("Age", min_value=0, max_value=100, value=30)
        income = st.number_input("Income", min_value=0)
        monthly_contribution = st.number_input("Monthly Contribution", min_value=0)
        retirement_age = st.number_input("Retirement Age", min_value=0, max_value=100, value=65)
        
        ethical_values = st.multiselect(
            "Ethical Values",
            options=["Green Energy", "No Fossil", "No Tobacco", "Inclusive", "Promotes Social Equity"]
        )
        
        risk_aversion = st.slider("Risk Aversion", min_value=0, max_value=10, value=5)

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        user_data = {
            "age": age,
            "income": income,
            "monthly_contribution": monthly_contribution,
            "retirement_age": retirement_age,
            "ethical_values": ethical_values,
            "risk_aversion": risk_aversion
        }

        ai_response = get_portfolio(user_data)

        if ai_response:
            st.write("### AI-Generated Portfolio")
            st.write(ai_response)

            # Parse the AI response
            investments = parse_investments(ai_response)

            if investments:
                # Display the pie chart
                display_pie_chart(investments)

                # Save the results (user data and AI response)
                save_results(user_data, ai_response)
            else:
                st.error("Failed to parse investment details from the AI response. Please try again.")
        else:
            st.error("Failed to generate portfolio. Please try again.")

def get_portfolio(user_data):
    user_message = (
        f"Create a diversified investment portfolio for a client with the following details:\n"
        f"Age: {user_data['age']}\n"
        f"Income: {user_data['income']}\n"
        f"Monthly Contribution: {user_data['monthly_contribution']}\n"
        f"Retirement Age: {user_data['retirement_age']}\n"
        f"Ethical Values: {', '.join(user_data['ethical_values'])}\n"
        f"Risk Aversion (0 to 10): {user_data['risk_aversion']}\n"
        "Please ensure the portfolio includes a mix of stocks, bonds, and cash, and provide recommendations for other suitable investments. "
        "Each investment should be listed in the following format: "
        '{"asset Name": "Asset Name", "ticker": "Ticker", "allocation": "X%","Category of asset":"Category", "rationale": "Reason for choosing this asset"}. '
        "Ensure that all tickers are accurate and can be found on Yahoo Finance."
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in financial advice. Your task is to generate a comprehensive investment portfolio for a client based on the details provided. "
                    "The portfolio should include a balanced mix of stocks, bonds, cash, and other investment options. "
                    "Output should be in valid JSON format without any text around the JSON output. "
                    "Tickers should be the ones used on Yahoo Finance, in the format 'AAPL', 'GOOGL', 'MSFT', etc. "
                    "Only output the investment recommendations and rationale. "
                    "Make sure to consider the client's age, income, monthly contribution, retirement age, ethical values, and risk aversion. "
                    "Each investment should be listed in the following format: "
                    '{"asset Name": "Asset Name", "ticker": "Ticker", "allocation": "X%","Category of asset":"Category", "rationale": "Reason for choosing this asset"}. '
                    "Ensure that all tickers are accurate and can be found on Yahoo Finance."
                )
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="llama3-8b-8192", 
        seed=42
    )

    ai_response = chat_completion.choices[0].message.content

    return ai_response

def parse_investments(ai_response):
    try:
        # Debugging: Print the AI response to inspect it
        st.write("### Debugging: AI Response")
        st.write(ai_response)

        # Attempt to correct common issues with JSON formatting
        ai_response = ai_response.replace('\n', '')
        ai_response = ai_response.replace('", "', '", "')

        # Extract the allocation details from the AI response
        investments = json.loads(ai_response)
        
        # Check the structure of investments
        if isinstance(investments, dict):
            investments = [{"asset Name": key, **value} for key, value in investments.items()]
        
        return investments
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error: {e}")
    except Exception as e:
        st.error(f"Error parsing AI response: {e}")
        st.write(ai_response)
    return None

def display_pie_chart(investments):
    labels = [inv['asset Name'] for inv in investments]
    sizes = [float(inv['allocation'].replace('%', '')) for inv in investments]

    fig = px.pie(
        values=sizes,
        names=labels,
        title='Portfolio Allocation',
        hole=0.3
    )

    st.plotly_chart(fig)

def save_results(user_data, ai_response):
    results = {
        "user_data": user_data,
        "ai_response": ai_response
    }

    with open("results.json", "a") as f:
        f.write(json.dumps(results) + "\n")
