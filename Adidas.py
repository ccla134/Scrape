import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as exceptions
import gspread

url = 'https://www.adidas.com/us/women-basketball-shoes'
html = requests.get(url)


s = BeautifulSoup(html.content, 'html.parser')

result = s.find('div', class_='plp-grid__1FP1J')
urls = result.find_all('a')

print(urls)