import pytest
from django.contrib.auth.models import Permission
from django.test.client import Client
from freezegun import freeze_time
from rest_framework import status

from conftest import ExampleUserCreator
from jobproject.models import JobOpening


@pytest.mark.django_db
class TestJobOpeningViewSet:
    def test_rejects_anonymous_user(
        self,
        client: Client,
    ) -> None:
        response = client.get("/api/v1/job-openings/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rejects_unauthorized_user(self, client: Client, example_user_creator: ExampleUserCreator) -> None:
        user = example_user_creator()
        assert client.login(username=user.username, password="Test123!")
        response = client.get("/api/v1/job-openings/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_empty_when_db_is_empty(self, client: Client, example_user_creator: ExampleUserCreator) -> None:
        user = example_user_creator()
        user.user_permissions.add(Permission.objects.get(codename="view_jobopening"))
        assert client.login(username=user.username, password="Test123!")

        response = client.get("/api/v1/job-openings/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_returns_jobopenings(self, client: Client, example_user_creator: ExampleUserCreator) -> None:
        user = example_user_creator()
        user.user_permissions.add(Permission.objects.get(codename="view_jobopening"))
        assert client.login(username=user.username, password="Test123!")

        with freeze_time("2024-12-31"):
            job: JobOpening = JobOpening.objects.create(
                applied="2025-01-01",
                active=True,
                notes="This is my note",
                url="https://example.com",
                company="Example Company",
                title="Cool Title",
                location="Remote",
            )

        response = client.get("/api/v1/job-openings/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "active": True,
                "applied": "2025-01-01T00:00:00-05:00",
                "company": "Example Company",
                "created": "2024-12-30T19:00:00-05:00",
                "id": job.id,
                "location": "Remote",
                "notes": "This is my note",
                "title": "Cool Title",
                "url": "https://example.com",
            }
        ]

    def test_returns_only_requested_fields(self, client: Client, example_user_creator: ExampleUserCreator) -> None:
        user = example_user_creator()
        user.user_permissions.add(Permission.objects.get(codename="view_jobopening"))
        assert client.login(username=user.username, password="Test123!")

        with freeze_time("2024-12-31"):
            JobOpening.objects.create(
                applied="2025-01-01",
                active=True,
                notes="This is my note",
                url="https://example.com",
                company="Example Company",
                title="Cool Title",
                location="Remote",
            )

        response = client.get("/api/v1/job-openings/?include=company,title")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "company": "Example Company",
                "title": "Cool Title",
            }
        ]

    def test_filters_by_requested_fields(self, client: Client, example_user_creator: ExampleUserCreator) -> None:
        user = example_user_creator()
        user.user_permissions.add(Permission.objects.get(codename="view_jobopening"))
        assert client.login(username=user.username, password="Test123!")

        with freeze_time("2024-12-31"):
            active_job = JobOpening.objects.create(
                applied="2025-01-01",
                active=True,
                notes="This is my note",
                url="https://example.com",
                company="Example Company",
                title="Cool Title",
                location="Remote",
            )

            canceled_job = JobOpening.objects.create(
                applied="2024-12-31",
                active=False,
                notes="They went with another applicant",
                url="https://example.com/sour-grapes",
                company="Meh Company",
                title="Meh Title",
                location="Remote",
            )

        active_response = client.get("/api/v1/job-openings/?active=true")
        assert active_response.status_code == status.HTTP_200_OK
        assert active_response.json() == [
            {
                "active": True,
                "applied": "2025-01-01T00:00:00-05:00",
                "company": "Example Company",
                "created": "2024-12-30T19:00:00-05:00",
                "id": active_job.id,
                "location": "Remote",
                "notes": "This is my note",
                "title": "Cool Title",
                "url": "https://example.com",
            }
        ]

        inactive_response = client.get("/api/v1/job-openings/?active=false")
        assert inactive_response.status_code == status.HTTP_200_OK
        assert inactive_response.json() == [
            {
                "active": False,
                "applied": "2024-12-31T00:00:00-05:00",
                "company": "Meh Company",
                "created": "2024-12-30T19:00:00-05:00",
                "id": canceled_job.id,
                "location": "Remote",
                "notes": "They went with another applicant",
                "title": "Meh Title",
                "url": "https://example.com/sour-grapes",
            }
        ]

    def test_filters_and_returns_only_requested_fields(self, client: Client, example_user_creator: ExampleUserCreator) -> None:
        """
        Just in case django-filter and the drf-queryfields get in a fight
        """
        user = example_user_creator()
        user.user_permissions.add(Permission.objects.get(codename="view_jobopening"))
        assert client.login(username=user.username, password="Test123!")

        with freeze_time("2024-12-31"):
            JobOpening.objects.create(
                applied="2025-01-01",
                active=True,
                notes="This is my note",
                url="https://example.com",
                company="Example Company",
                title="Cool Title",
                location="Remote",
            )

            JobOpening.objects.create(
                applied="2024-12-31",
                active=False,
                notes="They went with another applicant",
                url="https://example.com/sour-grapes",
                company="Meh Company",
                title="Meh Title",
                location="Remote",
            )

        active_response = client.get("/api/v1/job-openings/?active=true&include=active,company,title")
        assert active_response.status_code == status.HTTP_200_OK
        assert active_response.json() == [
            {
                "active": True,
                "company": "Example Company",
                "title": "Cool Title",
            }
        ]

        inactive_response = client.get("/api/v1/job-openings/?active=false&include=active,company,title")
        assert inactive_response.status_code == status.HTTP_200_OK
        assert inactive_response.json() == [
            {
                "active": False,
                "company": "Meh Company",
                "title": "Meh Title",
            }
        ]
    