import logging
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, MV_COLLECTION_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def aggregate_data():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]

        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "avg_rating": {"$avg": "$rating"},
                    "total_products": {"$sum": 1}
                }
            },
            {
                "$out": MV_COLLECTION_NAME
            }
        ]

        db[COLLECTION_NAME].aggregate(pipeline)
        logging.info(f"Materialized view '{MV_COLLECTION_NAME}' refreshed from '{COLLECTION_NAME}'.")

    except errors.PyMongoError as e:
        logging.error(f"MongoDB aggregation error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during aggregation: {e}")

if __name__ == "__main__":
    aggregate_data()
