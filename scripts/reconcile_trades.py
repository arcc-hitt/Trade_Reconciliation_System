import sqlite3
import logging

def reconcile_trades(client_orders, broker_trades):
    """
    Performs trade reconciliation by matching client orders with broker trades.
    """
    results = []
    
    for _, order in client_orders.iterrows():
        # Check for symbol matches
        symbol_matching_trades = broker_trades[broker_trades['symbol'] == order['symbol']]

        # Check for symbol and date matches
        matching_trades = symbol_matching_trades[symbol_matching_trades['trade_date'] == order['order_date']]

        # Determine broker_id based on matching conditions
        if matching_trades.empty:
            if symbol_matching_trades.empty:
                broker_id = "UNKNOWN_SYMBOL"  # No symbol match
            elif not symbol_matching_trades.empty:
                broker_id = "UNKNOWN_DATE"  # Symbol matches, but date does not
            else:
                broker_id = "UNKNOWN_BOTH"  # Neither symbol nor date matches

            # Append the pending result with the determined broker_id
            results.append((order['order_id'], broker_id, "Pending", 0, 0.0, 0.0, 0.0, 0.0))
            continue
        
        total_allocated = 0
        total_broker_quantity = matching_trades['quantity'].sum()
        
        # Compute weighted average price for reconciliation
        weighted_avg_price = (matching_trades['trade_price'] * matching_trades['quantity']).sum() / total_broker_quantity
        
        for _, trade in matching_trades.iterrows():
            # Determine allocation proportionally
            allocation_ratio = trade['quantity'] / total_broker_quantity
            allocation = min(order['quantity'] * allocation_ratio, trade['quantity'])
            
            # Calculate total cost and execution slippage
            total_cost = trade['net_amount'] + trade['brokerage_amount'] + trade['stt']
            slippage = order['order_price'] - weighted_avg_price
            
            # Determine reconciliation status
            status = "Partial" if allocation < order['quantity'] else "Matched"
            if trade['quantity'] > (order['quantity'] - total_allocated):
                status = "Excess"
            
            # Store reconciliation result
            results.append((order['order_id'], trade['broker_id'], status, allocation, total_cost, slippage, trade['stt'], trade['brokerage_amount']))
            
            total_allocated += allocation
            if total_allocated >= order['quantity']:
                break  # Stop processing if order is fully allocated
        
        # If order is not fully allocated, mark remaining as pending
        if total_allocated < order['quantity']:
            results.append((order['order_id'], trade['broker_id'], "Pending", 0, 0.0, 0.0, 0.0, 0.0))
    
    return results

def save_reconciliation_results(results, db_path):
    """
    Saves the reconciliation results into the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.executemany("""
        INSERT INTO reconciliation_results 
        (order_id, broker_id, status, allocated_quantity, total_cost, execution_slippage, stt, brokerage_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, results)
    
    conn.commit()
    conn.close()
    logging.info("Reconciliation results saved to the database.")