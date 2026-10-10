"""Demonstrate a fail-closed check against an immutable review snapshot.

A revision is a caller-supplied label, not a security token or content hash.
This example does not authenticate reviewers, persist decisions, or implement
the private application's final-send controls.
"""

from dataclasses import dataclass
from enum import StrEnum


class ReviewState(StrEnum):
    UNREVIEWED = "UNREVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalReason(StrEnum):
    MISSING_REVIEW = "MISSING_REVIEW"
    DIFFERENT_REVISION = "DIFFERENT_REVISION"
    NOT_APPROVED = "NOT_APPROVED"
    APPROVED_REVISION = "APPROVED_REVISION"


@dataclass(frozen=True, slots=True)
class ReviewSnapshot:
    """Editing content should not silently reuse a decision about older content."""

    revision: str
    state: ReviewState = ReviewState.UNREVIEWED

    def __post_init__(self) -> None:
        if not self.revision.strip():
            raise ValueError("revision must not be blank")
        if not isinstance(self.state, ReviewState):
            raise TypeError("state must be a ReviewState")


@dataclass(frozen=True, slots=True)
class ApprovalCheck:
    allowed: bool
    reason: ApprovalReason


def check_approval(
    current_revision: str, review: ReviewSnapshot | None
) -> ApprovalCheck:
    """Return an explanation without modifying the message or review.

    A successful result only answers this one educational question.
    It must not be used as authorization to send an email.
    """
    if not current_revision.strip():
        raise ValueError("current revision must not be blank")
    if review is None:
        return ApprovalCheck(False, ApprovalReason.MISSING_REVIEW)
    if review.revision != current_revision:
        return ApprovalCheck(False, ApprovalReason.DIFFERENT_REVISION)
    if review.state is not ReviewState.APPROVED:
        return ApprovalCheck(False, ApprovalReason.NOT_APPROVED)
    return ApprovalCheck(True, ApprovalReason.APPROVED_REVISION)
