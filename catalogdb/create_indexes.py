# transformations/create_indexes.py

import logging
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_indexes():
    try:
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][COLLECTION_NAME]

        # Composite unique index
        collection.create_index(
            [("product_id", 1), ("valid_from", 1)],
            unique=True,
            name="idx_product_version_unique"
        )
        logging.info("Created unique index: idx_product_version_unique on fields ['product_id', 'valid_from']")

        # Index on category
        collection.create_index("category", name="idx_category")
        logging.info("Created index: idx_category on field 'category'")

        # Index on brand
        collection.create_index("brand", name="idx_brand")
        logging.info("Created index: idx_brand on field 'brand'")

    except errors.PyMongoError as e:
        logging.error(f"MongoDB error while creating indexes: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during index creation: {e}")

if __name__ == "__main__":
    create_indexes()
