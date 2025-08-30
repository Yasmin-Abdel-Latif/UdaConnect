# Use an official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy controller script
COPY controller.py .

# Copy gRPC generated modules and supporting code
COPY modules/ ./modules/

# Set PYTHONPATH to include current directory and modules
ENV PYTHONPATH="/app:/app/modules"

# Run controller
CMD ["python", "controller.py"]
