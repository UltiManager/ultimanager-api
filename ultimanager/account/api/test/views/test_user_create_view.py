from account.api import views, serializers


def test_get_serializer_class():
    """
    Test which serializer class is used by the view.
    """
    view = views.UserCreateView()
    expected = serializers.UserCreationSerializer

    assert view.get_serializer_class() == expected
