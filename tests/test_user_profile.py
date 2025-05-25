import pytest
from src.user_profile import UserProfile

def test_friend_management():
    user1 = UserProfile("alice", "alice@example.com", 20)
    user2 = UserProfile("bob", "bob@example.com", 17)
    user3 = UserProfile("carol", "carol@example.com", 22)

    user1.add_friend(user2)
    user1.add_friend(user3)
    assert user1.friend_count() == 2
    user1.remove_friend(user2)
    assert user1.friend_count() == 1

    with pytest.raises(ValueError):
        user1.add_friend(user1)

def test_is_adult():
    user = UserProfile("dave", "dave@example.com", 18)
    assert user.is_adult()
    user.age = 19
    assert user.is_adult()

def test_email_domain():
    user = UserProfile("eve", "eve@domain.com", 25)
    assert user.email_domain() == "domain.com"
    user.email = "invalid_email"
    with pytest.raises(ValueError):
        user.email_domain()

def test_mutual_friends():
    u1 = UserProfile("f1", "f1@x.com", 20)
    u2 = UserProfile("f2", "f2@x.com", 21)
    u3 = UserProfile("f3", "f3@x.com", 22)
    u1.add_friend(u2)
    u1.add_friend(u3)
    u2.add_friend(u3)
    mutual = u1.mutual_friends(u2)
    assert u3 in mutual
