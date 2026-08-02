from rateLimiter.fixed_window import FixedWindow
from rateLimiter.clock import FakeClock
def test_limit():
    clock = FakeClock()

    limiter = FixedWindow(
        limit=2,
        window_size=10,
        clock=clock,
    )

    assert limiter.allow("alice")
    assert limiter.allow("alice")

    assert not limiter.allow("alice")


def test_window_reset():
    clock = FakeClock()

    limiter = FixedWindow(
        limit=2,
        window_size=10,
        clock=clock,
    )

    limiter.allow("alice")
    limiter.allow("alice")

    clock.advance(10)

    assert limiter.allow("alice")


def test_users_are_independent():
    clock = FakeClock()

    limiter = FixedWindow(
        limit=1,
        window_size=10,
        clock=clock,
    )

    assert limiter.allow("alice")
    assert limiter.allow("bob")