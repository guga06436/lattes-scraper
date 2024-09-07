import os
import argparse
import time
from dotenv import load_dotenv
import pandas as pd
from drivers.web_driver import WebDriverManager
from captcha.captcha_solver import CaptchaSolver
from scrapers.lattes_scraper import LattesScraper

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

def main(url):
    """
    Coordinates the setup, captcha-solving, and scraping of data from the Lattes platform.

    Args:
        url (str): The URL of the page to scrape.

    Steps:
        1. Initializes and starts the WebDriver.
        2. Solves the captcha using CaptchaSolver.
        3. Scrapes data using LattesScraper.
        4. Closes the WebDriver.

    Example Usage:
        Run this file from the terminal with the required arguments:
        $ python main.py --url "your_url_here"
    """
    
    # Initialize the WebDriver and CaptchaSolver
    driver_manager = WebDriverManager()
    driver = driver_manager.setup_driver()
    
    captcha_solver = CaptchaSolver(API_KEY)

    try:
        driver.get(url)
        driver.maximize_window()
        
        time.sleep(1)
        
        print("Solving Captcha...")
        # Solve captcha if present
        captcha_solver.solve_recaptcha(driver)
        print("Captcha Solved!")
        
        time.sleep(2)
        
        # Perform scraping
        print("Scrapping Data...")
        scraper = LattesScraper(driver)
        scraped_data = scraper.scrap_lattes_data()
        print("Data Scrapped!")

        # Convert the scraped data into a DataFrame
        df = pd.DataFrame([scraped_data])

        # Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)

        # Save the DataFrame to CSV file
        df.to_csv('data/sample.csv', index=False)

        print(f"Scraped data saved to data/sample.csv")
    
    finally:
        driver_manager.close_driver()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape data from a Lattes platform page.')
    parser.add_argument('--url', required=True, help='The URL of the Lattes platform page to scrape.')

    # Parse the arguments from the terminal
    args = parser.parse_args()

    # Call the main function with the provided URL
    main(args.url)