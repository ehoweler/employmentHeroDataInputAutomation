from page_objects.base_page import BasePage


class EmployeesList(BasePage):
    # Locators
    BUTTON_FILTER = "//button//i[@data-test-id='filter-icon' and contains(@class, 'hero-icon-search-outlined')][1]"
    TEXTBOX_SEARCH = "//input[@placeholder='Search...']"
    LIST_VIEW_MORE = "[data-test-id=\"subTabs-employment_records-tabs-tab-view-more-sub-tab\"]"
    LIST_EMPLOYMENT_HISTORY = "//li[contains(@data-test-id, 'employment_history')]"

    def search_employee(self, employee_name: str):
        """Search for an employee by name and press Enter."""
        search_box = self.page.locator(self.TEXTBOX_SEARCH)
        search_box.fill(employee_name)
        search_box.press("Enter")

    def employee_selected_locator(self, full_name: str):
        """Return the locator for the selected employee based on full name."""
        return self.page.locator(f"//h1/div[@title='{full_name}']")

    def search_result_value_locator(self, first_name: str):
        """Return the locator for the search result based on employee name."""
        return self.page.locator(f"(//div[@id='employee_files']//span/a[text()='{first_name}'])[1]")



