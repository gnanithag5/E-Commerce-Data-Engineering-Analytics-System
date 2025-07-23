-- Index on sales_transaction.staff_id
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = 'idx_sales_transaction_staff_id' AND n.nspname = 'public'
  ) THEN
    CREATE INDEX idx_sales_transaction_staff_id ON public.sales_transaction (staff_id);
  END IF;
END;
$$;

-- Index on sales_transaction.sales_outlet_id
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = 'idx_sales_transaction_sales_outlet_id' AND n.nspname = 'public'
  ) THEN
    CREATE INDEX idx_sales_transaction_sales_outlet_id ON public.sales_transaction (sales_outlet_id);
  END IF;
END;
$$;

-- Index on sales_transaction.customer_id
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = 'idx_sales_transaction_customer_id' AND n.nspname = 'public'
  ) THEN
    CREATE INDEX idx_sales_transaction_customer_id ON public.sales_transaction (customer_id);
  END IF;
END;
$$;

-- Index on sales_detail.transaction_id
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = 'idx_sales_detail_transaction_id' AND n.nspname = 'public'
  ) THEN
    CREATE INDEX idx_sales_detail_transaction_id ON public.sales_detail (transaction_id);
  END IF;
END;
$$;

-- Index on sales_detail.product_id
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = 'idx_sales_detail_product_id' AND n.nspname = 'public'
  ) THEN
    CREATE INDEX idx_sales_detail_product_id ON public.sales_detail (product_id);
  END IF;
END;
$$;

-- Index on product.product_type_id
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = 'idx_product_product_type_id' AND n.nspname = 'public'
  ) THEN
    CREATE INDEX idx_product_product_type_id ON public.product (product_type_id);
  END IF;
END;
$$;
