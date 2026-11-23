"""Domain ownership verification — skeleton router.

P0 stage 2 — DNS TXT challenges, expiring tokens. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["verification"])


@router.get("/verification/status")
def module_status() -> dict:
    return {"module": "verification", "status": "skeleton", "stage": "P0 stage 2 — DNS TXT challenges, expiring tokens"}
