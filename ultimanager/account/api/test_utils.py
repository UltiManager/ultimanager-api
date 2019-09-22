def return_for_conditions(obj, raise_ex=False, **kwargs):
    """
    Get a function that returns/raises an object and is suitable as a
    ``side_effect`` for a mock object.

    Args:
        obj:
            The object to return/raise.
        raise_ex:
            A boolean indicating if the object should be raised instead
            of returned.
        **kwargs:
            The keyword arguments that must be provided to the function
            being mocked in order for the provided object to be returned
            or raised. As long as the mocked function is called with at
            least the arguments provided to this function, the handler
            is triggered.

    Returns:
        A function usable as the side effect of a mocked object.
    """

    def handler(**inner_kwargs):
        if kwargs.items() <= inner_kwargs.items():
            if raise_ex:
                raise obj

            return obj

    return handler
