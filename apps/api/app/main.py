"""DomainFolio marketplace API — modular monolith (FastAPI).

Module boundaries (each module owns its models, schemas, services and
routers; cross-module calls go through the module's service layer, never
through another module's tables directly):

  auth         users, orgs, sessions, MFA (TOTP), passkeys, RBAC
  listings     domains, listings, portfolio, bulk import, landing pages
  verification DNS TXT ownership challenges, re-verification
  search       Meilisearch indexing / querying (read model)
  offers       offer / counteroffer engine, concurrency-safe accept
  escrow       provider adapters (Escrow.com sandbox stub), webhooks
  transfers    registrar push / inter-registrar transfer workflow
  auctions     timed auctions, bids, anti-sniping
  billing      commission engine, Stripe (gated — provider approval required)
  admin        moderation, audit log, disputes, fraud alerts
  ai           valuations (estimates only), categorisation, NL search

No business logic lives in routers. No module imports another module's
SQLAlchemy models.
"""

from fastapi import FastAPI

from app.api.deps import get_db  # noqa: F401  (re-exported for routers)
from app.core.config import settings
from app.modules.admin.router import router as admin_router
from app.modules.ai.router import router as ai_router
from app.modules.auctions.router import router as auctions_router
from app.modules.auth.router import router as auth_router
from app.modules.billing.router import router as billing_router
from app.modules.escrow.router import router as escrow_router
from app.modules.listings.router import router as listings_router
from app.modules.offers.router import router as offers_router
from app.modules.search.router import router as search_router
from app.modules.transfers.router import router as transfers_router
from app.modules.verification.router import router as verification_router

app = FastAPI(
    title="DomainFolio Marketplace API",
    description=(
        "Multi-vendor domain marketplace. P0 skeleton: module boundaries, "
        "health endpoints, and router registration. Business logic lands "
        "per P0 stage in docs/DOMAINFOLIO_MASTER_PLAN.md."
    ),
    version="0.1.0",
    docs_url="/api/docs" if settings.env != "production" else None,
    redoc_url=None,
)

for _router in (
    auth_router,
    listings_router,
    verification_router,
    search_router,
    offers_router,
    escrow_router,
    transfers_router,
    auctions_router,
    billing_router,
    admin_router,
    ai_router,
):
    app.include_router(_router, prefix="/api/v1")


@app.get("/api/health", tags=["ops"])
def health() -> dict:
    """Liveness probe. Checks nothing external by design."""
    return {"ok": True, "service": "domainfolio-api", "env": settings.env}


@app.get("/api/ready", tags=["ops"])
def ready() -> dict:
    """Readiness probe. P0 stage: database check is added when the first
    persistence-backed module lands; until then it reports the same
    liveness signal so deploy healthchecks have a stable contract."""
    return {"ok": True, "service": "domainfolio-api", "env": settings.env}
