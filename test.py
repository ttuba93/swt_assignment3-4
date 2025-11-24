import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
import os
import time

BS_USERNAME = os.environ.get('BROWSERSTACK_USERNAME', 'tubaabdugapparov_P5Kuky')
BS_ACCESS_KEY = os.environ.get('BROWSERSTACK_ACCESS_KEY', 'hDfxAsP1ezW1eXyU7e8p')
BS_URL = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

EMAIL = "your_email@example.com"
PASSWORD = "your_password"


class BrowserStackTestBase(unittest.TestCase):
    
    def setUp(self):
        options = self.get_browser_options()
        
        options.set_capability('build', 'Pinterest Test Suite')
        options.set_capability('project', 'SWT Assignment 3+4')
        options.set_capability('name', f'{self.__class__.__name__}.{self._testMethodName}')
        options.set_capability('browserstack.debug', 'true')
        options.set_capability('browserstack.console', 'verbose')
        options.set_capability('browserstack.networkLogs', 'true')
        
        self.driver = webdriver.Remote(
            command_executor=BS_URL,
            options=options
        )
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
    
    def tearDown(self):
        if self.driver:
            status = "passed" if self._outcome.success else "failed"
            self.driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", '
                f'"arguments": {{"status":"{status}", "reason": "Test {status}"}}}}'
            )
            self.driver.quit()
    
    def get_browser_options(self):
        return ChromeOptions()


class ChromeTests(BrowserStackTestBase):
    def get_browser_options(self):
        options = ChromeOptions()
        options.set_capability('browserName', 'Chrome')
        options.set_capability('browser_version', 'latest')
        options.set_capability('os', 'Windows')
        options.set_capability('os_version', '10')
        return options
    
    def test_01_sign_up(self):
        print("\nTest 1: Sign Up Page")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        try:
            signup_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-signup-button']"))
            )
            signup_button.click()
            print("✓ Clicked Sign Up button")
        except Exception as e:
            print(f"✗ Failed to click Sign Up button: {e}")
            self.fail("Sign Up button not found")
        
        time.sleep(2)
        
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
            )
            print("✓ Email field is present")
            self.assertTrue(email_field.is_displayed(), "Email field should be visible")
        except Exception as e:
            print(f"✗ Email field not found: {e}")
            self.fail("Email field not found on Sign Up page")
    
    def test_02_log_in(self):
        print("\n Test 2: Log In")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
            )
            login_button.click()
            print("✓ Clicked Log In button")
        except Exception as e:
            print(f"✗ Failed to click Log In button: {e}")
            self.fail("Log In button not found")
        
        time.sleep(2)
        
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.clear()
            email_input.send_keys(EMAIL)
            print(f"✓ Entered email: {EMAIL}")
        except Exception as e:
            print(f"✗ Failed to enter email: {e}")
            self.fail("Email input not found")
        
        try:
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(PASSWORD)
            print("✓ Entered password")
        except Exception as e:
            print(f"✗ Failed to enter password: {e}")
            self.fail("Password input not found")
        
        try:
            submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
            submit_button.click()
            print("✓ Clicked Submit button")
        except Exception as e:
            print(f"✗ Failed to click Submit: {e}")
            self.fail("Submit button not found")
        
        time.sleep(5)
        
        try:
            profile_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Profile']"))
            )
            print("✓ Successfully logged in - Profile button found")
            self.assertTrue(profile_element.is_displayed(), "Should be logged in")
        except Exception as e:
            print(f"✗ Login verification failed: {e}")
            self.fail("Login failed - Profile button not found")
    
    def test_03_log_out(self):
        print("\n Test 3: Log Out")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        print("✓ Logged in successfully")
        
        try:
            profile_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Profile']"))
            )
            profile_button.click()
            print("✓ Clicked Profile button")
        except Exception as e:
            print(f"✗ Failed to click Profile: {e}")
            self.fail("Profile button not found")
        
        time.sleep(3)
        
        try:
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[text()='Log out' or text()='Выйти']"))
            )
            logout_button.click()
            print("✓ Clicked Log Out button")
        except Exception as e:
            print(f"✗ Failed to click Log Out: {e}")
            self.fail("Log Out button not found")
        
        time.sleep(3)
        
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, 
                    "//*[@data-test-id='simple-login-button']"))
            )
            print("✓ Successfully logged out - Login button visible")
            self.assertTrue(login_button.is_displayed(), "Should be logged out")
        except Exception as e:
            print(f"✗ Logout verification failed: {e}")
            self.fail("Logout failed - Login button not found")
    
    def test_04_search_pin(self):
        print("\n Test 4: Search Pin")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        print("✓ Logged in successfully")
        
        try:
            search_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Search']"))
            )
            search_field.click()
            print("✓ Clicked search field")
        except Exception as e:
            print(f"✗ Failed to click search field: {e}")
            self.fail("Search field not found")
        
        time.sleep(4)
        
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Search']"))
            )
            search_input.clear()
            search_input.send_keys("interior design")
            print("✓ Entered search query: interior design")
        except Exception as e:
            print(f"✗ Failed to enter search query: {e}")
            self.fail("Search input not found")
        
        try:
            search_input.send_keys(Keys.ENTER)
            print("✓ Pressed Enter")
        except Exception as e:
            print(f"✗ Failed to press Enter: {e}")
            self.fail("Failed to submit search")
        
        time.sleep(4)
        
        try:
            current_url = self.driver.current_url
            self.assertIn("search", current_url.lower(), "Should be on search results page")
            print(f"✓ Search results page loaded: {current_url}")
        except Exception as e:
            print(f"✗ Search verification failed: {e}")
            self.fail("Search results not found")


