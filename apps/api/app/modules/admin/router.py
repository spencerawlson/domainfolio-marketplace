"""Administration — skeleton router.

P0 stage 9 — moderation, audit log, disputes, fraud alerts. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["admin"])


@router.get("/admin/status")
def module_status() -> dict:
    return {"module": "admin", "status": "skeleton", "stage": "P0 stage 9 — moderation, audit log, disputes, fraud alerts"}
