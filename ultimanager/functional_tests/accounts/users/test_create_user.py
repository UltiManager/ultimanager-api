import requests


def test_register_new_user(live_server, mailoutbox):
    """
    Registering a new user should send them a verification email.
    """
    data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "SuperS3curePassword",
    }
    response = requests.post(f"{live_server}/accounts/users/", json=data)
    response.raise_for_status()

    assert response.json() == {"email": data["email"], "name": data["name"]}
    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert "Verify" in msg.subject
    assert msg.to == [data["email"]]
