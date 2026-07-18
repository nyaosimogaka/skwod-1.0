.PHONY: help venv install run test lint migrate makemigrations makemigrate up down logs db-init clean

help:
	@echo "Game Makefile targets:"
	@echo "  venv           - Create a Python venv"
	@echo "  install        - Install dependencies"
	@echo "  run            - Start FastAPI dev server"
	@echo "  up             - Start DB containers (Podman)"
	@echo "  down           - Stop containers"
	@echo "  logs           - View DB container logs"
	@echo "  makemigrations - Generate Alembic migration (autogenerate)"
	@echo "  migrate        - Apply Alembic migrations"
	@echo "  makemigrate    - Generate and apply Alembic migration (dev)"
	@echo "  db-init        - Initialize DB if needed"
	@echo "  test           - Run tests"
	@echo "  lint           - Run ruff and black"
	@echo "  clean          - Remove .pyc and cache"

venv:
	virtualenv .venv

install: venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && uvicorn app.api.main:app --reload

up:
	podman-compose -f podman-compose.yml up -d

down:
	podman-compose -f podman-compose.yml down

logs:
	podman logs `podman ps -q --filter name=db | head -n 1`

makemigrations:
	@echo "Generating new Alembic migration (autogenerate)..."
	. .venv/bin/activate && alembic revision --autogenerate -m "Auto migration"

migrate:
	@echo "Applying all pending Alembic migrations to database..."
	. .venv/bin/activate && alembic upgrade head

makemigrate:
	@echo "Generate and apply Alembic migration (dev flow)..."
	. .venv/bin/activate && alembic revision --autogenerate -m "Auto migration"
	. .venv/bin/activate && alembic upgrade head

db-init:
	@echo "You can create DB/tables via Alembic or via your ORM."

test:
	. .venv/bin/activate && pytest

lint:
	. .venv/bin/activate && ruff app/ && black --check app/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
