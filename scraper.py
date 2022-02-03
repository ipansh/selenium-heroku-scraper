import scrapy
from scrapy import Selector
import requests
import pandas as pd
import time
from selenium import webdriver

def scrape_smartshanghai_listing(num_of_pages):
    """Function for scraping listing urls on the smart shanghai page."""

    listing_list = []

    for page in range(0,num_of_pages):
        url = 'https://www.smartshanghai.com/housing/apartments-rent/?page={}&bedrooms[0]=1&ownership_private=1&ownership_landlord=1&ownership_agency=1&view=list'.format(page)
        html = requests.get(url).text
    
        # Create a Selector selecting html as the HTML document
        sel = Selector(text = html)
    
        # Create a SelectorList of all div elements in the HTML document
        listings = sel.css('li.listing > a::attr(href)').extract()

        listing_list.extend(listings)

        return listing_list

def scrape_smartshanghai_data(listing_list):
    """Function for scraping data from each individual listing."""

    appended_data = []

    counter = 0

    for listing in listing_list:
        try:
            html = requests.get(listing).text
            sel = Selector(text = html)
        
            apartment_dict = {}

            apartment_dict['url'] = listing

            #1. ID
            apartment_dict['listing_id'] = listing[-7:]

            #2. Description
            description = sel.xpath('//div[@class = "listing-info"]/h1/text()').extract()[0].strip()
            apartment_dict['description'] = description

            #3. Price
            price = sel.xpath('//div[@class = "price"]/span[@class = "price"]/text()').extract()[0].strip('')
            price = int(price.replace(',',''))

            apartment_dict['price'] = price

            #4. Currency
            currency = sel.xpath('//div[@class = "price"]/span[@class = "currency"]/text()').extract()[0].strip()

            apartment_dict['currency'] = currency

            #5. Period
            period = sel.xpath('//div[@class = "price"]/span[@class = "periodType"]/text()').extract()[0].strip()
    
            apartment_dict['period'] = period

            #6. Posted
            posted_time = sel.xpath('//div[@class = "listing-info"]/div[@class = "posted-and-views"]/span[1]/text()').extract()[0].strip()
            apartment_dict['posted_time'] = posted_time

            #7. Type
            property_type = sel.xpath('//div[@class = "details"]/ul/li[1]/div/text()').extract()[0].strip()
            apartment_dict['property_type'] = property_type
    
            #8. Commission
            commission = sel.xpath('//div[@class = "details"]/ul/li[3]/div/text()').extract()[0].strip()
            apartment_dict['comission'] = commission
    
            #9. Bedrooms
            bedrooms = sel.xpath('//span[@itemprop="numberOfBedrooms"]/text()').extract()[0].strip()
            apartment_dict['bedrooms'] = bedrooms

            #10. Bathrooms
            bathrooms = sel.xpath('//span[@itemprop="numberOfBathroomsTotal"]/text()').extract()[0].strip()
            apartment_dict['bathrooms'] = bathrooms

            #11. Size
            size = sel.xpath('//div[@class = "details"]/ul/li[5]/div/text()').extract()[0].strip()
            apartment_dict['size'] = size
    
            #12. Floor
            floor = sel.xpath('//div[@class = "details"]/ul/li[6]/div/text()').extract()[0].strip()
            apartment_dict['floor'] = floor
    
            #13. Furnished
            furnished = sel.xpath('//div[@class = "details"]/ul/li[7]/div/text()').extract()[0].strip()
            apartment_dict['furnished'] = furnished
    
            #14. Windows
            windows = sel.xpath('//div[@class = "details"]/ul/li[8]/div/text()').extract()[0].strip()
            apartment_dict['windows'] = windows
    
            #15. District
            district = sel.xpath('//div[@class = "details"]/ul/li[9]/div/text()').extract()[0].strip()
            apartment_dict['district'] = district
    
            #16. Area
            area = sel.xpath('//div[@class = "details"]/ul/li[10]/div/text()').extract()[0].strip()
            apartment_dict['area'] = area
    
            #17. Metro
            metro = sel.xpath('//div[@class = "details"]/ul/li[12]/div/a[1]/text()').extract()[0].strip()
            apartment_dict['metro'] = metro

            #18. Metro Proximity
            metro_proximity = sel.xpath('//div[@class = "details"]/ul/li[12]/div/text()').extract()[0].strip()
            apartment_dict['metro_proxim'] = metro_proximity

            #19. Listing source
            list_source = sel.xpath('//p[@class = "agency-title"]/text()').extract()[0].strip()
            apartment_dict['list_source'] = list_source

            appended_data.append(apartment_dict)

            counter = counter+1
    
            if counter%15 == 0:
                print('Aggregated listings: {}.'.format(counter), end = ' ')
                #time.sleep(60)
        except:
            pass

        df = pd.DataFrame(appended_data)

        df = df.reset_index().rename(columns = {'index':'id'})

    return df


def scrape_wellcee_listings(selenium_driver):
    """Function for scraping data Wellceee's search page, implemented through Selenium."""

    selenium_driver.get("https://www.wellcee.com/rent-apartment/shanghai/list?cityId=15102233103895305#rentTypeIds=15103931190241306")
    selenium_response = selenium_driver.page_source

    new_selector = Selector(text=selenium_response)

    items = new_selector.xpath('//*[@class="house-item clearfix"]/a/@href').extract()

    items = list(set(['https://www.wellcee.com'+listing_id for listing_id in items]))

    return items


def scrape_wellcee_data(listing_list):
    appended_data = []

    counter = 0

    for url in listing_list:
        try:
            apartment_dict = {}

            text_response = requests.get(url).text
            sel = Selector(text = text_response)

            apartment_dict['url'] = url
            apartment_dict['price'] = sel.xpath('//p[@class = "price"]/text()').extract()[0].strip('Rent : ').strip('RMB/M')
            apartment_dict['location'] = sel.xpath('//p[@class = "house-address"]/text()').extract()[0]
            apartment_dict['district'] = sel.xpath('//span[@class = "breadcrumb-item"]/a/text()').extract()[2]
            apartment_dict['size'] = sel.xpath('//div[@class = "list clearfix"]/div/span/text()').extract()[7].strip('㎡')
            apartment_dict['floor'] = sel.xpath('//div[@class = "list clearfix"]/div/span/text()').extract()[11]

            appended_data.append(apartment_dict)

            counter = counter+1
    
            if counter%15 == 0:
                print('Aggregated listings: {}.'.format(counter), end = ' ')

        except:
            pass

    df = pd.DataFrame(appended_data)

    df = df.reset_index().rename(columns = {'index':'id'})

    return df