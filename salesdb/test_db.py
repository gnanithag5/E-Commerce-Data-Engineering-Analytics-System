import psycopg2
from psycopg2 import sql
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def test_database():
    logger.info(f"Starting DB schema validation for '{DB_NAME}'")
    status = 0  # 0 = success, 1 = failure

    TABLES_TO_CHECK = ["staff", "sales_transaction", "customer", "product"]
    COLUMNS_TO_CHECK = [("customer", "email"), ("product", "product_price")]
    FKS_TO_CHECK = ["sales_transaction", "sales_detail"]

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        def check_table(table_name):
            nonlocal status
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = %s
                );
            """, (table_name,))
            exists = cur.fetchone()[0]
            if exists:
                logger.info(f"Table '{table_name}' exists")
            else:
                logger.error(f"Table '{table_name}' NOT FOUND")
                status = 1

        def check_column(table_name, column_name):
            nonlocal status
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns
                    WHERE table_name = %s AND column_name = %s
                );
            """, (table_name, column_name))
            exists = cur.fetchone()[0]
            if exists:
                logger.info(f"Column '{column_name}' in '{table_name}' exists")
            else:
                logger.error(f"Column '{column_name}' in '{table_name}' MISSING")
                status = 1

        def check_fk_constraints(table_name):
            nonlocal status
            cur.execute("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = %s AND constraint_type = 'FOREIGN KEY';
            """, (table_name,))
            rows = cur.fetchall()
            if rows:
                logger.info(f"Foreign keys found in table '{table_name}'")
            else:
                logger.error(f"No foreign keys found in table '{table_name}'")
                status = 1

        def check_row_count(table_name):
            nonlocal status
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name)))
            count = cur.fetchone()[0]
            if count > 0:
                logger.info(f"Table '{table_name}' has {count} rows")
            else:
                logger.warning(f"Table '{table_name}' has no rows")
                status = 1

        # Execute checks
        for table in TABLES_TO_CHECK:
            check_table(table)
            check_row_count(table)

        for table, column in COLUMNS_TO_CHECK:
            check_column(table, column)

        for table in FKS_TO_CHECK:
            check_fk_constraints(table)

        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error during schema validation: {e}")
        status = 1

    if status == 0:
        logger.info("All schema and data checks passed.")
    else:
        logger.error("One or more checks failed. Review logs for details.")

    return status

# Run directly
if __name__ == "__main__":
    test_database()
