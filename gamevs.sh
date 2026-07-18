#!/bin/bash

###############################################################################
#   ██████╗  █████╗ ███╗   ███╗███████╗                                      #
#   ██╔══██╗██╔══██╗████╗ ████║██╔════╝                                      #
#   ██║  ██║███████║██╔████╔██║█████╗                                        #
#   ██║  ██║██╔══██║██║╚██╔╝██║██╔══╝                                        #
#   ██████╔╝██║  ██║██║ ╚═╝ ██║███████╗                                      #
#   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   "Game" Project Bootstrap           #
###############################################################################

# Colors for clarity
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# ASCII Logo
echo -e "${CYAN}"
cat << "EOF"
   ██████╗  █████╗ ███╗   ███╗███████╗ 
   ██╔══██╗██╔══██╗████╗ ████║██╔════╝ 
   ██║  ██║███████║██╔████╔██║█████╗   
   ██║  ██║██╔══██║██║╚██╔╝██║██╔══╝   
   ██████╔╝██║  ██║██║ ╚═╝ ██║███████╗ 
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝ 
        "Game" Project Bootstrap
EOF
echo -e "${NC}"

echo -e "${YELLOW}Welcome to the Game Project FastAPI Bootstrapper!${NC}"

################################################################################
# Helper function: Check and install system commands
################################################################################
check_install() {
  local CMD="$1"
  local PKG="$2"
  if ! command -v "$CMD" >/dev/null 2>&1; then
    echo -e "${YELLOW}$CMD not found. Installing...${NC}"
    # Try apt, yum, dnf, zypper, pacman
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get update && sudo apt-get install -y "$PKG"
    elif command -v yum >/dev/null 2>&1; then
      sudo yum install -y "$PKG"
    elif command -v dnf >/dev/null 2>&1; then
      sudo dnf install -y "$PKG"
    elif command -v zypper >/dev/null 2>&1; then
      sudo zypper install -y "$PKG"
    elif command -v pacman >/dev/null 2>&1; then
      sudo pacman -Sy --noconfirm "$PKG"
    else
      echo -e "${RED}No known package manager found! Install $PKG manually.${NC}"
      exit 1
    fi
  else
    echo -e "${GREEN}$CMD found.${NC}"
  fi
}

################################################################################
# OS Check
################################################################################
echo -e "${CYAN}Checking OS...${NC}"
if [[ "$(uname -s)" != "Linux" ]]; then
  echo -e "${RED}This script is for Linux systems only.${NC}"
  exit 1
fi

################################################################################
# Ensure core commands exist
################################################################################
check_install python3 python3
check_install pip pip
check_install tree tree

################################################################################
# Project setup questions
################################################################################
read -rp "$(echo -e ${CYAN}"Enter your FastAPI project name [default: skwod-api]: "${NC})" APPNAME
APPNAME="${APPNAME:-skwod-api}"

# Container engine selection
echo -e "${CYAN}Choose your container engine:${NC}"
echo "1) Podman (recommended)"
echo "2) Docker"
read -rp "$(echo -e ${YELLOW}"Choose option [1-2]: "${NC})" CONTAINER_CHOICE

# Container Compose logic & install
if [[ "$CONTAINER_CHOICE" == "2" ]]; then
  CONTAINER="docker"
  COMPOSE_CMD="docker-compose"
  check_install docker docker.io
  check_install docker-compose docker-compose
else
  CONTAINER="podman"
  COMPOSE_CMD="podman-compose"
  check_install podman podman
  # Install podman-compose with pip, not system package
  if ! command -v podman-compose >/dev/null 2>&1; then
    echo -e "${YELLOW}podman-compose not found. Installing with pip...${NC}"
    pip3 install --user podman-compose
    export PATH="$HOME/.local/bin:$PATH"
  else
    echo -e "${GREEN}podman-compose found.${NC}"
  fi
  # Post-install PATH fix
  if ! command -v podman-compose >/dev/null 2>&1; then
    echo -e "${RED}podman-compose still not found in PATH after install.${NC}"
    echo -e "${YELLOW}Try adding ~/.local/bin to your PATH:${NC} export PATH=\"\$HOME/.local/bin:\$PATH\""
    exit 1
  fi
fi

