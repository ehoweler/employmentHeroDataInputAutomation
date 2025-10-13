import pandas as pd
import os

from datetime import datetime
from config.playwright_config import PlaywrightConfig
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.employees_list_page import EmployeesList
from page_objects.certifications_page import Certifications


def test_add_certifications(page):
    def process_certifications(certifications_data, spreadsheet_path):
        success_count = 0
        failed_records = []

        for _, row in certifications_data.iterrows():
            try:
                page.reload()
                page.wait_for_timeout(2000)

                 # get data from spreadsheet and assign to variables
                first_name = row['First Name']
                last_name = row['Last Name']
                full_name = f"{first_name} {last_name}"
                certification_name = row['Certification Name']
                certification_type = row['Certification Type']
                assign_to = row['Assign To']
                optional_mandatory = row['Optional Mandatory']
                renewal_basis = row['Renewal Basis']

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

                # Click the MANAGE_CERTIFICATION_SETTINGS button
                page.click(certifications_page.MANAGE_CERTIFICATION_SETTINGS)

                # Wait for the new tab to open and switch to it
                new_page = page.context.wait_for_event("page")
                new_page.wait_for_load_state()

                try:
                    # Check if the certification already exists
                    search_box = new_page.get_by_role("textbox", name="Search")
                    search_box.click()
                    search_box.fill(certification_name)
                    search_box.press("Enter")
                    new_page.wait_for_timeout(5000)
                    existing_certification = new_page.get_by_role("link", name=certification_name)
                    if existing_certification.is_visible():
                        print(f"Certification '{certification_name}' already exists. Skipping...")
                        continue  # Skip to the next record if certification exists
                except Exception:
                    print(f"Certification '{certification_name}' not found. Proceeding with the test...")

                # Interact with the new tab
                new_page.get_by_role("button", name="Add certification").click()
                new_page.click(certifications_page.CERTIFICATION_NAME_INPUT)
                new_page.fill(certifications_page.CERTIFICATION_NAME_INPUT, certification_name)
                new_page.click(certifications_page.CERTIFICATION_TYPE_INPUT)
                new_page.get_by_role("option", name=f"{certification_type}").locator("div").click()
                new_page.click(certifications_page.ASSIGN_TO_INPUT)
                new_page.fill(certifications_page.ASSIGN_TO_INPUT, assign_to)
                # new_page.get_by_role("option", name=f"{assign_to}").locator("div").click()
                new_page.locator("[data-test-id=\"selected-items\"] [data-test-id=\"arrow-icon\"]").click()
                new_page.click(certifications_page.NEXT_BUTTON)
                new_page.wait_for_timeout(2000)
                # new_page.click(certifications_page.OPTIONAL_MANDATORY_INPUT)
                new_page.get_by_role("combobox", name="Is this certification").click()
                new_page.get_by_role("option", name=f"{optional_mandatory}").locator("div").click()
                # if renewal_basis == "One-off": #One-off is default so no need to select it
                    # new_page.click(certifications_page.ONE_OFF_RENEWAL)
                if renewal_basis == "Expiry date":
                    new_page.click(certifications_page.EXPIRY_DATE_RENEWAL)
                elif renewal_basis == "Renewing":
                    new_page.click(certifications_page.RENEWING_RENEWAL)
                    # need to add some additional code to do some stuff
                new_page.click(certifications_page.SAVE_BUTTON)
                new_page.get_by_role("button", name="Create").click()
                try:
                    # Check if the certification has been added
                    search_box = new_page.get_by_role("textbox", name="Search")
                    search_box.click()
                    search_box.fill(certification_name)
                    search_box.press("Enter")
                    new_page.wait_for_timeout(5000)
                    existing_certification = new_page.get_by_role("link", name=certification_name)
                    assert existing_certification.is_visible(), f"Certification '{certification_name}' not found for employee '{full_name}'"
                    success_count += 1

                except Exception as e:
                    failed_records.append(row)
                    print(f"Failed to process record for {certification_name}: {e}")

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
    employees_list_page = EmployeesList(page)
    certifications_page = Certifications(page)
    login_page = LoginPage(page)
    login_page.login(
        email=PlaywrightConfig.AUTH_EMAIL,
        password=PlaywrightConfig.AUTH_PASSWORD,
        welcome_message=PlaywrightConfig.HOMEPAGE_WELCOME_MESSAGE
    )

    # Load employee names from the spreadsheet
    spreadsheet_path = PlaywrightConfig.CERTIFICATIONS_SPREADSHEET_PATH
    certifications_data = pd.read_excel(spreadsheet_path)

    # First run
    failure_file_path, failure_count = process_certifications(certifications_data, spreadsheet_path)
    print(f"First run completed. Failures: {failure_count}")

    # Retry logic
    for attempt in range(2):  # Retry up to 2 times
        if failure_file_path:
            print(f"Retrying the test with failed records (Attempt {attempt + 2})...")
            failed_data = pd.read_excel(failure_file_path)
            failure_file_path, failure_count = process_certifications(failed_data, failure_file_path)
            print(f"Attempt {attempt + 2} completed. Failures: {failure_count}")
        else:
            break

    # Save final failures if any
    if failure_file_path:
        final_failures_path = os.path.join(
            os.path.dirname(spreadsheet_path),
            f"final_failures_certifications_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        os.rename(failure_file_path, final_failures_path)
        print(f"Final failures saved to {final_failures_path}")
