from django.contrib.auth.models import Permission
from playwright.sync_api import Page, expect
from pytest_django.live_server_helper import LiveServer

from jobproject.conftest import ExampleUserCreator


def test_hello_world_pw(page: Page, live_server: LiveServer, example_user_creator: ExampleUserCreator) -> None:
    admin_user = example_user_creator(is_staff=True)
    admin_user.user_permissions.add(Permission.objects.get(codename="view_jobopening"))
    page.goto(f"{live_server.url}/admin/")
    page.get_by_label("Username").fill(admin_user.username)
    page.get_by_label("Password").fill("Test123!")
    page.get_by_role("button", name="Log in").click()
    page.get_by_role("link", name="Job openings").click()
    expect(page.get_by_text("0 job openings")).to_be_visible()
