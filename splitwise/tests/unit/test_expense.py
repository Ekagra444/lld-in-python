import pytest
from splitwise.user import User
from splitwise.equal_split import EqualSplit
from splitwise.expense import Expense

def test_expense_calculates_shares():
    alice = User("1", "Alice")
    bob = User("2", "Bob")
    charlie = User("3", "Charlie")

    expense = Expense(
        id="e1",
        payer=alice,
        amount=900,
        participants=[alice, bob, charlie],
        split_strategy=EqualSplit(),
    )

    assert expense.shares == {
        alice: 300,
        bob: 300,
        charlie: 300,
    }

def test_expense_requires_payer_to_be_participant():
    alice = User("1", "Alice")
    bob = User("2", "Bob")

    with pytest.raises(ValueError):
        Expense(
            id="e1",
            payer=alice,
            amount=100,
            participants=[bob],
            split_strategy=EqualSplit(),
        )