import streamlit as st
from ai_call import get_portfolio, parse_investments, save_portfolio, load_all_portfolios, check_existing_portfolio
import plotly.express as px

def home_page():
    st.title("Home")
    st.write("Welcome to the Home page!")

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

def display_portfolio(investments):
    # Display a clean breakdown of the portfolio
    for inv in investments:
        st.subheader(inv['asset_name'])
        st.write(f"**Ticker**: {inv['ticker']}")
        st.write(f"**Allocation**: {inv['allocation']}")
        st.write(f"**Category**: {inv['category']}")
        st.write(f"**Rationale**: {inv['rationale']}")
        st.write("---")

    # Display the pie chart
    display_pie_chart(investments)

def display_pie_chart(investments):
    labels = [inv['asset_name'] for inv in investments]
    sizes = [float(str(inv['allocation']).replace('%', '')) for inv in investments]

    fig = px.pie(
        values=sizes,
        names=labels,
        title='Portfolio Allocation',
        hole=0.3
    )

    st.plotly_chart(fig)
