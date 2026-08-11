import pytest
from splitwise.user import User
from splitwise.equal_split import EqualSplit
from splitwise.expense import Expense
from splitwise.balance_book import BalanceBook

def test_apply_expense():
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

    book = BalanceBook()
    book.apply_expense(expense)

    assert book.get_balance(bob, alice) == 300
    assert book.get_balance(charlie, alice) == 300
    assert book.get_balance(alice, alice) == 0

def test_opposite_debt_cancel():
    alice = User("1", "Alice")
    bob = User("2", "Bob")

    expense1 = Expense(
        id="e1",
        payer=alice,
        amount=400,
        participants=[alice, bob],
        split_strategy=EqualSplit(),
    )

    book = BalanceBook()
    book.apply_expense(expense1)

    expense2 = Expense(
        id="e2",
        payer=bob,
        amount=400,
        participants=[alice, bob],
        split_strategy=EqualSplit(),
    )

    book.apply_expense(expense2)


    assert book.get_balance(bob, alice) == 0
    assert book.get_balance(alice, bob) == 0

def test_multiple_expense():
    alice = User("1", "Alice")
    bob = User("2", "Bob")

    expense1 = Expense(
        id="e1",
        payer=alice,
        amount=400,
        participants=[alice, bob],
        split_strategy=EqualSplit(),
    )

    book = BalanceBook()
    book.apply_expense(expense1)

    expense2 = Expense(
        id="e2",
        payer=bob,
        amount=100,
        participants=[alice, bob],
        split_strategy=EqualSplit(),
    )

    book.apply_expense(expense2)


    assert book.get_balance(bob, alice) == 150
    assert book.get_balance(alice, bob) == 0