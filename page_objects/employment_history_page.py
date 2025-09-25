from page_objects.base_page import BasePage


class EmploymentHistory(BasePage):
    BUTTON_ADD_EMPLOYMENT_HISTORY = "//button[normalize-space(text()) = 'Add employment history']"
    TEXTBOX_JOB_TITLE = "//input[@placeholder='Type here to search for job titles']"
    TEXTBOX_INDUSTRY_STANDARD_JOB_TITLE = "//input[@placeholder='Type here to search for standard job titles']"
    TEXTBOX_START_DATE = {"role": "textbox", "name": "Start date"}
    TEXTBOX_END_DATE = {"role": "textbox", "name": "End date"}
    LIST_EMPLOYMENT_TYPE = {"role": "combobox", "name": "Employment type (Optional)"}
    BUTTON_CREATE = "//button[text()='Create']"
    MESSAGE_SUCCESS = "(//div[text()='Create Employment History successfully!'])[1]"

    def option_employment_type_locator(self, employment_type: str):
        """Return the locator for the search result based on employee name."""
        return self.page.locator(f"//div[text()='{employment_type}']")
