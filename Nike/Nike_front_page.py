import requests
from selectolax.parser import HTMLParser
import chompjs
from bs4 import BeautifulSoup
import pandas as pd
import gspread
import time
import urllib3
import random
from Creds import username, password
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.proxy import Proxy, ProxyType #type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore

from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import selenium.common.exceptions as exceptions # type: ignore

gc = gspread.service_account(filename='trust-pilot-2023-830eb4f2e9b2.json')

sh = gc.open('Nike Column Write Order').get_worksheet(0)

sh.update('A' + str(1) + ':W' + str(1), [["Vendor Image", "Title", "UPC", "Product ID", "Full Price", "Current Price", "Discount", "Sub_Title", "Color Description", "Description", "Nike Size", "Brand", "Discounted", "Style Color", "Style Code", "Preorder", "Gender", "Product Type", "Product Group ID", "Status", "Full Title","URL", "Image_URL"]])
row = 2

# url = 'https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok'
# url = 'https://www.nike.com/w/sale-shoes-3yaepzy7ok'
url = 'https://www.nike.com/w/sale-shoes-3yaepzy7ok'

state = 'us_louisiana'
session = random.random()
session_time = 15
entry = ('http://customer-%s-st-%s-sessid-%s-sesstime-%d:%s@pr.oxylabs.io:7777' %
    (username, state, session, session_time, password))

proxies = {
    "http": entry,
    "https": entry
}

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': entry,
    'sslProxy': entry,
    'noProxy': ''
})

global driver
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 dtm_reg_debug 898_1711468096499")
options.proxy = proxy
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Remote(command_executor="http://192.168.1.145:4444", options=options)

try:
    driver.get(url)

   
    time.sleep(7)
    previous_height = driver.execute_script('return document.body.scrollHeight')
    count = 0
    while count <= 5:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        driver.execute_script("window.scroll(0,-500);")
        time.sleep(4)
        count = count + 1
        print(count)


    page_source = driver.page_source
    driver.quit()
except exceptions.WebDriverException:
    print('You need to download the new webdriver')

s = BeautifulSoup(page_source, 'html.parser')
results = s.find(id='skip-to-products')
shoe_link = results.find_all('a', class_='product-card__img-link-overlay')


