from flask import Flask, request, jsonify
import logging
from scripts import extract_trades
from scripts import reconcile_trades
from scripts import generate_reports
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/trigger-reconciliation', methods=['POST'])
def trigger_reconciliation():
    """
    Trigger the reconciliation process via Flask API.
    """
    try:
        # Load client orders and broker trades
        client_orders = extract_trades.load_client_orders("trades.db")
        broker_trades = extract_trades.parse_eml_files("broker_emails/")
        extract_trades.save_broker_trades_to_db(broker_trades, "trades.db")

        # Perform reconciliation
        results = reconcile_trades.reconcile_trades(client_orders, broker_trades)
        reconcile_trades.save_reconciliation_results(results, "trades.db")

        # Generate reports
        generate_reports.generate_reports("trades.db")

        return jsonify({"status": "success", "message": "Reconciliation and report generation completed."}), 200
    except Exception as e:
        logging.error(f"Error during reconciliation: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/broker-ranking', methods=['GET'])
def broker_ranking():
    """
    Generate broker rankings based on execution quality.
    """
    try:
        conn = sqlite3.connect("trades.db")
        # Calculate rankings based on slippage and total cost
        broker_ranking_query = """
            SELECT broker_id,
                   AVG(execution_slippage) AS avg_slippage,
                   SUM(total_cost) AS total_cost,
                   COUNT(*) AS trade_count
            FROM reconciliation_results
            GROUP BY broker_id
            ORDER BY avg_slippage ASC, total_cost ASC;
        """
        rankings = pd.read_sql_query(broker_ranking_query, conn)
        conn.close()

        rankings_list = rankings.to_dict(orient="records")
        return jsonify({"status": "success", "rankings": rankings_list}), 200
    except Exception as e:
        logging.error(f"Error generating broker ranking: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
