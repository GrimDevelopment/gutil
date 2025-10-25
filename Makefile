# Makefile

.PHONY: all backend frontend cli clean dev up down ps logs

all: backend cli


backend:
	@echo "Building backend..."
	cd backend && pip install -r requirements.txt

cli:
	@echo "Building CLI..."
	cd cli && pip install -r requirements.txt

clean:
	@echo "Cleaning up..."
	rm -rf backend/__pycache__ cli/__pycache__

dev: up

up:
	docker-compose up --build

down:
	docker-compose down

ps:
	docker-compose ps

logs:
	docker-compose logs -f
