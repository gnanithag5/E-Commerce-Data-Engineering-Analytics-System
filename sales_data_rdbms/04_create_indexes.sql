-- Indexing foreign key on sales_transaction.staff_id
CREATE INDEX idx_sales_transaction_staff_id ON public.sales_transaction (staff_id);

-- Indexing foreign key on sales_transaction.sales_outlet_id
CREATE INDEX idx_sales_transaction_sales_outlet_id ON public.sales_transaction (sales_outlet_id);

-- Indexing foreign key on sales_transaction.customer_id
CREATE INDEX idx_sales_transaction_customer_id ON public.sales_transaction (customer_id);

-- Indexing foreign key on sales_detail.transaction_id
CREATE INDEX idx_sales_detail_transaction_id ON public.sales_detail (transaction_id);

-- Indexing foreign key on sales_detail.product_id
CREATE INDEX idx_sales_detail_product_id ON public.sales_detail (product_id);

-- Indexing foreign key on product.product_type_id
CREATE INDEX idx_product_product_type_id ON public.product (product_type_id);
