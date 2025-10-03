# Age & Gender Prediction API

A production-ready, Dockerized FastAPI application for predicting age groups and gender from images using a quantized ONNX ResNet50 model.

## 🚀 Quick Start

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or use the quick start script
./quick-start.sh

# Or use Make
make build
make run
```

Visit http://localhost:8000/docs for interactive API documentation.

## ✨ Features

- 🐳 **Fully Dockerized** - Deploy anywhere with Docker
- ⚡ **Fast Inference** - Optimized ONNX Runtime for CPU
- 🔌 **REST API** - Clean endpoints with OpenAPI docs
- 📤 **Multiple Input Methods** - File upload, URL, or base64
- 🏥 **Health Checks** - Built-in monitoring
- 🔧 **Configurable** - Environment-based configuration

## 📦 What's Included

- **FastAPI Application** (`app.py`) - RESTful API server
- **Predictor Module** (`predictor.py`) - Model inference logic
- **Docker Setup** - Dockerfile and docker-compose.yml
- **Testing** (`test_api.py`) - Comprehensive API tests
- **Documentation** - Complete deployment guides

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Predict from file upload |
| `/predict/url` | POST | Predict from image URL |
| `/predict/base64` | POST | Predict from base64 image |
| `/docs` | GET | Interactive API docs (Swagger) |

## 💡 Usage Examples

### cURL

```bash
# Upload a file
curl -X POST "http://localhost:8000/predict" \
  -F "file=@image.jpg"

# Use an image URL
curl -X POST "http://localhost:8000/predict/url" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/image.jpg"}'
```

### Python

```python
import requests

# Upload file
with open('image.jpg', 'rb') as f:
    response = requests.post('http://localhost:8000/predict', files={'file': f})
    print(response.json())

# From URL
response = requests.post(
    'http://localhost:8000/predict/url',
    json={'url': 'https://example.com/image.jpg'}
)
print(response.json())
```

### Response Format

```json
{
  "age": {
    "prediction": "25-34",
    "confidence": 0.85,
    "all_probabilities": {
      "18-24": 0.05,
      "25-34": 0.85,
      "35-44": 0.08,
      "45-54": 0.01,
      "55+": 0.01
    }
  },
  "gender": {
    "prediction": "Man",
    "confidence": 0.92,
    "all_probabilities": {
      "Woman": 0.08,
      "Man": 0.92
    }
  }
}
```

## ⚙️ Configuration

Set environment variables in `docker-compose.yml` or via `-e` flags:

```yaml
environment:
  - HOST=0.0.0.0
  - PORT=8000
  - MODEL_PATH=model_quantized.onnx
  - AGE_CLASSES=18-24,25-34,35-44,45-54,55+
```

## 🧪 Testing

```bash
# Run the test suite
python test_api.py

# Or with Make
make test
```

## 📖 Documentation

- **[Complete Docker Documentation](README_DOCKER.md)** - Detailed deployment guide
- **[Migration Guide](MIGRATION_GUIDE.md)** - Converting from HuggingFace
- **[Makefile Commands](Makefile)** - Convenient shortcuts

## 🛠️ Development

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Docker Commands

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## ☁️ Cloud Deployment

Deploy to any cloud platform:

- **AWS ECS/Fargate** - Push to ECR and create ECS service
- **Google Cloud Run** - `gcloud run deploy`
- **Azure Container Instances** - `az container create`
- **Kubernetes** - `kubectl create deployment`

See [README_DOCKER.md](README_DOCKER.md) for detailed cloud deployment instructions.

## 📊 Performance

- **Model Size**: ~25MB (quantized ONNX)
- **Inference Time**: ~50-200ms per image (CPU)
- **Memory Usage**: ~500MB
- **Throughput**: ~5-20 requests/second (single container)

## 📁 Project Structure

```
.
├── app.py                 # FastAPI application
├── predictor.py          # Model predictor class
├── model_quantized.onnx  # ONNX model file (required)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose config
├── .dockerignore         # Docker ignore patterns
├── Makefile             # Convenient commands
├── test_api.py          # API tests
├── quick-start.sh       # Quick setup script
└── README.md            # This file
```

## 🔒 Security Notes

- CORS is enabled for all origins by default (development mode)
- For production, configure CORS properly in `app.py`
- Consider adding authentication/API keys for production
- Use HTTPS in production (add reverse proxy)

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

**Made with ❤️ using FastAPI and ONNX Runtime**
