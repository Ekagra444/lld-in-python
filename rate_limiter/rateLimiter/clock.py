from __future__ import annotations

import time
from abc import ABC, abstractmethod


class Clock(ABC):
    """Abstraction over time to make algorithms testable."""

    @abstractmethod
    def now(self) -> float:
        """Returns current monotonic time in seconds."""
        raise NotImplementedError


class SystemClock(Clock):
    """Production clock."""

    def now(self) -> float:
        return time.monotonic()


class FakeClock(Clock):
    """Deterministic clock used in tests."""

    def __init__(self, initial_time: float = 0.0) -> None:
        self._time = initial_time

    def now(self) -> float:
        return self._time

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("Cannot move clock backwards.")

        self._time += seconds

    def set(self, timestamp: float) -> None:
        if timestamp < self._time:
            raise ValueError("Cannot move clock backwards.")

        self._time = timestamp