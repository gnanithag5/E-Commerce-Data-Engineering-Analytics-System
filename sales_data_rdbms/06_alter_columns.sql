-- Changing product_description column to TEXT for better storage efficiency
ALTER TABLE public.product
  ALTER COLUMN description TYPE TEXT;

-- Adding is_active column as BOOLEAN to mark customer status
ALTER TABLE public.customer
  ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Changing product_price column to DECIMAL for accurate monetary values
ALTER TABLE public.product
  ALTER COLUMN product_price TYPE DECIMAL(10, 2);
