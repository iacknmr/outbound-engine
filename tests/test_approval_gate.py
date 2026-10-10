"""Only the standalone approval example is exercised."""

from dataclasses import FrozenInstanceError

import pytest

from portfolio_examples.approval_gate import (
    ApprovalReason,
    ReviewSnapshot,
    ReviewState,
    check_approval,
)


def test_missing_review_is_denied() -> None:
    assert check_approval("revision-1", None).reason is ApprovalReason.MISSING_REVIEW
    assert not check_approval("revision-1", None).allowed


def test_unreviewed_default_is_denied() -> None:
    result = check_approval("revision-1", ReviewSnapshot("revision-1"))
    assert not result.allowed
    assert result.reason is ApprovalReason.NOT_APPROVED


def test_rejection_is_denied() -> None:
    review = ReviewSnapshot("revision-1", ReviewState.REJECTED)
    assert not check_approval("revision-1", review).allowed


def test_exact_approved_revision_passes_this_gate_only() -> None:
    review = ReviewSnapshot("revision-1", ReviewState.APPROVED)
    result = check_approval("revision-1", review)
    assert result.allowed
    assert result.reason is ApprovalReason.APPROVED_REVISION


def test_changed_revision_does_not_reuse_approval() -> None:
    review = ReviewSnapshot("revision-1", ReviewState.APPROVED)
    result = check_approval("revision-2", review)
    assert not result.allowed
    assert result.reason is ApprovalReason.DIFFERENT_REVISION


def test_review_snapshot_is_immutable() -> None:
    review = ReviewSnapshot("revision-1")
    with pytest.raises(FrozenInstanceError):
        review.state = ReviewState.APPROVED  # type: ignore[misc]


@pytest.mark.parametrize("revision", ["", " ", "\n"])
def test_blank_snapshot_revision_is_rejected(revision: str) -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        ReviewSnapshot(revision)


def test_blank_current_revision_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        check_approval("", None)


def test_untyped_state_is_rejected() -> None:
    with pytest.raises(TypeError, match="ReviewState"):
        ReviewSnapshot("revision-1", "APPROVED")  # type: ignore[arg-type]
