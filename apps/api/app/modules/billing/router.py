"""Billing & commissions — skeleton router.

P0 stage 8 — commission engine; Stripe gated on provider approval. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["billing"])


@router.get("/billing/status")
def module_status() -> dict:
    return {"module": "billing", "status": "skeleton", "stage": "P0 stage 8 — commission engine; Stripe gated on provider approval"}
