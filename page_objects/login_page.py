from config.playwright_config import PlaywrightConfig
from page_objects.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    BUTTON_ALLOW = {"role": "button", "name": "Allow"}
    TEXTBOX_EMAIL = {"role": "textbox", "name": "Email"}
    TEXTBOX_PASSWORD = {"role": "textbox", "name": "Password"}
    BUTTON_SUBMIT_EMAIL = "[data-test-id=\"sign-in-email-submit-button\"]"
    BUTTON_SUBMIT_PASSWORD = "[data-test-id=\"sign-in-password-submit-button\"]"

    def login(self, email: str, password: str, welcome_message: str):
        """Perform login and verify welcome message."""
        self.page.goto(PlaywrightConfig.BASE_URL)
        self.click(self.BUTTON_ALLOW)
        self.fill(self.TEXTBOX_EMAIL, email)
        self.click(self.BUTTON_SUBMIT_EMAIL)
        self.page.wait_for_timeout(10000)  # Wait for proof you're human
        self.fill(self.TEXTBOX_PASSWORD, password)
        self.click(self.BUTTON_SUBMIT_PASSWORD)
        self.page.wait_for_timeout(30000)  # Wait for auth code input and for dashboard to load
        assert self.page.locator(f"text={welcome_message}").is_visible(), "Welcome message not found"
        print("Login successful")

