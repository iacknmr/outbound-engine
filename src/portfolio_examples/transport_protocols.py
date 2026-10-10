"""Typed ports with a fake implementation that only records Python objects.

No SMTP/IMAP libraries, network clients, credentials, MIME, mailbox commands,
provider adapters, or retries are present. "Submit" means append to a local list,
not send an email. A demo receipt is never evidence of external acceptance.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from portfolio_examples.lifecycle_types import DemoMessage, DemoReply


@dataclass(frozen=True, slots=True)
class DemoReceipt:
    """An in-memory record identifier, not an RFC message identifier."""

    reference: str
    recorded_locally: bool = True


class OutgoingPort(Protocol):
    """Describe the shape of an outgoing abstraction, not SMTP operations."""

    def submit(self, message: DemoMessage) -> DemoReceipt: ...


class IncomingPort(Protocol):
    """Describe a supplied-sample abstraction, not an IMAP mailbox client."""

    def read_samples(self) -> tuple[DemoReply, ...]: ...


class InMemoryTransport:
    """A deterministic fake for testing interface consumers.

    This is not a delivery simulator and makes no safety or persistence
    guarantee. Repeated submissions create repeated local records by design.
    """

    def __init__(self, replies: Iterable[DemoReply] = ()) -> None:
        self._messages: list[DemoMessage] = []
        self._replies = tuple(replies)

    @property
    def recorded_messages(self) -> tuple[DemoMessage, ...]:
        """Expose a snapshot rather than a mutable internal list."""
        return tuple(self._messages)

    def submit(self, message: DemoMessage) -> DemoReceipt:
        self._messages.append(message)
        return DemoReceipt(reference=f"demo-{len(self._messages)}")

    def read_samples(self) -> tuple[DemoReply, ...]:
        """Return only samples supplied by the caller; nothing is fetched."""
        return self._replies
