import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ai_call import load_all_portfolios

def monte_carlo_simulation(tickers, stock_alloc_overall, stock_alloc_individual, bond_alloc, cash_alloc, initial_deposit, monthly_contribution, years, simulations, seed=None):
    """
    Perform Monte Carlo simulation to estimate the future portfolio values.

    Parameters:
    - tickers (list): List of stock tickers to download data for.
    - stock_alloc_overall (float): Overall allocation to stocks in the portfolio.
    - stock_alloc_individual (pandas.Series): Individual allocations to stocks in the portfolio.
    - bond_alloc (float): Allocation to bonds in the portfolio.
    - cash_alloc (float): Allocation to cash in the portfolio.
    - initial_deposit (float): Initial deposit amount.
    - monthly_contribution (float): Monthly contribution amount.
    - years (int): Number of years to simulate.
    - simulations (int): Number of simulations to run.
    - seed (int, optional): Random seed for reproducibility.

    Returns:
    - median_values (pandas.Series): Median portfolio values for each time period.
    - optimistic_values (pandas.Series): Optimistic (95th percentile) portfolio values for each time period.
    - pessimistic_values (pandas.Series): Pessimistic (5th percentile) portfolio values for each time period.
    """
    if seed is not None:
        np.random.seed(seed)
    
    data = yf.download(tickers, period="max")['Adj Close']
    
    monthly_returns = data.resample('ME').ffill().pct_change().dropna()

    weighted_stock_returns = (monthly_returns * stock_alloc_individual).sum(axis=1)
    
    mean_bond_return = 0.035 / 12
    std_bond_return = 0.06 / np.sqrt(12)
    
    mean_cash_return = 0.015 / 12
    std_cash_return = 0.01 / np.sqrt(12)

    mean_stock_return = weighted_stock_returns.mean()
    std_stock_return = weighted_stock_returns.std()

    all_simulations = []

    for _ in range(simulations):
        portfolio_value = initial_deposit
        portfolio_values = [portfolio_value]
        for i in range(years * 12):
            random_stock_return = np.random.normal(mean_stock_return, std_stock_return)
            random_bond_return = np.random.normal(mean_bond_return, std_bond_return)
            random_cash_return = np.random.normal(mean_cash_return, std_cash_return)
            total_return = (random_stock_return * stock_alloc_overall + 
                            random_bond_return * bond_alloc + 
                            random_cash_return * cash_alloc)
            portfolio_value = (portfolio_value + monthly_contribution) * (1 + total_return)
            portfolio_values.append(portfolio_value)
        all_simulations.append(portfolio_values)

    simulation_df = pd.DataFrame(all_simulations).T

    median_values = simulation_df.median(axis=1)
    optimistic_values = simulation_df.quantile(0.95, axis=1)
    pessimistic_values = simulation_df.quantile(0.05, axis=1)

    return median_values, optimistic_values, pessimistic_values

def simulation_page():
    """
    Renders the simulation page.

    This function displays a simulation page with various parameters for simulating a portfolio's performance.
    It loads all portfolios, allows the user to select a portfolio to simulate, and modifies simulation parameters
    such as retirement age, initial deposit, and monthly contribution. It then performs a Monte Carlo simulation
    to generate projected portfolio values over time and displays the results using metrics and a plot.
    """
    st.title("📈 Simulation")

    all_portfolios = load_all_portfolios()
    if not all_portfolios:
        st.warning("No portfolios generated yet. Please go to the Portfolio Creation page to generate a portfolio.")
        return

    st.sidebar.title("Modify Simulation Parameters")
    portfolio_options = [f"{portfolio['portfolio_name']}" for portfolio in all_portfolios]
    selected_portfolio = st.sidebar.selectbox("Select a portfolio to simulate", portfolio_options)
    
    if selected_portfolio:
        portfolio_index = portfolio_options.index(selected_portfolio)
        investments = all_portfolios[portfolio_index]['portfolio']
        user_data = all_portfolios[portfolio_index]['user_data']
        
        retirement_age = st.sidebar.number_input("Retirement Age", min_value=user_data['age'] + 1, max_value=100, value=user_data['retirement_age'])
        initial_deposit = st.sidebar.number_input("Initial Deposit", min_value=0, value=user_data['Initial_investment'])
        monthly_contribution = st.sidebar.number_input("Monthly Contribution", min_value=0, value=user_data['monthly_contribution'])
        years = retirement_age - user_data['age']
        simulations = 1000
        seed = 42

        if years <= 0:
            st.error("Retirement age must be greater than current age.")
            return
        
        stock_alloc_overall = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Stock'])
        bond_alloc = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Bond'])
        cash_alloc = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Cash'])

        tickers = [inv['ticker'] for inv in investments if inv['category'] == 'Stock']
        stock_alloc_individual = [float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Stock']
        stock_alloc_individual = [alloc / stock_alloc_overall for alloc in stock_alloc_individual]

        median_values, optimistic_values, pessimistic_values = monte_carlo_simulation(tickers, stock_alloc_overall, stock_alloc_individual, bond_alloc, cash_alloc, initial_deposit, monthly_contribution, years, simulations, seed)

        results_df = pd.DataFrame({
            'Month': range(len(median_values)),
            'Median Value': median_values,
            'Optimistic Value': optimistic_values,
            'Pessimistic Value': pessimistic_values
        })

        total_deposited = initial_deposit + (monthly_contribution * years * 12)
        extra_revenue_generated = median_values.iloc[-1] - total_deposited

        # Display the summary boxes
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="💰 Total Amount Deposited", value=f"${total_deposited:,.2f}")
        with col2:
            st.metric(label="📈 Final Portfolio Value (Median)", value=f"${median_values.iloc[-1]:,.2f}")
        with col3:
            st.metric(label="📊 Extra Revenue Generated (Median)", value=f"${extra_revenue_generated:,.2f}")

        # Plot the projection results
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=results_df['Month'], y=results_df['Median Value'],
                                 mode='lines', name='Median Value'))
        fig.add_trace(go.Scatter(x=results_df['Month'], y=results_df['Optimistic Value'],
                                 mode='lines', name='Optimistic Value (95th Percentile)'))
        fig.add_trace(go.Scatter(x=results_df['Month'], y=results_df['Pessimistic Value'],
                                 mode='lines', name='Pessimistic Value (5th Percentile)'))

        fig.update_layout(title='Portfolio Value Over Time',
                          xaxis_title='Month',
                          yaxis_title='Portfolio Value ($)',
                          template='plotly_white')

        st.plotly_chart(fig)
        
        # Explanation Text
        final_median_value = median_values.iloc[-1]
        years_post_retirement = 80 - retirement_age
        months_post_retirement = years_post_retirement * 12
        monthly_withdrawal = final_median_value / months_post_retirement

        st.write(f"""
        Based on the median projection, your portfolio could grow to **\${final_median_value:,.2f}** by the time you retire. 
        However, considering the optimistic and pessimistic scenarios, your portfolio could range from **\${pessimistic_values.iloc[-1]:,.2f}** to **\${optimistic_values.iloc[-1]:,.2f}**.

        Assuming you live until the age of 80, you would be able to withdraw approximately **\${monthly_withdrawal:,.2f}** per month from your median portfolio value.
        """)

