import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
import os
import time

BS_USERNAME = os.environ.get('BROWSERSTACK_USERNAME', 'tubaabdugapparov_P5Kuky')
BS_ACCESS_KEY = os.environ.get('BROWSERSTACK_ACCESS_KEY', 'hDfxAsP1ezW1eXyU7e8p')
BS_URL = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

class BrowserStackTestBase(unittest.TestCase):
    
    def setUp(self):
        options = self.get_browser_options()
        
        options.set_capability('build', 'Python Test Suite')
        options.set_capability('project', 'Automated Testing Homework')
        options.set_capability('name', f'{self.__class__.__name__}.{self._testMethodName}')
        options.set_capability('browserstack.debug', 'true')
        options.set_capability('browserstack.console', 'verbose')
        options.set_capability('browserstack.networkLogs', 'true')
        
        self.driver = webdriver.Remote(
            command_executor=BS_URL,
            options=options
        )
        self.driver.implicitly_wait(10)
    
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
    
    def test_01_google_search(self):
        self.driver.get("https://www.google.com")
        
        try:
            accept_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'I agree')]"))
            )
            accept_btn.click()
        except:
            pass
        
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("BrowserStack")
        search_box.submit()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        self.assertIn("BrowserStack", self.driver.title)
    
    def test_02_wikipedia_navigation(self):
        self.driver.get("https://www.wikipedia.org")
        
        english_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='js-link-box-en']"))
        )
        english_link.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        
        self.assertIn("Wikipedia", self.driver.title)


class FirefoxTests(BrowserStackTestBase):
    
    def get_browser_options(self):
        options = FirefoxOptions()
        options.set_capability('browserName', 'Firefox')
        options.set_capability('browser_version', 'latest')
        options.set_capability('os', 'Windows')
        options.set_capability('os_version', '10')
        return options
    
    def test_01_google_search(self):
        self.driver.get("https://www.google.com")
        
        try:
            accept_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'I agree')]"))
            )
            accept_btn.click()
        except:
            pass
        
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("BrowserStack")
        search_box.submit()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        self.assertIn("BrowserStack", self.driver.title)
    
    def test_02_wikipedia_navigation(self):
        self.driver.get("https://www.wikipedia.org")
        
        english_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='js-link-box-en']"))
        )
        english_link.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        
        self.assertIn("Wikipedia", self.driver.title)


class SafariTests(BrowserStackTestBase):
    
    def get_browser_options(self):
        options = SafariOptions()
        options.set_capability('browserName', 'Safari')
        options.set_capability('browser_version', 'latest')
        options.set_capability('os', 'OS X')
        options.set_capability('os_version', 'Big Sur')
        return options
    
    def test_01_google_search(self):
        self.driver.get("https://www.google.com")
        
        try:
            accept_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'I agree')]"))
            )
            accept_btn.click()
        except:
            pass
        
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("BrowserStack")
        search_box.submit()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        self.assertIn("BrowserStack", self.driver.title)
    
    def test_02_wikipedia_navigation(self):
        self.driver.get("https://www.wikipedia.org")
        
        english_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='js-link-box-en']"))
        )
        english_link.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        
        self.assertIn("Wikipedia", self.driver.title)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ChromeTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FirefoxTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SafariTests))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)