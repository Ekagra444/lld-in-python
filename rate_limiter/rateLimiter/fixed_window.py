from .strategy import RateLimitStrategy
from .models import FixedWindowState
import threading
from .clock import Clock

class FixedWindow(RateLimitStrategy):

    def __init__(
        self,
        limit: int,
        window_size: float,
        clock:Clock
    ) -> None:

        if limit <= 0:
            raise ValueError("limit must be positive")

        if window_size <= 0:
            raise ValueError("window_size must be positive")

        self._limit = limit
        self._window_size = window_size

        self._states: dict[str, FixedWindowState] = {}
        self._map_lock = threading.Lock()
        self._clock = clock

    def _get_or_create_state(
        self,
        key: str,
    ) -> FixedWindowState:

        with self._map_lock:

            state = self._states.get(key)

            if state is None:
                state = FixedWindowState(
                    request_count=0,
                    window_start=self._clock.now(),
                )

                self._states[key] = state

            return state
    
    
    def _advance_window(
        self,
        state: FixedWindowState,
        now: float,
    ) -> None:

        elapsed_windows = int(
            (now - state.window_start)
            // self._window_size
        )

        if elapsed_windows == 0:
            return

        state.request_count = 0

        state.window_start += (
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

            if state.request_count >= self._limit:
                return False

            state.request_count += 1

            return True