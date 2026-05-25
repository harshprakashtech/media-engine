# Base image
FROM python:3.12-slim

# Environment
ENV PYTHONUNBUFFERED=1

# Work directory
WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create temp directories
RUN mkdir -p temp/youtube

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "300", "config.wsgi:application"]