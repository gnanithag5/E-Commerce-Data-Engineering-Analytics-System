import logging
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]

        if COLLECTION_NAME in db.list_collection_names():
            db[COLLECTION_NAME].drop()
            logging.info(f"Dropped existing collection: {COLLECTION_NAME}")

        product_schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["product_id", "name", "category", "brand", "price"],
                "properties": {
                    "product_id": {"bsonType": "string"},
                    "name": {"bsonType": "string"},
                    "category": {
                        "enum": ["Laptop", "Smartphone", "Television"]
                    },
                    "brand": {"bsonType": "string"},
                    "price": {
                        "bsonType": "double",
                        "minimum": 0
                    },
                    "specs": {"bsonType": "object"},
                    "in_stock": {"bsonType": "bool"},
                    "rating": {"bsonType": "double"},
                    "reviews_count": {"bsonType": "int"},
                    "updated_at": {"bsonType": "string"}
                }
            }
        }

        db.create_collection(
            COLLECTION_NAME,
            validator=product_schema,
            validationLevel='moderate'
        )
        logging.info(f"Collection '{COLLECTION_NAME}' created with schema in database '{DB_NAME}'.")

    except errors.PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    run()
