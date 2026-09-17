FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create output directory and uploads dir
RUN mkdir -p /app/output /app/uploads

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run as non-root (root amplifies any write primitive inside the container)
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app/uploads /app/output
USER appuser

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
