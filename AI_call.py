from groq import Groq
import json

groq_api = "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"
client = Groq(api_key=groq_api)

def get_portfolio(user_data):
    user_message = (
        f"Create a diversified investment portfolio for a client with the following details:\n"
        f"Age: {user_data['age']}\n"
        f"Income: {user_data['income']}\n"
        f"Monthly Contribution: {user_data['monthly_contribution']}\n"
        f"Retirement Age: {user_data['retirement_age']}\n"
        f"Ethical Values: {', '.join(user_data['ethical_values'])}\n"
        f"Risk Aversion: {user_data['risk_aversion']}\n"
        "Please ensure the portfolio includes a mix of stocks, bonds, and cash. "
        "Return the portfolio as a JSON list with each item in the following format: "
        '{"asset_name": "Asset Name", "ticker": "Ticker", "allocation": "X%", "category": "Category", "rationale": "Reason for choosing this asset"}.'
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in financial advice. Your task is to generate a comprehensive investment portfolio for a client based on the details provided. "
                    "The portfolio should include a balanced mix of stocks, bonds, cash, and other investment options. "
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
    try:
        # Extract the allocation details from the AI response
        investments = json.loads(ai_response)
        return investments
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Error parsing AI response: {e}")
    return None

def save_portfolio(user_data, investments, portfolio_name):
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
    try:
        with open("portfolios.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def check_existing_portfolio(user_data):
    all_portfolios = load_all_portfolios()
    for portfolio in all_portfolios:
        if portfolio['user_data'] == user_data:
            return portfolio['portfolio']
    return None
