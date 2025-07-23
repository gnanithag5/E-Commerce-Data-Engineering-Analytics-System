import psycopg2
import logging
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

TABLES = [
    'dim_date',
    'dim_customer',
    'dim_product',
    'dim_staff',
    'dim_outlet',
    'fact_sales'
]

def test_tables():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cur = conn.cursor()
        logging.info("Verifying data warehouse tables...")

        for table in TABLES:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                count = cur.fetchone()[0]
                if count > 0:
                    logging.info(f"{table} has {count} rows.")
                else:
                    logging.warning(f"{table} exists but is empty.")
            except Exception as e:
                logging.error(f"Failed to query {table}: {e}")

        cur.close()
        conn.close()
    except Exception as e:
        logging.exception("Could not connect to database for testing.")

if __name__ == "__main__":
    test_tables()
