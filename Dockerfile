# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y git

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port Flask will run on
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
