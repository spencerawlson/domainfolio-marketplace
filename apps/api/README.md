# DomainFolio Marketplace API (FastAPI)

Modular monolith backend. P0 skeleton: module boundaries, health
endpoints, escrow provider-adapter interface with a sandbox-only stub,
Alembic migration chain, Celery wiring.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env   # then fill in values; never commit .env
uvicorn app.main:app --reload --port 8000
```

API docs (non-production only): http://localhost:8000/api/docs

## Tests

```bash
pytest -q
```

No database, Redis, or Meilisearch is needed for the skeleton suite.

## Migrations

```bash
alembic upgrade head
alembic revision -m "stage N: <what>"   # one revision per P0 stage
```

Schema changes go through Alembic only — never `CREATE TABLE IF NOT
EXISTS` in app code.

## Layout

```
app/
  core/        config, security (passwords, JWT)
  db/          engine/session, declarative base
  api/         shared FastAPI deps (auth context, DB session)
  modules/     one package per bounded context; each owns its
               models, schemas, services, routers
    auth/ listings/ verification/ search/ offers/
    escrow/ (providers/ adapters) transfers/ auctions/
    billing/ admin/ ai/
  workers/     Celery app + task modules
alembic/       migration chain (0001_initial = skeleton tables)
tests/         pytest suite
```
