"""Auctions — skeleton router.

P1 — timed auctions, anti-sniping, shill detection. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["auctions"])


@router.get("/auctions/status")
def module_status() -> dict:
    return {"module": "auctions", "status": "skeleton", "stage": "P1 — timed auctions, anti-sniping, shill detection"}
