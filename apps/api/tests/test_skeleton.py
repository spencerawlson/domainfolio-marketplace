"""Skeleton test suite. These tests prove the skeleton wires up: the app
imports, every module router is registered, health endpoints answer,
and the escrow stub behaves as a sandbox-only simulation.

Run: `pytest -q` (from apps/api). No database, Redis, or Meilisearch
is needed — the skeleton must not require infrastructure to import.
"""

import os

os.environ.setdefault("JWT_SECRET", "test-secret-not-for-production")
os.environ.setdefault("SESSION_SECRET", "test-session-secret")

from fastapi.testclient import TestClient

from app.main import app
from app.modules.escrow.providers.stub import StubEscrowProvider
from app.modules.escrow.providers.base import EscrowStatus

client = TestClient(app)

MODULES = [
    "auth",
    "listings",
    "verification",
    "search",
    "offers",
    "escrow",
    "transfers",
    "auctions",
    "billing",
    "admin",
    "ai",
]


def test_health_ok():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert r.json()["service"] == "domainfolio-api"


def test_ready_ok():
    r = client.get("/api/ready")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_openapi_lists_all_module_routers():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]
    for module in MODULES:
        assert f"/api/v1/{module}/status" in paths, module


def test_every_module_reports_skeleton_status():
    for module in MODULES:
        r = client.get(f"/api/v1/{module}/status")
        assert r.status_code == 200, module
        body = r.json()
        assert body["module"] == module
        assert body["status"] == "skeleton"


def test_escrow_webhook_without_secret_is_503_not_silent_accept():
    r = client.post("/escrow/webhooks/stub", content=b"{}")
    # The router is mounted under /api/v1 by main.py; the direct path
    # is not registered. Either way it must never silently accept.
    assert r.status_code in (404, 503)


def test_escrow_webhook_requires_configured_secret():
    r = client.post("/api/v1/escrow/webhooks/stub", content=b"{}")
    assert r.status_code == 503  # no ESCROW_WEBHOOK_SECRET in test env


def test_escrow_webhook_unknown_provider_is_404():
    r = client.post("/api/v1/escrow/webhooks/unknown", content=b"{}")
    assert r.status_code == 404


def test_stub_escrow_is_sandbox_only():
    provider = StubEscrowProvider()
    tx = provider.create_transaction(
        buyer_id="buyer-1",
        seller_id="seller-1",
        domain="example.com",
        amount_cents=100000,
    )
    assert tx.status == EscrowStatus.CREATED
    assert tx.metadata["sandbox"] is True
    assert tx.provider_ref.startswith("stub-")
    assert provider.get_status(tx.provider_ref) == EscrowStatus.CREATED
    assert (
        provider.cancel_transaction(tx.provider_ref, reason="test")
        == EscrowStatus.CANCELLED
    )


def test_stub_escrow_rejects_unknown_ref():
    provider = StubEscrowProvider()
    try:
        provider.get_status("stub-does-not-exist")
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for unknown stub transaction")
