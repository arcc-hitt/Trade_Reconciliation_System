import sqlite3
import logging

def reconcile_trades(client_orders, broker_trades):
    """
    Performs trade reconciliation by matching client orders with broker trades.
    """
    results = []
    
    for _, order in client_orders.iterrows():
        # Filter trades by symbol and date
        matching_trades = broker_trades[(broker_trades['symbol'] == order['symbol']) &
                                        (broker_trades['trade_date'] == order['order_date'])]

        # No matching trades found
        if matching_trades.empty:
            if matching_trades.empty:
                broker_id = "UNMATCHED_SYMBOL"  # No symbol match
            elif not matching_trades.empty:
                broker_id = "UNMATCHED_DATE"  # Symbol matches, but date does not
            else:
                broker_id = "UNMATCHED_BOTH"  # Neither symbol nor date matches

            # Append the pending result with the determined broker_id
            results.append((order['order_id'], broker_id, "Pending", 0, 0.0, 0.0, 0.0, 0.0))
            continue
        
         # Handle edge case: Multiple brokers for the same stock
        total_broker_quantity = matching_trades['quantity'].sum()
        weighted_avg_price = (matching_trades['trade_price'] * matching_trades['quantity']).sum() / total_broker_quantity

        total_allocated = 0
        for _, trade in matching_trades.iterrows():
            allocation = 0
            if total_broker_quantity > order['quantity']:
                # Proportional allocation if multiple trades exceed order quantity
                allocation = (trade['quantity'] / total_broker_quantity) * order['quantity']
                status = "Partial" if allocation < trade['quantity'] else "Matched"
            elif trade['quantity'] == order['quantity'] - total_allocated:
                # Exact match
                allocation = trade['quantity']
                status = "Matched"
            elif trade['quantity'] < order['quantity'] - total_allocated:
                # Partial match
                allocation = trade['quantity']
                status = "Partial"
            else:
                # Excess quantity
                allocation = order['quantity'] - total_allocated
                status = "Excess"

            # Calculate costs
            total_cost = trade['net_amount'] + trade['brokerage_amount'] + trade['stt']
            execution_slippage = order['order_price'] - (trade['net_amount'] / trade['quantity'])

            results.append((
                order['order_id'],
                trade['broker_id'],
                status,
                allocation,
                total_cost,
                execution_slippage,
                trade['stt'],
                trade['brokerage_amount']
            ))

            total_allocated += allocation
            if total_allocated >= order['quantity']:
                break
        
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