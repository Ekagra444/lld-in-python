import pytest

from splitwise.user import User
from splitwise.exact_split import ExactSplit


@pytest.fixture
def users():
    return {
        "alice": User(id="1", name="Alice"),
        "bob": User(id="2", name="Bob"),
        "charlie": User(id="3", name="Charlie"),
    }


def test_exact_split_returns_requested_shares(users):
    strategy = ExactSplit(
        shares={
            users["alice"]: 300,
            users["bob"]: 400,
            users["charlie"]: 300,
        }
    )

    shares = strategy.calculate_shares(
        users=list(users.values()),
        amount=1000,
    )

    assert shares == {
        users["alice"]: 300,
        users["bob"]: 400,
        users["charlie"]: 300,
    }


def test_exact_split_shares_must_sum_to_expense_amount(users):
    strategy = ExactSplit(
        shares={
            users["alice"]: 300,
            users["bob"]: 300,
            users["charlie"]: 300,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_exact_split_rejects_negative_share(users):
    strategy = ExactSplit(
        shares={
            users["alice"]: 500,
            users["bob"]: -100,
            users["charlie"]: 600,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_exact_split_requires_all_participants(users):
    strategy = ExactSplit(
        shares={
            users["alice"]: 500,
            users["bob"]: 500,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_exact_split_rejects_extra_user(users):
    david = User(id="4", name="David")

    strategy = ExactSplit(
        shares={
            users["alice"]: 300,
            users["bob"]: 300,
            users["charlie"]: 300,
            david: 100,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=1000,
        )


def test_exact_split_rejects_non_positive_expense(users):
    strategy = ExactSplit(
        shares={
            users["alice"]: 0,
            users["bob"]: 0,
            users["charlie"]: 0,
        }
    )

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            users=list(users.values()),
            amount=0,
        )