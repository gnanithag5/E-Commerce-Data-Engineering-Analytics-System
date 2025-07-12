-- Adding foreign key constraints

ALTER TABLE public.sales_transaction
    ADD FOREIGN KEY (staff_id)
    REFERENCES public.staff (staff_id)
    NOT VALID;

ALTER TABLE public.sales_transaction
    ADD FOREIGN KEY (sales_outlet_id)
    REFERENCES public.sales_outlet (sales_outlet_id)
    NOT VALID;

ALTER TABLE public.sales_transaction
    ADD FOREIGN KEY (customer_id)
    REFERENCES public.customer (customer_id)
    NOT VALID;

ALTER TABLE public.sales_detail
    ADD FOREIGN KEY (transaction_id)
    REFERENCES public.sales_transaction (transaction_id)
    NOT VALID;

ALTER TABLE public.sales_detail
    ADD FOREIGN KEY (product_id)
    REFERENCES public.product (product_id)
    NOT VALID;

ALTER TABLE public.product
    ADD FOREIGN KEY (product_type_id)
    REFERENCES public.product_type (product_type_id)
    NOT VALID;



