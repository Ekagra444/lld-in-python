from splitwise.user import User
def test_users_with_same_id_are_equal():
    user1 = User(id="1", name="Alice")
    user2 = User(id="1", name="Alice")

    assert user1 == user2


def test_users_with_different_ids_are_not_equal():
    user1 = User(id="1", name="Alice")
    user2 = User(id="2", name="Alice")

    assert user1 != user2


def test_user_can_be_used_as_dictionary_key():
    user = User(id="1", name="Alice")

    balances = {user: 100}

    assert balances[user] == 100