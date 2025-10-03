#!/bin/bash

# Quick start script for Age & Gender Prediction API
set -e

echo "================================"
echo "Age & Gender Prediction API"
echo "Quick Start Script"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker Compose is installed"

# Check if model file exists
if [ ! -f "model_quantized.onnx" ]; then
    echo "❌ Model file 'model_quantized.onnx' not found!"
    echo "   Please ensure the model file is in the current directory."
    exit 1
fi

echo "✓ Model file found"
echo ""

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✓ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo ""

# Start the service
echo "🚀 Starting the service..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✓ Service started successfully"
else
    echo "❌ Failed to start service"
    exit 1
fi

echo ""
echo "⏳ Waiting for service to be ready..."
sleep 5

# Check health
echo "🏥 Checking service health..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✓ Service is healthy and ready!"
else
    echo "⚠️  Service may not be fully ready yet. Check logs with: docker-compose logs"
fi

echo ""
echo "================================"
echo "✨ Setup Complete!"
echo "================================"
echo ""
echo "Your API is now running at:"
echo "  🌐 http://localhost:8000"
echo ""
echo "Useful links:"
echo "  📖 API Documentation: http://localhost:8000/docs"
echo "  📚 Alternative Docs:  http://localhost:8000/redoc"
echo "  🏥 Health Check:      http://localhost:8000/health"
echo ""
echo "Useful commands:"
echo "  📋 View logs:       docker-compose logs -f"
echo "  🛑 Stop service:    docker-compose down"
echo "  🔄 Restart:         docker-compose restart"
echo "  🧪 Run tests:       python test_api.py"
echo ""
echo "Test the API with:"
echo "  curl -X POST http://localhost:8000/predict -F 'file=@your_image.jpg'"
echo ""
echo "For more information, see README_DOCKER.md"
echo "================================"

