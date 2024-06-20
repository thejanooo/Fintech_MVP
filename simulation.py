import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import json

def simulation_page():
    st.title("Portfolio Simulation")
    
    portfolio = load_portfolio()
    
    if portfolio:
        investments = portfolio['portfolio']
        display_simulation_options(investments)
    else:
        st.warning("No portfolio generated yet. Please go to the Home page to generate a portfolio.")

def display_simulation_options(investments):
    st.write("### Monte Carlo Simulation")

    years = st.number_input("Enter the number of years for the simulation", min_value=1, value=10)
    
    if st.button("Run Simulation"):
        run_simulation(investments, years)

def run_simulation(investments, years):
    tickers = [inv['ticker'] for inv in investments]
    allocations = np.array([float(inv['allocation'].replace('%', '')) for inv in investments]) / 100
    prices = fetch_prices(tickers)
    
    if prices is None:
        st.error("Failed to fetch historical prices for the tickers.")
        return

    simulations = monte_carlo_simulation(prices, allocations, years)
    display_simulation_results(simulations, years)

def fetch_prices(tickers):
    prices = {}
    try:
        for ticker in tickers:
            data = yf.download(ticker, start='2010-01-01')['Adj Close']
            prices[ticker] = data
        prices_df = pd.DataFrame(prices)
        return prices_df
    except Exception as e:
        st.error(f"Error fetching prices: {e}")
        return None

def monte_carlo_simulation(prices, allocations, years, num_simulations=1000):
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    portfolio_mean = np.dot(allocations, mean_returns)
    portfolio_std_dev = np.sqrt(np.dot(allocations.T, np.dot(cov_matrix, allocations)))
    
    simulations = np.zeros((num_simulations, years))
    
    for i in range(num_simulations):
        simulation = np.random.normal(portfolio_mean, portfolio_std_dev, years)
        simulations[i] = np.cumprod(1 + simulation)
    
    return simulations

def display_simulation_results(simulations, years):
    st.write("### Simulation Results")
    
    end_values = simulations[:, -1]
    mean_end_value = np.mean(end_values)
    median_end_value = np.median(end_values)
    st.write(f"Mean end value: ${mean_end_value:.2f}")
    st.write(f"Median end value: ${median_end_value:.2f}")
    
    st.line_chart(simulations.T)

def load_portfolio():
    try:
        with open("portfolios.json", "r") as file:
            portfolios = json.load(file)
            # For simplicity, load the first portfolio. Modify as needed to choose a specific portfolio.
            return portfolios[0] if portfolios else None
    except (FileNotFoundError, json.JSONDecodeError):
        return None