for i in range(0, len(shoe_link)):
    resp = requests.get(shoe_link[i]['href'], proxies=proxies)


    s = BeautifulSoup(resp.content, 'html.parser')
    style = s.find('li', class_='description-preview__style-color ncss-li').get_text(strip=True, separator=':').split(' ')[1]
    variation = s.find_all('div', class_='css-b8rwz8 tooltip-component-container')
    pic = s.find('div', class_='css-1rayx7p')
    pic = pic.find_all('img')

    html = HTMLParser(resp.text)
    data = html.css("script[type = 'application/json']")

    product = chompjs.parse_js_object(data[0].text())

    if len(variation) == 0:
        print(style)
        one = product['props']['pageProps']['initialState']['Threads']['products'][style]['skus']
        productId = product['props']['pageProps']['initialState']['Threads']['products'][style]['productId']
        width = product['props']['pageProps']['initialState']['Threads']['products'][style]['width']
        styleCode = product['props']['pageProps']['initialState']['Threads']['products'][style]['styleCode']
        category = product['props']['pageProps']['initialState']['Threads']['products'][style]['category']
        preOrder = product['props']['pageProps']['initialState']['Threads']['products'][style]['preOrder']
        genders = product['props']['pageProps']['initialState']['Threads']['products'][style]['genders']
        brand = product['props']['pageProps']['initialState']['Threads']['products'][style]['brand']
        productType = product['props']['pageProps']['initialState']['Threads']['products'][style]['productType']
        productGroupId = product['props']['pageProps']['initialState']['Threads']['products'][style]['productGroupId']
        status = product['props']['pageProps']['initialState']['Threads']['products'][style]['status']
        subTitle = product['props']['pageProps']['initialState']['Threads']['products'][style]['subTitle']
        fullTitle = product['props']['pageProps']['initialState']['Threads']['products'][style]['fullTitle']
        colorDescription = product['props']['pageProps']['initialState']['Threads']['products'][style]['colorDescription']
        descriptionPreview = product['props']['pageProps']['initialState']['Threads']['products'][style]['descriptionPreview']
        discounted = product['props']['pageProps']['initialState']['Threads']['products'][style]['discounted']

        # print(one)

        for x in range(len(one)):
            nikeSize = one[x]['nikeSize']
            gtin = one[x]['gtin']
            price = product['props']['pageProps']['initialState']['Threads']['products'][style]['fullPrice']
            curPrice = product['props']['pageProps']['initialState']['Threads']['products'][style]['currentPrice']
            try:
                discountCal = round((float(price) - float(curPrice)) / float(price), 2) * 100
            except:
                discountCal = 99.9
            # sh.update('A' + str(row), "=IMAGE(R" + str(row) +",4, 125, 100)", raw=False)
            time.sleep(1)
            sh.update('A' + str(row) + ':W' + str(row), [["=IMAGE(W" + str(row) +",4, 125, 100)", "=hyperlink(V" + str(row)+ ",U" + str(row)+")", gtin, productId, price, curPrice, discountCal, subTitle, colorDescription, descriptionPreview, nikeSize, brand, discounted, style, styleCode, preOrder, 'genders', productType, productGroupId, status, fullTitle, url, pic[1]['src']]], raw=False)
            row = row + 1
            print(nikeSize, gtin, price, curPrice, discountCal, productId, width, style, styleCode, category, preOrder, genders, brand, productType, productGroupId, status, subTitle, fullTitle, colorDescription, descriptionPreview, discounted, url, pic[1]['src'])
    else:
        for i in range(0, len(variation)):
            var = variation[i].find('a')
            html = requests.get(var['href'], proxies=proxies)
            s = BeautifulSoup(html.content, 'html.parser')
            style = s.find('li', class_='description-preview__style-color ncss-li').get_text(strip=True, separator=':').split(' ')[1]
            pic = s.find('div', class_='css-1rayx7p')
            pic = pic.find_all('img')

            print(style)
            one = product['props']['pageProps']['initialState']['Threads']['products'][style]['skus']
            productId = product['props']['pageProps']['initialState']['Threads']['products'][style]['productId']
            width = product['props']['pageProps']['initialState']['Threads']['products'][style]['width']
            styleCode = product['props']['pageProps']['initialState']['Threads']['products'][style]['styleCode']
            category = product['props']['pageProps']['initialState']['Threads']['products'][style]['category']
            preOrder = product['props']['pageProps']['initialState']['Threads']['products'][style]['preOrder']
            genders = product['props']['pageProps']['initialState']['Threads']['products'][style]['genders']
            brand = product['props']['pageProps']['initialState']['Threads']['products'][style]['brand']
            productType = product['props']['pageProps']['initialState']['Threads']['products'][style]['productType']
            productGroupId = product['props']['pageProps']['initialState']['Threads']['products'][style]['productGroupId']
            status = product['props']['pageProps']['initialState']['Threads']['products'][style]['status']
            subTitle = product['props']['pageProps']['initialState']['Threads']['products'][style]['subTitle']
            fullTitle = product['props']['pageProps']['initialState']['Threads']['products'][style]['fullTitle']
            colorDescription = product['props']['pageProps']['initialState']['Threads']['products'][style]['colorDescription']
            descriptionPreview = product['props']['pageProps']['initialState']['Threads']['products'][style]['descriptionPreview']
            discounted = product['props']['pageProps']['initialState']['Threads']['products'][style]['discounted']

            # print(one)

            for x in range(len(one)):
                nikeSize = one[x]['nikeSize']
                gtin = one[x]['gtin']
                price = product['props']['pageProps']['initialState']['Threads']['products'][style]['fullPrice']
                curPrice = product['props']['pageProps']['initialState']['Threads']['products'][style]['currentPrice']
                try:
                    discountCal = round((float(price) - float(curPrice)) / float(price), 2) * 100
                except:
                    discountCal = 99.9
                time.sleep(1)
                # sh.update('A' + str(row) + ':W' + str(row), [["=IMAGE(W" + str(row) +",4, 125, 100)", "=hyperlink(V" + str(row)+ ",U" + str(row)+")", subTitle, colorDescription, descriptionPreview, gtin, nikeSize, brand, discounted, price, curPrice, discountCal, style, styleCode, preOrder, 'genders', productType, productGroupId, status, productId, fullTitle, var['href'], pic[1]['src']]], raw=False)
                sh.update('A' + str(row) + ':W' + str(row), [["=IMAGE(W" + str(row) +",4, 125, 100)", "=hyperlink(V" + str(row)+ ",U" + str(row)+")", gtin, productId, price, curPrice, discountCal, subTitle, colorDescription, descriptionPreview, nikeSize, brand, discounted, style, styleCode, preOrder, 'genders', productType, productGroupId, status, fullTitle, var['href'], pic[1]['src']]], raw=False)
                row = row + 1
                print(nikeSize, gtin, price, curPrice, discountCal, productId, width, style, styleCode, category, preOrder, genders, brand, productType, productGroupId, status, subTitle, fullTitle, colorDescription, descriptionPreview, discounted, var['href'], pic[1]['src'])

print("Item count written: ", row - 1)