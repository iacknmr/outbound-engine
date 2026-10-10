"""A supplied signal returns a hint, not a business operation."""

import pytest

from portfolio_examples.routing_example import Destination, ExampleSignal, route_hint


@pytest.mark.parametrize(
    "signal,destination",
    [
        (ExampleSignal.POSITIVE, Destination.SALES_HANDOFF),
        (ExampleSignal.AMBIGUOUS, Destination.OPERATOR_REVIEW),
        (ExampleSignal.OPT_OUT, Destination.SUPPRESS),
        (None, Destination.OPERATOR_REVIEW),
    ],
)
def test_simplified_route_mapping(
    signal: ExampleSignal | None, destination: Destination
) -> None:
    assert route_hint(signal) is destination


def test_unknown_string_is_not_silently_routed() -> None:
    with pytest.raises(TypeError, match="ExampleSignal"):
        route_hint("POSITIVE")  # type: ignore[arg-type]
