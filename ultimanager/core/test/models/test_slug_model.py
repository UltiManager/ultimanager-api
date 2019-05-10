import string
from unittest import mock

from django.utils.text import slugify

from core import models


@mock.patch("core.models.BaseModel.clean")
def test_clean_populate_slug(mock_super_clean):
    """
    Cleaning an instance with no slug should generate a new slug.
    """
    name = "foo"
    inst = models.SlugModel()
    setattr(inst, models.SlugModel.SLUG_SOURCE, name)

    slug = "foo-bar"
    with mock.patch.object(
        inst, "generate_slug", return_value=slug
    ) as mock_gen_slug:
        inst.clean()

    assert mock_super_clean.call_count == 1
    assert inst.slug == slug
    assert mock_gen_slug.call_args[0] == (name,)


@mock.patch("core.models.BaseModel.clean")
def test_clean_slug_exists(mock_super_clean):
    """
    Cleaning an instance that already has a slug should not replace the
    slug.
    """
    name = "foo"
    slug = "bar-baz"
    inst = models.SlugModel(slug=slug)
    setattr(inst, models.SlugModel.SLUG_SOURCE, name)

    new_slug = "foo-bar"
    with mock.patch.object(
        inst, "generate_slug", return_value=new_slug
    ) as mock_gen_slug:
        inst.clean()

    assert mock_super_clean.call_count == 1
    assert inst.slug == slug
    assert mock_gen_slug.call_count == 0


@mock.patch("core.models.get_random_string")
def test_generate_slug(mock_random_string):
    """
    Generating a slug should return the provided string with a random
    suffix appended.
    """
    suffix = "a" * models.SlugModel.SLUG_ID_LENGTH
    mock_random_string.return_value = suffix

    name = "Foo Bar"
    expected = f"{slugify(name)}-{suffix}"

    slug = models.SlugModel.generate_slug(name)

    assert slug == expected
    assert mock_random_string.call_args[1] == {
        "allowed_chars": string.ascii_lowercase,
        "length": models.SlugModel.SLUG_ID_LENGTH,
    }


@mock.patch("core.models.get_random_string")
def test_generate_slug_long_name(mock_random_string):
    """
    Generating a slug should return the provided string with a random
    suffix appended.
    """
    suffix = "a" * models.SlugModel.SLUG_ID_LENGTH
    mock_random_string.return_value = suffix

    name = "Foo Bar " * models.SlugModel.SLUG_TEXT_LENGTH
    expected = f"{slugify(name)[:models.SlugModel.SLUG_TEXT_LENGTH]}-{suffix}"

    slug = models.SlugModel.generate_slug(name)

    assert slug == expected
    assert mock_random_string.call_args[1] == {
        "allowed_chars": string.ascii_lowercase,
        "length": models.SlugModel.SLUG_ID_LENGTH,
    }
