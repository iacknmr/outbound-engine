"""The fake stores samples locally; no connection implementation exists."""

from dataclasses import FrozenInstanceError

import pytest

from portfolio_examples.lifecycle_types import (
    CampaignLabel,
    DemoMessage,
    DemoReply,
    SendLabel,
)
from portfolio_examples.transport_protocols import (
    IncomingPort,
    InMemoryTransport,
    OutgoingPort,
)


def message() -> DemoMessage:
    return DemoMessage(
        sender="sender@example.com",
        recipient="alex@example.net",
        subject="Fictional interface example",
        body="Hi Alex, this is only an in-memory example for Acme Infrastructure.",
    )


def test_fake_satisfies_both_typed_ports() -> None:
    fake = InMemoryTransport([DemoReply("Fictional reply")])
    outgoing: OutgoingPort = fake
    incoming: IncomingPort = fake
    receipt = outgoing.submit(message())
    assert receipt.reference == "demo-1"
    assert receipt.recorded_locally
    assert incoming.read_samples() == (DemoReply("Fictional reply"),)


def test_fake_does_not_claim_delivery_or_deduplication() -> None:
    fake = InMemoryTransport()
    first = fake.submit(message())
    second = fake.submit(message())
    assert (first.reference, second.reference) == ("demo-1", "demo-2")
    assert len(fake.recorded_messages) == 2


def test_recorded_snapshot_does_not_change_on_later_submission() -> None:
    fake = InMemoryTransport()
    fake.submit(message())
    snapshot = fake.recorded_messages
    fake.submit(message())
    assert len(snapshot) == 1
    assert len(fake.recorded_messages) == 2


def test_samples_are_copied_from_caller_container() -> None:
    supplied = [DemoReply("Fictional reply")]
    fake = InMemoryTransport(supplied)
    supplied.clear()
    assert fake.read_samples() == (DemoReply("Fictional reply"),)


def test_empty_fake_has_no_external_work() -> None:
    fake = InMemoryTransport()
    assert fake.read_samples() == ()
    assert fake.recorded_messages == ()


def test_demo_message_is_immutable() -> None:
    sample = message()
    with pytest.raises(FrozenInstanceError):
        sample.body = "changed"  # type: ignore[misc]


def test_lifecycle_values_are_labels_only() -> None:
    assert tuple(CampaignLabel) == (
        CampaignLabel.DRAFT,
        CampaignLabel.ACTIVE,
        CampaignLabel.PAUSED,
        CampaignLabel.ARCHIVED,
    )
    assert SendLabel.NEEDS_REVIEW.value == "NEEDS_REVIEW"
