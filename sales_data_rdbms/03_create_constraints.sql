-- Ensure valid email format (basic regex check for email format)
ALTER TABLE public.customer
ADD CONSTRAINT check_email_format CHECK (email ~* '^.+@.+\..+$');


-- Ensure quantity is non-negative
ALTER TABLE public.sales_detail
ADD CONSTRAINT check_positive_quantity CHECK (quantity >= 0);


-- Ensure price is non-negative
ALTER TABLE public.sales_detail
ADD CONSTRAINT check_positive_price CHECK (price >= 0);