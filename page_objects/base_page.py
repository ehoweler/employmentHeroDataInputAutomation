from playwright.sync_api import Page
from playwright.sync_api import Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def visit(self, url: str):
        """Navigate to a specific URL."""
        self.page.goto(url)

    def get_element(self, locator: str):
        """Return an element handle."""
        return self.page.locator(locator)

    def press(self, locator, param):
        pass

    def tab(self, locator: str):
        """Press Tab on the specified locator."""
        resolved_locator = self.page.locator(locator)  # Resolve the string to a Locator object
        resolved_locator.press("Tab")

    def click(self, locator):
        """Click an element using a locator."""
        if isinstance(locator, dict):
            # Handle locators defined for get_by_role
            self.page.get_by_role(locator["role"], name=locator["name"]).click()
        elif isinstance(locator, str):
            # Handle standard string selectors
            self.page.locator(locator).click()
        else:
            raise ValueError("Invalid locator type. Must be a string or dictionary.")

    def fill(self, locator, text):
        """Fill an input field using a locator."""
        if isinstance(locator, dict):
            # Handle locators defined for get_by_role
            self.page.get_by_role(locator["role"], name=locator["name"]).fill(text)
        elif isinstance(locator, str):
            # Handle standard string selectors
            self.page.locator(locator).fill(text)
        else:
            raise ValueError("Invalid locator type. Must be a string or dictionary.")

    def get_text(self, locator: str) -> str:
        """Get text from an element."""
        return self.page.locator(locator).text_content()

    def goto(self, url: str):
        """Navigate to a specific URL."""
        self.page.goto(url)

    def get_by_role(self, role: str, name: str):
        """Get element by role and name."""
        return self.page.get_by_role(role, name=name)

    def locator(self, locator: str):
        """Return an element handle."""
        return self.page.locator(locator)

    def wait_for_timeout(self, timeout: int):
        """Wait for a specific timeout in milliseconds."""
        self.page.wait_for_timeout(timeout)




