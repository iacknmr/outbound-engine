"""A simple arithmetic limit check, deliberately not a capacity allocator.

The caller supplies two independent counters. This does not reproduce private
provider accounting, mailbox selection, pacing, reservation, or scheduling.
A read-only answer cannot reserve capacity or prevent concurrent consumption.
"""

from dataclasses import dataclass
from enum import StrEnum


class CapacityReason(StrEnum):
    MAILBOX_LIMIT = "MAILBOX_LIMIT"
    PROVIDER_LIMIT = "PROVIDER_LIMIT"


@dataclass(frozen=True, slots=True)
class DailyBudget:
    """A fictional usage/limit pair with explicit input validation."""

    used: int
    limit: int

    def __post_init__(self) -> None:
        for value in (self.used, self.limit):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError("usage and limit must be integers")
            if value < 0:
                raise ValueError("usage and limit must be non-negative")

    @property
    def remaining(self) -> int:
        """Over-budget input is allowed; remaining capacity is never negative."""
        return max(0, self.limit - self.used)


@dataclass(frozen=True, slots=True)
class CapacityCheck:
    available: bool
    reasons: tuple[CapacityReason, ...]


def check_capacity(mailbox: DailyBudget, provider: DailyBudget) -> CapacityCheck:
    """Require both supplied budgets to have room, with no side effects.

    Equality blocks. A zero limit blocks. No counter is incremented.
    This teaching example defines no production provider-ceiling semantics.
    """
    reasons: list[CapacityReason] = []
    if mailbox.used >= mailbox.limit:
        reasons.append(CapacityReason.MAILBOX_LIMIT)
    if provider.used >= provider.limit:
        reasons.append(CapacityReason.PROVIDER_LIMIT)
    return CapacityCheck(not reasons, tuple(reasons))
