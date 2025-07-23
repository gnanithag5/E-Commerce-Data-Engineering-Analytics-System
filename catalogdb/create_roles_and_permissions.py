import logging
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_roles_and_users():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        admin_db = client["admin"]

        users = [
            {
                "user": "appUser",
                "pwd": "appPassword123",
                "roles": [{"role": "readWrite", "db": DB_NAME}]
            },
            {
                "user": "analyticsUser",
                "pwd": "readOnly456",
                "roles": [{"role": "read", "db": DB_NAME}]
            }
        ]

        for user in users:
            try:
                admin_db.command("createUser", user["user"], pwd=user["pwd"], roles=user["roles"])
                logging.info(f"Created user: {user['user']}")
            except errors.OperationFailure as e:
                if "already exists" in str(e):
                    logging.warning(f"User '{user['user']}' already exists. Skipping.")
                else:
                    logging.error(f"Error creating user '{user['user']}': {e}")
                    raise

    except errors.PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    create_roles_and_users()
