"""Authentication & identity — skeleton router.

P0 stage 1 — accounts, email verification, MFA, passkeys, RBAC. Endpoints land with that stage; until then the
module reports its skeleton status and nothing else.
"""

from fastapi import APIRouter

router = APIRouter(tags=["auth"])


@router.get("/auth/status")
def module_status() -> dict:
    return {"module": "auth", "status": "skeleton", "stage": "P0 stage 1 — accounts, email verification, MFA, passkeys, RBAC"}
