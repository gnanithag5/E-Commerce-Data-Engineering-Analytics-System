import os
import logging
import pandas as pd
from datetime import datetime
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

BASE_DIR = os.path.dirname(__file__)
STAGING = os.path.join(BASE_DIR, 'staging')
TRANSFORMED = os.path.join(BASE_DIR, 'transformed')
os.makedirs(TRANSFORMED, exist_ok=True)

def load_csv(filename):
    try:
        path = os.path.join(STAGING, filename)
        return pd.read_csv(path)
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return pd.DataFrame()

def run_transformations():
   
    logging.info("Clear out existing transformed files")
    if os.path.exists(TRANSFORMED):
        for file in os.listdir(TRANSFORMED):
            file_path = os.path.join(TRANSFORMED, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            
    logging.info("Running transformations...")

    # Load raw CSVs
    customer_df = load_csv('customer.csv')
    product_df = load_csv('product.csv')
    product_type_df = load_csv('product_type.csv')
    sales_outlet_df = load_csv('sales_outlet.csv')
    staff_df = load_csv('staff.csv')
    sales_tx_df = load_csv('sales_transaction.csv')
    sales_detail_df = load_csv('sales_detail.csv')
    product_catalog_df = load_csv('product_catalog.csv')

    try:
        # DIM: Customer
        dim_customer = customer_df[['customer_id', 'customer_name', 'email', 'gender', 'reg_date']]
        dim_customer.to_csv(os.path.join(TRANSFORMED, 'dim_customer.csv'), index=False)

        # DIM: Product
        dim_product = pd.merge(product_df, product_type_df, on='product_type_id', how='left')
        dim_product['product_id'] = dim_product['product_id'].astype(str)
        catalog = product_catalog_df[['product_id', 'category', 'brand', 'spec_processor', 'spec_ram', 'spec_storage', 'spec_screen_size']].drop_duplicates()
        catalog['product_id'] = catalog['product_id'].astype(str)
        dim_product = pd.merge(dim_product, catalog, how='left', on='product_id')
        dim_product.to_csv(os.path.join(TRANSFORMED, 'dim_product.csv'), index=False)


        # DIM: Staff
        dim_staff = staff_df[['staff_id', 'first_name', 'last_name', 'position', 'location']]
        dim_staff.to_csv(os.path.join(TRANSFORMED, 'dim_staff.csv'), index=False)

        # DIM: Outlet
        dim_outlet = sales_outlet_df[['sales_outlet_id', 'sales_outlet_type', 'city']]
        dim_outlet.to_csv(os.path.join(TRANSFORMED, 'dim_outlet.csv'), index=False)

        # DIM: Date
        sales_tx_df['transaction_date'] = pd.to_datetime(sales_tx_df['transaction_date'], errors='coerce')
        dim_date = sales_tx_df[['transaction_date']].drop_duplicates()
        dim_date['year'] = dim_date['transaction_date'].dt.year
        dim_date['month'] = dim_date['transaction_date'].dt.month
        dim_date['day'] = dim_date['transaction_date'].dt.day
        dim_date.to_csv(os.path.join(TRANSFORMED, 'dim_date.csv'), index=False)

                # FACT: Sales

        # Step 1: Drop ID if exists
        if 'sales_detail_id' in sales_detail_df.columns:
            sales_detail_df.drop(columns=['sales_detail_id'], inplace=True)

        # Step 2: Ensure product_id is a string
        sales_detail_df['product_id'] = sales_detail_df['product_id'].astype(str)
        sales_tx_df['transaction_id'] = sales_tx_df['transaction_id'].astype(int)

        # Step 3: Compute unit_price if needed (optional: depends on your data)
        # sales_detail_df['unit_price'] = sales_detail_df['price'] / sales_detail_df['quantity']

        # Step 4: Group and recompute
        sales_detail_agg = sales_detail_df.groupby(['transaction_id', 'product_id'], as_index=False).agg({
            'quantity': 'sum',
            'price': 'sum'  # this gives total price for summed quantity
        })

        # Step 5: Merge with transaction table
        fact_sales = pd.merge(sales_detail_agg, sales_tx_df, on='transaction_id', how='left')

        # Step 6: Reorder and compute total
        fact_sales = fact_sales[[
            'transaction_id', 'transaction_date', 'product_id',
            'customer_id', 'staff_id', 'sales_outlet_id',
            'quantity', 'price'
        ]]

        fact_sales['total_amount'] = fact_sales['price']  # already total
        fact_sales.to_csv(os.path.join(TRANSFORMED, 'fact_sales.csv'), index=False)

        logging.info("Transformations complete.")

    except Exception as e:
        logging.exception("Transformation failed.")

if __name__ == "__main__":
    run_transformations()
