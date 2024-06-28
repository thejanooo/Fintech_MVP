import streamlit as st
from ai_call import get_portfolio, parse_investments, save_portfolio, load_all_portfolios, check_existing_portfolio
import plotly.express as px

def portfolio_creation_page():
    """
    Renders the portfolio creation page.

    This function displays a form where users can input their portfolio details such as name, age, initial investment,
    monthly contribution, retirement age, ethical values, and risk aversion. Upon submitting the form, the function
    checks if a portfolio with the same user data already exists. If it does, the existing portfolio is displayed.
    Otherwise, the function calls an AI model to generate a portfolio based on the user data, parses the AI response,
    and saves the portfolio to a file.

    Returns:
        None
    """
    st.markdown(
        """
        <h2 style="text-align: center;">
            Retire<span style="color: #538786;">Wise</span>
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.title("Portfolio Creation")
    st.write("Welcome to RetireWise! Your personalized path to a secure future. Let's create your portfolio.")

    with st.form(key='user_form'):
        portfolio_name = st.text_input("Portfolio Name", value="")
        age = st.number_input("Age", min_value=0, max_value=100, value=30)
        Initial_investment = st.number_input("Initial investment", min_value=0)
        monthly_contribution = st.number_input("Monthly Contribution", min_value=0)
        retirement_age = st.number_input("Retirement Age", min_value=0, max_value=100, value=65)
        
        ethical_values = st.multiselect(
            "Ethical Values",
            options=["Green Energy", "No Fossil", "No Tobacco", "Inclusive", "Promotes Social Equity"]

        )
        
        risk_aversion = st.selectbox(
            "Risk Aversion",
            options=["Low", "Neutral", "High"]
        )
        
        submit_button = st.form_submit_button(label='Create Portfolio')

    if submit_button:
        if not portfolio_name:
            st.error("Please provide a name for your portfolio.")
        else:
            user_data = {
                "age": age,
                "Initial_investment": Initial_investment,
                "monthly_contribution": monthly_contribution,
                "retirement_age": retirement_age,
                "ethical_values": ethical_values,
                "risk_aversion": risk_aversion
            }

            # Check if the portfolio for the given user data already exists
            existing_portfolio = check_existing_portfolio(user_data)
            if existing_portfolio:
                st.success("A portfolio with the same user data already exists.")
                st.session_state.portfolio = existing_portfolio
            else:
                ai_response = get_portfolio(user_data)

                if ai_response:
                    # Parse the AI response
                    investments = parse_investments(ai_response)

                    if investments:
                        # Save the portfolio to a file along with user data and name
                        save_portfolio(user_data, investments, portfolio_name)
                        st.session_state.portfolio = investments
                        st.success("Portfolio generated and saved successfully!")
                    else:
                        st.error("Failed to parse investment details from the AI response. Please try again.")
                else:
                    st.error("Failed to generate portfolio. Please try again.")
