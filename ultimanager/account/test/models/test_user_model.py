from account import models, managers


def test_get_email_field_name():
    """
    Users should use their 'email' field to store their email address.
    """
    assert models.User.get_email_field_name() == "email"


def test_get_full_name():
    """
    The user's full name should be equal to their name.
    """
    user = models.User(name="John Smith")

    assert user.get_full_name() == user.name


def test_get_short_name():
    """
    The user's short name should be equivalent to their name.
    """
    user = models.User(name="John Smith")

    assert user.get_short_name() == user.name


def test_get_username():
    """
    A user's username should be their email address.
    """
    user = models.User(email="test@example.com")

    assert user.get_username() == user.email


def test_objects_type():
    """
    The user model should use our custom user manager.
    """
    assert isinstance(models.User.objects, managers.UserManager)


def test_repr():
    """
    The representation of a user should include the information required
    to find the user instance again.
    """
    user = models.User(name="John Smith")
    expected = f"<account.User: id={repr(user.pk)} name={repr(user.name)}>"

    assert repr(user) == expected


def test_str():
    """
    The string representation of a user should be the user's name.
    """
    user = models.User(name="John Smith")

    assert str(user) == user.name
