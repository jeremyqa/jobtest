import pytest
from django.contrib.auth.models import User

from conftest import ExampleUserCreator


def test_is_it_working():
    assert True


@pytest.mark.django_db
def test_the_db_marker(example_user_creator: ExampleUserCreator):
    """
    Basic test to make sure pytest-django and conftest work.
    """
    example_user_creator(username="SomeOtherFriend")
    example_user_creator()
    assert User.objects.count() == 2
    assert User.objects.filter(username="SomeOtherFriend").count() == 1
