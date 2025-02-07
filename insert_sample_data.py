import sqlite3

def insert_sample_data(db_path="trades.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert sample client orders
    sample_orders = [
        # 1. Exact match scenarios:
        # INE738I01010 appears in trade file 1 with QTY = 680.
        ("ORD_EXACT_738", "C001", "INE738I01010", 680, 3596.65, "2024-06-12"),
        # INE457L01029 appears in trade file 1 with QTY = 5358.
        ("ORD_EXACT_457", "C002", "INE457L01029", 5358, 980.09, "2024-06-12"),

        # 2. Partial match (proportional allocation) scenario:
        # INE700A01033 is present in three trade files (total QTY ≈ 49884). Order is less than total available.
        ("ORD_PARTIAL_700", "C003", "INE700A01033", 30000, 1100.50, "2024-06-12"),

        # 3. Pending scenario (order not fully filled):
        # INE982J01020 appears in trade file 1 with QTY = 30000. Order exceeds available quantity.
        ("ORD_PENDING_982", "C004", "INE982J01020", 35000, 984.88, "2024-06-12"),

        # 4. Multiple brokers / proportional allocation scenario:
        # INE736A01011 is present in trade file 2 and trade file 3 (total QTY = 37500).
        ("ORD_MULTIBROKER_736", "C005", "INE736A01011", 20000, 1820.00, "2024-06-12"),

        # 5. Multiple brokers / exact fill scenario:
        # INE624Z01016 is present in trade file 2 and trade file 3 (total QTY = 10080).
        ("ORD_EXACT_MULTI_624", "C006", "INE624Z01016", 10080, 680.00, "2024-06-12"),

        # 6. Multiple brokers / partial match with splitting:
        # INE002A01018 is present in trade file 2 and trade file 3 (total QTY = 5940). Order is less than total available.
        ("ORD_PARTIAL_MULTI_002", "C007", "INE002A01018", 3000, 1550.00, "2024-06-12"),

        # 7. No matching trade scenario:
        # Symbol "FAKE00000000" does not appear in any trade file.
        ("ORD_NO_MATCH", "C008", "FAKE00000000", 5000, 1000.00, "2024-06-12"),
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
