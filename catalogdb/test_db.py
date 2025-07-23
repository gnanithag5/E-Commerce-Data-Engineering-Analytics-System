# scripts/test_db.py

import logging
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def check_collection_exists(db):
    if COLLECTION_NAME not in db.list_collection_names():
        raise AssertionError(f"Collection '{COLLECTION_NAME}' not found in database '{DB_NAME}'.")
    logging.info("Collection exists: OK")

def check_document_count(collection, expected_count=1000):
    count = collection.count_documents({})
    if count != expected_count:
        raise AssertionError(f"Document count mismatch: expected {expected_count}, found {count}.")
    logging.info(f"Document count: {count} OK")

def check_unique_product_ids(collection):
    total = collection.count_documents({})
    unique = len(collection.distinct("product_id"))
    if unique != total:
        raise AssertionError(f"Duplicate product_id values found: {total - unique} duplicates.")
    logging.info(f"All product_id values are unique: {unique} OK")

def run_health_checks():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        logging.info("Starting MongoDB health checks...")
        logging.info("--------------------------------------")

        check_collection_exists(db)
        check_document_count(collection)
        check_unique_product_ids(collection)

        logging.info("--------------------------------------")
        logging.info("All health checks passed!")

    except AssertionError as ae:
        logging.error(f"Health check failed: {ae}")
    except Exception as e:
        logging.error(f"Unexpected error during health checks: {e}")

if __name__ == "__main__":
    run_health_checks()
