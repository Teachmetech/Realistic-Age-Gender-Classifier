.PHONY: help build run stop logs clean test dev

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker image"
	@echo "  make run      - Run container with docker-compose"
	@echo "  make stop     - Stop and remove containers"
	@echo "  make logs     - Show container logs"
	@echo "  make clean    - Remove containers and images"
	@echo "  make test     - Test the API"
	@echo "  make dev      - Run locally without Docker"

build:
	docker-compose build

run:
	docker-compose up -d
	@echo "API running at http://localhost:8000"
	@echo "Docs at http://localhost:8000/docs"

stop:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker rmi age-gender-classifier-age-gender-api 2>/dev/null || true

test:
	@echo "Testing health endpoint..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "API not running"

dev:
	python app.py

