from unittest import mock

from account import managers, models


@mock.patch("account.managers.UserManager.create_user")
def test_create_superuser(mock_create_user):
    """
    Creating a super user should act identically to ``create_user``
    except ``is_staff`` and ``is_superuser`` should be set to ``True``
    by default.
    """
    kwargs = {"name": "John Smith", "password": "password"}
    manager = managers.UserManager()

    user = manager.create_superuser(**kwargs)

    assert user == mock_create_user.return_value
    assert mock_create_user.call_args[1] == dict(
        **kwargs, is_staff=True, is_superuser=True
    )


def test_create_user():
    """
    Creating a user should pass all fields except the password directly
    to the new user instance and then save it. The password should be
    set using the ``set_password`` method.
    """
    manager = managers.UserManager()
    manager.model = mock.Mock(spec=models.User)

    is_staff = True
    name = "John Smith"
    password = "password"

    user = manager.create_user(is_staff=True, name=name, password=password)

    assert manager.model.call_args[1] == {"is_staff": is_staff, "name": name}
    assert user.set_password.call_args[0] == (password,)
    assert user.save.call_count == 1
