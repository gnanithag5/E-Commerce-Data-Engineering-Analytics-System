#!/bin/bash

# Check if the environment parameter is passed
if [ -z "$1" ]; then
  echo "Error: No environment specified. Please provide 'development', 'staging', or 'production'."
  exit 1
fi

# Define the target environment (development, staging, production)
TARGET_ENV="$1"  # This gets the environment as a command-line argument (e.g., development)

# Set up database connection based on the environment
case "$TARGET_ENV" in
  development)
    DB_HOST="localhost"
    DB_PORT="5432"
    DB_NAME="dev_db"
    DB_USER="dev_user"
    DB_PASSWORD="dev_password"
    echo "Setting up environment: Development"
    ;;
  staging)
    DB_HOST="staging_host"
    DB_PORT="5432"
    DB_NAME="staging_db"
    DB_USER="staging_user"
    DB_PASSWORD="staging_password"
    echo "Setting up environment: Staging"
    ;;
  production)
    DB_HOST="prod_host"
    DB_PORT="5432"
    DB_NAME="prod_db"
    DB_USER="prod_user"
    DB_PASSWORD="prod_password"
    echo "Setting up environment: Production"
    ;;
  *)
    echo "Invalid environment specified. Choose from 'development', 'staging', or 'production'."
    exit 1
    ;;
esac

# Run migrations
echo "Applying migrations to $TARGET_ENV environment..."
./scripts/apply_migrations.sh

# Run database tests
echo "Running database tests..."
./scripts/test_database.sh

# Deployment steps (optional, can be added as per your deployment process)
echo "Deployment to $TARGET_ENV completed successfully!"
