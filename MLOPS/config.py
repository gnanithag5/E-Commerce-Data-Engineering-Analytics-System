from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_URL = f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

POSTGRES_PROPERTIES = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "driver": "org.postgresql.Driver"
}

JDBC_JAR_PATH = os.getenv("JDBC_JAR_PATH")
