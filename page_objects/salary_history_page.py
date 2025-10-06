from page_objects.base_page import BasePage


class SalaryHistory(BasePage):
    # Locators
    ADD_SALARY = "//button[normalize-space(text()) = 'Add salary']"
    EFFECTIVE_FROM = "(//input[@placeholder='Select date'])[1]"
    CONTINUOUS_EMPLOYMENT_DATE = "(//input[@placeholder='Select date'])[2]"
    SALARY = "//input[@value='not_hour']"
    HOURLY_PAY = "//input[@value='hour']"
    ZERO_HOUR = "//span[text()='This employee is a zero-hour based employee']"
    PAY_RATE = "(//input[@placeholder='Input salary'])[1]"
    PAY_FREQUENCY = "(//div/i[@data-test-id='arrow-icon'])[2]" # if zer-hour is yes
    PAY_FREQUENCY_1 = "(//div/input[@name='salary_type']/following-sibling::div)[1]"
    PAY_FREQUENCY_2 = "(//div/input[@name='salary_type']/following-sibling::div)[2]"
    PAY_FREQUENCY_1_MONTH = "//li[@id='downshift-:rb:-item-1']/div"
    PAY_FREQUENCY_1_FORTNIGHT = "//li[@id='downshift-:rb:-item-2']/div"
    PAY_FREQUENCY_1_DAY = "//li[@id='downshift-:rb:-item-3']/div"
    PAY_FREQUENCY_2_MONTH = "//input[@aria-activedescendant='downshift-:rd:-item-1']"
    PAY_FREQUENCY_2_FORTNIGHT = "//input[@aria-activedescendant='downshift-:rd:-item-1']"
    PAY_FREQUENCY_2_DAY = "//input[@aria-activedescendant='downshift-:rd:-item-1']"
    ACTUAL_WEEKLY_HOURS = "//input[@name='hours_per_week']"
    ACTUAL_DAYS_PER_WEEK = "//input[@name='days_per_week']"
    FTE_WEEKLY_HOURS = "//input[@name='full_time_equivalent_units']"
    EFFECTIVE_PAY_RATE = "//input[@name='effective_salary']"
    PAID_IRREGULARLY = "//input[@name='employee_paid_irregularly']/following-sibling::span"
    ROLLED_UP_HOLIDAY_PAY = "//input[@name='apply_rolled_up_holiday_pay']/following-sibling::span"
    PAY_CATEGORY = "//input[@id='hero-theme-select-input__undefined__pay_category_id']"
    PAY_SCHEDULE = "//span[text()='Pay schedule']/parent::label/parent::div/parent::div/following-sibling::div/div/div"
    NMW_NLW_ELIGIBILITY = "//span[text()='NMW / NLW Eligibility']/parent::label/parent::div/parent::div/following-sibling::div/div/div"
    APPRENTICE = "//span[text()='Apprentice']/parent::label/parent::div/parent::div/following-sibling::div/div/div"
    REASON_FOR_CHANGE = "//span[text()='Reason for change']/parent::label/parent::div/parent::div/following-sibling::div/div/div"
    COMMENTS = "//textarea[@name='comments']"
    SAVE = "//button[text()='Save']"
    SAVED_MESSAGE = "//div[text()='Update successfully ']"
    # SAVED_MESSAGE = "//div[contains(normalize-space(), 'Success')]"
    SALARY_EXPAND_BUTTON = "//button[@data-test-id='salaryHistoriesExpandButton']"
    VIEW_ALL_BUTTON = "//button[@data-test-id='view-all-salaries-button']"



    def option_salary_history_locator(self, option: str):
        """Return the locator for the search result based on employee name."""
        return self.page.locator(f"//li/div[text()='{option}']")

    def option_pay_frequency_1_locator(self, option: str): # use this one when the option is not Annum
        """Return the locator for the search result based on employee name."""
        return self.page.locator(f"(//div[text()='{option}'])[1]")

    def option_pay_frequency_2_locator(self, option: str): # use this one when the option is Annum
        """Return the locator for the search result based on employee name."""
        return self.page.locator(f"(//div[text()='{option}'])[1]")




