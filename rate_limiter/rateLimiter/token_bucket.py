from __future__ import annotations

import threading
from .clock import Clock
from .models import Bucket
from .strategy import RateLimitStrategy

class TokenBucket(RateLimitStrategy):

    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        clock:Clock
    ) -> None:

        if capacity <= 0:
            raise ValueError("capacity must be positive")

        if refill_rate <= 0:
            raise ValueError("refill_rate must be positive")

        self._capacity = capacity
        self._refill_rate = refill_rate

        self._buckets: dict[str, Bucket] = {}

        self._map_lock = threading.Lock()
        self._clock = clock

    def _get_or_create_bucket(
        self,
        key: str,
    ) -> Bucket:
        with self._map_lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = Bucket(tokens=self._capacity, last_refill=self._clock.now())
                self._buckets[key] = bucket
            return bucket
    def _refill(
            self,
            bucket:Bucket,
            now:float,
    )->None:
        elapsed = now - bucket.last_refill
        tokens_to_add = int(
            elapsed*self._refill_rate
        )
        if tokens_to_add == 0:
            return
        bucket.tokens = min(
            self._capacity,
            bucket.tokens + tokens_to_add
        )
        bucket.last_refill = tokens_to_add/self._refill_rate

    def allow(self, key:str):
        bucket = self._get_or_create_bucket(key)
        with bucket.lock:
            now = self._clock.now()
            # bucket.last_access=self._clock.now()
            self._refill(bucket,now)
            if(bucket.tokens<1):
                return False
            bucket.tokens-=1
            return True
