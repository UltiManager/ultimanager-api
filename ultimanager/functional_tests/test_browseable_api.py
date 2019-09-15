def test_view_browsable_api(client):
    """
    Test viewing the browsable API.

    Regression test for #22
    """
    # Arbitrary endpoint. Important thing is we access an endpoint of
    # the browsable API and force an HTML response so that template
    # rendering is used.
    client.get("/accounts/users/", HTTP_ACCEPT="text/html")
