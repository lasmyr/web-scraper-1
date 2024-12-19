from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import pandas as pd


# Initialize WebDriver
options = Options()
options.headless = True  # Optional: Run headless (without UI)
driver = webdriver.Chrome(options=options)

# Open the page
driver.get('https://www.pesobility.com/stock')
time.sleep(10)

# Get headers
heads=driver.find_elements(By.XPATH, '//thead//th')
headers=[]
for i in range(0, len(heads)):
    headers.append(heads[i].text)
headers_f=["_"+x.replace(" ", "_").replace("(%)", "").replace("-", "_").lower().strip("_") for x in headers]

# get data
tables = driver.find_elements(By.XPATH, '//tbody')
data=tables[3].find_elements(By.TAG_NAME, "td") # table is the 3rd table 

# extract cell values from table element
data_values=list()
for i in range(0, len(data)):
    val=data[i].text
    data_values.append(val)

# create a table based on len(headers)
stock_prices = pd.DataFrame([data_values[i:i+len(headers)] for i in range(0, len(data_values), len(headers))], columns=[headers_f])

# format data
stock_prices._current_price=stock_prices._current_price.apply(lambda x:x.str.split(" ").str[0].astype(float))
stock_prices._previous_close=stock_prices._previous_close.apply(lambda x:x.str.split(" ").str[0].astype(float))
stock_prices._52_week_high=stock_prices._52_week_high.apply(lambda x:x.str.split(" ").str[0].astype(float))
stock_prices._52_week_low=stock_prices._52_week_low.apply(lambda x:x.str.split(" ").str[0].astype(float))

# add load datetime
stock_prices["load_datetime"]="{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
    time.localtime().tm_year
    , time.localtime().tm_mon
    , time.localtime().tm_mday
    , time.localtime().tm_hour
    , time.localtime().tm_min
    , time.localtime().tm_sec
)
print(time.localtime())

# save to outpath
# if not os.path.isdir("\web-scraping-1\outputs"):
#     os.mkdir(os.getcwd()+"\\outputs")
#     print("{} path created".format(os.getcwd()+"\\outputs"))
outpath=".\\outputs\\stock_prices_historical.csv"

# outpath=os.path.dirname(os.getcwd())+"\\outputs\\stock_prices_historical.csv"
stock_prices.to_csv(outpath,mode='a', header=False)

# close driver
driver.quit()