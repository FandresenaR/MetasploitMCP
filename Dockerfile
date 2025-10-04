# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies that might be needed
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port (adjust if your app uses a different port)
EXPOSE 8080

# Run the application
# Using 0.0.0.0 to bind to all interfaces (required for Fly.io)
# Remove --mock flag to connect to external Metasploit (set MSFRPCD_HOST, MSFRPCD_PORT, MSFRPCD_PASSWORD as secrets)
CMD ["python", "MetasploitMCP.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8080"]
