DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_fact_sales_date' AND n.nspname = 'public'
    ) THEN
        CREATE INDEX idx_fact_sales_date ON fact_sales(transaction_date);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_fact_sales_product' AND n.nspname = 'public'
    ) THEN
        CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_fact_sales_customer' AND n.nspname = 'public'
    ) THEN
        CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_fact_sales_staff' AND n.nspname = 'public'
    ) THEN
        CREATE INDEX idx_fact_sales_staff ON fact_sales(staff_id);
    END IF;
END
$$;
