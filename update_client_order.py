import sqlite3

def update_client_order(db_path="trades.db", order_id="ORD001", new_values=None):
    if not new_values:
        print("No values provided to update.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Dynamically construct the SQL query
    set_clause = ", ".join([f"{key} = ?" for key in new_values.keys()])
    query = f"UPDATE client_orders SET {set_clause} WHERE order_id = ?"

    # Execute the query
    cursor.execute(query, list(new_values.values()) + [order_id])

    conn.commit()
    conn.close()
    print(f"Order {order_id} updated successfully with values: {new_values}")

# Run the function to update specific columns
if __name__ == "__main__":
    update_client_order(
        db_path="trades.db",
        order_id="ORD009",  # Specify the order_id to update
        new_values={         # Only specify the columns you want to update
            "order_date": "2024-06-12",
        }
    )
