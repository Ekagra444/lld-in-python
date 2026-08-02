import pytest

from rateLimiter.clock import FakeClock
from rateLimiter.token_bucket import TokenBucket


def test_invalid_capacity():
    with pytest.raises(ValueError):
        TokenBucket(0, 1,clock=FakeClock())


def test_invalid_refill_rate():
    with pytest.raises(ValueError):
        TokenBucket(10, 0,clock=FakeClock())


def test_first_request_allowed():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=5,
        refill_rate=1,
        clock=clock,
    )

    assert limiter.allow("alice")


def test_capacity():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=2,
        refill_rate=1,
        clock=clock,
    )

    assert limiter.allow("alice")
    assert limiter.allow("alice")

    assert not limiter.allow("alice")


def test_refill_after_one_second():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=2,
        refill_rate=1,
        clock=clock,
    )

    limiter.allow("alice")
    limiter.allow("alice")

    assert not limiter.allow("alice")

    clock.advance(1)

    assert limiter.allow("alice")


def test_fractional_refill():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=1,
        refill_rate=2,
        clock=clock,
    )

    limiter.allow("alice")

    assert not limiter.allow("alice")

    clock.advance(0.4)

    assert not limiter.allow("alice")

    clock.advance(0.1)

    assert limiter.allow("alice")


def test_bucket_never_exceeds_capacity():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=5,
        refill_rate=100,
        clock=clock,
    )

    limiter.allow("alice")

    clock.advance(100)

    for _ in range(5):
        assert limiter.allow("alice")

    assert not limiter.allow("alice")


def test_users_are_independent():
    clock = FakeClock()

    limiter = TokenBucket(
        capacity=1,
        refill_rate=1,
        clock=clock,
    )

    assert limiter.allow("alice")
    assert limiter.allow("bob")

    assert not limiter.allow("alice")
    assert not limiter.allow("bob")