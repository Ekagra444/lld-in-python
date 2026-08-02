from abc import ABC, abstractmethod


class RateLimitStrategy(ABC):
    """
    Contract implemented by every rate limiting algorithm.

    A strategy owns:
        - configuration
        - runtime state
        - synchronization
        - algorithm

    It should NOT know anything about HTTP,
    users, APIs or business rules.
    """
    @abstractmethod
    def allow(self, key: str) -> bool:
        """Returns True if request should be allowed."""
        raise NotImplementedError