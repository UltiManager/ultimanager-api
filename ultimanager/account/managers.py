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

    def create_user(
        self, email: str, name: str, password: str = None, **kwargs
    ):
        """
        Create a new user and save them in the database.

        Args:
            email:
                The user's email address.
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
        user = self.model(email=email, name=name, **kwargs)
        user.set_password(password)

        user.save()

        return user

    def get_by_natural_key(self, email: str):
        """
        Get a user by their email address.

        Args:
            email:
                The email address of the user to return.

        Returns:
            The user with the specified email address.
        """
        return self.get(email=email)
