# Use a Python base image
FROM python:3.9-slim AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 (for Gunicorn)
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
