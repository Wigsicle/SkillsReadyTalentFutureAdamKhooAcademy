#!/bin/bash
# entrypoint.sh
export PGPASSWORD="password"

echo "Waiting for database to be ready..."
# Wait for the job_database container to be ready
wait-for-it.sh job_database:5432 --timeout=30 --strict -- echo "Database is up!"

# Run Alembic migrations
cd /SRTFAKA
echo "Running Alembic migrations..."
alembic upgrade head
psql -h 172.18.0.2 -U postgres -d academy_db -a -f populate.sql
unset PGPASSWORD
cd /

# Start the application after migrations
echo "Starting Uvicorn server..."
uvicorn SRTFAKA.apiGateway.main:app --host 0.0.0.0 --port 80
