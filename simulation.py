import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ai_call import load_all_portfolios

def monte_carlo_simulation(tickers, stock_alloc_overall, stock_alloc_individual, bond_alloc, cash_alloc, initial_deposit, monthly_contribution, years, simulations, seed=None):
    """
    Perform Monte Carlo simulation to estimate the range of possible portfolio values over a given number of years.

    Parameters:
    tickers (list): List of stock tickers to download historical data for.
    stock_alloc_overall (float): Overall allocation to stocks in the portfolio.
    stock_alloc_individual (pd.Series): Allocation to individual stocks within the overall stock allocation.
    bond_alloc (float): Allocation to bonds in the portfolio.
    cash_alloc (float): Allocation to cash in the portfolio.
    initial_deposit (float): Initial deposit amount.
    monthly_contribution (float): Monthly contribution amount.
    years (int): Number of years to simulate.
    simulations (int): Number of simulations to run.
    seed (int, optional): Seed value for random number generation. Defaults to None.

    Returns:
    tuple: A tuple containing the median, optimistic, and pessimistic values of the portfolio over time.
    """

    if seed is not None:
        np.random.seed(seed)
    
    # Download historical data for the tickers
    data = yf.download(tickers, period="max")['Adj Close']
    
    # Calculate monthly returns
    monthly_returns = data.resample('ME').ffill().pct_change().dropna()

    # Calculate weighted monthly returns for individual stocks within the overall stock allocation
    weighted_stock_returns = (monthly_returns * stock_alloc_individual).sum(axis=1)
    
    # Assumed mean and standard deviation for bonds and cash
    mean_bond_return = 0.035 / 12  # 3.5% annual return converted to monthly
    std_bond_return = 0.06 / np.sqrt(12)  # 6% annual standard deviation converted to monthly
    
    mean_cash_return = 0.015 / 12  # 1.5% annual return converted to monthly
    std_cash_return = 0.01 / np.sqrt(12)  # 1% annual standard deviation converted to monthly

    # Calculate mean and standard deviation of weighted stock returns
    mean_stock_return = weighted_stock_returns.mean()
    std_stock_return = weighted_stock_returns.std()

    # Store portfolio values for each simulation
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

    # Convert the simulations to a DataFrame
    simulation_df = pd.DataFrame(all_simulations).T

    # Calculate percentiles for each month
    median_values = simulation_df.median(axis=1)
    optimistic_values = simulation_df.quantile(0.95, axis=1)
    pessimistic_values = simulation_df.quantile(0.05, axis=1)

    return median_values, optimistic_values, pessimistic_values

def simulation_page():
    """
    Renders the simulation page.

    This function displays a simulation page that allows the user to select a portfolio and simulate its performance over time.
    The user can update simulation parameters such as retirement age, initial deposit, and monthly contribution.
    The function runs a Monte Carlo simulation to generate projected portfolio values and displays the results in a plot.

    """
    st.title("Simulation")

    all_portfolios = load_all_portfolios()
    if not all_portfolios:
        st.warning("No portfolios generated yet. Please go to the Home page to generate a portfolio.")
        return

    # Columns for side-by-side layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Allow the user to select a portfolio
        portfolio_options = [f"{portfolio['portfolio_name']} (Portfolio {i+1})" for i, portfolio in enumerate(all_portfolios)]
        selected_portfolio = st.selectbox("Select a portfolio to simulate", portfolio_options)
    
        if selected_portfolio:
            portfolio_index = portfolio_options.index(selected_portfolio)
            investments = all_portfolios[portfolio_index]['portfolio']
            user_data = all_portfolios[portfolio_index]['user_data']
            
            # User inputs for updating simulation parameters
            retirement_age = st.number_input("Retirement Age", min_value=user_data['age'] + 1, max_value=100, value=user_data['retirement_age'])
            initial_deposit = st.number_input("Initial Deposit", min_value=0, value=user_data['Initial_investment'])
            monthly_contribution = st.number_input("Monthly Contribution", min_value=0, value=user_data['monthly_contribution'])
            years = retirement_age - user_data['age']
            simulations = 1000
            seed = 42

            # Calculate the number of years to retirement
            if years <= 0:
                st.error("Retirement age must be greater than current age.")
                return
            
            # Prepare the allocations
            stock_alloc_overall = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Stock'])
            bond_alloc = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Bond'])
            cash_alloc = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Cash'])

            # Fetch tickers for stocks
            tickers = [inv['ticker'] for inv in investments if inv['category'] == 'Stock']
            stock_alloc_individual = [float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Stock']
            stock_alloc_individual = [alloc / stock_alloc_overall for alloc in stock_alloc_individual]  # Normalize individual stock allocations

            # Run the Monte Carlo simulation
            median_values, optimistic_values, pessimistic_values = monte_carlo_simulation(tickers, stock_alloc_overall, stock_alloc_individual, bond_alloc, cash_alloc, initial_deposit, monthly_contribution, years, simulations, seed)

            # Convert results to a DataFrame for plotting
            results_df = pd.DataFrame({
                'Month': range(len(median_values)),
                'Median Value': median_values,
                'Optimistic Value': optimistic_values,
                'Pessimistic Value': pessimistic_values
            })

            # Display the final portfolio value statistics below the input fields
            total_deposited = initial_deposit + (monthly_contribution * years * 12)
            st.write(f"**Total amount deposited:** ${total_deposited:,.2f}")
            st.write(f"**Final portfolio value (Median):** ${median_values.iloc[-1]:,.2f}")
            st.write(f"**Final portfolio value (Optimistic):** ${optimistic_values.iloc[-1]:,.2f}")
            st.write(f"**Final portfolio value (Pessimistic):** ${pessimistic_values.iloc[-1]:,.2f}")
            st.write(f"**Extra revenue generated (Median):** ${median_values.iloc[-1] - total_deposited:,.2f}")
            
    with col2:
        if selected_portfolio:
            # Plot the projection results
            st.write("### Portfolio Projection Results")
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

