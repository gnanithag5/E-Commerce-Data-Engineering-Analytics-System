from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"

# Load .env file
load_dotenv(dotenv_path)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

MONGO_URI = os.getenv("MONGO_URI")
MONGODB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")
MV_COLLECTION_NAME = os.getenv("MV_COLLECTION_NAME")

RDBMS_HOST = os.getenv("RDBMS_HOST")
RDBMS_PORT = os.getenv("RDBMS_PORT")
RDBMS_USER = os.getenv("RDBMS_USER")
RDBMS_PASSWORD = os.getenv("RDBMS_PASSWORD")
RDBMS_DB = os.getenv("RDBMS_DB")

