class PlaywrightConfig:
    BASE_URL = "https://secure.employmenthero.com/users/sign_in"
    TIMEOUT = 30000  # Timeout in milliseconds
    HEADLESS = False  # Set to True to run in headless mode
    VIEWPORT = {"width": 1280, "height": 720}  # Default viewport size
    AUTH_EMAIL = "elske.howeler@outlook.com"
    AUTH_PASSWORD = "EHAutomation1"
    BROWSER = "chromium"  # Browser to use
    RETRY_COUNT = 2  # Number of retries for failed tests
    SCREENSHOT_ON_FAILURE = True  # Capture screenshots on failure
    ENABLE_TRACING = True  # Enable tracing for debugging
    ENV = "staging"  # Environment setting
    NETWORK_TIMEOUT = 10000  # Network request timeout in milliseconds
    HOMEPAGE_WELCOME_MESSAGE = "Welcome Elske"  # Expected welcome message after login
    EMPLOYMENT_SPREADSHEET_PATH = r"C:\Users\elske\PycharmProjects\employmentHeroDataInputAutomation\employment_history.xlsx"
    SALARY_SPREADSHEET_PATH = r"C:\Users\elske\PycharmProjects\employmentHeroDataInputAutomation\salary_history.xlsx"