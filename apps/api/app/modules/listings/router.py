"""Listings & portfolio — skeleton router.

P0 stage 3 — domains, listings, bulk CSV import. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["listings"])


@router.get("/listings/status")
def module_status() -> dict:
    return {"module": "listings", "status": "skeleton", "stage": "P0 stage 3 — domains, listings, bulk CSV import"}
