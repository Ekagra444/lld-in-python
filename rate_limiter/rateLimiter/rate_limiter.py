from .strategy import RateLimitStrategy


class RateLimiter:
    """
    Public entry point.

    Consumers should depend on this class,
    not on concrete algorithms.
    """

    def __init__(
        self,
        strategy: RateLimitStrategy,
    ):
        self._strategy = strategy

    def allow(self, key: str) -> bool:
        return self._strategy.allow(key)
    
    def get_strategy(self):
        return self._strategy