from selenium import webdriver
import scraper
import os
from sqlalchemy import create_engine

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
selenium_driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
db_access_key = os.environ.get("POSTGRE")

if __name__ == "__main__":
    cnx = create_engine(db_access_key)

    print('Scraping in progress...', end = ' ')

    listing_list_result = scraper.scrape_wellcee_listings(selenium_driver)
    df = scraper.scrape_wellcee_data(listing_list_result)
    df.to_sql('wellcee_listings', cnx, schema = 'public', index = False, chunksize=100, if_exists='replace', method = 'multi')
    print('Wellcee data uploaded!')    

    listing_list_result = scraper.scrape_smartshanghai_listing(3)
    df = scraper.scrape_smartshanghai_data(listing_list_result)
    df.to_sql('smart_shanghai_listings', cnx, schema = 'public', index = False, chunksize=100, if_exists='replace', method = 'multi')
    print('Smart Shanghai data uploaded!')   

   