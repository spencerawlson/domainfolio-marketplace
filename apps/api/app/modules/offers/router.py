"""Offers & negotiations — skeleton router.

P0 stage 5 — counteroffers, expiry, concurrency-safe accept. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["offers"])


@router.get("/offers/status")
def module_status() -> dict:
    return {"module": "offers", "status": "skeleton", "stage": "P0 stage 5 — counteroffers, expiry, concurrency-safe accept"}
