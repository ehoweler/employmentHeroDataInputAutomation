from playwright.sync_api import Playwright, sync_playwright
from config.playwright_config import PlaywrightConfig
import pytest
from page_objects.login_page import LoginPage


def test_valid_login(page):
    # Create the LoginPage object
    login_page = LoginPage(page)
    login_page.login(
        email=PlaywrightConfig.AUTH_EMAIL,
        password=PlaywrightConfig.AUTH_PASSWORD,
        welcome_message=PlaywrightConfig.HOMEPAGE_WELCOME_MESSAGE
    )


