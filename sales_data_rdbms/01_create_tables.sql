-- The DROP statements have been added to ensure that no errors occur if the script is mistakenly run more than once
DROP TABLE IF EXISTS public.staff CASCADE;
DROP TABLE IF EXISTS public.sales_outlet CASCADE;
DROP TABLE IF EXISTS public.customer CASCADE;
DROP TABLE IF EXISTS public.sales_detail CASCADE;
DROP TABLE IF EXISTS public.product CASCADE;
DROP TABLE IF EXISTS public.product_type CASCADE;
DROP TABLE IF EXISTS public.sales_transaction CASCADE;
--

--Create the partitioned table (sales_transaction) with partitioning specifications
CREATE TABLE public.sales_transaction (
    transaction_id integer,
    transaction_date date,
    transaction_time time without time zone,
    sales_outlet_id integer,
    staff_id integer,
    customer_id integer,
    PRIMARY KEY (transaction_id, transaction_date)  -- Primary key including transaction_date for partitioning
)
PARTITION BY RANGE (transaction_date);  -- Partitioning by transaction_date

-- Step 2: Create partitions for each year (example)
CREATE TABLE public.sales_transaction_2023 PARTITION OF public.sales_transaction
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE public.sales_transaction_2024 PARTITION OF public.sales_transaction
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE public.sales_transaction_2025 PARTITION OF public.sales_transaction
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');


CREATE TABLE public.staff
(
    staff_id integer,
    first_name character varying(50),
    last_name character varying(50),
    "position" character varying(50),
    start_date date,
    location character varying(5),
    PRIMARY KEY (staff_id)
);

CREATE TABLE public.sales_outlet
(
    sales_outlet_id integer,
    sales_outlet_type character varying(20),
    address character varying(50),
    city character varying(40),
    telephone character varying(15),
    postal_code integer,
    manager integer,
    PRIMARY KEY (sales_outlet_id)
);

CREATE TABLE public.customer
(
    customer_id integer,
    customer_name character varying(50),
    email character varying(50),
    reg_date date,
    card_number character varying(15),
    date_of_birth date,
    gender character(1),
    PRIMARY KEY (customer_id)
);

CREATE TABLE public.sales_detail
(
    sales_detail_id integer,
    transaction_id integer,
    product_id integer,
    quantity integer,
    price double precision,
    PRIMARY KEY (sales_detail_id)
);


CREATE TABLE public.product
(
    product_id integer,
    product_name character varying(100),
    description character varying(250),
    product_price double precision,
    product_type_id integer,
    PRIMARY KEY (product_id)
);

CREATE TABLE public.product_type
(
    product_type_id integer,
    product_type character varying(50),
    product_category character varying(50),
    PRIMARY KEY (product_type_id)
);
