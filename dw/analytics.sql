-- 1. Revenue by product category and/or month using GROUPING SETS
DROP MATERIALIZED VIEW IF EXISTS mv_sales_grouping_sets;
CREATE MATERIALIZED VIEW mv_sales_grouping_sets AS
SELECT
    p.product_category,
    d.month,
    SUM(f.total_amount) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_date d ON f.transaction_date = d.transaction_date
GROUP BY GROUPING SETS (
    (p.product_category, d.month),
    (p.product_category),
    (d.month),
    ()
);

-- 2. Revenue rolled up from product name to category to grand total
DROP MATERIALIZED VIEW IF EXISTS mv_sales_rollup_product_category;
CREATE MATERIALIZED VIEW mv_sales_rollup_product_category AS
SELECT
    p.product_category,
    p.product_name,
    SUM(f.total_amount) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY ROLLUP (p.product_category, p.product_name);

-- 3. Revenue by all combinations of product category and year using CUBE
DROP MATERIALIZED VIEW IF EXISTS mv_sales_cube_category_year;
CREATE MATERIALIZED VIEW mv_sales_cube_category_year AS
SELECT
    p.product_category,
    d.year,
    SUM(f.total_amount) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_date d ON f.transaction_date = d.transaction_date
GROUP BY CUBE (p.product_category, d.year);

-- 4. Same as above, but replace NULLs with 'ALL' using GROUPING()
DROP MATERIALIZED VIEW IF EXISTS mv_sales_cube_labeled;
CREATE MATERIALIZED VIEW mv_sales_cube_labeled AS
SELECT
    CASE WHEN GROUPING(p.product_category) = 1 THEN 'ALL' ELSE p.product_category END AS product_category,
    CASE WHEN GROUPING(d.year) = 1 THEN 'ALL' ELSE d.year::TEXT END AS year,
    SUM(f.total_amount) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_date d ON f.transaction_date = d.transaction_date
GROUP BY CUBE (p.product_category, d.year);

-- Refresh all views
REFRESH MATERIALIZED VIEW mv_sales_grouping_sets;
REFRESH MATERIALIZED VIEW mv_sales_rollup_product_category;
REFRESH MATERIALIZED VIEW mv_sales_cube_category_year;
REFRESH MATERIALIZED VIEW mv_sales_cube_labeled;
