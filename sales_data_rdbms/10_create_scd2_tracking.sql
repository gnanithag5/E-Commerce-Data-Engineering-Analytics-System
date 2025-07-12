-- Step 1: Alter the customer table to add historical tracking columns
ALTER TABLE public.customer
ADD COLUMN start_date DATE DEFAULT CURRENT_DATE,
ADD COLUMN end_date DATE,
ADD COLUMN current_flag BOOLEAN DEFAULT TRUE;

-- Step 2: Alter the product table to add historical tracking columns
ALTER TABLE public.product
ADD COLUMN start_date DATE DEFAULT CURRENT_DATE,
ADD COLUMN end_date DATE,
ADD COLUMN current_flag BOOLEAN DEFAULT TRUE;

-- Step 3: Create a trigger function for customer changes (SCD Type 2)
CREATE OR REPLACE FUNCTION public.customer_scd2_trigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if there's a change in customer_name, email, or card_number
    IF NEW.customer_name <> OLD.customer_name OR NEW.email <> OLD.email OR NEW.card_number <> OLD.card_number THEN
        -- Close the old record
        UPDATE public.customer
        SET end_date = CURRENT_DATE, current_flag = FALSE
        WHERE customer_id = OLD.customer_id AND current_flag = TRUE;

        -- Insert a new record to track the change (new version of the customer record)
        INSERT INTO public.customer (customer_id, customer_name, email, reg_date, card_number, date_of_birth, gender, start_date, end_date, current_flag)
        VALUES (OLD.customer_id, NEW.customer_name, NEW.email, NEW.reg_date, NEW.card_number, NEW.date_of_birth, NEW.gender, CURRENT_DATE, NULL, TRUE);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 4: Create the trigger for the customer table to track changes (SCD Type 2)
CREATE TRIGGER customer_scd2_trigger
AFTER UPDATE ON public.customer
FOR EACH ROW
WHEN (OLD.customer_name IS DISTINCT FROM NEW.customer_name OR OLD.email IS DISTINCT FROM NEW.email OR OLD.card_number IS DISTINCT FROM NEW.card_number)
EXECUTE FUNCTION public.customer_scd2_trigger();

-- Step 5: Create a trigger function for product price changes (SCD Type 2)
CREATE OR REPLACE FUNCTION public.product_price_scd2_trigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if there's a change in product price
    IF NEW.product_price <> OLD.product_price THEN
        -- Close the old record
        UPDATE public.product
        SET end_date = CURRENT_DATE, current_flag = FALSE
        WHERE product_id = OLD.product_id AND current_flag = TRUE;

        -- Insert a new record to track the change (new version of the product record)
        INSERT INTO public.product (product_id, product_name, description, product_price, product_type_id, start_date, end_date, current_flag)
        VALUES (OLD.product_id, NEW.product_name, NEW.description, NEW.product_price, NEW.product_type_id, CURRENT_DATE, NULL, TRUE);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 6: Create the trigger for the product table to track price changes (SCD Type 2)
CREATE TRIGGER product_price_scd2_trigger
AFTER UPDATE ON public.product
FOR EACH ROW
WHEN (OLD.product_price IS DISTINCT FROM NEW.product_price)
EXECUTE FUNCTION public.product_price_scd2_trigger();
