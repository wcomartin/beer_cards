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

# Copy the startup script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Expose the port that Gunicorn will listen on
EXPOSE 8000

# Run the startup script
CMD ["./start.sh"]