from splitwise.user import User
from splitwise.equal_split import EqualSplit
import pytest

def test_equal_split():
    users = [
        User("1", "Alice"),
        User("2", "Bob"),
        User("3", "Charlie"),
    ]

    strategy = EqualSplit()

    shares = strategy.calculate_shares(
        participants=users,
        amount=900,
    )

    assert shares == {
        users[0]: 300,
        users[1]: 300,
        users[2]: 300,
    }


def test_equal_split_rejects_empty_participants():
    strategy = EqualSplit()

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            participants=[],
            amount=100,
        )

def test_equal_split_rejects_non_positive_amount():
    strategy = EqualSplit()

    with pytest.raises(ValueError):
        strategy.calculate_shares(
            participants=[User("1", "Alice")],
            amount=0,
        )

def test_equal_split_distributes_remainder():
    users = [
        User("1", "Alice"),
        User("2", "Bob"),
        User("3", "Charlie"),
    ]

    shares = EqualSplit().calculate_shares(
        participants=users,
        amount=100,
    )

    assert sum(shares.values()) == 100