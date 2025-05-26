# https://www.virustotal.com/gui/file/8dc1415cbb828fc5198d370fff00f30012439be772d776f407a7217bc217b27f?nocache=1

import os
import sys 
import time
import random
import logging
import argparse
import getpass
from colorama import init, Fore, Style
from pyfiglet import Figlet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize colorama
init()

# Custom formatter for colored logging
class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages"""
    
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        # Add color to the level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

# Set up logging with colors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_bot.log', mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Apply colored formatter to console handler
console_handler = logging.getLogger().handlers[1]
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add colored print functions
def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

def print_highlight(message):
    print(f"{Style.BRIGHT}{message}{Style.RESET_ALL}")

class LinkedInConnector:
    # Define some common XPaths as constants for clarity, though many are method-specific
    LOGIN_EMAIL_ID = 'username'
    LOGIN_PASSWORD_ID = 'password'
    LOGIN_BUTTON_XPATH = '//button[contains(text(), "Sign in") or contains(text(), "Oturum aç")]|//button[@type="submit"]'
    TWO_FA_INPUT_XPATH = '//input[@id="input__email_verification_pin" or @id="verification-code"]'
    SEARCH_RESULTS_CONNECT_BUTTON_XPATH = '//button[.//span[text()="Bağlantı kur" or text()="Connect"]]'
    MODAL_ADD_NOTE_BUTTON_XPATH = '//button[contains(@aria-label, "Add a note") or contains(@aria-label, "Not ekle")] | //button[.//span[text()="Not ekle" or text()="Add a note"]]'
    MODAL_CUSTOM_MESSAGE_ID = 'custom-message'
    MODAL_SEND_BUTTON_XPATH = '//button[contains(@aria-label, "Send invitation") or contains(@aria-label, "Send now") or contains(@aria-label, "Send") or contains(@aria-label, "Gönder")] | //button[.//span[text()="Gönder" or text()="Send"]]'

    def __init__(self, headless=False, connection_note=None, use_notes=False):
        """Initialize the LinkedIn connector
        
        Args:
            headless (bool): Run browser in headless mode
            connection_note (str, optional): Custom connection note to include with requests
            use_notes (bool): Whether to send connection requests with notes (default: False)
        """
        self.use_notes = use_notes
        
        # Validate connection note if provided
        if connection_note and use_notes:
            if len(connection_note) > 300:
                print_warning("Connection note is too long. It will be truncated to 300 characters.")
                connection_note = connection_note[:300]
            self.connection_note = connection_note
        else:
            self.connection_note = None
        
        self._limit_reported = False
        self.driver = None
        self.wait = None
        self.short_wait = None
        self.email = None
        self.password = None
        self.headless = headless

    def initialize_browser(self):
        """Initialize the browser after user chooses login method"""
        self.driver = self.setup_driver(self.headless)
        self.wait = WebDriverWait(self.driver, 20)
        self.short_wait = WebDriverWait(self.driver, 5)

    def setup_login(self):
        """Setup login method and credentials"""
        # Ask user for login preference
        while True:
            login_choice = input("How would you like to login?\n1. Enter credentials in console\n2. Login through browser\nEnter your choice (1 or 2): ").strip()
            if login_choice in ['1', '2']:
                break
            print_warning("Please enter either 1 or 2")
        
        if login_choice == '1':
            # Get credentials from console
            while True:
                self.email = input("Enter your LinkedIn email: ").strip()
                if not self.email:
                    print_warning("Email cannot be empty. Please try again.")
                    continue
                if '@' not in self.email or '.' not in self.email:
                    print_warning("Please enter a valid email address.")
                    continue
                break

            while True:
                self.password = getpass.getpass("Enter your LinkedIn password: ").strip()
                if not self.password:
                    print_warning("Password cannot be empty. Please try again.")
                    continue
                if len(self.password) < 6:
                    print_warning("Password must be at least 6 characters long.")
                    continue
                break

            if not all([self.email, self.password]):
                logging.error("Email and password fields cannot be empty.")
                raise ValueError("Missing LinkedIn credentials.")
            
            # Initialize browser after getting credentials
            self.initialize_browser()
        else:
            # Initialize browser first for manual login
            self.initialize_browser()
            print_info("Opening LinkedIn login page. Please login manually in the browser.")
            self.driver.get("https://www.linkedin.com/login")
            self.email = None
            self.password = None

    def setup_driver(self, headless_mode):
        """Set up the Chrome WebDriver with cross-platform compatibility"""
        chrome_options = Options()
        
        # Configure headless mode if requested
        if headless_mode:
            logging.info("Browser will run in background (headless mode).")
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-gpu')
        else:
            logging.info("Browser will run in visible mode. (Tip: You can run in background using --headless argument)")
        
        # Common settings for all operating systems
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Try different methods to initialize the WebDriver
        attempts = [
            self._init_webdriver_with_auto_install,
            self._init_webdriver_from_path,
            self._init_webdriver_direct
        ]
        
        last_error = None
        for attempt in attempts:
            try:
                driver = attempt(chrome_options)
                if driver:
                    # Additional configurations after driver initialization
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    return driver
            except Exception as e:
                last_error = e
                logging.warning(f"WebDriver initialization attempt failed: {str(e)}")
        
        raise Exception(f"All WebDriver initialization methods failed. Last error: {str(last_error)}")
    
    def _init_webdriver_with_auto_install(self, chrome_options):
        """Initialize WebDriver with automatic ChromeDriver installation"""
        try:
            # Initialize ChromeDriverManager with default settings
            driver_manager = ChromeDriverManager()
            driver_path = driver_manager.install()
            
            # On Mac, the actual chromedriver binary is inside a versioned directory
            if sys.platform == 'darwin' and '/chromedriver-mac-' in driver_path:
                # Find the actual chromedriver binary
                chromedriver_dir = os.path.dirname(driver_path)
                chromedriver_bin = os.path.join(chromedriver_dir, 'chromedriver')
                if os.path.exists(chromedriver_bin):
                    driver_path = chromedriver_bin
            
            # Set execution permissions (for Unix systems)
            if os.name != 'nt':
                os.chmod(driver_path, 0o755)
            
            # Create service with the correct binary path
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set a reasonable window size for headless mode
            if '--headless=new' in chrome_options.arguments:
                driver.set_window_size(1920, 1080)
                
            return driver
            
        except Exception as e:
            logging.warning(f"Auto-install method failed: {str(e)}")
            logging.warning(f"Driver path attempted: {driver_path}" if 'driver_path' in locals() else "")
            return None
    
    def _init_webdriver_from_path(self, chrome_options):
        """Initialize WebDriver using ChromeDriver from system PATH"""
        try:
            service = Service()
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            logging.warning(f"System PATH method failed: {str(e)}")
            return None
    
    def _init_webdriver_direct(self, chrome_options):
        """Last resort: Try direct initialization without service"""
        try:
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            logging.warning(f"Direct initialization failed: {str(e)}")
            return None

    def _is_logged_in(self):
        """Checks if the user is currently logged in by looking for feed indicators."""
        current_url = self.driver.current_url
        return any(x in current_url for x in ["/feed", "/dashboard", "/mynetwork", "/jobs", "/messaging", "/notifications", "ana-sayfa", "akis"])


    def wait_for_2fa(self, max_wait_minutes=15):
        """Wait for user to complete 2FA verification"""
        logging.info("2FA verification required. Please check your authentication app or email...")
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60

        while time.time() - start_time < max_wait_seconds:
            if self._is_logged_in():
                logging.info("2FA verification successful!")
                return True

            try:
                verification_input_elements = self.driver.find_elements(By.XPATH, self.TWO_FA_INPUT_XPATH)
                if verification_input_elements and verification_input_elements[0].is_displayed():
                    logging.info("Please enter your verification code in the browser and press 'Submit' or 'Verify'...")
            except NoSuchElementException:
                pass
            except Exception as e:
                logging.debug(f"Error checking 2FA input: {str(e)}")

            time.sleep(5)

        logging.error("2FA verification timed out or could not be completed.")
        return False

    def login(self):
        """Login to LinkedIn with manual security check and 2FA handling"""
        try:
            if self.email and self.password:
                # Console login
                print_info("\n=== ATTENTION ===")
                print_info("Starting login process. Please be ready to complete any security checks.")
                self.driver.get("https://www.linkedin.com/login")
                time.sleep(2)
                
                # Enter email
                email_field = self.wait.until(EC.presence_of_element_located((By.ID, self.LOGIN_EMAIL_ID)))
                email_field.clear()
                email_field.send_keys(self.email)
                
                # Enter password
                password_field = self.wait.until(EC.presence_of_element_located((By.ID, self.LOGIN_PASSWORD_ID)))
                password_field.clear()
                password_field.send_keys(self.password)
                
                # Click login button
                login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.LOGIN_BUTTON_XPATH)))
                login_button.click()

                # Check for security check or 2FA
                security_check_phrases = [
                    "checkpoint/challenge", 
                    "security/challenge",
                    "checkpoint/"
                ]
                
                if any(phrase in self.driver.current_url for phrase in security_check_phrases) or \
                   self.driver.find_elements(By.XPATH, self.TWO_FA_INPUT_XPATH):
                    
                    print_info("\n=== SECURITY CHECK OR 2FA REQUIRED ===")
                    print_info("Please complete the security check or 2FA verification in the browser.")
                    print_info("1. Complete any security checks (CAPTCHA, email verification, etc.)")
                    print_info("2. If prompted for 2FA, enter the code from your authenticator app or email")
                    print_info("3. Wait until you are fully logged in to LinkedIn")
                    print_info("4. The bot will continue automatically once verification is complete")
                    print_info("Time limit: 5 minutes\n")
                    
                    # Wait for user to complete the verification
                    max_wait_minutes = 5
                    start_time = time.time()
                    
                    while time.time() - start_time < (max_wait_minutes * 60):
                        if self._is_logged_in():
                            print_success("\nSecurity check completed successfully!")
                            return True
                        time.sleep(5)
                    
                    print_warning("\nSecurity check timed out. Please try again.")
                    return False
                
                # Check for login errors
                error_messages = {
                    "error-for-password": "Incorrect password. Please try again.",
                    "error-for-username": "Invalid email address. Please try again."
                }

                for error_id, error_message in error_messages.items():
                    try:
                        error_element = self.driver.find_element(By.ID, error_id)
                        if error_element.is_displayed():
                            print_error(f"\n{error_message}")
                            return False
                    except NoSuchElementException:
                        continue

                # If we're logged in, return success
                if self._is_logged_in():
                    print_success("\nLogin successful!")
                    return True

            else:
                # Browser login - wait for user to login manually
                print_info("\n=== MANUAL LOGIN REQUIRED ===")
                print_info("Please login to LinkedIn in the browser that just opened.")
                print_info("1. Enter your credentials")
                print_info("2. Complete any security checks or 2FA verification")
                print_info("3. The bot will continue automatically once you're logged in")
                print_info("Time limit: 5 minutes\n")
                
                self.driver.get("https://www.linkedin.com/login")
                
                # Wait for user to complete login
                max_wait_minutes = 5
                start_time = time.time()
                
                while time.time() - start_time < (max_wait_minutes * 60):
                    if self._is_logged_in():
                        print_success("\nLogin successful!")
                        return True
                    time.sleep(5)
                
                print_warning("\nLogin timed out. Please try again.")
                return False

            print_error("\nLogin failed for unknown reason.")
            return False

        except Exception as e:
            print_error(f"\nLogin failed: {str(e)}")
            logging.error(f"Login error: {str(e)}")
            return False

    def send_connection_request_on_profile_page(self, profile_url, message=None):
        """Send a connection request from a specific profile page
        
        Args:
            profile_url (str): URL of the profile to connect with
            message (str, optional): Custom message to include with the connection request
        """
        try:
            logging.info(f"Navigating to profile: {profile_url}")
            self.driver.get(profile_url)
            time.sleep(random.uniform(3, 6))

            connect_button_xpath = (
                '//div[contains(@class, "pvs-profile-actions")]//button[.//span[text()="Connect" or text()="Bağlantı kur"]] | '
                '//button[contains(@class, "artdeco-button--primary") and (.//span[text()="Connect"] or .//span[text()="Bağlantı kur"])]'
            )
            connect_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, connect_button_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
            time.sleep(0.5)
            connect_button.click()
            logging.info("Connect button clicked on profile page.")
            time.sleep(random.uniform(1, 3))

            # Only pass the message if notes are enabled
            custom_message = message if self.use_notes else None
            self._handle_connection_modal(custom_message=custom_message)

            logging.info(f"Connection request sent (profile page): {profile_url}")
            time.sleep(random.uniform(2, 4))
            return True

        except TimeoutException:
            logging.warning(f"Connect button not found or timed out: {profile_url}")
            page_content = self.driver.page_source.lower()
            if "pending" in page_content or "beklemede" in page_content:
                 logging.info(f"Connection request already pending: {profile_url}")
                 return True
            if "1st degree connection" in page_content or "1. derece bağlantı" in page_content:
                 logging.info(f"Already connected: {profile_url}")
                 return True
            return False
        except Exception as e:
            logging.error(f"Error sending connection request on profile page {profile_url}: {str(e)}", exc_info=True)
            return False

    def check_weekly_limit_popups(self):
        """Checks for known weekly limit pop-up modals and attempts to close them."""
        try:
            limit_modal_xpath = '//div[contains(@class, "artdeco-modal__content") and (contains(., "limit") or contains(., "sınır"))]'
            limit_modals_found = self.driver.find_elements(By.XPATH, limit_modal_xpath)

            if limit_modals_found:
                logging.warning("Potential limit modal detected.")
                dismiss_button_xpaths = [
                    './/button[contains(@class, "artdeco-modal__dismiss")]',
                    './/button[contains(text(), "Got it") or contains(text(), "Anladım")]',
                    './/button[contains(@aria-label, "Dismiss") or contains(@aria-label, "Kapat")]'
                ]
                for modal_element in limit_modals_found:
                    modal_text_lower = modal_element.text.lower()
                    if "haftalık davet sınırına ulaştınız" in modal_text_lower or \
                       "weekly invitation limit" in modal_text_lower:
                        if not self._limit_reported:
                            logging.error("\n" + "="*70 +
                                        "\nERROR: Weekly connection limit reached (Detected via modal)!" +
                                        "\nPlease try again next week." +
                                        "\n" + "="*70)
                            self._limit_reported = True
                        for xpath in dismiss_button_xpaths:
                            try:
                                close_button = modal_element.find_element(By.XPATH, xpath)
                                close_button.click()
                                logging.info("Limit modal closed.")
                                time.sleep(1)
                                return True # Limit reached
                            except NoSuchElementException:
                                continue
                        return True

        except Exception as e:
            logging.debug(f"Error checking limit modal: {str(e)}")
        return False

    def send_connection_requests_from_search(self, keywords, max_requests=30):
        """Send connection requests to people in search results"""
        try:
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords.replace(' ', '%20')}"
            logging.info(f"Searching: {keywords} - URL: {search_url}")
            self.driver.get(search_url)
            time.sleep(random.uniform(3, 5))

            if self.check_invitation_limit(silent=False) or self.check_weekly_limit_popups():
                return 0

            request_count = 0
            page = 1

            while request_count < max_requests:
                logging.info(f"Processing page {page}. Requests sent: {request_count}/{max_requests}")
                self._scroll_to_bottom_of_page()

                connect_buttons_found = self.driver.find_elements(By.XPATH, self.SEARCH_RESULTS_CONNECT_BUTTON_XPATH)
                
                if not connect_buttons_found:
                    logging.info("No 'Connect' buttons found on this page.")
                    page_content = self.driver.page_source.lower()
                    if "no results found" in page_content or "sonuç bulunamadı" in page_content:
                        logging.info("No search results found.")
                        break
                    if not self._go_to_next_search_page():
                        logging.info("No more pages found or reached the end.")
                        break
                    page += 1
                    time.sleep(random.uniform(3, 5))
                    continue

                logging.info(f"Found {len(connect_buttons_found)} potential connect buttons on the page.")
                
                for i, button in enumerate(connect_buttons_found):
                    if request_count >= max_requests:
                        logging.info("Maximum request count reached.")
                        break

                    # Check for weekly limit before processing each button
                    if self.check_invitation_limit(silent=True) or self.check_weekly_limit_popups():
                        if not self._limit_reported:
                            logging.error("\n" + "="*70 +
                                      "\nERROR: Weekly connection request limit reached!" +
                                      "\nPlease try again next week." +
                                      "\n" + "="*70)
                            self._limit_reported = True
                        return request_count

                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                        time.sleep(random.uniform(0.5, 1.5))

                        if button.is_displayed() and button.is_enabled():
                            button_text = button.text.strip()
                            logging.info(f"Processing button #{i+1} ({button_text})...")
                            
                            button.click()
                            time.sleep(random.uniform(1, 2))

                            modal_handled = self._handle_connection_modal()
                            
                            if modal_handled:
                                request_count += 1
                                logging.info(f"Connection request sent: {request_count}/{max_requests}")
                            else:
                                logging.warning("Connection modal could not be handled or request could not be sent.")
                                self._close_any_generic_modal()

                            wait_time = 1
                            logging.info(f"Waiting {wait_time} seconds for next request...")
                            time.sleep(wait_time)
                        else:
                            logging.warning(f"Button #{i+1} not visible or not enabled, skipping.")

                    except ElementClickInterceptedException:
                        logging.warning("Button click intercepted. Probably an overlay/popup. Attempting to close...")
                        self._close_any_generic_modal()
                        time.sleep(1)
                    except Exception as e:
                        logging.warning(f"Error sending a connection request: {str(e)}")
                        if "message type unsupported" in str(e).lower():
                            logging.warning("There might be a temporary issue with browser communication. Continuing.")
                        
                        # Check for limit after an error occurs
                        if self.check_invitation_limit(silent=True) or self.check_weekly_limit_popups():
                            if not self._limit_reported:
                                logging.error("\n" + "="*70 +
                                          "\nERROR: Weekly connection request limit reached!" +
                                          "\nPlease try again next week." +
                                          "\n" + "="*70)
                                self._limit_reported = True
                            return request_count

                if request_count < max_requests:
                    if not self._go_to_next_search_page():
                        logging.info("No more pages found.")
                        break
                    page += 1
                    logging.info(f"Moving to page {page}...")
                    time.sleep(random.uniform(3, 5))

            return request_count

        except Exception as e:
            logging.error(f"General error while sending connection requests: {str(e)}", exc_info=True)
            return locals().get('request_count', 0)


    def _scroll_to_bottom_of_page(self):
        """Scrolls to the bottom of the page to load all dynamic content."""
        logging.info("Scrolling to bottom of page...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 5

        while scroll_attempts < max_scroll_attempts:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.debug("Reached bottom of page.")
                break
            last_height = new_height
            scroll_attempts += 1
        if scroll_attempts == max_scroll_attempts:
            logging.warning("Maximum scroll attempts reached. Some content might not be loaded.")


    def _handle_connection_modal(self, custom_message=None):
        """Handle the connection modal and send the connection request.
        
        Args:
            custom_message (str, optional): Custom message to include with the connection request
            
        Returns:
            bool: True if the connection request was sent successfully, False otherwise
        """
        try:
            # Wait for the modal to appear
            self.short_wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "artdeco-modal--layer-default")]')
            ))
            
            # Only add a note if notes are explicitly enabled and we have a message to send
            if self.use_notes and (custom_message or self.connection_note):
                message_to_send = custom_message or self.connection_note
                try:
                    # Try to find and click the "Add a note" button if it exists
                    add_note_button = self.short_wait.until(
                        EC.element_to_be_clickable((By.XPATH, self.MODAL_ADD_NOTE_BUTTON_XPATH))
                    )
                    logging.info("Add note button found, clicking...")
                    add_note_button.click()
                    time.sleep(random.uniform(0.5, 1.5))

                    # Find the note field and enter the message
                    note_field = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, 
                            f"//textarea[@id='{self.MODAL_CUSTOM_MESSAGE_ID}' or @name='message' or contains(@class, 'message')]"))
                    )
                    logging.info(f"Adding note: '{message_to_send[:30]}...'")
                    note_field.clear()
                    note_field.send_keys(message_to_send)
                    time.sleep(random.uniform(0.5, 1))
                except TimeoutException:
                    logging.info("Add note button not found. Looking for direct message field...")
                    try:
                        # Some modals might have the note field directly visible
                        note_field_elements = self.driver.find_elements(
                            By.XPATH, 
                            f"//textarea[@id='{self.MODAL_CUSTOM_MESSAGE_ID}' or @name='message' or contains(@class, 'message')]"
                        )
                        if note_field_elements and note_field_elements[0].is_displayed():
                            logging.info(f"Adding note directly: '{message_to_send[:30]}...'")
                            note_field_elements[0].clear()
                            note_field_elements[0].send_keys(message_to_send)
                            time.sleep(random.uniform(0.5, 1))
                    except NoSuchElementException:
                        logging.info("Note field not found. Sending without a note.")
            else:
                # In default mode, we want to click the 'Not olmadan gönderin' button
                logging.info("Sending connection request without a note (default mode).")
                
                # Try to find and click the 'Not olmadan gönderin' button
                try:
                    # First try the exact Turkish text
                    send_without_note = self.short_wait.until(
                        EC.element_to_be_clickable((By.XPATH, 
                            '//button[.//span[text()="Not olmadan gönderin"]] | '
                            '//button[text()="Not olmadan gönderin"] | '
                            '//button[contains(@aria-label, "Not olmadan gönderin")] | '
                            # Fallback for English UI
                            '//button[.//span[text()="Send without a note"]] | '
                            '//button[text()="Send without a note"] | '
                            '//button[contains(@aria-label, "Send without a note")] | '
                            # More generic fallbacks
                            '//button[contains(., "Not olmadan")] | '
                            '//button[contains(., "without a note")] | '
                            '//button[contains(., "Send") and not(contains(., "Add")) and not(contains(., "Note"))] | '
                            '//button[contains(., "Gönder") and not(contains(., "Not"))]'))
                    )
                    logging.info("Found 'Not olmadan gönderin' button, clicking...")
                    send_without_note.click()
                    time.sleep(random.uniform(1, 2))
                    return True
                except (TimeoutException, NoSuchElementException) as e:
                    logging.info(f"Could not find 'Not olmadan gönderin' button: {str(e)}, trying default send button...")
            
            # Find and click the send button
            # First try to find a button that's not the cancel button
            try:
                send_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        f"{self.MODAL_SEND_BUTTON_XPATH}["
                        "not(contains(@aria-label, 'Cancel') or contains(@aria-label, 'İptal')) "
                        "and not(contains(@class, 'cancel'))]"
                    ))
                )
                logging.info("Send button found, clicking...")
                send_button.click()
                time.sleep(random.uniform(1, 2))
            except TimeoutException:
                # If we can't find the main send button, try to find any button that says 'Send' or 'Gönder'
                try:
                    send_button = self.driver.find_element(
                        By.XPATH,
                        '//button[contains(., "Send") or contains(., "Gönder")] | '
                        '//button[contains(@aria-label, "Send") or contains(@aria-label, "Gönder")] | '
                        '//button[.//span[text()="Send" or text()="Gönder"]]'
                    )
                    if send_button.is_displayed() and send_button.is_enabled():
                        logging.info("Alternative send button found, clicking...")
                        send_button.click()
                        time.sleep(random.uniform(1, 2))
                    else:
                        raise NoSuchElementException("Send button not clickable")
                except (NoSuchElementException, ElementNotInteractableException) as e:
                    logging.error(f"Could not find or click send button: {str(e)}")
                    self._close_any_generic_modal()
                    return False
            return True

        except TimeoutException:
            logging.warning("Send button not found or timed out in connection modal.")
            self._close_any_generic_modal(specific_modal_xpath='//div[contains(@class, "artdeco-modal--layer-default")]')
            return False
        except Exception as e:
            logging.error(f"Error handling connection modal: {str(e)}", exc_info=True)
            self._close_any_generic_modal(specific_modal_xpath='//div[contains(@class, "artdeco-modal--layer-default")]')
            return False

    def _close_any_generic_modal(self, specific_modal_xpath=None):
        """Attempts to close any visible modal."""
        try:
            if specific_modal_xpath:
                modals = self.driver.find_elements(By.XPATH, specific_modal_xpath)
                if modals and modals[0].is_displayed():
                    logging.debug(f"Attempting to close specific modal: {specific_modal_xpath}")
                    common_close_xpaths = [
                        './/button[contains(@aria-label, "Dismiss") or contains(@aria-label, "Kapat")]',
                        './/button[contains(@class, "artdeco-modal__dismiss")]',
                        './/button[contains(@aria-label, "Cancel") or contains(@aria-label, "İptal")]'
                    ]
                    for xpath in common_close_xpaths:
                        try:
                            close_button = modals[0].find_element(By.XPATH, xpath)
                            if close_button.is_displayed() and close_button.is_enabled():
                                close_button.click()
                                logging.info("Specific modal closed.")
                                time.sleep(0.5)
                                return True
                        except: pass
            
            active_modals_close_buttons = self.driver.find_elements(By.XPATH, '//div[contains(@class, "artdeco-modal__header") and preceding-sibling::div[contains(@class, "artdeco-modal__overlay")]]/following-sibling::button[contains(@class, "artdeco-modal__dismiss")] | //button[@aria-label="Dismiss"]')
            if active_modals_close_buttons:
                for btn in active_modals_close_buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        logging.info("Closing a generic modal...")
                        btn.click()
                        time.sleep(0.5)
                        return True

            overlay = self.driver.find_elements(By.XPATH, '//div[contains(@class, "artdeco-modal__overlay--is-current")]')
            if overlay and overlay[0].is_displayed():
                logging.info("Pressing Escape to close a generic modal.")
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(1)
                return True
            
        except Exception as e:
            logging.debug(f"Error closing modal: {e}")
        return False


    def _go_to_next_search_page(self):
        """Navigate to the next page of search results"""
        try:
            next_button_xpath = (
                '//button[@aria-label="Sonraki" and not(@disabled)] | '
                '//button[@aria-label="Next" and not(@disabled)] | '
                '//li[contains(@class, "active") or contains(@class, "selected")]/following-sibling::li[1]/button[not(@disabled)]'
            )
            next_button = self.short_wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
            time.sleep(0.5)
            next_button.click()
            time.sleep(random.uniform(2, 4))
            return True
        except TimeoutException:
            logging.info("Next page button not found or not clickable. Probably the last page.")
        except Exception as e:
            logging.warning(f"Could not navigate to next page: {str(e)}")
        return False

    def check_invitation_limit(self, silent=False):
        """Check if LinkedIn's weekly invitation limit has been hit."""
        try:
            limit_messages = [
                "haftalık davet sınırına ulaştınız", "weekly invitation limit",
                "bağlantı isteği gönderemezsiniz", "you cannot send connection requests",
                "sınırı aşıldı", "limit has been reached",
                "too many invitations", "çok fazla davet",
                "you're out of invitations for now", "şimdilik davet hakkınız kalmadı"
            ]
            page_source = self.driver.page_source.lower()
            for msg in limit_messages:
                if msg in page_source:
                    if not silent and not self._limit_reported:
                        logging.error("\n" + "="*70 +
                                      "\nERROR: Weekly connection request limit reached (Detected in page source)!" +
                                      "\nPlease try again next week." +
                                      "\n" + "="*70)
                        self._limit_reported = True
                    return True
        except Exception as e:
            if not silent:
                logging.warning(f"Error checking limit: {str(e)}")
        return False

    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("Browser closed")
            except Exception as e:
                logging.error(f"Error closing browser: {e}")

