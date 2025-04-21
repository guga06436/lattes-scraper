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

def process_single_url(url, driver, captcha_solver):
    """
    Process a single URL to scrape data from the Lattes platform.
    
    Args:
        url (str): URL to process
        driver: WebDriver instance
        captcha_solver: CaptchaSolver instance
        
    Returns:
        dict: Scraped data from the URL
    """
    driver.get(url)
    driver.maximize_window()
    
    time.sleep(1)
    
    print("Solving Captcha...")
    # Solve captcha if present
    captcha_solver.solve_recaptcha(driver)
    print("Captcha Solved!")
    
    time.sleep(2)
    
    # Perform scraping
    print("Scraping Data...")
    scraper = LattesScraper(driver)
    scraped_data = scraper.scrap_lattes_data()
    print("Data Scraped!")
    
    return scraped_data

def main_url(url):
    """
    Process a single URL to scrape data from the Lattes platform.
    
    Args:
        url (str): The URL of the page to scrape.
    """
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)
    
    # Initialize the WebDriver and CaptchaSolver
    driver_manager = WebDriverManager()
    driver = driver_manager.setup_driver()
    
    captcha_solver = CaptchaSolver(API_KEY)
    
    try:
        # Process single URL
        scraped_data = process_single_url(url, driver, captcha_solver)
        
        # Convert the scraped data into a DataFrame
        df = pd.DataFrame([scraped_data])
        
        # Save the DataFrame to CSV file
        df.to_csv('data/sample.csv', index=False)
        
        print(f"Scraped data saved to data/sample.csv")
    
    finally:
        driver_manager.close_driver()

def main_csv(csv_file):
    """
    Process multiple URLs from a CSV file to scrape data from the Lattes platform.
    
    Args:
        csv_file (str): The path to a CSV file containing URLs to scrape.
    """
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)
    
    # Initialize the WebDriver and CaptchaSolver
    driver_manager = WebDriverManager()
    driver = driver_manager.setup_driver()
    
    captcha_solver = CaptchaSolver(API_KEY)
    
    try:
        # Read data csv
        df = pd.read_csv(csv_file)
        
        # Create an empty df for output and fail
        df_output = pd.DataFrame()
        df_fail = pd.DataFrame(columns=df.columns)
        
        # Filter only non null lattes
        df = df[df.lattes.notna()]
        
        for index, row in df.iterrows():
            try:
                url = row['lattes']
                scraped_data = process_single_url(url, driver, captcha_solver)
                
                # Combine the original row with scraped data
                combined_data = row.to_dict()  
                combined_data.update(scraped_data)
                
                # Append to df_output
                df_output = pd.concat([df_output, pd.DataFrame([combined_data])], ignore_index=True)       
                
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                # Add to fail DataFrame
                df_fail.loc[len(df_fail)] = row
        
        # Save the DataFrames to CSV file
        df_output.to_csv('data/sample_success.csv', index=False)
        df_fail.to_csv('data/sample_fail.csv', index=False)
        
        # Log
        print(f"Processed {len(df_output)} successfully and {len(df_fail)} failed")
        print(f"Success data saved to data/sample_success.csv")
        print(f"Failed data saved to data/sample_fail.csv")
    
    finally:
        driver_manager.close_driver()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape data from a Lattes platform page.')
    parser.add_argument('--mode', required=True, choices=['url', 'csv'], 
                        help='The mode to run the script: "url" for a single URL or "csv" for multiple URLs from a CSV file')
    parser.add_argument('--input', required=True, 
                        help='The input value: a URL when mode is "url" or a path to a CSV file when mode is "csv"')

    # Parse the arguments from the terminal
    args = parser.parse_args()

    # Call the appropriate function based on the mode
    if args.mode == 'url':
        main_url(args.input)
    elif args.mode == 'csv':
        main_csv(args.input)