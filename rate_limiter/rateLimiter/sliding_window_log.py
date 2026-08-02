from __future__ import annotations

import threading
from .clock import Clock
from .models import SlidingWindowState
from .strategy import RateLimitStrategy

class SlidingWindowLog(RateLimitStrategy):

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
        self._window_size= window_size
        self._windows:dict[str,SlidingWindowState]={}
        self._map_lock = threading.Lock()
        self._clock=clock
    def _get_or_create_window(
            self,
            key:str,
    )->SlidingWindowState:
        with self._map_lock:
            state = self._windows.get(key)
            if state is None:
                state = SlidingWindowState()
                self._windows[key]=state
            return state
    def _cleanup(
            self,
            state:SlidingWindowState,
            now:float
    )->None:
        expiry = now - self._window_size
        while(state.timestamps and state.timestamps[0]<=expiry):
            state.timestamps.popleft()
    
    def allow(self, key:str):
        state = self._get_or_create_window(key)
        with state.lock:
            now = self._clock.now()
            self._cleanup(state,now)
            if len(state.timestamps)>=self._limit:
                return False
            state.timestamps.append(now)
            return True