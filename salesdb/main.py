import subprocess
import psycopg2
import os
import time
import logging
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# ---------------------- Logging Configuration ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ---------------------- Utility Functions ----------------------

def create_database():
    """Creates the PostgreSQL database if it doesn't exist."""
    try:
        logger.info(f"Checking if database exists...")
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Drop if exists
        cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{DB_NAME}' AND pid <> pg_backend_pid();")
        cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
        logger.info(f"Dropped database {DB_NAME}")

        # Create again
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        logger.info(f"Created database {DB_NAME}")


        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to check or create database: {e}")
        exit(1)

def run_sql_file(file_path):
    """Executes a SQL file using psql."""
    logger.info(f"Running SQL script: {file_path}")
    result = subprocess.run(
        ['psql', '-h', DB_HOST, '-p', str(DB_PORT), '-U', DB_USER, '-d', DB_NAME, '-f', file_path],
        env={**os.environ, 'PGPASSWORD': DB_PASSWORD},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Error executing {file_path}:\n{result.stderr}")
        exit(1)
    else:
        logger.info(f"Successfully executed {file_path}")

def run_python_script(script_path):
    """Runs a Python script."""
    logger.info(f"Running Python script: {script_path}")
    result = subprocess.run(
        ['python', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Error running {script_path}:\n{result.stderr}")
        exit(1)
    else:
        logger.info(f"Successfully ran {script_path}")

# ---------------------- Main Execution ----------------------

if __name__ == "__main__":
    logger.info("Starting full pipeline...")

    create_database()

    run_sql_file("create_schema.sql")
    run_sql_file("create_roles_and_permissions.sql")
    run_python_script("generate_data.py")
    run_python_script("test_db.py")
    run_sql_file("create_indexes.sql")
    run_sql_file("create_scd2_tracking.sql")
    run_sql_file("create_product_audit_and_triggers.sql")

    logger.info("All steps completed successfully.")
