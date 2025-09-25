import pandas as pd
import os
from datetime import datetime
from config.playwright_config import PlaywrightConfig
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.employees_list_page import EmployeesList
from page_objects.employment_history_page import EmploymentHistory


def test_add_career_history(page):
    def process_employee_data(employee_data, spreadsheet_path):
        success_count = 0
        failed_records = []

        for _, row in employee_data.iterrows():
            try:
                page.reload()
                page.wait_for_timeout(2000)

                # get data from spreadsheet and assign to variables
                first_name = row['First Name']
                last_name = row['Last Name']
                full_name = f"{first_name} {last_name}"
                start_date = row['Start Date'].strftime('%d/%m/%Y')
                end_date = row['End Date'].strftime('%d/%m/%Y')
                job_title = row['Job Title']
                industry_standard_job_title = row['Industry Standard Job Title']
                employment_type = row['Employment Type']

                # Navigate to employee's profile
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
                assert employee_selected.is_visible(), f"Employee '{full_name}' not correctly selected"

                # Add employment history
                employees_list_page.click(employees_list_page.LIST_VIEW_MORE)
                employees_list_page.click(employees_list_page.LIST_EMPLOYMENT_HISTORY)
                page.wait_for_timeout(1000)
                employment_history_page.click(employment_history_page.BUTTON_ADD_EMPLOYMENT_HISTORY)

                employment_history_page.fill(employment_history_page.TEXTBOX_JOB_TITLE, job_title)
                employment_history_page.tab(employment_history_page.TEXTBOX_JOB_TITLE)
                employment_history_page.fill(employment_history_page.TEXTBOX_INDUSTRY_STANDARD_JOB_TITLE,
                                             industry_standard_job_title)
                employment_history_page.tab(employment_history_page.TEXTBOX_INDUSTRY_STANDARD_JOB_TITLE)
                employment_history_page.fill(employment_history_page.TEXTBOX_START_DATE, start_date)
                employment_history_page.click(employment_history_page.TEXTBOX_END_DATE)
                employment_history_page.fill(employment_history_page.TEXTBOX_END_DATE, end_date)
                page.locator("body").click()
                employment_history_page.click(employment_history_page.LIST_EMPLOYMENT_TYPE)
                employment_type_option = employment_history_page.option_employment_type_locator(employment_type)
                employment_type_option.click()
                page.wait_for_timeout(1000)
                employment_history_page.click(employment_history_page.BUTTON_CREATE)
                page.wait_for_timeout(5000)
                # assert success message
                success_message = page.locator(employment_history_page.MESSAGE_SUCCESS)
                assert success_message.is_visible(), "Success message not found"
                home_page.click(home_page.BUTTON_HOME)

                success_count += 1

            except Exception as e:
                failed_records.append(row)
                print(f"Failed to process record for {full_name}: {e}")

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
    employees_list_page = EmployeesList(page)
    employment_history_page = EmploymentHistory(page)
    login_page = LoginPage(page)
    login_page.login(
        email=PlaywrightConfig.AUTH_EMAIL,
        password=PlaywrightConfig.AUTH_PASSWORD,
        welcome_message=PlaywrightConfig.HOMEPAGE_WELCOME_MESSAGE
    )

    # Load employee names from the spreadsheet
    spreadsheet_path = PlaywrightConfig.EMPLOYMENT_SPREADSHEET_PATH
    employee_data = pd.read_excel(spreadsheet_path)

    # First run
    failure_file_path, failure_count = process_employee_data(employee_data, spreadsheet_path)
    print(f"First run completed. Failures: {failure_count}")

    # Re-run if there are failures
    if failure_file_path:
        print("Re-running the test with failed records...")
        failed_data = pd.read_excel(failure_file_path)
        _, re_run_failures = process_employee_data(failed_data, failure_file_path)
        print(f"Re-run completed. Remaining failures: {re_run_failures}")
