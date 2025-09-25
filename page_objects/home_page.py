from page_objects.base_page import BasePage


class HomePage(BasePage):
    # Locators
    ICON_PEOPLE = "[data-test-id=\"primary-item-icon-wrapper-people\"]"
    LINK_EMPLOYEES_LIST = {"role": "link", "name": "Employees List"}
    BUTTON_HOME = "//span[text()='Home']"
