import streamlit as st
import plotly.express as px
from ai_call import load_all_portfolios

def portfolio_page():
    st.title("📊 Portfolio Breakdown")
    
    all_portfolios = load_all_portfolios()
    if not all_portfolios:
        st.warning("No portfolios generated yet. Please go to the Portfolio Creation page to generate a portfolio.")
        return
    
    st.sidebar.title("Select a Portfolio to view")
    portfolio_options = [f"{portfolio['portfolio_name']}" for  portfolio in all_portfolios]
    selected_portfolio = st.sidebar.selectbox("Select a portfolio to view", portfolio_options)
    
    if selected_portfolio:
        portfolio_index = portfolio_options.index(selected_portfolio)
        investments = all_portfolios[portfolio_index]['portfolio']
        user_data = all_portfolios[portfolio_index]['user_data']
        
        initial_investment = st.sidebar.number_input("Initial Investment", min_value=0, value=user_data['Initial_investment'])
        monthly_contribution = st.sidebar.number_input("Monthly Contribution", min_value=0, value=user_data['monthly_contribution'])
        
        display_overall_portfolio(investments, user_data, initial_investment, monthly_contribution)

def display_overall_portfolio(investments, user_data, initial_investment, monthly_contribution):
    categories = {}
    for inv in investments:
        category = inv['category']
        allocation = float(inv['allocation'].replace('%', ''))
        if category in categories:
            categories[category] += allocation
        else:
            categories[category] = allocation

    category_labels = list(categories.keys())
    category_sizes = list(categories.values())

    fig = px.pie(
        values=category_sizes,
        names=category_labels,
        title='Portfolio Allocation by Category',
        hole=0.3,
        height=500
    )

    st.plotly_chart(fig)

    selected_category = st.selectbox("Select a category to view details", category_labels)
    
    if selected_category:
        display_category_details(investments, selected_category, initial_investment, monthly_contribution)
    
def display_category_details(investments, selected_category, initial_investment, monthly_contribution):
    category_investments = [inv for inv in investments if inv['category'] == selected_category]
    
    st.write(f"### {selected_category} Breakdown")
    
    for inv in category_investments:
        if inv['category'] == 'Stock':
            st.markdown(f"**Asset Name**: {inv['asset_name']}")
            st.markdown(f"**Ticker**: {inv['ticker'] if inv['ticker'] else 'N/A'}")
            st.markdown(f"**Allocation**: {inv['allocation']}")
            st.markdown(f"**Category**: {inv['category']}")
        st.markdown(f"**Rationale**: {inv['rationale']}")
        st.markdown("---")
        
    st.write("#### Investment Breakdown")
    for inv in category_investments:
        allocation = float(inv['allocation'].replace('%', ''))
        initial_amount = initial_investment * (allocation / 100)
        monthly_amount = monthly_contribution * (allocation / 100)
        st.markdown(f"- **{inv['asset_name']} ({inv['category']}):** Initial: \${initial_amount:,.2f}, Monthly: \${monthly_amount:,.2f}")

