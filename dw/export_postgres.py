import os
import logging
import pandas as pd
import psycopg2
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, RDBMS_DB

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

# Connection config
DB_CONFIG = {
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'dbname': RDBMS_DB
}

# Output folder
BASE_DIR = os.path.dirname(__file__)
STAGING_DIR = os.path.join(BASE_DIR, 'staging')
os.makedirs(STAGING_DIR, exist_ok=True)

TABLES = [
    'staff',
    'sales_outlet',
    'customer',
    'product_type',
    'product',
    'sales_transaction',
    'sales_detail'
]

def extract_table_to_csv(table_name, conn):
    try:
        logging.info(f"Extracting table: {table_name}")
        query = f"SELECT * FROM public.{table_name}"
        df = pd.read_sql_query(query, conn)

        csv_path = os.path.join(STAGING_DIR, f"{table_name}.csv")
        df.to_csv(csv_path, index=False)
        logging.info(f"Saved: {csv_path}")
    except Exception as e:
        logging.exception(f"Failed to extract table: {table_name}")

def main():
    try:
        logging.info("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)

        for table in TABLES:
            extract_table_to_csv(table, conn)

        conn.close()
        logging.info("Extraction complete.")

    except Exception as e:
        logging.exception("Error during PostgreSQL extraction")

if __name__ == "__main__":
    main()
