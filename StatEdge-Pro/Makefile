# StatEdge Pro - Makefile

# Variables
APP_NAME=statedge-pro
PORT=8000

# Development
.PHONY: dev
dev:
	python main.py

# Run with uvicorn
.PHONY: run
run:
	uvicorn main:app --host 0.0.0.0 --port $(PORT) --reload

# Run with uvicorn in production mode
.PHONY: run-prod
run-prod:
	uvicorn main:app --host 0.0.0.0 --port $(PORT) --workers 4

# Run tests
.PHONY: test
 test:
	python -m pytest tests/ -v

# Run tests with coverage
.PHONY: test-coverage
test-coverage:
	python -m pytest tests/ -v --cov=src --cov-report=html

# Lint code
.PHONY: lint
lint:
	ruff check src/
	ruff format --check src/

# Format code
.PHONY: format
format:
	ruff format src/

# Type check
.PHONY: type-check
type-check:
	mypy src/

# Build Docker image
.PHONY: build
build:
	docker build -t $(APP_NAME) .

# Run with Docker
.PHONY: run-docker
run-docker:
	docker run -p $(PORT):$(PORT) -e APP_ENV=development $(APP_NAME)

# Run with Docker Compose
.PHONY: up
down:
	docker-compose down

.PHONY: up
up:
	docker-compose up --build

# Run Docker Compose in detached mode
.PHONY: up-detached
up-detached:
	docker-compose up -d --build

# Stop Docker Compose
.PHONY: stop
stop:
	docker-compose stop

# Show Docker Compose logs
.PHONY: logs
logs:
	docker-compose logs -f

# Show Docker Compose logs for specific service
.PHONY: logs-service
logs-service:
	docker-compose logs -f $(SERVICE)

# Run migrations (placeholder)
.PHONY: migrate
migrate:
	@echo "Database migrations not implemented yet"

# Create virtual environment
.PHONY: venv
venv:
	python -m venv venv
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt

# Install pre-commit hooks
.PHONY: install-hooks
install-hooks:
	pip install pre-commit
	pre-commit install

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf *.log
	rm -rf *.sqlite

# Show help
.PHONY: help
help:
	@echo "StatEdge Pro Makefile"
	@echo "====================="
	@echo ""
	@echo "Available targets:"
	@echo "  dev             - Run development server"
	@echo "  run             - Run with uvicorn"
	@echo "  run-prod        - Run in production mode"
	@echo "  test            - Run tests"
	@echo "  test-coverage   - Run tests with coverage"
	@echo "  lint            - Lint code"
	@echo "  format          - Format code"
	@echo "  type-check      - Type check code"
	@echo "  build           - Build Docker image"
	@echo "  run-docker      - Run with Docker"
	@echo "  up              - Start services with Docker Compose"
	@echo "  down            - Stop services with Docker Compose"
	@echo "  up-detached     - Start services in detached mode"
	@echo "  stop            - Stop Docker Compose services"
	@echo "  logs            - Show Docker Compose logs"
	@echo "  logs-service    - Show logs for specific service"
	@echo "  venv            - Create virtual environment"
	@echo "  install-hooks   - Install pre-commit hooks"
	@echo "  clean           - Clean build artifacts"
	@echo "  help            - Show this help message"