# Database selection
echo -e "${CYAN}Choose your database:${NC}"
echo "1) PostgreSQL (recommended)"
echo "2) MySQL"
echo "3) SQLite (dev only, not for prod!)"
read -rp "$(echo -e ${YELLOW}"Choose option [1-3]: "${NC})" DBCHOICE
case "$DBCHOICE" in
  1)
    DB="postgres"
    DB_IMAGE_DOCKER="postgres:16"
    DB_IMAGE_PODMAN="docker.io/library/postgres:16"
    DB_PORT=5432
    DB_DRIVER="asyncpg"
    ;;
  2)
    DB="mysql"
    DB_IMAGE_DOCKER="mysql:8"
    DB_IMAGE_PODMAN="docker.io/library/mysql:8"
    DB_PORT=3306
    DB_DRIVER="aiomysql"
    ;;
  3)
    DB="sqlite"
    DB_IMAGE_DOCKER=""
    DB_IMAGE_PODMAN=""
    DB_PORT=""
    DB_DRIVER="sqlite"
    echo -e "${YELLOW}SQLite is only for dev! For production, use PostgreSQL or MySQL.${NC}"
    ;;
  *)
    echo -e "${RED}Invalid database choice. Exiting.${NC}"
    exit 1
    ;;
esac

################################################################################
# Password generator for secrets
################################################################################
gen_password() {
  head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 24
}

################################################################################
# Project environments and .env setup
################################################################################
ENVIRONMENTS=("dev" "stage" "prod")
mkdir -p "$APPNAME"
for ENV in "${ENVIRONMENTS[@]}"; do
  DBUSER="${APPNAME}_${ENV}_user"
  DBPASS="$(gen_password)"
  SECRET_KEY="$(gen_password)"
  ENVFILE="$APPNAME/.env.$ENV"
  if [[ "$DB" != "sqlite" ]]; then
    cat <<EOF > "$ENVFILE"
DB_HOST=localhost
DB_PORT=${DB_PORT}
DB_NAME=${APPNAME}_$ENV
DB_USER=$DBUSER
DB_PASS=$DBPASS
SECRET_KEY=$SECRET_KEY
ENV=$ENV
EOF
  else
    cat <<EOF > "$ENVFILE"
DB_PATH=${APPNAME}_$ENV.db
SECRET_KEY=$SECRET_KEY
ENV=$ENV
EOF
  fi
done

################################################################################
# requirements.txt creation
################################################################################
cat <<EOF > "$APPNAME/requirements.txt"
fastapi>=0.110
uvicorn[standard]
pydantic>=2.7
pydantic_settings
python-dotenv
alembic
${DB_DRIVER}
ruff
black
pytest
pytest-asyncio
httpx
EOF

################################################################################
# Generate robust Makefile with Alembic automation
################################################################################
cat <<EOF > "$APPNAME/Makefile"
.PHONY: help venv install run test lint migrate makemigrations makemigrate up down logs db-init clean

help:
	@echo "Game Makefile targets:"
	@echo "  venv           - Create a Python venv"
	@echo "  install        - Install dependencies"
	@echo "  run            - Start FastAPI dev server"
	@echo "  up             - Start DB containers (${CONTAINER^})"
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
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && uvicorn app.api.main:app --reload

up:
	${COMPOSE_CMD} -f ${CONTAINER}-compose.yml up -d

down:
	${COMPOSE_CMD} -f ${CONTAINER}-compose.yml down