def get_user_input(prompt, default_value, type_converter=str):
    """Generic function to get user input with a default value and type."""
    while True:
        try:
            value_str = input(f"{prompt} (Default: {default_value}): ").strip()
            if not value_str:
                return default_value
            
            # Special validation for search terms
            if "search term" in prompt.lower():
                if len(value_str) < 2:
                    print_warning("Search term must be at least 2 characters long.")
                    continue
                if len(value_str) > 100:
                    print_warning("Search term is too long. Please keep it under 100 characters.")
                    continue
            
            # Special validation for max requests
            if "maximum number of connection requests" in prompt.lower():
                value = type_converter(value_str)
                if value < 1:
                    print_warning("Maximum requests must be at least 1.")
                    continue
                if value > 100:
                    print_warning("Maximum requests cannot exceed 100 to avoid rate limiting.")
                    continue
                return value
            
            # Special validation for connection note
            if "connection request note" in prompt.lower():
                if len(value_str) > 300:
                    print_warning("Connection note is too long. It will be truncated to 300 characters.")
                    value_str = value_str[:300]
            
            return type_converter(value_str)
        except ValueError:
            print_warning(f"Please enter a valid {type_converter.__name__}.")
        except KeyboardInterrupt:
            print_warning("\nOperation cancelled by user.")
            sys.exit(0)


