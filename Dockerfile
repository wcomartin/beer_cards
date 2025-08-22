# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This must be *before* running flask db upgrade
COPY . .

# Run database migrations
ENV FLASK_APP=app.py
# Set FLASK_APP for the migration command
RUN flask db upgrade

# Expose the port that Gunicorn will listen on
EXPOSE 8000

# Run the application using Gunicorn
# The 'app:app' refers to the 'app' instance within 'app.py'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]