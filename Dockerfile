# Base Linux image
FROM python:3.12-slim

# Prevent Python buffering logs
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]