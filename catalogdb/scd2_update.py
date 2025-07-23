# transformations/scd_update.py

import logging
from datetime import datetime
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def update_product_scd(product_id, name, new_price):
    try:
        now = datetime.utcnow()
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][COLLECTION_NAME]

        # Step 1: Find current version
        current_doc = collection.find_one({"product_id": product_id, "is_current": True})
        if not current_doc:
            logging.warning(f"No current version found for product_id: {product_id}. Skipping update.")
            return

        # Step 2: Expire the current version
        collection.update_one(
            {"_id": current_doc["_id"]},
            {"$set": {"valid_to": now, "is_current": False}}
        )
        logging.info(f"Expired current version for product_id: {product_id}")

        # Step 3: Insert new version with updated values, copying other fields
        new_version = current_doc.copy()
        new_version.pop("_id")  # remove MongoDB internal ID
        new_version.update({
            "name": name,
            "price": new_price,
            "valid_from": now,
            "valid_to": None,
            "is_current": True
        })

        collection.insert_one(new_version)
        logging.info(f"Inserted new version for product_id: {product_id} at {now.isoformat()}")

    except errors.PyMongoError as e:
        logging.error(f"MongoDB error during SCD update: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during SCD update: {e}")

if __name__ == "__main__":
    update_product_scd("ABC123", "UltraBook X", 999.99)
