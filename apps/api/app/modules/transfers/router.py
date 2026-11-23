"""Domain transfers — skeleton router.

P0 stage 7 — registrar push / inter-registrar workflow. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["transfers"])


@router.get("/transfers/status")
def module_status() -> dict:
    return {"module": "transfers", "status": "skeleton", "stage": "P0 stage 7 — registrar push / inter-registrar workflow"}
