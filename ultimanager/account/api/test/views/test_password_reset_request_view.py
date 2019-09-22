from account.api import views, serializers


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.PasswordResetRequestView()
    expected = serializers.PasswordResetRequestSerializer

    assert view.get_serializer_class() == expected
