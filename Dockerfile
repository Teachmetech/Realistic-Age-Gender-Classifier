# Use Python 3.10 slim image for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY predictor.py .
COPY app.py .
COPY model_quantized.onnx .

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV MODEL_PATH=model_quantized.onnx
ENV AGE_CLASSES=18-24,25-34,35-44,45-54,55+

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["python", "app.py"]