def show_help():
    """Display usage instructions for the tool"""
    print_highlight("\nLINKEDAUTO - KULLANIM KILAVUZU")
    print_highlight("="*50 + "\n")
    
    print_info("TEMEL KULLANIM:")
    print(Fore.CYAN + "  python linkedin_connector.py" + Style.RESET_ALL + " - Varsayılan ayarlarla başlat")
    
    print_info("\nSEÇENEKLER:")
    print(Fore.YELLOW + "  --headless" + Style.RESET_ALL + "        Tarayıcıyı arka planda çalıştır")
    print(Fore.YELLOW + "  -k, --keywords" + Style.RESET_ALL + "     Arama anahtar kelimeleri (örn: 'yazılım mühendisi')")
    print(Fore.YELLOW + "  -m, --max_requests" + Style.RESET_ALL + "  Gönderilecek maksimum bağlantı isteği sayısı")
    print(Fore.YELLOW + "  -n, --note" + Style.RESET_ALL + "           Bağlantı isteğine eklenecek özel not")
    
    print_info("\nÖRNEKLER:")
    print("  " + Fore.CYAN + "python linkedin_connector.py --headless" + Style.RESET_ALL)
    print("  " + Fore.CYAN + 'python linkedin_connector.py -k "yapay zeka uzmanı" -m 20' + Style.RESET_ALL)
    print("  " + Fore.CYAN + 'python linkedin_connector.py -n "Ortak projeler hakkında görüşmek isterim"' + Style.RESET_ALL)
    
    print("\n" + Fore.YELLOW + "NOT:" + Style.RESET_ALL + " LinkedIn'in Kullanım Şartları'na uygun şekilde kullanın.")
    print("="*50 + "\n")
    sys.exit(0)


