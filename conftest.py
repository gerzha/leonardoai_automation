import pytest

from base import BasePage, PagesManager


@pytest.fixture(scope="session")
def pages_manager(playwright):
    browser_type = getattr(playwright, "chromium")
    with PagesManager(browser_type) as pages:
        yield pages


@pytest.fixture()
def login_page(pages_manager, request):
    app_base_url = "https://app.leonardo.ai"

    def _page(name):
        page = pages_manager.new_page()

        base_page = BasePage(page)
        base_page.load(app_base_url)

        def delete_acc(name):
            base_page.page.get_by_label("Close AI Generations settings").click()
            base_page.page.locator("a").filter(has_text="Settings").click()
            base_page.page.get_by_role("link", name="Account Management").click()
            base_page.page.get_by_role("button", name="Delete Account").click()
            base_page.page.get_by_role("textbox").fill(name)
            base_page.page.get_by_role("button", name="Delete My Account").click()
            base_page.page.get_by_role("button", name="Sign in").wait_for(
                state="visible", timeout=6000
            )

        request.addfinalizer(lambda: delete_acc(name))
        return base_page

    return _page
