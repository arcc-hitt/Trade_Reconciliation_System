import sqlite3
import pandas as pd
import logging
from email import policy
from email.parser import BytesParser
from pathlib import Path
from io import BytesIO 

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_client_orders(db_path):
    """
    Load client orders from the SQLite database.
    """
    logging.info("Loading client orders from database...")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM client_orders", conn)
    conn.close()
    logging.info(f"Loaded {len(df)} client orders.")
    return df

def parse_eml_files(eml_folder):
    """
    Parse .eml files containing broker trade data.
    """
    trade_data = []
    eml_files = Path(eml_folder).glob("*.eml")
    
    for eml_file in eml_files:
        logging.info(f"Processing email file: {eml_file}")
        try:
            with open(eml_file, 'rb') as file:
                msg = BytesParser(policy=policy.default).parse(file)
                for attachment in msg.iter_attachments():
                    if attachment.get_filename().endswith('.xlsx'):
                        byte_stream = BytesIO(attachment.get_payload(decode=True))
                        df = pd.read_excel(byte_stream) 
                        df.columns = [col.strip().lower() for col in df.columns]
                        
                        df.rename(columns={
                            'instrument isin': 'symbol',
                            'qty': 'quantity',
                            'cost': 'trade_price',
                            'net amount': 'net_amount',
                            'brokerage amount': 'brokerage_amount',
                            'stt': 'stt',
                            'deal date': 'trade_date',
                            'party code/sebi regn code of party': 'broker_id',
                            'buy/sell flag': 'buy_sell_flag',
                            'settlement date': 'settlement_date',
                            'exchange code': 'exchange_code',
                            'depository code': 'depository_code',
                            'col 8': 'col_8'
                        }, inplace=True)
                        trade_data.append(df)
        except Exception as e:
            logging.error(f"Error processing {eml_file}: {e}")
    
    all_trades = pd.concat(trade_data, ignore_index=True) if trade_data else pd.DataFrame()
    logging.info(f"Extracted {len(all_trades)} trades from email attachments.")
    return all_trades

def save_broker_trades_to_db(broker_trades, db_path="trades.db"):
    """
    Save broker trades into the SQLite database.
    """
    logging.info("Saving broker trades to database...")
    if not broker_trades.empty:
        conn = sqlite3.connect(db_path)
        broker_trades.to_sql("broker_trades", conn, if_exists='append', index=False)
        conn.close()
        logging.info("Broker trades saved successfully.")
    else:
        logging.warning("No broker trades to save.")

if __name__ == "__main__":
    client_orders = load_client_orders("trades.db")
    broker_trades = parse_eml_files("broker_emails/")
    save_broker_trades_to_db(broker_trades, "trades.db")
    logging.info("Trade extraction and saving process completed.")