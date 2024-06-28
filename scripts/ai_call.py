from groq import Groq
import json

groq_api = "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"
client = Groq(api_key=groq_api)

def get_portfolio(user_data):
    """
    Generate a diversified investment portfolio for a client based on the provided user data.

    Args:
        user_data (dict): A dictionary containing the following details:
            - 'age' (int): The client's age.
            - 'Initial_investment' (float): The initial investment amount.
            - 'monthly_contribution' (float): The monthly contribution amount.
            - 'retirement_age' (int): The desired retirement age.
            - 'ethical_values' (list): A list of ethical values.
            - 'risk_aversion' (str): The client's risk aversion level.

    Returns:
        str: The generated investment portfolio as a JSON string. Each item in the portfolio is in the following format:
            {
                "asset_name": "Asset Name",
                "ticker": "Ticker" (only for stocks, leave empty for bonds and cash),
                "allocation": "X%",
                "category": "Category (Stock/Bond/Cash)",
                "rationale": "Reason for choosing this asset"
            }
    """
    user_message = (
        f"Create a diversified investment portfolio for a client with the following details:\n"
        f"Age: {user_data['age']}\n"
        f"Initial_investment: {user_data['Initial_investment']}\n"
        f"Monthly Contribution: {user_data['monthly_contribution']}\n"
        f"Retirement Age: {user_data['retirement_age']}\n"
        f"Ethical Values: {', '.join(user_data['ethical_values'])}\n"
        f"Risk Aversion: {user_data['risk_aversion']}\n"
        "Ensure the portfolio includes a mix of stocks, bonds, and cash with detailed tickers only for stocks. "
        "Do not include tickers for bonds and cash. "
        "Return the portfolio as a JSON list with each item in the following format: "
        '{"asset_name": "Asset Name", "ticker": "Ticker" (only for stocks, leave empty for bonds and cash), "allocation": "X%", "category": "Category (Stock/Bond/Cash)", "rationale": "Reason for choosing this asset"}.'
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in financial advice. Your task is to generate a comprehensive investment portfolio for a client based on the details provided. "
                    "Output should be in valid JSON format without any text around the JSON output. "
                    "Tickers should be the ones used on Yahoo Finance, in the format 'AAPL', 'GOOGL', 'MSFT', etc. "
                    "Only output the investment recommendations and rationale in the specified format."
                )
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="llama3-70b-8192", 
        seed=42
    )

    ai_response = chat_completion.choices[0].message.content

    return ai_response

def parse_investments(ai_response):
    """
    Parses the AI response and returns the investments as a Python object.

    Args:
        ai_response (str): The AI response in JSON format.

    Returns:
        list or dict or None: The parsed investments as a Python object, or None if there was an error parsing the response.
    """
    try:
        investments = json.loads(ai_response)
        return investments
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Error parsing AI response: {e}")
    return None

def save_portfolio(user_data, investments, portfolio_name):
    """
    Saves the user's portfolio data to a JSON file.

    Parameters:
    user_data (dict): A dictionary containing user data.
    investments (list): A list of investments in the portfolio.
    portfolio_name (str): The name of the portfolio.

    Returns:
    None
    """
    portfolio_data = {
        "user_data": user_data,
        "portfolio": investments,
        "portfolio_name": portfolio_name
    }
    
    all_portfolios = load_all_portfolios()
    all_portfolios.append(portfolio_data)
    
    with open("portfolios.json", "w") as file:
        json.dump(all_portfolios, file)

def load_all_portfolios():
    """
    Load all portfolios from the 'portfolios.json' file.

    Returns:
        A list of portfolios loaded from the file.
        If the file is not found or cannot be decoded as JSON, an empty list is returned.
    """
    try:
        with open("scripts/portfolios.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def check_existing_portfolio(user_data):
    """
    Check if there is an existing portfolio for the given user data.

    Parameters:
    user_data (dict): The user data to check against existing portfolios.

    Returns:
    dict or None: The existing portfolio if found, None otherwise.
    """
    all_portfolios = load_all_portfolios()
    for portfolio in all_portfolios:
        if portfolio['user_data'] == user_data:
            return portfolio['portfolio']
    return None
