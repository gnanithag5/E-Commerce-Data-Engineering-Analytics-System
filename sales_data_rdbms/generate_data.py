import psycopg2
from faker import Faker
import random
import string

# Initialize Faker instance for generating random data
fake = Faker()

# Database connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "your_database"
DB_USER = "your_user"
DB_PASSWORD = "your_password"

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# Helper function to generate random strings
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 1. Generate data for the staff table (e.g., 200 staff members)
def generate_staff_data(num_records=200):
    staff_data = []
    for _ in range(num_records):
        staff_data.append(
            (
                fake.unique.random_number(digits=5),
                fake.first_name(),
                fake.last_name(),
                random.choice(['Manager', 'Clerk', 'Salesperson']),
                fake.date_this_decade(),
                random.choice(['NY', 'CA', 'TX', 'FL', 'WA', 'OH'])
            )
        )
    return staff_data

# 2. Generate data for the sales_outlet table (e.g., 50 sales outlets)
def generate_sales_outlet_data(num_records=50):
    sales_outlet_data = []
    for _ in range(num_records):
        sales_outlet_data.append(
            (
                fake.unique.random_number(digits=5),
                random.choice(['Retail', 'Wholesale']),
                fake.address(),
                fake.city(),
                fake.phone_number(),
                fake.zipcode(),
                random.randint(1, 50)  # Random manager id (staff_id)
            )
        )
    return sales_outlet_data

# 3. Generate data for the customer table (e.g., 1000 customers)
def generate_customer_data(num_records=1000):
    customer_data = []
    for _ in range(num_records):
        customer_data.append(
            (
                fake.unique.random_number(digits=5),
                fake.name(),
                fake.email(),
                fake.date_this_decade(),
                random_string(15),  # Random card number
                fake.date_of_birth(minimum_age=18, maximum_age=80),
                random.choice(['M', 'F'])
            )
        )
    return customer_data

# 4. Generate data for the sales_detail table (e.g., 5000 records of sales)
def generate_sales_detail_data(num_records=5000):
    sales_detail_data = []
    for _ in range(num_records):
        sales_detail_data.append(
            (
                fake.unique.random_number(digits=5),
                random.randint(1, 200),  # Random transaction_id (matching number of sales_transactions)
                random.randint(1, 50),  # Random product_id (matching number of products)
                random.randint(1, 100),  # Quantity
                round(random.uniform(5.0, 500.0), 2)  # Price
            )
        )
    return sales_detail_data

# 5. Generate data for the product table (e.g., 200 products)
def generate_product_data(num_records=200):
    product_data = []
    for _ in range(num_records):
        product_data.append(
            (
                fake.unique.random_number(digits=5),
                fake.word(),
                fake.text(max_nb_chars=200),
                round(random.uniform(5.0, 500.0), 2),  # Random price
                random.randint(1, 10)  # Random product_type_id
            )
        )
    return product_data

# 6. Generate data for the product_type table (e.g., 10 product types)
def generate_product_type_data(num_records=10):
    product_type_data = []
    for _ in range(num_records):
        product_type_data.append(
            (
                fake.unique.random_number(digits=5),
                fake.word(),
                random.choice(['Electronics', 'Furniture', 'Clothing', 'Toys', 'Books'])
            )
        )
    return product_type_data

# Insert generated data into the database
def insert_data():
    # Insert data into staff table
    staff_data = generate_staff_data(200)
    cur.executemany("""
        INSERT INTO public.staff (staff_id, first_name, last_name, "position", start_date, location)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, staff_data)
    print("Inserted staff data.")

    # Insert data into sales_outlet table
    sales_outlet_data = generate_sales_outlet_data(50)
    cur.executemany("""
        INSERT INTO public.sales_outlet (sales_outlet_id, sales_outlet_type, address, city, telephone, postal_code, manager)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, sales_outlet_data)
    print("Inserted sales_outlet data.")

    # Insert data into customer table
    customer_data = generate_customer_data(1000)
    cur.executemany("""
        INSERT INTO public.customer (customer_id, customer_name, email, reg_date, card_number, date_of_birth, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, customer_data)
    print("Inserted customer data.")

    # Insert data into sales_detail table
    sales_detail_data = generate_sales_detail_data(5000)
    cur.executemany("""
        INSERT INTO public.sales_detail (sales_detail_id, transaction_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s, %s)
    """, sales_detail_data)
    print("Inserted sales_detail data.")

    # Insert data into product table
    product_data = generate_product_data(200)
    cur.executemany("""
        INSERT INTO public.product (product_id, product_name, description, product_price, product_type_id)
        VALUES (%s, %s, %s, %s, %s)
    """, product_data)
    print("Inserted product data.")

    # Insert data into product_type table
    product_type_data = generate_product_type_data(10)
    cur.executemany("""
        INSERT INTO public.product_type (product_type_id, product_type, product_category)
        VALUES (%s, %s, %s)
    """, product_type_data)
    print("Inserted product_type data.")

    # Commit all transactions
    conn.commit()

# Run the data generation script
if __name__ == "__main__":
    try:
        insert_data()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        cur.close()
        conn.close()
