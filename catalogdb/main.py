# main.py

import logging
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
import create_schema
import create_roles_and_permissions
import generate_data
import test_db
import create_indexes
import aggregation_data
import scd2_update

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_database_if_not_exists():
    """Force MongoDB to create the database if it doesn't exist."""
    try:
        logging.info("Checking MongoDB server and ensuring database exists...")
        client = MongoClient(MONGO_URI)
        if DB_NAME not in client.list_database_names():
            logging.info(f"Database does not exist. Forcing creation...")
            # Force creation by inserting and deleting a dummy document
            temp_collection = client[DB_NAME]["__temp__init__"]
            temp_collection.insert_one({"temp": True})
            temp_collection.drop()
            logging.info(f"Database created.")
        else:
            logging.info(f"Database already exists.")
    except errors.PyMongoError as e:
        logging.error(f"MongoDB connection or creation error: {e}")
        exit(1)

def run_pipeline():
    logging.info("=== MongoDB ETL Pipeline Starting ===")

    create_database_if_not_exists()

    logging.info("Step 1: Creating schema...")
    create_schema.run()

    logging.info("Step 2: Creating roles and permissions...")
    create_roles_and_permissions.create_roles_and_users()

    logging.info("Step 3: Generating and inserting data...")
    generate_data.generate_and_insert_data()

    logging.info("Step 4: Running database health checks...")
    test_db.run_health_checks()

    logging.info("Step 5: Creating indexes...")
    create_indexes.create_indexes()

    logging.info("Step 6: Generating data aggregation (materialized view)...")
    aggregation_data.aggregate_data()

    logging.info("Step 7: Performing sample SCD2 update...")
    scd2_update.update_product_scd("ABC123", "UltraBook X", 999.99)

    logging.info("=== MongoDB ETL Pipeline Completed ===")

if __name__ == "__main__":
    run_pipeline()
