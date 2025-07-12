-- Enabling referential integrity on sales_transaction.staff_id
ALTER TABLE public.sales_transaction
  VALIDATE CONSTRAINT fk_staff_id;

-- Enabling referential integrity on sales_transaction.sales_outlet_id
ALTER TABLE public.sales_transaction
  VALIDATE CONSTRAINT fk_sales_outlet_id;

-- Enabling referential integrity on sales_transaction.customer_id
ALTER TABLE public.sales_transaction
  VALIDATE CONSTRAINT fk_customer_id;

-- Enabling referential integrity on sales_detail.transaction_id
ALTER TABLE public.sales_detail
  VALIDATE CONSTRAINT fk_transaction_id;

-- Enabling referential integrity on sales_detail.product_id
ALTER TABLE public.sales_detail
  VALIDATE CONSTRAINT fk_product_id;

-- Enabling referential integrity on product.product_type_id
ALTER TABLE public.product
  VALIDATE CONSTRAINT fk_product_type_id;
