from django.db.models import manager


class UserManager(manager.Manager):
    """
    Manager for our custom user model.
    """

    def create_superuser(self, **kwargs):
        """
        Create a new superuser.

        Args:
            **kwargs:
                The keyword arguments to create the new user with. See
                :py:meth:`create_user` for the required arguments.

        Returns:
            The newly created superuser.
        """
        kwargs.update({"is_staff": True, "is_superuser": True})

        return self.create_user(**kwargs)

    def create_user(self, name: str, password: str = None, **kwargs):
        """
        Create a new user and save them in the database.

        Args:
            name:
                The user's name.
            password:
                The user's password.
            **kwargs:
                Additional arguments to pass to the user instance being
                created.

        Returns:
            The newly created user instance.
        """
        user = self.model(name=name, **kwargs)
        user.set_password(password)

        user.save()

        return user
