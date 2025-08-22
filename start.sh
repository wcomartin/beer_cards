#!/bin/sh

# Set FLASK_APP environment variable
export FLASK_APP=app.py

# Create the database if it doesn't exist (Flask-SQLAlchemy will create it on first access)
# This step is implicitly handled by flask db upgrade if the file doesn't exist,
# but explicitly touching it ensures the directory exists.
mkdir -p instance

# Run database migrations
echo "Running database migrations..."
flask db upgrade
echo "Database migrations complete."

# Run the seeding script
echo "Running database seeding..."
python seed_admin.py
echo "Database seeding complete."

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 app:app