def main():
    # Check for --help or -h flag before anything else
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
    
    # ASCII Art Title
    f = Figlet(font='slant')
    title = f.renderText('LinkedAuto')
    print_highlight(Fore.CYAN + title + Style.RESET_ALL)
    
    # Links
    print_highlight(Fore.MAGENTA + "GitHub: " + Fore.BLUE + "https://github.com/xeloxa" + Style.RESET_ALL)
    print_highlight(Fore.MAGENTA + "Website: " + Fore.BLUE + "https://xeloxa.netlify.app" + Style.RESET_ALL + "\n")
    
    # Supported Languages
    print_info("Supported Languages:")
    print_info("- English")
    print_info("- Turkish (LinkedIn Interface Only)\n")

    # --- LEGAL DISCLAIMER ---
    print_highlight("\n" + "-"*80)
    print_warning("⚠️ This tool is for educational purposes only. Avoid violating LinkedIn's Terms of Service. You are responsible for any consequences that may arise from using this tool.")
    print_highlight("-"*80 + "\n")
    # --- LEGAL DISCLAIMER END ---

    # Quick Start Option
    print_highlight("\n=== QUICK START OPTION ===")
    print_info("1. Start with default settings (Recommended)")
    print_info("2. Customize settings")
    while True:
        try:
            quick_choice = input("\nYour choice (1/2, Default: 1): ").strip()
            if not quick_choice:
                quick_choice = '1'
            if quick_choice not in ['1', '2']:
                print_warning("Please enter either 1 or 2.")
                continue
            break
        except KeyboardInterrupt:
            print_warning("\nOperation cancelled by user.")
            sys.exit(0)
    
    parser = argparse.ArgumentParser(description="LinkedIn Connection Bot - Professional Networking Automation Tool", add_help=False)
    parser.add_argument(
        "--help", "-h",
        action="store_true",
        help="Show this help message and exit."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in background (headless mode)."
    )
    parser.add_argument(
        "-k", "--keywords",
        type=str,
        help="Search keywords (e.g., 'cybersecurity expert')."
    )
    parser.add_argument(
        "-m", "--max_requests",
        type=int,
        help="Maximum number of connection requests to send."
    )
    parser.add_argument(
        "-n", "--note",
        type=str,
        help="Custom note to send with connection requests."
    )
    parser.add_argument(
        "--use-notes",
        action="store_true",
        help="Send connection requests with notes (default: False)."
    )
    parser.set_defaults(headless=False, use_notes=False)
    
    args = parser.parse_args()
    
    # Show help if requested
    if args.help:
        show_help()

    # Default values
    default_keywords = "python developer"
    default_max_requests = 30
    default_note = ""  # Empty by default since we're not using notes

    # Use default values if quick start is selected
    if quick_choice in ['', '1']:
        print_info("\nStarting with default settings...")
        if not args.keywords:
            args.keywords = default_keywords
        if not args.max_requests:
            args.max_requests = default_max_requests
        if not args.note:
            args.note = default_note
        
        # Show browser by default
        effective_headless_mode = False
        print_info(f"Search Term: {args.keywords}")
        print_info(f"Maximum Requests: {args.max_requests}")
        if args.use_notes and args.note:
            print_info(f"Connection Note: {args.note[:50]}...")
        else:
            print_info("Connection Note: Not using notes (default)")
        print_info("Browser will run in visible mode.")
        print_success("\nStarting process...\n")
    else:
        # Normal flow
        effective_headless_mode = args.headless
        
        # Ask about headless mode if not set via command line
        if not args.headless and '--headless' not in sys.argv:
            while True:
                try:
                    headless_choice = input("\nDo you want to run the browser in background (headless mode)? "
                                        "(Y/y Yes, N/n No - Default: No): ").strip().lower()
                    if not headless_choice:
                        effective_headless_mode = False
                        break
                    if headless_choice not in ['y', 'yes', 'n', 'no']:
                        print_warning("Please enter Y/y for Yes or N/n for No.")
                        continue
                    effective_headless_mode = headless_choice in ['y', 'yes']
                    break
                except KeyboardInterrupt:
                    print_warning("\nOperation cancelled by user.")
                    sys.exit(0)

    # Only ask for user input in custom mode
    if quick_choice not in ['', '1']:
        print_highlight("\n=== LinkedIn Connection Bot ===")
        print_info("This script searches LinkedIn and")
        print_info("sends connection requests to found profiles.\n")
        
        # If keywords not provided via CLI, ask for "Enter" prompt
        fully_interactive_setup = not (args.keywords or args.max_requests is not None or args.note)
        if fully_interactive_setup:
            while True:
                try:
                    user_input = input("Press Enter to configure settings and continue...").strip()
                    if user_input:
                        print_warning("Please just press Enter to continue.")
                        continue
                    break
                except KeyboardInterrupt:
                    print_warning("\nOperation cancelled by user.")
                    sys.exit(0)

        try:
            search_term = args.keywords or get_user_input(
                "\nEnter your search term",
                default_keywords
            )
            max_requests = args.max_requests if args.max_requests is not None else get_user_input(
                "Enter maximum number of connection requests",
                default_max_requests,
                int
            )
            connection_note = args.note or get_user_input(
                "Enter connection request note (Press Enter for default)",
                default_note
            )
        except KeyboardInterrupt:
            print_warning("\nOperation cancelled by user.")
            sys.exit(0)
    else:
        # Set values for quick start
        search_term = args.keywords or default_keywords
        max_requests = args.max_requests or default_max_requests
        connection_note = args.note or default_note

    connector = None
    try:
        # Create connector without initializing browser
        connector = LinkedInConnector(headless=effective_headless_mode, connection_note=connection_note)
        
        # Setup login method and initialize browser
        connector.setup_login()
        
        if not connector.login():
            print_error("Login failed. Terminating program.")
            return

        print_highlight(f"\n=== Sending connection requests for '{search_term}' (Max: {max_requests}) ===")
        
        request_count = connector.send_connection_requests_from_search(search_term, max_requests)

        print_success(f"\nTotal {request_count} connection requests sent.")
        if connector._limit_reported:
            print_warning("Operation stopped due to weekly limit.")
        elif request_count == max_requests:
            print_success("Maximum request count reached. Operation completed.")
        else:
            print_info("Search results exhausted or fewer requests sent for other reasons. Operation completed.")

    except ValueError as ve:
        print_error(f"Setup error: {ve}")
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
    except Exception as e:
        print_error(f"Unexpected error in main program: {str(e)}")
    finally:
        if connector and connector.driver:
            connector.close()
        print_info("Program terminated.")

if __name__ == "__main__":
    main()