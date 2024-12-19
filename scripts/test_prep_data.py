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
headers_f=["ix"]+headers_f+["load_datetime"]

# close driver
driver.quit()

# read raw
raw=pd.read_csv(".\\outputs\\stock_prices_historical.csv", header=None)
raw.columns=headers_f

# format data
raw["load_date"]=raw["load_datetime"].apply(lambda x:x.split(" ")[0])
numcols=['_current_price', '_previous_close', '_52_week_high', '_52_week_low']
for col in numcols:
    raw[col]=raw[col].astype(float)

# get average, min, max per day
cleaned=raw.groupby(["load_date", "_symbol", "_name"]).agg(
    current_day_price_avg=('_current_price', 'mean')
    , current_day_price_min=('_current_price', 'min')
    , current_day_price_max=('_current_price', 'max')    
    , previous_day_close=('_previous_close', 'mean')
    , _52_wk_high_avg=('_52_week_high', 'mean')
    , _52_wk_low_avg=('_52_week_low', 'mean')
    , rec_count=('_symbol', 'count')
)

cleaned.to_csv(".\\outputs\\stock_prices_prepped_{}{:02d}{:02d}{:02d}{:02d}.csv".format(
    time.localtime().tm_year
    , time.localtime().tm_mon
    , time.localtime().tm_mday
    , time.localtime().tm_hour
    , time.localtime().tm_min
    )
    , index=False
)