from selenium import webdriver
import scraper
import os
from sqlalchemy import create_engine, text
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
selenium_driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
db_access_key = os.environ.get("POSTGRE")

if __name__ == "__main__":
    cnx = create_engine(db_access_key)

    sql = '''select * from public.wellcee_listings;'''

    query = text(sql)
    current_df = pd.read_sql_query(query, cnx)

    print('Scraping in progress...', end = ' ')

    listing_list_result = scraper.scrape_wellcee_listings(selenium_driver)
    print(listing_list_result)		
    df = scraper.scrape_wellcee_data(listing_list_result)
    final_df = pd.concat([current_df,df]).drop_duplicates().drop(columns = ['id']).reset_index().rename(columns = {'index':'id'})
    print(final_df)
    final_df.to_sql('wellcee_listings', cnx, schema = 'public', index = False, chunksize=100, if_exists='replace', method = 'multi')

    print('Wellcee data uploaded!')

    ### SMARTSHANGHAI
    sql = '''select * from public.smart_shanghai_listings;'''

    query = text(sql)
    current_df = pd.read_sql_query(query, cnx)

    print('Scraping in progress...', end = ' ')

    listing_list_result = scraper.scrape_smartshanghai_listing(3)
    print(listing_list_result)		
    df = scraper.scrape_smartshanghai_data(listing_list_result)
    final_df = pd.concat([current_df,df]).drop_duplicates().drop(columns = ['id']).reset_index().rename(columns = {'index':'id'})
    print(final_df)
    final_df.to_sql('smart_shanghai_listings', cnx, schema = 'public', index = False, chunksize=100, if_exists='replace', method = 'multi')

    print('Smart Shanghai data uploaded!')