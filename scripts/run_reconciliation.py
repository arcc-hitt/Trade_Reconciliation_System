# Run Reconciliation Process
import logging
import extract_trades
import reconcile_trades
import generate_reports

if __name__ == "__main__":
    logging.info("Starting trade reconciliation process...")
    
    client_orders = extract_trades.load_client_orders("trades.db")
    broker_trades = extract_trades.parse_eml_files("broker_emails/")
    extract_trades.save_broker_trades_to_db(broker_trades, "trades.db")
    
    results = reconcile_trades.reconcile_trades(client_orders, broker_trades)
    reconcile_trades.save_reconciliation_results(results, "trades.db")
    
    logging.info("Generating reports...")
    generate_reports.generate_reports("trades.db")
    
    logging.info("Reconciliation process completed successfully.")