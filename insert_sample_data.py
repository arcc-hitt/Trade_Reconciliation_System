import sqlite3

def insert_sample_data(db_path="trades.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert sample client orders
    sample_orders = [
        ("ORD001", "C001", "INE700A01033", 15000, 1100.50, "2024-06-12"),
        ("ORD002", "C002", "INE738I01010", 1000, 3600.00, "2024-06-12"),
        ("ORD003", "C003", "INE457L01029", 5500, 985.00, "2024-06-12"),
        ("ORD004", "C004", "INE665J01013", 600, 3880.00, "2024-06-12"),
        ("ORD005", "C005", "INE982J01020", 30000, 980.00, "2024-06-12"),
        ("ORD006", "C006", "INE736A01011", 20000, 1820.00, "2024-06-12"),
        ("ORD007", "C007", "INE624Z01016", 10000, 670.00, "2024-06-12"),
        ("ORD008", "C008", "INE002A01018", 4000, 1555.00, "2024-06-11"),
        ("ORD009", "C009", "INE002A01021", 4500, 1655.00, "2024-06-12"),
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO client_orders (order_id, client_id, symbol, quantity, order_price, order_date)
    VALUES (?, ?, ?, ?, ?, ?);
    """, sample_orders)

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

# Run the function to insert sample data
if __name__ == "__main__":
    insert_sample_data()
