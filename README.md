# DomainFolio Marketplace — modular monolith (Option B)
#
# Status: Phase 1 skeleton. Docs + app shells + health endpoints.
# The existing lander app (spencerawlson/domainfolio) is untouched and
# stays live. Nothing here deploys, charges, or moves money.

## Layout

```
docs/                  Phase 1 design docs (master plan, architecture, schema)
apps/
  web/                 Next.js 15 + TypeScript + Tailwind frontend shell
  api/                 FastAPI backend — modular monolith
    app/
      core/            config, security (passwords, JWT)
      db/              engine/session, declarative base
      api/             shared FastAPI deps
      modules/         auth, listings, verification, search, offers,
                       escrow (providers/ adapters), transfers,
                       auctions, billing, admin, ai
      workers/         Celery app + tasks
    alembic/           migration chain (0001_initial = skeleton tables)
    tests/             pytest suite (skeleton: no infra needed)
docker-compose.yml     local dev: Postgres 16, Redis 7, Meilisearch, api,
                       worker, web (loopback ports only)
.github/workflows/    CI: backend tests, frontend typecheck/tests/build
```

## Quick start (local dev)

```bash
cp .env.example .env        # fill in JWT_SECRET / SESSION_SECRET
docker compose up --build   # needs Docker; not available in the sandbox
```

Without Docker, run the pieces separately:

```bash
# API
cd apps/api && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 8000

# Web
cd apps/web && npm install
npm run typecheck && npm test && npm run build
```

## Rules that do not change

- No listing activates without ownership verification (DNS TXT).
- A payment is never reported as secured without authoritative
  provider confirmation. No internal escrow or custody, ever.
- Stripe Connect stays disabled until the provider approves this
  business model. Escrow stays on the sandbox stub until an
  Escrow.com sandbox account exists and is approved.
- No seeded inventory, no fabricated listings, sales figures, or
  testimonials — anywhere, including demos and screenshots.
- Schema changes go through Alembic only. One revision per stage.
- No deploy, no paid accounts, no real money without Spencer's
  explicit approval per step.
```

