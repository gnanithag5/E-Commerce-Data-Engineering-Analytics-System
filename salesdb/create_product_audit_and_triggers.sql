-- Step 1: Create the audit table
CREATE TABLE public.product_audit (
    product_id integer,
    old_price DECIMAL(10, 2),
    new_price DECIMAL(10, 2),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by integer, -- staff_id of the person making the change
    PRIMARY KEY (product_id, change_date)
);

-- Step 2: Add triggers to track changes in the `product` table

-- Trigger function to capture price changes
CREATE OR REPLACE FUNCTION public.product_price_update_audit() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.product_price <> OLD.product_price THEN
        INSERT INTO public.product_audit (product_id, old_price, new_price, changed_by)
        VALUES (OLD.product_id, OLD.product_price, NEW.product_price, NEW.staff_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS product_price_update_trigger ON public.product;

-- Step 3: Create the trigger for the `product` table
CREATE TRIGGER product_price_update_trigger
AFTER UPDATE ON public.product
FOR EACH ROW
EXECUTE FUNCTION public.product_price_update_audit();
