import random
import logging
from faker import Faker
from datetime import datetime
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
fake = Faker()

categories = {
    "Laptop": ["Intel i5", "Intel i7", "AMD Ryzen 5"],
    "Smartphone": ["A16 Bionic", "Snapdragon 8 Gen 2"],
    "Television": ["OLED", "QLED"]
}

brands = {
    "Laptop": ["Dell", "HP", "Lenovo"],
    "Smartphone": ["Apple", "Samsung", "OnePlus"],
    "Television": ["LG", "Sony", "Samsung"]
}

def generate_product():
    category = random.choice(list(categories.keys()))
    
    specs = {}
    if category == "Laptop":
        specs = {
            "processor": random.choice(categories[category]),
            "ram": random.choice(["8GB", "16GB"]),
            "storage": random.choice(["256GB SSD", "512GB SSD"]),
            "screen_size": random.choice(["13.3 inch", "15.6 inch"]),
        }
    elif category == "Smartphone":
        specs = {
            "processor": random.choice(categories[category]),
            "storage": random.choice(["128GB", "256GB"]),
            "camera": random.choice(["12MP", "48MP"]),
            "battery": random.choice(["3000mAh", "4000mAh"]),
        }
    elif category == "Television":
        specs = {
            "screen_type": random.choice(categories[category]),
            "screen_size": random.choice(["43 inch", "55 inch"]),
            "smart_tv": True,
        }

    return {
        "product_id": fake.unique.bothify(text="???###"),
        "name": fake.catch_phrase(),
        "category": category,
        "brand": random.choice(brands[category]),
        "price": round(random.uniform(200, 2000), 2),
        "specs": specs,
        "available_colors": random.sample(["Black", "Silver", "White", "Blue"], k=2),
        "in_stock": random.choice([True, False]),
        "rating": round(random.uniform(3.5, 5.0), 1),
        "reviews_count": random.randint(0, 1000),
        "updated_at": datetime.utcnow().isoformat()
    }

def generate_and_insert_data(n=1000):
    try:
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][COLLECTION_NAME]

        # Clear previous data
        collection.delete_many({})
        logging.info(f"Cleared existing data in '{COLLECTION_NAME}' collection.")

        # Insert new data
        data = [generate_product() for _ in range(n)]
        result = collection.insert_many(data)
        logging.info(f"Inserted {len(result.inserted_ids)} documents into '{COLLECTION_NAME}'.")

    except errors.PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during data generation: {e}")

if __name__ == "__main__":
    generate_and_insert_data()
