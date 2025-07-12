#!/bin/bash

# Database connection details
DB_HOST="localhost"
DB_PORT="port_number"
DB_NAME="your_database"
DB_USER="your_user"
DB_PASSWORD="your_password"

# Export password for psql
export PGPASSWORD=$DB_PASSWORD

# Check if required tables exist
echo "Checking if necessary tables exist..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "\dt" | grep -q "public.staff" || echo "Table staff does not exist"
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "\dt" | grep -q "public.sales_transaction" || echo "Table sales_transaction does not exist"

# Check for important columns (e.g., email column in customer table)
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT column_name FROM information_schema.columns WHERE table_name = 'customer';" | grep -q "email" || echo "Column email is missing in customer table"

# Additional integrity checks (e.g., foreign key constraints)
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT constraint_name FROM information_schema.table_constraints WHERE table_name = 'sales_transaction' AND constraint_type = 'FOREIGN KEY';" || echo "Foreign key constraints missing in sales_transaction"
