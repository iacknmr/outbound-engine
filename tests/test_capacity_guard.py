"""Boundary tests for arithmetic only: no selection or reservation."""

import pytest

from portfolio_examples.capacity_guard import (
    CapacityReason,
    DailyBudget,
    check_capacity,
)


def test_both_budgets_have_room() -> None:
    result = check_capacity(DailyBudget(0, 2), DailyBudget(1, 3))
    assert result.available
    assert result.reasons == ()


@pytest.mark.parametrize("used", [2, 3])
def test_mailbox_at_or_over_limit_blocks(used: int) -> None:
    result = check_capacity(DailyBudget(used, 2), DailyBudget(0, 3))
    assert not result.available
    assert result.reasons == (CapacityReason.MAILBOX_LIMIT,)


@pytest.mark.parametrize("used", [3, 4])
def test_provider_at_or_over_limit_blocks(used: int) -> None:
    result = check_capacity(DailyBudget(0, 2), DailyBudget(used, 3))
    assert not result.available
    assert result.reasons == (CapacityReason.PROVIDER_LIMIT,)


def test_zero_limits_block_with_both_reasons() -> None:
    result = check_capacity(DailyBudget(0, 0), DailyBudget(0, 0))
    assert not result.available
    assert result.reasons == (
        CapacityReason.MAILBOX_LIMIT,
        CapacityReason.PROVIDER_LIMIT,
    )


def test_check_does_not_consume_capacity() -> None:
    mailbox = DailyBudget(0, 2)
    provider = DailyBudget(1, 3)
    assert check_capacity(mailbox, provider) == check_capacity(mailbox, provider)
    assert (mailbox.used, provider.used) == (0, 1)


@pytest.mark.parametrize("used,limit,remaining", [(0, 2, 2), (2, 2, 0), (3, 2, 0)])
def test_remaining_never_becomes_negative(
    used: int, limit: int, remaining: int
) -> None:
    assert DailyBudget(used, limit).remaining == remaining


@pytest.mark.parametrize("used,limit", [(-1, 2), (0, -1)])
def test_negative_inputs_are_rejected(used: int, limit: int) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        DailyBudget(used, limit)


@pytest.mark.parametrize("value", [True, 1.5, "2"])
def test_non_integer_inputs_are_rejected(value: object) -> None:
    with pytest.raises(TypeError, match="integers"):
        DailyBudget(value, 2)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="integers"):
        DailyBudget(0, value)  # type: ignore[arg-type]
