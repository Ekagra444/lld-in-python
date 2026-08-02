from .strategy import RateLimitStrategy
from .models import SlidingCounterState
import threading
from .clock import Clock

class SlidingWindowCounter(RateLimitStrategy):

    def __init__(
        self,
        limit: int,
        window_size: float,
        clock:Clock,
    ) -> None:

        if limit <= 0:
            raise ValueError("limit must be positive")

        if window_size <= 0:
            raise ValueError("window_size must be positive")

        self._limit = limit
        self._window_size = window_size

        self._states: dict[str, SlidingCounterState] = {}
        self._map_lock = threading.Lock()
        self._clock=clock
    
    
    def _get_or_create_state(
        self,
        key: str,
    ) -> SlidingCounterState:

        with self._map_lock:

            state = self._states.get(key)

            if state is None:
                now = self._clock.now()

                state = SlidingCounterState(
                    previous_count=0,
                    current_count=0,
                    current_window_start=now,
                )

                self._states[key] = state

            return state
    
    def _advance_window(
        self,
        state: SlidingCounterState,
        now: float,
    ) -> None:
        elapsed_windows = int(
            (now - state.current_window_start)
            // self._window_size
        )

        if elapsed_windows == 0:
            return

        if elapsed_windows == 1:
            state.previous_count = state.current_count
        else:
            state.previous_count = 0

        state.current_count = 0
        state.current_window_start += (
            elapsed_windows * self._window_size
        )

    def allow(
        self,
        key: str,
    ) -> bool:

        state = self._get_or_create_state(key)

        with state.lock:

            now = self._clock.now()

            self._advance_window(state, now)

            elapsed = now - state.current_window_start

            weight = (
                self._window_size - elapsed
            ) / self._window_size

            effective_count = (
                state.current_count
                + state.previous_count * weight
            )

            if effective_count >= self._limit:
                return False

            state.current_count += 1

            return True