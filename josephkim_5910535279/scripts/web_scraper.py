import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


url = "https://www.cnbc.com/world/?region=world"

'''
response = requests.get(url, headers = {
    "User-Agent": "Mozilla/5.0"
    })
response.raise_for_status()
#print(response.text)
'''

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options = options)
driver.get(url)

time.sleep(6)

html = driver.page_source
driver.quit()


output = "../data/raw_data/web_data.html"


# write the html data into the raw_data directory
with open(output, "w", encoding="utf-8") as f: 
    f.write(html)


# print the first 10 ines of saved HTML
with open(output, "r", encoding="utf-8") as f:
    for i in range(10):
        print(f.readline().rstrip())