class FirefoxTests(BrowserStackTestBase):
    
    def get_browser_options(self):
        options = FirefoxOptions()
        options.set_capability('browserName', 'Firefox')
        options.set_capability('browser_version', 'latest')
        options.set_capability('os', 'Windows')
        options.set_capability('os_version', '10')
        return options
    
    def test_01_sign_up(self):
        print("\n Test 1: Sign Up Page")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        signup_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-signup-button']"))
        )
        signup_button.click()
        print("✓ Clicked Sign Up button")
        time.sleep(2)
        
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
        )
        print("✓ Email field is present")
        self.assertTrue(email_field.is_displayed(), "Email field should be visible")
    
    def test_02_log_in(self):
        print("\nTest 2: Log In ")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        
        profile_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Profile']"))
        )
        print("✓ Successfully logged in")
        self.assertTrue(profile_element.is_displayed(), "Should be logged in")
    
    def test_03_log_out(self):
        print("\n Test 3: Log Out")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        
        profile_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Profile']"))
        )
        profile_button.click()
        time.sleep(3)
        
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//*[text()='Log out' or text()='Выйти']"))
        )
        logout_button.click()
        time.sleep(3)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 
                "//*[@data-test-id='simple-login-button']"))
        )
        print("✓ Successfully logged out")
        self.assertTrue(login_button.is_displayed(), "Should be logged out")
    
    def test_04_search_pin(self):
        print("\n Test 4: Search Pin ")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        
        search_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Search']"))
        )
        search_field.click()
        time.sleep(4)
        
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Search']"))
        )
        search_input.send_keys("interior design")
        search_input.send_keys(Keys.ENTER)
        time.sleep(4)
        
        current_url = self.driver.current_url
        self.assertIn("search", current_url.lower(), "Should be on search results page")
        print(f"✓ Search completed: {current_url}")


class SafariTests(BrowserStackTestBase):
    
    def get_browser_options(self):
        options = SafariOptions()
        options.set_capability('browserName', 'Safari')
        options.set_capability('browser_version', 'latest')
        options.set_capability('os', 'OS X')
        options.set_capability('os_version', 'Big Sur')
        return options
    
    def test_01_sign_up(self):
        print("\n Test 1: Sign Up Page")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        signup_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-signup-button']"))
        )
        signup_button.click()
        print("✓ Clicked Sign Up button")
        time.sleep(2)
        
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
        )
        print("✓ Email field is present")
        self.assertTrue(email_field.is_displayed(), "Email field should be visible")
    
    def test_02_log_in(self):
        print("\n Test 2: Log In")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        
        profile_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Profile']"))
        )
        print("✓ Successfully logged in")
        self.assertTrue(profile_element.is_displayed(), "Should be logged in")
    
    def test_03_log_out(self):
        print("\n Test 3: Log Out")
        
        # Log in first
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        
        # Log out
        profile_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Profile']"))
        )
        profile_button.click()
        time.sleep(3)
        
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//*[text()='Log out' or text()='Выйти']"))
        )
        logout_button.click()
        time.sleep(3)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 
                "//*[@data-test-id='simple-login-button']"))
        )
        print("✓ Successfully logged out")
        self.assertTrue(login_button.is_displayed(), "Should be logged out")
    
    def test_04_search_pin(self):
        print("\n Test 4: Search Pin")
        
        self.driver.get("https://www.pinterest.com")
        time.sleep(2)
        
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='simple-login-button']"))
        )
        login_button.click()
        time.sleep(2)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        submit_button.click()
        time.sleep(5)
        
        # Search
        search_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Search']"))
        )
        search_field.click()
        time.sleep(4)
        
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Search']"))
        )
        search_input.send_keys("interior design")
        search_input.send_keys(Keys.ENTER)
        time.sleep(4)
        
        current_url = self.driver.current_url
        self.assertIn("search", current_url.lower(), "Should be on search results page")
        print(f"✓ Search completed: {current_url}")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    print("Pinterest BrowserStack Test Suite")
    
    print("\nAdding Chrome tests...")
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ChromeTests))
    
    print("Adding Firefox tests...")
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FirefoxTests))
    
    print("Adding Safari tests...")
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SafariTests))
    
    print(f"\nTotal tests: 12 (4 tests × 3 browsers)")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
