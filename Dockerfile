FROM python:3.8

# Install ffmpeg and system dependencies as root
USER root
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create videos directory with proper permissions
RUN mkdir -p /app/static/videos && chown -R 1000:1000 /app/static/videos

# Switch to non-root user for security
USER 1000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
