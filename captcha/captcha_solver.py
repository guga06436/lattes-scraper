from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By
import time

class CaptchaSolver:
    """
    Handles interactions with the TwoCaptcha service to solve reCAPTCHA challenges.
    """

    def __init__(self, api_key):
        """
        Initializes the CaptchaSolver class with the TwoCaptcha API key.

        Args:
            api_key (str): The API key for the TwoCaptcha service.
        """
        self.api_key = api_key
        self.solver = TwoCaptcha(api_key)

    def get_site_key(self, driver):
        """
        Extracts the site key required for solving reCAPTCHA from the web page.

        Args:
            driver (webdriver): The WebDriver instance used to interact with the web page.

        Returns:
            str: The site key for the reCAPTCHA challenge.
            None: If no site key is found.
        """
        try:
            # Find the iframe containing the reCAPTCHA and get the 'src' attribute
            iframe_element = driver.find_element(By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
            iframe_src = iframe_element.get_attribute("src")
            params = iframe_src.split('&')
            
            # Extract the sitekey parameter from the URL
            for param in params:
                if param.startswith("k="):
                    return param.split('=')[1]
                
            return None
        except Exception as e:
            print(f'Error getting the sitekey: {e}')
            return None

    def solve_recaptcha(self, driver):
        """
        Solves the reCAPTCHA using the TwoCaptcha service and injects the solution into the web page.

        Args:
            driver (webdriver): The WebDriver instance used to interact with the web page.

        Returns:
            bool: Returns True after successfully solving the captcha and injecting the response.
        """
        # Retrieve the site key from the page
        sitekey = self.get_site_key(driver)
        if not sitekey:
            print("Sitekey not found.")
            return False
        
        url = driver.current_url
        response = None

        # Retry up to 10 times if there's an error solving the captcha
        for i in range(10):
            try:
                # Send the sitekey and URL to TwoCaptcha to solve the captcha
                response = self.solver.recaptcha(sitekey=sitekey, url=url)
            except Exception as ex:
                print(f"Error solving captcha: {ex}, retrying... ({i+1}/10)")
                if i == 9:  # If it's the last iteration, raise the exception
                    raise ex
            else:
                break

        # Extract the solution code from the response
        code = response['code']

        # Find the reCAPTCHA response element
        recaptcha_response_element = driver.find_element(By.ID, 'g-recaptcha-response')

        # Inject the solution into the page
        driver.execute_script('arguments[0].style.display = "block";', recaptcha_response_element)
        driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)

        # Trigger the reCAPTCHA callback (this may vary depending on the website)
        driver.execute_script(f'___grecaptcha_cfg.clients[0].P.P.callback("{code}")')

        # Allow time for the reCAPTCHA to process the solution
        time.sleep(2)
        
        # Optionally click the submit button if needed
        submit_button = driver.find_element(By.ID, 'submitBtn')
        submit_button.click()
        
        return True