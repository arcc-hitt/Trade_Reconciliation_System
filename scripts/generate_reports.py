import sqlite3
import pandas as pd
import logging

# Setup logging to track execution details
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_reports(db_path):
    """
    Generates three reports: matched trades, unmatched trades, and broker summary.
    """
    conn = sqlite3.connect(db_path)
    
    logging.info("Generating matched and unmatched trades reports...")
    # Fetch matched and unmatched trades from the reconciliation_results table
    matched = pd.read_sql_query("SELECT * FROM reconciliation_results WHERE status='Matched'", conn)
    unmatched = pd.read_sql_query("SELECT * FROM reconciliation_results WHERE status IN ('Pending', 'Partial', 'Excess')", conn)
    
    # Save reports as CSV files
    matched.to_csv("reports/matched_trades.csv", index=False)
    unmatched.to_csv("reports/unmatched_trades.csv", index=False)
    
    logging.info("Generating broker comparison report...")
    # Summarize broker trades by broker_id and symbol
    broker_summary = pd.read_sql_query("""
        SELECT broker_id, order_id, COUNT(*) AS trade_count, 
               SUM(allocated_quantity) AS total_quantity, 
               SUM(total_cost) AS total_cost
        FROM reconciliation_results
        GROUP BY broker_id, order_id
    """, conn)
    
    # Save broker summary report
    broker_summary.to_csv("reports/broker_summary.csv", index=False)
    conn.close()
    logging.info("Reports generated successfully.")

def generate_broker_ranking_report(db_path):
    """
    Generate a broker ranking report based on execution quality.
    """
    conn = sqlite3.connect(db_path)
    broker_ranking_query = """
        SELECT broker_id,
               AVG(execution_slippage) AS avg_slippage,
               SUM(total_cost) AS total_cost,
               COUNT(*) AS trade_count
        FROM reconciliation_results
        GROUP BY broker_id
        ORDER BY avg_slippage ASC, total_cost ASC;
    """
    broker_rankings = pd.read_sql_query(broker_ranking_query, conn)
    broker_rankings.to_csv("reports/broker_ranking.csv", index=False)
    conn.close()
    logging.info("Broker ranking report generated.")
