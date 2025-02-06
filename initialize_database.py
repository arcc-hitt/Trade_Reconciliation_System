import sqlite3

def initialize_database(db_path="trades.db"):
    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create client_orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client_orders (
        order_id TEXT PRIMARY KEY,
        client_id TEXT,
        symbol TEXT,
        quantity INTEGER,
        order_price REAL,
        order_date TEXT
    );
    """)

    # Create broker_trades table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS broker_trades (
        symbol TEXT,
        broker_id TEXT,
        buy_sell_flag TEXT,
        quantity INTEGER,
        trade_price REAL,
        trade_date TEXT,
        net_amount REAL,
        settlement_date TEXT,
        brokerage_amount REAL,
        stt REAL,
        exchange_code TEXT,
        depository_code TEXT,
        col_8 TEXT
    );
    """)

    # Create reconciliation_results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reconciliation_results (
        rec_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        broker_id INTEGER,
        status TEXT,
        allocated_quantity INTEGER,
        total_cost REAL,
        execution_slippage REAL,
        stt REAL,
        brokerage_amount REAL
    );
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# Run the function to initialize the database
if __name__ == "__main__":
    initialize_database()
