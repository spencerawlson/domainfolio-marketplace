"""Search — skeleton router.

P0 stage 4 — Meilisearch read model, filters. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["search"])


@router.get("/search/status")
def module_status() -> dict:
    return {"module": "search", "status": "skeleton", "stage": "P0 stage 4 — Meilisearch read model, filters"}
