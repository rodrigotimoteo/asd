import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import ChromiumOptions
import json
from datetime import date
import schedule
import time

CHROMEDRIVER_PATH = "./chromedriver"
SAVE_TO_CSV = True
PRICES_CSV = "prices.csv"
iphone_array = []


def load_urls():
    with open('urls.json') as f:
        data = json.load(f)

    for item in data['url']:
        iphone = {"model": None, "url": None}
        iphone['model'] = item['model']
        iphone['url'] = item['url']
        iphone_array.append(iphone)


def search():
    for iphone in iphone_array:
        options = ChromiumOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

        driver.get(iphone['url'])

        cost = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/main/div[1]/div[2]/div[1]/div[2]/div['
                                             '1]/div[2]/div/p').text
        cost = int(cost.split(' ')[0])
        currentDate = date.today()
        pricefound = False

        for p in seen_prices:
            if p['model'] == iphone['model'] and p['date'] == currentDate:
                if cost < p['cost']:
                    p['cost'] = cost
                pricefound = True
                break
        if not pricefound:
            seen_prices.append({'model': iphone['model'], 'cost': cost, 'date': currentDate})

    with open('price_history.csv', 'w', newline='') as csvfile:
        fieldnames = ['model', 'cost', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for price in seen_prices:
            writer.writerow(price)


load_urls()
seen_prices = []
search()
schedule.every().hour.do(search)
while 1:
    schedule.run_pending()
    time.sleep(1)
