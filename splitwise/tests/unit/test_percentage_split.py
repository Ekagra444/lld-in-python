import pytest

from splitwise.percentage_split import PercentageSplit
from splitwise.user import User


@pytest.fixture
def users():
    return {
        "alice": User(id="1", name="Alice"),
        "bob": User(id="2", name="Bob"),
        "charlie": User(id="3", name="Charlie"),
    }


def test_percentage_split(users):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 5000,    # 50%
            users["bob"]: 3000,      # 30%
            users["charlie"]: 2000,  # 20%
        }
    )

    shares = strategy.calculate_shares(
        users=list(users.values()),
        amount=1000,
    )

    assert shares == {
        users["alice"]: 500,
        users["bob"]: 300,
        users["charlie"]: 200,
    }


def test_percentage_split_distributes_remainder_to_largest_remainder(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 3333,    # 33.33%
            users["bob"]: 3333,      # 33.33%
            users["charlie"]: 3334,  # 33.34%
        }
    )

    shares = strategy.calculate_shares(
        users=list(users.values()),
        amount=100,
    )

    assert shares == {
        users["alice"]: 33,
        users["bob"]: 33,
        users["charlie"]: 34,
    }

    assert sum(shares.values()) == 100


def test_percentage_split_remainder_does_not_depend_on_user_order(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 3333,
            users["bob"]: 3333,
            users["charlie"]: 3334,
        }
    )

    shares = strategy.calculate_shares(
        users=[
            users["charlie"],
            users["bob"],
            users["alice"],
        ],
        amount=100,
    )

    assert shares == {
        users["alice"]: 33,
        users["bob"]: 33,
        users["charlie"]: 34,
    }


def test_percentage_split_uses_user_id_as_tie_breaker():
    bob = User(id="2", name="Bob")
    alice = User(id="1", name="Alice")

    strategy = PercentageSplit(
        percentages={
            bob: 5000,
            alice: 5000,
        }
    )

    shares = strategy.calculate_shares(
        users=[bob, alice],
        amount=101,
    )

    # Both have the same remainder.
    # Alice has the smaller ID, so Alice gets
    # the additional rupee.
    assert shares == {
        alice: 51,
        bob: 50,
    }


def test_percentage_split_requires_percentages_to_sum_to_100(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 5000,
            users["bob"]: 3000,
            users["charlie"]: 1000,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_percentage_split_rejects_negative_percentage(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 5000,
            users["bob"]: -1000,
            users["charlie"]: 6000,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_percentage_split_requires_all_participants(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 5000,
            users["bob"]: 5000,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_percentage_split_rejects_extra_participant(
    users,
):
    david = User(id="4", name="David")

    strategy = PercentageSplit(
        percentages={
            users["alice"]: 2500,
            users["bob"]: 2500,
            users["charlie"]: 2500,
            david: 2500,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_percentage_split_rejects_non_positive_amount(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 5000,
            users["bob"]: 5000,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=[
                users["alice"],
                users["bob"],
            ],
            amount=0,
        )


def test_percentage_split_always_preserves_total(
    users,
):
    strategy = PercentageSplit(
        percentages={
            users["alice"]: 3333,
            users["bob"]: 3333,
            users["charlie"]: 3334,
        }
    )

    shares = strategy.calculate_shares(
        users=list(users.values()),
        amount=999,
    )

    assert sum(shares.values()) == 999