import streamlit as st
import plotly.express as px
from scripts.ai_call import load_all_portfolios

def portfolio_page():
    """
    Renders the portfolio breakdown page.

    This function displays the portfolio breakdown page, which allows the user to select a portfolio
    to view and provides options for customizing the initial investment and monthly contribution.
    It calls the `load_all_portfolios` function to load all portfolios and displays a warning message
    if no portfolios are generated yet.

    Returns:
        None
    """
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
    """
    Displays the overall portfolio allocation by category and allows the user to select a category to view details.

    Parameters:
    - investments (list): A list of investment dictionaries containing information about each investment.
    - user_data (dict): A dictionary containing user-specific data.
    - initial_investment (float): The initial investment amount.
    - monthly_contribution (float): The monthly contribution amount.

    Returns:
    None
    """
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
    """
    Displays the details of investments in a selected category.

    Parameters:
    - investments (list): A list of investment dictionaries.
    - selected_category (str): The category of investments to display.
    - initial_investment (float): The initial investment amount.
    - monthly_contribution (float): The monthly contribution amount.

    Returns:
    None
    """
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

