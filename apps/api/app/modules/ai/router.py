"""AI intelligence — skeleton router.

P2 — valuations (estimates only), categorisation, NL search. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["ai"])


@router.get("/ai/status")
def module_status() -> dict:
    return {"module": "ai", "status": "skeleton", "stage": "P2 — valuations (estimates only), categorisation, NL search"}
