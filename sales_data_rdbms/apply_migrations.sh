#!/bin/bash

# Database connection details (You can adjust based on environment)
DB_HOST="localhost"
DB_PORT="port_number"
DB_NAME="your_database"
DB_USER="your_user"
DB_PASSWORD="your_password"

# Export password for psql
export PGPASSWORD=$DB_PASSWORD

# Get the latest applied migration from the migrations table (this table tracks migrations)
LATEST_MIGRATION=$(psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT migration_name FROM migrations ORDER BY applied_at DESC LIMIT 1;")

# Loop over migration files and apply them
for migration in migrations/*.sql; do
  MIGRATION_NAME=$(basename "$migration")
  
  if [ "$MIGRATION_NAME" != "$LATEST_MIGRATION" ]; then
    echo "Applying migration: $MIGRATION_NAME"
    
    # Apply the migration
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f "$migration"
    
    # Log the migration in the migrations table
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "INSERT INTO migrations (migration_name, applied_at) VALUES ('$MIGRATION_NAME', NOW());"
  fi
done
