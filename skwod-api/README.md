# skwod-api

**Game Project Bootstrap**

## Setup

- Use `make help` for all commands!

## How to start development

```sh
cd skwod-api
make install
make up        # start DB in Podman
make run       # start FastAPI app (see README for env vars)
```

## Database Migrations

- Generate migration: `make makemigrations`
- Apply migrations:   `make migrate`
- (Dev) Generate + apply: `make makemigrate`

## DB credentials are in .env files for each environment (dev, stage, prod).

## Containers

- To view DB logs: `make logs`
- To stop DB: `make down`

## Testing

- Run tests: `make test`
- Lint: `make lint`

## Project Structure

```
skwod-api/
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
├── podman-compose.yml
├── README.md
├── Makefile
├── venv/ (not included in repo)
```

## For more info, see Makefile and doc/gmail_notifications.md
