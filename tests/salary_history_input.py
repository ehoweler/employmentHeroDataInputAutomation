import pandas as pd
import os
from datetime import datetime

from config.playwright_config import PlaywrightConfig
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.employees_list_page import EmployeesList
from page_objects.salary_history_page import SalaryHistory


def test_add_salary_history(page):
    def process_salary_data(salary_data, spreadsheet_path):
        success_count = 0
        failed_records = []

        for _, row in salary_data.iterrows():
            try:
                page.reload()
                page.wait_for_timeout(2000)

                # get data from spreadsheet and assign to variables
                first_name = row['First Name']  # mandatory field
                last_name = row['Last Name']  # mandatory field
                full_name = f"{first_name} {last_name}"
                effective_from = row['Effective from'].strftime('%d/%m/%Y')
                continuous_employment_date = row.get('Continuous employment date', None)
                continuous_employment_date = continuous_employment_date.strftime('%d/%m/%Y') if pd.notna(
                    continuous_employment_date) else ''
                pay_rates = row['Pay rates']
                zero_hour = str(row.get('zero-hour', '')).strip().lower() if pd.notna(row.get('zero-hour', '')) else ''
                pay_frequency = row.get('Pay frequency', '').strip().capitalize() if pd.notna(
                    row.get('Pay frequency', '')) else ''
                actual_weekly_hours = str(row['Actual weekly hours'])
                fte_weekly_hours = str(row['Full-time equivalent weekly hours'])
                effective_pay_rate = str(row['Effective pay rate'])
                fte_weekly_hours = str(row.get('Full-time equivalent weekly hours', '')).strip().lower() if pd.notna(
                    row.get('Full-time equivalent weekly hours', '')) else ''
                effective_pay_rate = str(row['Effective pay rate'])
                pay_frequency_2 = row.get('Pay frequency 2', '').strip().capitalize() if pd.notna(
                    row.get('Pay frequency 2', '')) else ''
                paid_irregularly = str(row.get('Employee is paid irregularly', '')).strip().lower() if pd.notna(
                    row.get('Employee is paid irregularly', '')) else ''
                rolled_up_holiday_pay = str(row.get('Apply rolled up holiday pay', '')).strip().lower() if pd.notna(
                    row.get('Apply rolled up holiday pay', '')) else ''
                pay_category = row['Pay category']
                pay_schedule = row['Pay schedule']
                nmw_nlw_eligibility = row['NMW/NLW eligibility']
                apprentice = row['Apprentice']
                reason_for_change = row['Reason for change']
                comments = row.get('Comments', '').strip().lower() if pd.notna(row.get('Comments', '')) else ''

                page.reload()
                page.wait_for_timeout(5000)
                home_page.click(home_page.ICON_PEOPLE)
                home_page.click(home_page.LINK_EMPLOYEES_LIST)
                employees_list_page.click(employees_list_page.BUTTON_FILTER)
                employees_list_page.search_employee(full_name)
                page.wait_for_timeout(1000)
                search_result_value = employees_list_page.search_result_value_locator(first_name)
                search_result_value.click()
                page.wait_for_timeout(1000)
                employee_selected = employees_list_page.employee_selected_locator(full_name)
                page.wait_for_timeout(5000)
                if not employee_selected.is_visible():
                    # Attempt to click or perform an action to make the element visible
                    page.click(employees_list_page.BUTTON_FILTER)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(2000)  # Wait for the element to appear
                assert employee_selected.is_visible(), f"Employee '{full_name}' not correctly selected"

                salary_history_page.click(salary_history_page.ADD_SALARY)

                salary_history_page.fill(salary_history_page.EFFECTIVE_FROM, effective_from)
                salary_history_page.click(salary_history_page.CONTINUOUS_EMPLOYMENT_DATE)
                page.locator("body").click()  # Click outside to close date picker
                salary_history_page.fill(salary_history_page.CONTINUOUS_EMPLOYMENT_DATE, continuous_employment_date)
                page.locator("body").click()  # Click outside to close date picker

                if pay_rates == 'Salary':
                    salary_history_page.click(salary_history_page.SALARY)
                if pay_rates == 'Hourly Pay':
                    salary_history_page.click(salary_history_page.HOURLY_PAY)

                if zero_hour.lower() == 'yes':
                    salary_history_page.click(salary_history_page.ZERO_HOUR)
                    salary_history_page.click(salary_history_page.EFFECTIVE_PAY_RATE)
                    salary_history_page.fill(salary_history_page.EFFECTIVE_PAY_RATE, effective_pay_rate)
                    if pay_frequency != '':
                        salary_history_page.click(salary_history_page.PAY_FREQUENCY)
                        page.wait_for_timeout(2000)
                        if pay_frequency != 'Annum': # if it is annum you don't have to do anything as it is already selected
                            if pay_frequency == 'Month':
                                page.get_by_role("option", name="Month").locator("div").click()
                            if pay_frequency == 'Fortnight':
                                page.get_by_role("option", name="Fortnight").locator("div").click()
                            if pay_frequency == 'Day':
                                page.get_by_role("option", name="Day").locator("div").click()

                if pay_rates == 'Hourly Pay':
                    salary_history_page.click(salary_history_page.EFFECTIVE_PAY_RATE)
                    salary_history_page.fill(salary_history_page.EFFECTIVE_PAY_RATE, effective_pay_rate)

                else:
                    salary_history_page.click(salary_history_page.ACTUAL_WEEKLY_HOURS)
                    salary_history_page.fill(salary_history_page.ACTUAL_WEEKLY_HOURS, actual_weekly_hours)
                    salary_history_page.fill(salary_history_page.FTE_WEEKLY_HOURS, fte_weekly_hours)
                    salary_history_page.click(salary_history_page.EFFECTIVE_PAY_RATE)
                    salary_history_page.fill(salary_history_page.EFFECTIVE_PAY_RATE, effective_pay_rate)
                    if pay_frequency_2 != '':
                        salary_history_page.click(salary_history_page.PAY_FREQUENCY_2)
                        page.wait_for_timeout(2000)
                        if pay_frequency_2 != 'Annum':  # if it is annum you don't have to do anything as it is already selected
                            if pay_frequency_2 == 'Month':
                                page.get_by_role("option", name="Month").locator("div").click()
                            if pay_frequency_2 == 'Fortnight':
                                page.get_by_role("option", name="Fortnight").locator("div").click()
                            if pay_frequency_2 == 'Day':
                                page.get_by_role("option", name="Day").locator("div").click()
                                salary_history_page.click(salary_history_page.ACTUAL_DAYS_PER_WEEK)
                                salary_history_page.fill(salary_history_page.ACTUAL_DAYS_PER_WEEK, actual_weekly_hours)

                if str(paid_irregularly).strip().lower() == 'yes':
                    salary_history_page.click(salary_history_page.PAID_IRREGULARLY)
                    if str(rolled_up_holiday_pay).strip().lower() == 'yes':
                        salary_history_page.click(salary_history_page.ROLLED_UP_HOLIDAY_PAY)

                salary_history_page.click(salary_history_page.PAY_CATEGORY)
                pay_category_option = salary_history_page.option_salary_history_locator(pay_category)
                pay_category_option.click()
                salary_history_page.click(salary_history_page.PAY_SCHEDULE)
                pay_schedule_option = salary_history_page.option_salary_history_locator(pay_schedule)
                pay_schedule_option.click()
                salary_history_page.click(salary_history_page.NMW_NLW_ELIGIBILITY)
                nmw_nlw_eligibility_option = salary_history_page.option_salary_history_locator(nmw_nlw_eligibility)
                nmw_nlw_eligibility_option.click()
                salary_history_page.click(salary_history_page.APPRENTICE)
                apprentice_option = salary_history_page.option_salary_history_locator(apprentice)
                apprentice_option.click()
                salary_history_page.click(salary_history_page.REASON_FOR_CHANGE)
                reason_for_change_option = salary_history_page.option_salary_history_locator(reason_for_change)
                reason_for_change_option.click()
                # enter any comments from spreadsheet
                salary_history_page.fill(salary_history_page.COMMENTS, comments)
                # save the salary record
                salary_history_page.click(salary_history_page.SAVE)
                # check to see the toast message for Success appears (with a timeout built in), if it doesn't it should go to rerun
                try:
                    page.wait_for_selector(
                        "xpath=//div[contains(text(), 'Success')]",
                        timeout=5000)
                    print("Toast appeared!")
                except:
                    print("Toast message not found.")
                home_page.click(home_page.BUTTON_HOME)

                success_count += 1

            except Exception as e:
                failed_records.append(row)
                print(f"Failed to process record: {e}")

        if failed_records:
            failures_df = pd.DataFrame(failed_records)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            failure_file_path = os.path.join(
                os.path.dirname(spreadsheet_path),
                f"failures_{timestamp}.xlsx"
            )
            failures_df.to_excel(failure_file_path, index=False)
            print(f"Failed records saved to {failure_file_path}")
            return failure_file_path, len(failed_records)

        return None, 0

    # Create the HomePage object
    home_page = HomePage(page)
    # Create the EmployeesList object
    employees_list_page = EmployeesList(page)
    # Create the SalaryHistory object
    salary_history_page = SalaryHistory(page)
    # Create the LoginPage object
    login_page = LoginPage(page)
    login_page.login(
        email=PlaywrightConfig.AUTH_EMAIL,
        password=PlaywrightConfig.AUTH_PASSWORD,
        welcome_message=PlaywrightConfig.HOMEPAGE_WELCOME_MESSAGE
    )

    # Load employee names from the spreadsheet
    spreadsheet_path = PlaywrightConfig.SALARY_SPREADSHEET_PATH
    salary_data = pd.read_excel(spreadsheet_path)  # Use pandas to read the spreadsheet

    # First run
    failure_file_path, failure_count = process_salary_data(salary_data, spreadsheet_path)
    print(f"First run completed. Failures: {failure_count}")

    # Retry logic
    for attempt in range(2):  # Retry up to 2 times
        if failure_file_path:
            print(f"Retrying the test with failed records (Attempt {attempt + 2})...")
            failed_data = pd.read_excel(failure_file_path)
            failure_file_path, failure_count = process_salary_data(failed_data, failure_file_path)
            print(f"Attempt {attempt + 2} completed. Failures: {failure_count}")
        else:
            break

    # Save final failures if any
    if failure_file_path:
        final_failures_path = os.path.join(
            os.path.dirname(spreadsheet_path),
            f"final_failures_salary_history_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        os.rename(failure_file_path, final_failures_path)
        print(f"Final failures saved to {final_failures_path}")
