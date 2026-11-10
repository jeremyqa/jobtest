import pytest
from django.contrib.auth.models import User
from django.test.client import Client
from rest_framework import status  # type: ignore

from jobproject.conftest import ExampleUserCreator


def test_is_it_working() -> None:
    assert True


@pytest.mark.django_db
def test_the_db_marker(example_user_creator: ExampleUserCreator) -> None:
    """
    Basic test to make sure pytest-django and conftest work.
    """
    example_user_creator(username="SomeOtherFriend")
    example_user_creator()
    assert User.objects.count() == 2
    assert User.objects.filter(username="SomeOtherFriend").count() == 1


@pytest.mark.django_db
def test_manual_login(
    example_user_creator: ExampleUserCreator,
    client: Client,
) -> None:
    this_user = example_user_creator(username="this_user", password="Test123!")

    example_user_creator(username="other_user", password="Nope123!")

    res = client.post(
        path="/api/token/",
        data={"username": this_user.username, "password": "Test123!"},
        content_type="application/json",
    )
    assert res.status_code == status.HTTP_200_OK
    json_res = res.json()
    assert json_res["access"]
    assert json_res["refresh"]
