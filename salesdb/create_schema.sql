-- The DROP statements have been added to ensure that no errors occur if the script is mistakenly run more than once
-- Drop child tables first
DROP TABLE IF EXISTS public.sales_detail CASCADE;
DROP TABLE IF EXISTS public.sales_transaction_2025 CASCADE;
DROP TABLE IF EXISTS public.sales_transaction_2024 CASCADE;
DROP TABLE IF EXISTS public.sales_transaction_2023 CASCADE;
DROP TABLE IF EXISTS public.sales_transaction CASCADE;

-- Then intermediate
DROP TABLE IF EXISTS public.product CASCADE;
DROP TABLE IF EXISTS public.customer CASCADE;
DROP TABLE IF EXISTS public.staff CASCADE;
DROP TABLE IF EXISTS public.sales_outlet CASCADE;

-- Finally lookup
DROP TABLE IF EXISTS public.product_type CASCADE;

--

CREATE TABLE public.sales_transaction
(
    transaction_id integer,
    transaction_date date,
    transaction_time time without time zone,
    sales_outlet_id integer,
    staff_id integer,
    customer_id integer,
    PRIMARY KEY (transaction_id)
);


CREATE TABLE public.staff
(
    staff_id integer,
    first_name character varying(50),
    last_name character varying(50),
    position character varying(50),
    start_date date,
    location character varying(5),
    PRIMARY KEY (staff_id)
);

CREATE TABLE public.sales_outlet
(
    sales_outlet_id integer,
    sales_outlet_type character varying(20),
    address character varying(100),
    city character varying(40),
    telephone character varying(30),
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



-- Adding foreign key constraints

ALTER TABLE public.sales_transaction
    ADD CONSTRAINT fk_staff_id
    FOREIGN KEY (staff_id)
    REFERENCES public.staff (staff_id)
    ;

ALTER TABLE public.sales_transaction
    ADD CONSTRAINT fk_sales_outlet_id
    FOREIGN KEY (sales_outlet_id)
    REFERENCES public.sales_outlet (sales_outlet_id)
    ;

ALTER TABLE public.sales_transaction
    ADD CONSTRAINT fk_customer_id
    FOREIGN KEY (customer_id)
    REFERENCES public.customer (customer_id)
    ;

ALTER TABLE public.sales_detail
    ADD CONSTRAINT fk_transaction_id
    FOREIGN KEY (transaction_id)
    REFERENCES public.sales_transaction (transaction_id)
;

ALTER TABLE public.sales_detail
    ADD CONSTRAINT fk_product_id
    FOREIGN KEY (product_id)
    REFERENCES public.product (product_id)
    ;

ALTER TABLE public.product
    ADD CONSTRAINT fk_product_type_id
    FOREIGN KEY (product_type_id)
    REFERENCES public.product_type (product_type_id)
    ;



-- Ensure valid email format (basic regex check for email format)
ALTER TABLE public.customer DROP CONSTRAINT IF EXISTS check_email_format;
ALTER TABLE public.customer
ADD CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
);


-- Ensure quantity is non-negative
ALTER TABLE public.sales_detail DROP CONSTRAINT IF EXISTS check_positive_quantity;
ALTER TABLE public.sales_detail
ADD CONSTRAINT check_positive_quantity CHECK (quantity >= 0);


-- Ensure price is non-negative
ALTER TABLE public.sales_detail DROP CONSTRAINT IF EXISTS check_positive_price;
ALTER TABLE public.sales_detail
ADD CONSTRAINT check_positive_price CHECK (price >= 0);

-- Ensure the sales_detail has unique transactio_id and product_id
--ALTER TABLE public.sales_detail
--ADD CONSTRAINT unique_transaction_product UNIQUE (transaction_id, product_id);

-- Changing product_description column to TEXT for better storage efficiency
ALTER TABLE public.product
  ALTER COLUMN description TYPE TEXT;

-- Adding is_active column as BOOLEAN to mark customer status
ALTER TABLE public.customer
  ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Changing product_price column to DECIMAL for accurate monetary values
ALTER TABLE public.product
  ALTER COLUMN product_price TYPE DECIMAL(10, 2);