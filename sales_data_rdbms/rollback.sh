#!/bin/bash

# Database connection details
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="your_database"
DB_USER="your_user"
DB_PASSWORD="your_password"

# Export password for psql
export PGPASSWORD=$DB_PASSWORD

# Get the last applied migration
LAST_MIGRATION=$(psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT migration_name FROM migrations ORDER BY applied_at DESC LIMIT 1;")

# Rollback the last migration
if [ -n "$LAST_MIGRATION" ]; then
  echo "Rolling back migration: $LAST_MIGRATION"
  
  # Example: Manually revert the last migration (if possible)
  psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "DELETE FROM migrations WHERE migration_name = '$LAST_MIGRATION';"
  
else
  echo "No migrations found to rollback."
fi
