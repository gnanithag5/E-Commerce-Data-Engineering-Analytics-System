import psycopg2
from faker import Faker
import random
import string
import logging
from datetime import date

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection details
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Initialize Faker instance
fake = Faker()

# Helper function to generate random strings
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Data Generators
def generate_staff_data(num_records=200):
    return [
        (
            i + 1,
            fake.first_name(),
            fake.last_name(),
            random.choice(['Manager', 'Clerk', 'Salesperson']),
            fake.date_this_decade(),
            random.choice(['NY', 'CA', 'TX', 'FL', 'WA', 'OH'])
        )
        for i in range(num_records)
    ]

def generate_sales_outlet_data(num_records=50):
    return [
        (
            i + 1,
            random.choice(['Retail', 'Wholesale']),
            fake.address(),
            fake.city(),
            fake.phone_number(),
            fake.zipcode(),
            random.randint(1, 200)  # manager staff_id
        )
        for i in range(num_records)
    ]

def generate_customer_data(num_records=1000):
    return [
        (
            i + 1,
            fake.name(),
            fake.email(),
            fake.date_this_decade(),
            random_string(15),
            fake.date_of_birth(minimum_age=18, maximum_age=80),
            random.choice(['M', 'F'])
        )
        for i in range(num_records)
    ]

# Define categories and brands
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

# Map for product_type_id generation
product_type_list = list(categories.keys())  # ['Laptop', 'Smartphone', 'Television']

def generate_product_type_data():
    return [
        (i + 1, product_type_list[i], "Electronics")
        for i in range(len(product_type_list))
    ]

def generate_product_data(num_records=200):
    data = []
    for i in range(num_records):
        product_type = random.choice(product_type_list)
        brand = random.choice(brands[product_type])
        spec = random.choice(categories[product_type])

        product_name = f"{brand} {product_type}"
        description = f"{brand} {product_type} with {spec}"
        price = round(random.uniform(200, 2000), 2)
        product_type_id = product_type_list.index(product_type) + 1

        data.append((
            i + 1,
            product_name,
            description,
            price,
            product_type_id
        ))
    return data


def generate_sales_transaction_data(num_records=1000):
    return [
        (
            i + 1,
            fake.date_between(start_date=date(2023, 1, 1), end_date=date(2025, 1, 31)),
            fake.time(),
            random.randint(1, 50),    # sales_outlet_id
            random.randint(1, 200),   # staff_id
            random.randint(1, 1000)   # customer_id
        )
        for i in range(num_records)
    ]

def generate_sales_detail_data(num_records=5000):
    return [
        (
            i + 1,
            random.randint(1, 1000),  # transaction_id
            random.randint(1, 200),   # product_id
            random.randint(1, 100),
            round(random.uniform(5.0, 500.0), 2)
        )
        for i in range(num_records)
    ]

# Individual Insert Functions
def insert_product_types(cur):
    logger.info("Inserting product types...")
    cur.executemany(
        "INSERT INTO public.product_type (product_type_id, product_type, product_category) VALUES (%s, %s, %s)",
        generate_product_type_data()
    )

def insert_products(cur):
    logger.info("Inserting products...")
    cur.executemany(
        "INSERT INTO public.product (product_id, product_name, description, product_price, product_type_id) VALUES (%s, %s, %s, %s, %s)",
        generate_product_data()
    )

def insert_staff(cur):
    logger.info("Inserting staff...")
    cur.executemany(
        "INSERT INTO public.staff (staff_id, first_name, last_name, position, start_date, location) VALUES (%s, %s, %s, %s, %s, %s)",
        generate_staff_data()
    )

def insert_sales_outlets(cur):
    logger.info("Inserting sales outlets...")
    cur.executemany(
        "INSERT INTO public.sales_outlet (sales_outlet_id, sales_outlet_type, address, city, telephone, postal_code, manager) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        generate_sales_outlet_data()
    )

def insert_customers(cur):
    logger.info("Inserting customers...")
    cur.executemany(
        "INSERT INTO public.customer (customer_id, customer_name, email, reg_date, card_number, date_of_birth, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        generate_customer_data()
    )

def insert_transactions(cur):
    logger.info("Inserting transactions...")
    cur.executemany(
        "INSERT INTO public.sales_transaction (transaction_id, transaction_date, transaction_time, sales_outlet_id, staff_id, customer_id) VALUES (%s, %s, %s, %s, %s, %s)",
        generate_sales_transaction_data()
    )

def insert_sales_details(cur):
    logger.info("Inserting sales details...")
    cur.executemany("""
        INSERT INTO public.sales_detail (sales_detail_id, transaction_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s, %s)
    """, generate_sales_detail_data())


# Main Insert Function
def insert_data():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
            host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()

        insert_product_types(cur)
        insert_products(cur)
        insert_staff(cur)
        insert_sales_outlets(cur)
        insert_customers(cur)
        insert_transactions(cur)
        insert_sales_details(cur)

        conn.commit()
        logger.info("All data inserted successfully.")
    
    except Exception as e:
        logger.error("Error during data insertion", exc_info=True)
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        logger.info("Connection closed.")

# Run directly
if __name__ == "__main__":
    insert_data()
