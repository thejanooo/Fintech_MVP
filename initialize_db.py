import sqlite3

def initialize_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create portfolios table
    c.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            portfolio_name TEXT,
            portfolio_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create simulations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            simulation_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
