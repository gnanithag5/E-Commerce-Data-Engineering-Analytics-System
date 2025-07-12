-- Step 1: Create a materialized view for total sales by outlet
CREATE MATERIALIZED VIEW public.total_sales_by_outlet AS
SELECT
    sales_outlet_id,
    SUM(price * quantity) AS total_sales,
    EXTRACT(YEAR FROM transaction_date) AS year,
    EXTRACT(QUARTER FROM transaction_date) AS quarter
FROM public.sales_detail sd
JOIN public.sales_transaction st ON st.transaction_id = sd.transaction_id
GROUP BY sales_outlet_id, year, quarter;

-- Step 2: Create a materialized view for daily sales summaries
CREATE MATERIALIZED VIEW public.daily_sales_summary AS
SELECT
    transaction_date,
    SUM(price * quantity) AS total_sales
FROM public.sales_detail sd
JOIN public.sales_transaction st ON st.transaction_id = sd.transaction_id
GROUP BY transaction_date;

-- Step 3: Refresh materialized views periodically
REFRESH MATERIALIZED VIEW public.total_sales_by_outlet;
REFRESH MATERIALIZED VIEW public.daily_sales_summary;
