"""Escrow webhook endpoint — skeleton.

Rules enforced here (and in the real adapter later):
- A webhook is rejected (401) unless its signature verifies against
  the configured provider secret. No secret configured -> 503, not a
  silent accept.
- Processing is idempotent: the same provider event id processed twice
  must change state once. (Dedup store lands with the P0 escrow stage.)
"""

from fastapi import APIRouter, Header, HTTPException, Request

from app.modules.escrow.providers.stub import get_provider

router = APIRouter(tags=["escrow"])


@router.get("/escrow/status")
def module_status() -> dict:
    return {
        "module": "escrow",
        "status": "skeleton",
        "stage": "P0 stage 6 — provider adapters, sandbox only",
    }


@router.post("/escrow/webhooks/{provider}")
async def escrow_webhook(
    provider: str,
    request: Request,
    x_escrow_signature: str | None = Header(default=None),
) -> dict:
    from app.core.config import settings

    if provider != "stub":
        raise HTTPException(status_code=404, detail="unknown escrow provider")
    if not settings.escrow_webhook_secret:
        raise HTTPException(
            status_code=503,
            detail="escrow webhook secret not configured; refusing to accept events",
        )
    payload = await request.body()
    adapter = get_provider()
    if not x_escrow_signature or not adapter.verify_webhook_signature(
        payload, x_escrow_signature
    ):
        raise HTTPException(status_code=401, detail="invalid webhook signature")
    # Idempotent processing + state sync land with the P0 escrow stage.
    return {"ok": True, "provider": provider, "status": "signature verified (stub)"}
