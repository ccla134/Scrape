
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as exceptions
import gspread

urls = ['https://www.adidas.com/us/women-basketball-shoes',
        'https://www.adidas.com/us/women-basketball-shoes?start=48',
        'https://www.adidas.com/us/women-basketball-shoes?start=96']

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# response = requests.get(url, headers=headers)

# 

# result = s.find('div', class_='container')
# # #urls = result.find_all('a')

# print(s)

global driver
options = Options()
options.add_argument("start-maximized")
# options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option('useAutomationExtension', False)

page_source = ['', '', '']
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
for i in range(0, len(urls)):
    driver.get(urls[i])
    page_source[i] = driver.page_source

for i in range (0, len(page_source)):
    s = BeautifulSoup(page_source[i], 'html.parser')
    result = s.find('div', class_='product-container___3GvlZ')
    cards = result.find_all('div', class_='glass-product-card__assets')

    for j in range(0, len(cards)):
        url = cards[j].find('a')
        if url['href'].split('/')[1] == 'us':
            url = 'https://www.adidas.com/' + url['href']
        else:
            url = url['href']
        driver.get(url)
        dump = driver.page_source
        d = BeautifulSoup(dump, 'html.parser')
        title = d.find('h1', class_='name___120FN')
        print(title, url)
driver.close()


