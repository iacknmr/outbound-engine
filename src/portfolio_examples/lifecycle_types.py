"""A few immutable vocabulary types for classroom examples.

These are not production records, database models, or a transition system.
A label alone does not grant permission to perform any external operation.
"""

from dataclasses import dataclass
from enum import StrEnum


class CampaignLabel(StrEnum):
    """Labels only: there is deliberately no campaign implementation."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"


class SendLabel(StrEnum):
    """An illustrative vocabulary, not a delivery recovery state machine."""

    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    NEEDS_REVIEW = "NEEDS_REVIEW"


@dataclass(frozen=True, slots=True)
class DemoMessage:
    """Fictional content for an in-memory transport example.

    Strings are intentionally not SMTP headers or a MIME representation.
    This object provides neither address validation nor delivery capability.
    """

    sender: str
    recipient: str
    subject: str
    body: str


@dataclass(frozen=True, slots=True)
class DemoReply:
    """A supplied sample, not a fetched or classified mailbox message."""

    text: str
