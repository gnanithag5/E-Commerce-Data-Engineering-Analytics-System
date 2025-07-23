-- DROP OLD TABLES IF THEY EXIST
DROP TABLE IF EXISTS public.fact_sales CASCADE;
DROP TABLE IF EXISTS public.dim_date CASCADE;
DROP TABLE IF EXISTS public.dim_outlet CASCADE;
DROP TABLE IF EXISTS public.dim_staff CASCADE;
DROP TABLE IF EXISTS public.dim_product CASCADE;
DROP TABLE IF EXISTS public.dim_customer CASCADE;

-- DIMENSION TABLES
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    gender TEXT,
    reg_date DATE
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INT PRIMARY KEY,
    product_name TEXT,
    description TEXT,
    product_price NUMERIC,
    start_date DATE,
    end_date DATE,
    current_flag BOOLEAN,
    product_type_id INT,
    product_type TEXT,
    product_category TEXT,
    category TEXT,
    brand TEXT,
    spec_processor TEXT,
    spec_ram TEXT,
    spec_storage TEXT,
    spec_screen_size TEXT
);

CREATE TABLE IF NOT EXISTS dim_staff (
    staff_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    position TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS dim_outlet (
    sales_outlet_id INT PRIMARY KEY,
    sales_outlet_type TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    transaction_date DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);

-- FACT TABLE
CREATE TABLE IF NOT EXISTS fact_sales (
    transaction_id INT,
    transaction_date DATE,
    product_id INT,
    customer_id INT,
    staff_id INT,
    sales_outlet_id INT,
    quantity INT,
    price NUMERIC,
    total_amount NUMERIC,
    PRIMARY KEY (transaction_id, product_id),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(transaction_date),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (staff_id) REFERENCES dim_staff(staff_id),
    FOREIGN KEY (sales_outlet_id) REFERENCES dim_outlet(sales_outlet_id)
);
