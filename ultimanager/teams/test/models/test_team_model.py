from teams import models


def test_repr():
    """
    The representation of a team should include all the information
    required to find the team again for debugging purposes.
    """
    team = models.Team(name="Team", slug="foo")
    expected = (
        f"<teams.Team: id={repr(team.pk)} name={repr(team.name)} "
        f"slug={repr(team.slug)}>"
    )

    assert repr(team) == expected


def test_str():
    """
    Converting a team to a string should return the team's name.
    """
    team = models.Team(name="Team 1")

    assert str(team) == team.name
