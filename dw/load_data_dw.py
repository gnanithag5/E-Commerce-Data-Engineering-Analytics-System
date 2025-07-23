import os
import logging
import pandas as pd
import psycopg2
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

BASE_DIR = os.path.dirname(__file__)
TRANSFORMED = os.path.join(BASE_DIR, 'transformed')

TABLES = [
    'dim_date',
    'dim_customer',
    'dim_product',
    'dim_staff',
    'dim_outlet',
    'fact_sales'
]

def insert_csv_to_table(conn, csv_path, table_name):
    logging.info(f"Loading {csv_path} into {table_name}...")
    df = pd.read_csv(csv_path)
    
    df.replace(['NaN', 'nan', 'NaT'], None, inplace=True)
    df = df.where(pd.notnull(df), None)

    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
            df[col] = df[col].apply(lambda x: x if pd.notnull(x) else None)

    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
        for _, row in df.iterrows():
            cols = ','.join(row.index)
            placeholders = ','.join(['%s'] * len(row))
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
            cur.execute(sql, tuple(row))
    conn.commit()

def main():
    logging.info("Loading transformed data into data warehouse...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

    for table in TABLES:
        try:
            csv_path = os.path.join(TRANSFORMED, f"{table}.csv")
            insert_csv_to_table(conn, csv_path, table)
            logging.info(f" Loaded: {table}")
        except Exception as e:
            logging.exception(f" Failed to load table: {table}")

    conn.close()
    logging.info("All loads completed.")

if __name__ == "__main__":
    main()
