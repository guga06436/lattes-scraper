from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    """
    Manages the setup and teardown of the Selenium WebDriver.
    """
    
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        """
        Initializes and returns a Selenium WebDriver instance.

        Returns:
            webdriver.Chrome: The initialized WebDriver instance.
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Set default wait time
        return self.driver

    def close_driver(self):
        """
        Closes the WebDriver if it has been initialized.

        Returns:
            None
        """
        if self.driver:
            self.driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    """
    Manages the setup and teardown of the Selenium WebDriver.
    """
    
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        """
        Initializes and returns a Selenium WebDriver instance.

        Returns:
            webdriver.Chrome: The initialized WebDriver instance.
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Set default wait time
        return self.driver

    def close_driver(self):
        """
        Closes the WebDriver if it has been initialized.

        Returns:
            None
        """
        if self.driver:
            self.driver.quit()
