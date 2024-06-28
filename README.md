# RetireWise

## Overview
RetireWise is an AI-driven platform designed to provide personalized, ethical, and continuously optimized retirement planning solutions. This platform aims to make retirement planning accessible, transparent, and effective for everyone by leveraging cutting-edge AI technology to deliver highly personalized investment recommendations.

## Features
- **Generate a Portfolio with AI based on user info:** Creates a personalized investment portfolio using the Groq API based on user profiles including initial deposit, monthly contribution, retirement age, age, ethical values, and risk tolerance.
- **Investment Portfolio Visualization:** Displays portfolio allocation by category using interactive visualizations.
- **Investment Details:** Provides detailed information about the investments in the portfolio.
- **Portfolio Simulation:** Uses Monte Carlo simulation to simulate different investment scenarios and outcomes to help users make informed decisions.

## Project Structure
- `main.py`: The main entry point of the Streamlit web application.
- `portfolio_creation.py`: Handles the creation of user portfolios based on their input.
- `portfolio.py`: Manages and displays the details of user portfolios.
- `simulation.py`: Simulates different investment scenarios and outcomes.
- `ai_call.py`: Interfaces with the AI model (Groq API) to generate personalized investment recommendations.
- `home_page.py`: Manages the home page content and user interface.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/thejanooo/Fintech_MVP.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Fintech_MVP
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit application:
   ```bash
   streamlit run scripts/main.py
   ```
2. Open your web browser and go to `http://localhost:8501` to access the RetireWise application.