logs:
	${CONTAINER} logs \`${CONTAINER} ps -q --filter name=db | head -n 1\`

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
EOF

################################################################################
# Compose files for Podman and Docker with full image paths for Podman
################################################################################
if [[ "$CONTAINER" == "podman" ]]; then
  compose_file="$APPNAME/podman-compose.yml"
  DB_IMAGE="$DB_IMAGE_PODMAN"
else
  compose_file="$APPNAME/docker-compose.yml"
  DB_IMAGE="$DB_IMAGE_DOCKER"
fi

if [[ "$DB" == "sqlite" ]]; then
  # No compose file needed
  DB_IMAGE=""
else
  cat <<EOF > "$compose_file"
version: "3.9"
services:
  db:
    image: ${DB_IMAGE}
    restart: always
    environment:
EOF

  if [[ "$DB" == "postgres" ]]; then
    cat <<EOF >> "$compose_file"
      POSTGRES_DB: ${APPNAME}_dev
      POSTGRES_USER: ${APPNAME}_dev_user
      POSTGRES_PASSWORD: $(gen_password)
    ports:
      - "${DB_PORT}:${DB_PORT}"
    volumes:
      - db_data:/var/lib/postgresql/data
EOF
  elif [[ "$DB" == "mysql" ]]; then
    cat <<EOF >> "$compose_file"
      MYSQL_DATABASE: ${APPNAME}_dev
      MYSQL_USER: ${APPNAME}_dev_user
      MYSQL_PASSWORD: $(gen_password)
      MYSQL_ROOT_PASSWORD: $(gen_password)
    ports:
      - "${DB_PORT}:${DB_PORT}"
    volumes:
      - db_data:/var/lib/mysql
EOF
  fi

  cat <<EOF >> "$compose_file"
volumes:
  db_data:
EOF
fi

################################################################################
# Project structure scaffolding (documented)
################################################################################
mkdir -p "$APPNAME/app/api" "$APPNAME/app/core" "$APPNAME/app/models" "$APPNAME/app/schemas" "$APPNAME/app/services" "$APPNAME/app/db" "$APPNAME/app/tasks" "$APPNAME/tests"
touch "$APPNAME/app/api/__init__.py" "$APPNAME/app/core/__init__.py" "$APPNAME/app/models/__init__.py" "$APPNAME/app/schemas/__init__.py" "$APPNAME/app/services/__init__.py" "$APPNAME/app/db/__init__.py" "$APPNAME/app/tasks/__init__.py" "$APPNAME/tests/__init__.py"

cat <<EOF > "$APPNAME/app/core/settings.py"
"""
App settings using Pydantic V2 and pydantic_settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    DB_HOST: str = None
    DB_PORT: int = None
    DB_NAME: str = None
    DB_USER: str = None
    DB_PASS: str = None
    DB_PATH: str = None
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=f".env.{ENV}")

settings = Settings()
EOF

cat <<EOF > "$APPNAME/app/api/main.py"
"""
Entrypoint for the FastAPI application.
"""
from fastapi import FastAPI
from app.core.settings import settings

app = FastAPI(title="${APPNAME}")

@app.get("/")
def root():
    return {"message": "Hello from ${APPNAME}!", "env": settings.ENV}
EOF

cat <<EOF > "$APPNAME/README.md"
# ${APPNAME}

**Game Project Bootstrap**

## Setup

- Use \`make help\` for all commands!

## How to start development

\`\`\`sh
cd ${APPNAME}
make install
make up        # start DB in ${CONTAINER^}
make run       # start FastAPI app (see README for env vars)
\`\`\`

## Database Migrations

- Generate migration: \`make makemigrations\`
- Apply migrations:   \`make migrate\`
- (Dev) Generate + apply: \`make makemigrate\`

## DB credentials are in .env files for each environment (dev, stage, prod).

## Containers

- To view DB logs: \`make logs\`
- To stop DB: \`make down\`

## Testing

- Run tests: \`make test\`
- Lint: \`make lint\`

## Project Structure

\`\`\`
${APPNAME}/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
├── tests/
├── .env.dev
├── .env.stage
├── .env.prod
├── requirements.txt
├── ${CONTAINER}-compose.yml
├── README.md
├── Makefile
├── venv/ (not included in repo)
\`\`\`

## For more info, see Makefile and doc/gmail_notifications.md
EOF

################################################################################
# Optional notification doc (as before)
################################################################################
mkdir -p "$APPNAME/doc"
cat <<EOF > "$APPNAME/doc/gmail_notifications.md"
# Gmail SMTP Build/Test Notifications

To enable build/test failure notifications:

1. Go to https://myaccount.google.com/security and enable "App passwords" for your account.
2. Add the following to your secrets or .env files:
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=465
   EMAIL_USER=youremail@gmail.com
   EMAIL_PASS=your-app-password
3. See FastAPI docs for [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).
4. Add notification calls to your test/build steps as needed.

**Note:** Never commit email credentials to your repo!
EOF

################################################################################
# Show project structure (with tree)
################################################################################
cd "$APPNAME"
echo -e "${CYAN}Your project structure:${NC}"
tree -a -I '.venv|__pycache__|*.pyc'

echo -e "${GREEN}Setup complete! Use:${NC} ${YELLOW}make help${NC} ${GREEN}for all commands.${NC}"

################################################################################
# End of script
################################################################################