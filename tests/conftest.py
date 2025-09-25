import pytest
from playwright.sync_api import sync_playwright
from config.playwright_config import PlaywrightConfig


@pytest.fixture(scope="function")
def page():
    print(f"Headless mode: {PlaywrightConfig.HEADLESS}")  # Debugging
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Force non-headless mode
        context = browser.new_context(viewport=PlaywrightConfig.VIEWPORT)
        page = context.new_page()
        yield page
        browser.close()