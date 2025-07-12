-- Step 1: Create roles
CREATE ROLE read_only;
CREATE ROLE data_entry;
CREATE ROLE admin;

-- Step 2: Grant permissions
-- Read-only role can only SELECT data from most tables
GRANT SELECT ON public.sales_transaction, public.sales_detail, public.product TO read_only;

-- Data entry role can INSERT and UPDATE on the product table
GRANT INSERT, UPDATE ON public.product TO data_entry;

-- Admin role can do everything
GRANT ALL PRIVILEGES ON public.* TO admin;

-- Step 3: Restrict access to sensitive tables (e.g., customer data, staff salaries)
REVOKE ALL PRIVILEGES ON public.customer FROM read_only, data_entry;
REVOKE ALL PRIVILEGES ON public.staff FROM read_only, data_entry;

-- Admin can still access sensitive data
GRANT SELECT, INSERT, UPDATE ON public.customer, public.staff TO admin;
