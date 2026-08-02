from concurrent.futures import ThreadPoolExecutor

from rateLimiter.clock import FakeClock
from rateLimiter.token_bucket import TokenBucket


def test_token_bucket_thread_safety():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=100,
        refill_rate=1,
        clock=clock,
    )

    def worker(_) -> bool:
        return limiter.allow("alice")

    with ThreadPoolExecutor(max_workers=500) as executor:
        results = list(executor.map(worker, range(500)))

    assert sum(results) == 100