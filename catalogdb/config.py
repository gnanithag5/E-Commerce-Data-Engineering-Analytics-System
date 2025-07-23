from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"

# Load .env file
load_dotenv(dotenv_path)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
MV_COLLECTION_NAME = os.getenv("MV_COLLECTION_NAME")