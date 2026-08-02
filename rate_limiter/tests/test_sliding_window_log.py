from rateLimiter.clock import FakeClock
from rateLimiter.sliding_window_log import SlidingWindowLog


def test_limit():
    clock = FakeClock()

    limiter = SlidingWindowLog(
        limit=2,
        window_size=10,
        clock=clock,
    )

    assert limiter.allow("alice")
    assert limiter.allow("alice")

    assert not limiter.allow("alice")


def test_window_expiry():
    clock = FakeClock()

    limiter = SlidingWindowLog(
        limit=2,
        window_size=10,
        clock=clock,
    )

    limiter.allow("alice")
    limiter.allow("alice")

    clock.advance(10)

    assert limiter.allow("alice")


def test_cleanup_multiple_requests():
    clock = FakeClock()

    limiter = SlidingWindowLog(
        limit=5,
        window_size=10,
        clock=clock,
    )

    for _ in range(5):
        limiter.allow("alice")

    clock.advance(100)

    assert limiter.allow("alice")