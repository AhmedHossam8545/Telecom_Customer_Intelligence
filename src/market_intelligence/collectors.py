"""Egyptian telecom market collection was cancelled. This module is intentionally empty."""


class MarketCollectionCancelledError(RuntimeError):
    """Raised if market collection is called after the scope cancellation."""


def collect_operator_plans(*_args, **_kwargs):
    raise MarketCollectionCancelledError(
        "Egyptian telecom market collection is cancelled and is not implemented."
    )
