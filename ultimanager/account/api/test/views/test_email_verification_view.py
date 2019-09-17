from account.api import views, serializers


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.EmailVerificationView()
    expected = serializers.EmailVerificationSerializer

    assert view.get_serializer_class() == expected
