from typing import Protocol

import pytest
from django.contrib.auth.models import User


class ExampleUserCreator(Protocol):
    def __call__(
        self,
        username: str = "TestFriend",
        password: str = "Test123!",
        firstname: str = "Test123!",
        lastname: str = "Tes",
        email: str = "test@example.com",
        is_staff: bool = False,
        is_active: bool = True,
        date_joined: str = "2024-12-31",
    ) -> User:
        pass


@pytest.fixture
def example_user_creator() -> ExampleUserCreator:
    def _inner_example_user_creator(
        username: str = "TestFriend",
        password: str = "Test123!",
        firstname: str = "Firs",
        lastname: str = "Tes",
        email: str = "test@example.com",
        is_staff: bool = False,
        is_active: bool = True,
        date_joined: str = "2024-12-31",
    ) -> User:
        return User.objects.create_user(
            username=username,
            password=password,
            first_name=firstname,
            last_name=lastname,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            date_joined=date_joined,
        )

    return _inner_example_user_creator
