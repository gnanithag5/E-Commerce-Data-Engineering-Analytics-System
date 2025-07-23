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

-- Step 2: Grant permissions to read_only
GRANT SELECT ON TABLE public.sales_transaction TO read_only;
GRANT SELECT ON TABLE public.sales_detail TO read_only;
GRANT SELECT ON TABLE public.product TO read_only;

-- Step 3: Grant permissions to data_entry
GRANT INSERT, UPDATE ON TABLE public.product TO data_entry;

-- Step 4: Grant full privileges to admin
GRANT USAGE ON SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin;

-- Ensure future tables/sequences/functions also obey the same rules
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_only;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE ON TABLES TO data_entry;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO admin;

-- Step 5: Restrict sensitive access
REVOKE ALL PRIVILEGES ON TABLE public.customer FROM read_only, data_entry;
REVOKE ALL PRIVILEGES ON TABLE public.staff FROM read_only, data_entry;

-- Step 6: Explicitly allow admin on sensitive tables
GRANT SELECT, INSERT, UPDATE ON public.customer TO admin;
GRANT SELECT, INSERT, UPDATE ON public.staff TO admin;
