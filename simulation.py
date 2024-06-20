import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ai_call import load_all_portfolios

def fetch_ticker_data(tickers, period="10y"):
    data = {}
    for ticker in tickers:
        try:
            ticker_data = yf.Ticker(ticker)
            history = ticker_data.history(period=period)
            if not history.empty:
                data[ticker] = history['Close']
            else:
                data[ticker] = None
        except Exception as e:
            st.write(f"Error fetching data for {ticker}: {e}")
            data[ticker] = None
    return data

def deterministic_projection(data, stock_weight, bond_weight, cash_weight, initial_deposit, monthly_contribution, num_years, stock_rate, bond_rate, cash_rate):
    months = num_years * 12
    monthly_stock_rate = stock_rate / 12
    monthly_bond_rate = bond_rate / 12
    monthly_cash_rate = cash_rate / 12

    projected_values = np.zeros(months)
    portfolio_value = initial_deposit
    for month in range(months):
        # Calculate returns for each asset type
        stock_return = monthly_stock_rate
        bond_return = monthly_bond_rate
        cash_return = monthly_cash_rate

        # Calculate the new portfolio value based on the returns and weights
        stock_part = portfolio_value * stock_weight * (1 + stock_return)
        bond_part = portfolio_value * bond_weight * (1 + bond_return)
        cash_part = portfolio_value * cash_weight * (1 + cash_return)

        # Add the monthly contribution to the portfolio value
        portfolio_value = stock_part + bond_part + cash_part + monthly_contribution
        projected_values[month] = portfolio_value

    return projected_values

def simulation_page():
    st.title("Simulation")

    all_portfolios = load_all_portfolios()
    if not all_portfolios:
        st.warning("No portfolios generated yet. Please go to the Home page to generate a portfolio.")
        return

    # Allow the user to select a portfolio
    portfolio_options = [f"{portfolio['portfolio_name']} (Portfolio {i+1})" for i, portfolio in enumerate(all_portfolios)]
    selected_portfolio = st.selectbox("Select a portfolio to simulate", portfolio_options)
    
    if selected_portfolio:
        portfolio_index = portfolio_options.index(selected_portfolio)
        investments = all_portfolios[portfolio_index]['portfolio']
        user_data = all_portfolios[portfolio_index]['user_data']
        
        # Columns for side-by-side layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # User inputs for updating simulation parameters
            retirement_age = st.number_input("Retirement Age", min_value=user_data['age'] + 1, max_value=100, value=user_data['retirement_age'])
            initial_deposit = st.number_input("Initial Deposit", min_value=0, value=user_data['Initial_investment'])
            monthly_contribution = st.number_input("Monthly Contribution", min_value=0, value=user_data['monthly_contribution'])

        # Calculate the number of years to retirement
        num_years = retirement_age - user_data['age']
        if num_years <= 0:
            st.error("Retirement age must be greater than current age.")
            return
        
        # Fetch historical data for each ticker
        tickers = [inv['ticker'] for inv in investments if inv['category'] == 'Stock']
        ticker_data = fetch_ticker_data(tickers)
        
        # Filter out tickers with no data
        valid_tickers = [ticker for ticker, data in ticker_data.items() if data is not None]
        if not valid_tickers:
            st.error("No valid data available for the selected portfolio.")
            return
        
        data = pd.DataFrame({ticker: ticker_data[ticker] for ticker in valid_tickers})
        stock_weight = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Stock'])
        bond_weight = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Bond'])
        cash_weight = sum([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['category'] == 'Cash'])
        
        # Calculate historical stock return
        returns = np.log(data / data.shift(1)).dropna()
        mean_annual_return = np.dot(np.array([float(inv['allocation'].replace('%', '')) / 100 for inv in investments if inv['ticker'] in valid_tickers]), returns.mean()) * 252  # Annualize mean return
        
        # Ensure the mean_annual_return is within a reasonable range
        mean_annual_return = max(min(mean_annual_return, 0.15), 0.05)  # Assume returns are between 5% and 15%
        
        # Define fixed growth rates for bonds and cash
        bond_rate = 0.02  # 2% annual return for bonds
        cash_rate = 0.005  # 0.5% annual return for cash

        # Run deterministic projection for the average scenario
        average_projection = deterministic_projection(data, stock_weight, bond_weight, cash_weight, initial_deposit, monthly_contribution, num_years, mean_annual_return, bond_rate, cash_rate)
        
        # Calculate total deposited amount
        total_deposited = initial_deposit + (monthly_contribution * num_years * 12)
        
        with col2:
            # Plot the projection results
            st.write("### Portfolio Projection Results")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=np.arange(1, len(average_projection) + 1), y=average_projection, mode='lines', name='Average'))
            fig.update_layout(title='Deterministic Projection of Portfolio Value', xaxis_title='Months', yaxis_title='Portfolio Value ($)')
            st.plotly_chart(fig)

        # Display the final portfolio value statistics below the input fields
        with col1:
            st.write(f"**Total amount deposited:** ${total_deposited:.2f}")
            st.write(f"**Final portfolio value (Average):** ${average_projection[-1]:.2f}")
            st.write(f"**Extra revenue generated (Average):** ${average_projection[-1] - total_deposited:.2f}")

