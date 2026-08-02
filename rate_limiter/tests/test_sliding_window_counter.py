from rateLimiter.clock import FakeClock
from rateLimiter.sliding_window_counter import SlidingWindowCounter


def test_limit():
    clock = FakeClock()

    limiter = SlidingWindowCounter(
        limit=2,
        window_size=10,
        clock=clock,
    )

    assert limiter.allow("alice")
    assert limiter.allow("alice")

    assert not limiter.allow("alice")


def test_window_shift():
    clock = FakeClock()

    limiter = SlidingWindowCounter(
        limit=2,
        window_size=10,
        clock=clock,
    )

    limiter.allow("alice")
    limiter.allow("alice")

    clock.advance(20)

    assert limiter.allow("alice")


def test_skip_multiple_windows():
    clock = FakeClock()

    limiter = SlidingWindowCounter(
        limit=2,
        window_size=10,
        clock=clock,
    )

    limiter.allow("alice")
    limiter.allow("alice")

    clock.advance(100)

    assert limiter.allow("alice")