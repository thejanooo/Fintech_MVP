import streamlit as st
import plotly.express as px
from ai_call import load_all_portfolios

def portfolio_page():
    st.title("Portfolio")
    
    all_portfolios = load_all_portfolios()
    if not all_portfolios:
        st.warning("No portfolios generated yet. Please go to the Home page to generate a portfolio.")
        return
    
    # Allow the user to select a portfolio
    portfolio_options = [f"{portfolio['portfolio_name']} (Portfolio {i+1})" for i, portfolio in enumerate(all_portfolios)]
    selected_portfolio = st.selectbox("Select a portfolio to view", portfolio_options)
    
    if selected_portfolio:
        portfolio_index = portfolio_options.index(selected_portfolio)
        investments = all_portfolios[portfolio_index]['portfolio']
        display_portfolio(investments)

def display_portfolio(investments):
    st.write("### Portfolio Breakdown")
    # Display a clean breakdown of the portfolio
     # Display the pie chart
    display_pie_chart(investments)
    for inv in investments:
        st.markdown(f"**{inv['asset_name']}**")
        st.markdown(f"**Ticker**: {inv['ticker']}")
        st.markdown(f"**Allocation**: {inv['allocation']}")
        st.markdown(f"**Category**: {inv['category']}")
        st.markdown(f"**Rationale**: {inv['rationale']}")
        st.markdown("---")

   

def display_pie_chart(investments):
    labels = [inv['asset_name'] for inv in investments]
    sizes = [float(str(inv['allocation']).replace('%', '')) for inv in investments]

    fig = px.pie(
        values=sizes,
        names=labels,
        title='Portfolio Allocation',
        hole=0.3,
        height=500
    )

    st.plotly_chart(fig)
