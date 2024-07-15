#!/bin/bash

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply Alembic migrations
echo "Applying database migrations..."
alembic upgrade head

# Start uvicorn server
echo "Starting uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port 8000
