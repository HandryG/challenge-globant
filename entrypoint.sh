#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up - executing command"

# Note: We're not creating tables automatically now, 
# as the DDL will be executed directly in PostgreSQL console

# Execute DDL commands
echo "Executing DDL commands..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f /challenge-globant/sql/create_tables.sql

# Start the application
exec uvicorn challenge-project.main:challenge-project --host 0.0.0.0 --port 8000 --reload