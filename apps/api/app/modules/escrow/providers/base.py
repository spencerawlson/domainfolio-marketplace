"""Escrow provider adapter interface.

The marketplace never talks to an escrow provider directly — it talks
to this interface. Swapping providers (Escrow.com -> another) means
writing one new adapter, not rewriting the marketplace. Every method
is explicit about what "secured" means: a payment is only ever
reported as secured when the provider itself says so.

Sandbox rule: no adapter may move real money. The stub adapter is the
only one wired until an Escrow.com sandbox account exists and Spencer
approves the integration.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class EscrowStatus(str, Enum):
    CREATED = "created"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_SECURED = "payment_secured"  # provider-confirmed only
    TRANSFER_INITIATED = "transfer_initiated"
    TRANSFER_CONFIRMED = "transfer_confirmed"
    SETTLED = "settled"
    REFUNDED = "refunded"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"


@dataclass
class EscrowTransaction:
    provider_ref: str
    status: EscrowStatus
    buyer_id: str
    seller_id: str
    domain: str
    amount_cents: int
    currency: str = "USD"
    metadata: dict = field(default_factory=dict)


class EscrowProvider(ABC):
    """One adapter per escrow provider. All I/O is provider-side; the
    marketplace stores only the provider reference + the last
    provider-confirmed status."""

    name: str = "base"

    @abstractmethod
    def create_transaction(
        self, *, buyer_id: str, seller_id: str, domain: str, amount_cents: int, currency: str = "USD"
    ) -> EscrowTransaction:
        raise NotImplementedError

    @abstractmethod
    def get_status(self, provider_ref: str) -> EscrowStatus:
        raise NotImplementedError

    @abstractmethod
    def cancel_transaction(self, provider_ref: str, *, reason: str) -> EscrowStatus:
        raise NotImplementedError

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Default: no provider signature scheme configured -> reject.
        Adapters override with the provider's real scheme (HMAC, etc.)."""
        return False
