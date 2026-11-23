"""Stub escrow provider — sandbox simulation only.

Returns deterministic, clearly-marked simulated responses. It never
touches a real provider, never moves money, and every transaction it
creates is labelled `sandbox: true` in metadata so a stub record can
never be mistaken for a real secured payment.
"""

from __future__ import annotations

import hashlib

from app.modules.escrow.providers.base import (
    EscrowProvider,
    EscrowStatus,
    EscrowTransaction,
)


class StubEscrowProvider(EscrowProvider):
    name = "stub"

    def __init__(self) -> None:
        self._store: dict[str, EscrowTransaction] = {}

    def create_transaction(
        self, *, buyer_id: str, seller_id: str, domain: str, amount_cents: int, currency: str = "USD"
    ) -> EscrowTransaction:
        ref = "stub-" + hashlib.sha256(
            f"{buyer_id}:{seller_id}:{domain}:{amount_cents}".encode()
        ).hexdigest()[:16]
        tx = EscrowTransaction(
            provider_ref=ref,
            status=EscrowStatus.CREATED,
            buyer_id=buyer_id,
            seller_id=seller_id,
            domain=domain,
            amount_cents=amount_cents,
            currency=currency,
            metadata={"sandbox": True, "provider": "stub"},
        )
        self._store[ref] = tx
        return tx

    def get_status(self, provider_ref: str) -> EscrowStatus:
        tx = self._store.get(provider_ref)
        if tx is None:
            raise KeyError(f"unknown stub transaction {provider_ref}")
        return tx.status

    def cancel_transaction(self, provider_ref: str, *, reason: str) -> EscrowStatus:
        tx = self._store.get(provider_ref)
        if tx is None:
            raise KeyError(f"unknown stub transaction {provider_ref}")
        tx.status = EscrowStatus.CANCELLED
        tx.metadata["cancel_reason"] = reason
        return tx.status


def get_provider() -> EscrowProvider:
    """Provider factory. Only the stub exists in the skeleton. Wiring a
    real provider requires an explicit settings change AND Spencer's
    approval — see docs/DOMAINFOLIO_MASTER_PLAN.md."""
    from app.core.config import settings

    if settings.escrow_provider == "stub":
        return StubEscrowProvider()
    raise RuntimeError(
        f"escrow provider '{settings.escrow_provider}' is not configured; "
        "no real provider may be wired without approval"
    )
