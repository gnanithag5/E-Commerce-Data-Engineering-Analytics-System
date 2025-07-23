import os
import subprocess
import logging
import psycopg2
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# --- Paths ---
BASE_DIR = os.path.dirname(__file__)
SQL_DIR = BASE_DIR
SCRIPTS = {
    "export_postgres": os.path.join(BASE_DIR, "export_postgres.py"),
    "export_mongodb": os.path.join(BASE_DIR, "export_mongodb.py"),
    "transform": os.path.join(BASE_DIR, "transform_data.py"),
    "load": os.path.join(BASE_DIR, "load_data_dw.py"),
    "test_db": os.path.join(BASE_DIR, "test_db.py")
}
SQL_FILES = {
    "schema": os.path.join(SQL_DIR, "create_fact_dim_tables.sql"),
    "roles": os.path.join(SQL_DIR, "create_roles_and_permissions.sql"),
    "index": os.path.join(SQL_DIR, "create_index.sql"),
    "analytics": os.path.join(SQL_DIR, "analytics.sql")
}

# --- Create DB if not exists ---
def create_database():
    try:
        logger.info("Checking if database exists...")
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE {DB_NAME};')
            logger.info("Database created.")
        else:
            logger.info("Database already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to check or create database: {e}")
        exit(1)

# --- Run SQL File ---
def run_sql_file(sql_file):
    try:
        logger.info(f"Running SQL file: {sql_file}")
        command = f'psql -h {DB_HOST} -U {DB_USER} -d {DB_NAME} -f "{sql_file}"'
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD
        subprocess.run(command, shell=True, check=True, env=env)
        logger.info(f"Executed: {os.path.basename(sql_file)}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed: {sql_file}\n{e}")
        exit(1)

# --- Run Python Script ---
def run_python_script(script_path):
    try:
        logger.info(f"Running script: {os.path.basename(script_path)}")
        subprocess.run(["python", script_path], check=True)
        logger.info(f"Completed: {os.path.basename(script_path)}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed: {script_path}\n{e}")
        exit(1)

# --- Pipeline ---
def run_pipeline():
    create_database()
    run_sql_file(SQL_FILES["schema"])
    run_sql_file(SQL_FILES["roles"])
    run_python_script(SCRIPTS["export_postgres"])
    run_python_script(SCRIPTS["export_mongodb"])
    run_python_script(SCRIPTS["transform"])
    run_python_script(SCRIPTS["load"])
    run_python_script(SCRIPTS["test_db"])
    run_sql_file(SQL_FILES["index"])
    run_sql_file(SQL_FILES["analytics"])
    logger.info("Pipeline execution complete.")

if __name__ == "__main__":
    run_pipeline()
