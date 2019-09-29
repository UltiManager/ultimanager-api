from authentication import views, serializers


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.SessionCreationView()
    expected = serializers.SessionCreationSerializer

    assert view.get_serializer_class() == expected
