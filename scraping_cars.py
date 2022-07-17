# importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

# defining the headers
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

all_url_links = []
car_name = []
# function to make request
def get_request(page):
    base_url = f"https://www.houseofcars.co.ke/stock-list/page/{page}/"
    
    response = requests.get(base_url, headers=header)
    
    # soup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # extracting the links
    container_wrap = soup.find_all('div', attrs={'class':'car-content'})
    
    for wrap in container_wrap:
        car_title = wrap.find('a')
        car_url = car_title['href']
        all_url_links.append(car_url) # appending the url of each car
        car_name.append(car_title.text) # appending the name of each car
        
    sleep_time = range(5, 13)
    random_time = random.choice(sleep_time)
    time.sleep(random_time)
        
    print(f"Finished getting data from page {page}")
    print(f'Waited {random_time} seconds!')
    
# function to get data from each car link
def get_car_details(url_link, row):
    global cars_dataframe_df
    global cars_title
    response = requests.get(url_link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # price
    car_price = soup.find_all('span', attrs={'class':'new-price'})
    if car_price:
        car_price = car_price[-1].text
    
    # year
    year = soup.find('li', attrs={'class':'car_year'})
    if year:
        year = year.text
    
    # make
    make = soup.find('li', attrs={'class':'car_make'})
    if make:
        make = make.text
    
    # model
    model = soup.find('li', attrs={'class':'car_model'})
    if model:
        model = model.text
    
    # body style
    body_style = soup.find('li', attrs={'class':'car_body_style'})
    if body_style:
        body_style = body_style.find('strong').text
    
    # car condition
    condition = soup.find('li', attrs={'class':'car_condition'})
    if condition:
        condition = condition.find('strong').text
    
    # mileage
    mileage = soup.find('li', attrs={'class':'car_mileage'})
    if mileage:
        mileage = mileage.find('strong').text
    
    # transmission type
    transmission = soup.find('li', attrs={'class':'car_transmission'})
    if transmission:
        transmission = transmission.find('strong').text
    
    # engine power
    engine = soup.find('li', attrs={'class':'car_engine'})
    if engine:
        engine = engine.find('strong').text    
    
    # fuel type
    fuel_type = soup.find('li', attrs={'class':'car_fuel_type'})
    if fuel_type:
        fuel_type = fuel_type.find('strong').text
    
    # exterior color
    exterior_color = soup.find('li', attrs={'class':'car_exterior_color'})
    if exterior_color:
        exterior_color = exterior_color.find('strong').text
    
    # interior color
    interior_color = soup.find('li', attrs={'class':'car_interior_color'})
    if interior_color:
        interior_color = interior_color.find('strong').text
    
    # stock number
    stock_number = soup.find('li', attrs={'class':'car_stock_number'})
    if stock_number:
        stock_number = stock_number.find('strong').text
    
    # vin number
    vin_number = soup.find('li', attrs={'class':'car_vin_number'})
    if vin_number:
        vin_number = vin_number.find('strong').text
    
    # appending details to the dataframe
    row_data = pd.DataFrame({'Car Name': cars_title[row],'Price': car_price, 'Year': year, 'Car Make': make, 'Car Model': model,
                             'Body Style': body_style, 'Condition Status': condition, 'Mileage': mileage,
                             'Transmission Type': transmission, 'Engine Power': engine, 'Fuel Type': fuel_type, 
                             'Exterior Color': exterior_color, 'Interior Color': interior_color, 
                             'Stock Number': stock_number, 'Vin Number': vin_number}, index=[row])
    
    # concatenating the dataframe
    cars_dataframe_df = pd.concat([cars_dataframe_df, row_data])
    
    sleep_time = range(3, 8)
    random_time = random.choice(sleep_time)
    time.sleep(random_time)
        
    print(f"Finished extracting from {make}, {row}")
    print(f'Waited {random_time} seconds!')
    
if __name__ == "__main__":
    print("Start of making requests...")
    
    # number of pages 
    number_of_pages = 12
    
    # finding if dataframe csv already exists or not
    list_path = os.listdir('H:\WORK\Pixel Tech\Pixel Academy\Side-Projects\Car Website Scraper')
    # let name of our csv be cars_for_sale.csv
    if 'cars_for_sale.csv' not in list_path:
        page_requests = [get_request(page) for page in range(1, number_of_pages+1)]
        # saving it to csv
        cars = {'Car Name':car_name, 'Car URL': all_url_links}
        cars_dataframe = pd.DataFrame(cars)
        # saving to csv
        cars_dataframe.to_csv('cars_for_sale.csv')
    else: # means the file already exists, we import it
        print()
        cars_dataframe = pd.read_csv('cars_for_sale.csv')
        
    # find which option was used
    if len(all_url_links) == 0:
        all_url_links = list(cars_dataframe['Car URL'])
        cars_title = list(cars_dataframe['Car Name'])
        
    cars_dataframe_df = pd.DataFrame()
    # parse each link and extract data
    car_details = [get_car_details(url_link, row) for row,url_link in enumerate(all_url_links)]
    