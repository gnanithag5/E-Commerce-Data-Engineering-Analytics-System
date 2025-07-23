-- Step 1: Create roles if they don't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'read_only') THEN
    CREATE ROLE read_only;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'data_entry') THEN
    CREATE ROLE data_entry;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
    CREATE ROLE admin;
  END IF;
END$$;

-- Step 2: Grant permissions
GRANT SELECT ON public.sales_transaction, public.sales_detail, public.product TO read_only;
GRANT INSERT, UPDATE ON public.product TO data_entry;

GRANT USAGE ON SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_only;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE ON TABLES TO data_entry;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;

-- Step 3: Restrict access to sensitive tables
REVOKE ALL PRIVILEGES ON public.customer FROM read_only, data_entry;
REVOKE ALL PRIVILEGES ON public.staff FROM read_only, data_entry;

GRANT SELECT, INSERT, UPDATE ON public.customer, public.staff TO admin;
