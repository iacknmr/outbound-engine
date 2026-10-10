"""Three illustrative routing hints, not a classifier or workflow engine.

The signal is supplied by the test caller. There is no AI prompt, provider,
confidence policy, complete business decision tree, or persistence.
Returning SUPPRESS does not create a suppression record or any side effect.
"""

from enum import StrEnum


class ExampleSignal(StrEnum):
    POSITIVE = "POSITIVE"
    AMBIGUOUS = "AMBIGUOUS"
    OPT_OUT = "OPT_OUT"


class Destination(StrEnum):
    SALES_HANDOFF = "SALES_HANDOFF"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    SUPPRESS = "SUPPRESS"


def route_hint(signal: ExampleSignal | None) -> Destination:
    """Keep missing evidence in human review instead of guessing intent."""
    if signal is None:
        return Destination.OPERATOR_REVIEW
    if not isinstance(signal, ExampleSignal):
        raise TypeError("signal must be an ExampleSignal or None")
    if signal is ExampleSignal.POSITIVE:
        return Destination.SALES_HANDOFF
    if signal is ExampleSignal.OPT_OUT:
        return Destination.SUPPRESS
    return Destination.OPERATOR_REVIEW
