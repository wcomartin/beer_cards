# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Gunicorn will listen on
EXPOSE 8000

# Run the application using Gunicorn
# The 'app:app' refers to the 'app' instance within 'app.py'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
