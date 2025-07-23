import os
import logging
import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI, MONGODB_NAME, COLLECTION_NAME

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

# Output path
BASE_DIR = os.path.dirname(__file__)
STAGING_DIR = os.path.join(BASE_DIR, 'staging')
os.makedirs(STAGING_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(STAGING_DIR, 'product_catalog.csv')

def flatten_document(doc):
    flat = {
        "product_id": doc.get("product_id"),
        "name": doc.get("name"),
        "category": doc.get("category"),
        "brand": doc.get("brand"),
        "price": doc.get("price"),
        "in_stock": doc.get("in_stock"),
        "rating": doc.get("rating"),
        "reviews_count": doc.get("reviews_count"),
        "updated_at": doc.get("updated_at"),
    }
    specs = doc.get("specs", {})
    for key, value in specs.items():
        flat[f"spec_{key}"] = value
    return flat

def main():
    try:
        logging.info("Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        collection = client[MONGODB_NAME][COLLECTION_NAME]

        logging.info(f"Extracting documents from collection: {COLLECTION_NAME}")
        cursor = collection.find({})
        flattened_data = [flatten_document(doc) for doc in cursor]

        df = pd.DataFrame(flattened_data)
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Flattened catalog exported to {OUTPUT_FILE}")

    except Exception as e:
        logging.exception("Failed to export data from MongoDB.")

if __name__ == "__main__":
    main()
