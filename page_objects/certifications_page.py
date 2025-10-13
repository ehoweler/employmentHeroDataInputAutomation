from page_objects.base_page import BasePage

class Certifications(BasePage):
    # Locators
    MANAGE_CERTIFICATION_SETTINGS= "//button[normalize-space(text())='Manage certification settings']"
    ADD_CERTIFICATION = "//button[normalize-space(text()) = 'Add certification']"
    CERTIFICATION_NAME_INPUT = "//input[@name='certificationName']"
    CERTIFICATION_TYPE_INPUT = "//input[@id='hero-theme-select-input__CREATE_CERTIFICATION_FORM__certificationCategory']"
    ASSIGN_TO_INPUT = "//input[@name='assigneesList']"
    NEXT_BUTTON = "//button[normalize-space(text())='Next']"
    OPTIONAL_MANDATORY_INPUT = "//input[@id='hero-theme-select-input__CREATE_CERTIFICATION_FORM__assigneesRequired']"
    ONE_OFF_RENEWAL = "//span[text()='One-off']"
    EXPIRY_DATE_RENEWAL = "//span[text()='Expiry date']"
    RENEWING_RENEWAL = "//span[text()='Renewing']"
    SAVE_BUTTON = "//button[normalize-space(text())='Save']"
    SEARCH_CERTIFICATIONS = "//input[@placeholder='Search']"


    def option_certification_name_locator(self, option: str):
        """Return the locator for the search result based on certification name."""
        return self.page.locator(f"//td/a[text()='{option}']")

    def search_certification(self, certification_name: str):
        """Search for an employee by name and press Enter."""
        search_box = self.page.locator(self.SEARCH_CERTIFICATIONS)
        search_box.click()
        search_box.fill(certification_name)
        search_box.press("Enter")