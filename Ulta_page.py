import requests
from bs4 import BeautifulSoup
import gspread

gc = gspread.service_account(filename='Creds.json')
sh = gc.open('TestScrapeSheet1')
sh = sh.get_worksheet(7)

url = 'https://www.ulta.com/p/hydrate-sheer-shampoo-pimprod2017793?sku=2565103'
html = requests.get(url)
s = BeautifulSoup(html.content, 'html.parser')
title = s.find('span', class_='Text-ds Text-ds--title-5 Text-ds--left')
brand = s.find('a', class_='Link_Huge Link_Huge--compact')
list = s.find('ul', id='Breadcrumbs__List')
category = list.find_all('a', class_='Link_Huge Link_Huge--secondary')
info = s.find('div', class_='ProductInformation')
productNum = info.find('p', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600')
pricing = s.find('div', class_='ProductPricing')
salePrice = pricing.find('span', class_='Text-ds Text-ds--title-6 Text-ds--left Text-ds--magenta-500')
orginalPrice = pricing.find('span', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600 Text-ds--line-through')
price = pricing.find('span',  class_='Text-ds Text-ds--title-6 Text-ds--left Text-ds--black')
productVar = s.find('div', class_='ProductDimension')
productDem = productVar.find('span', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--black')
reviewOver = s.find('div', class_='ReviewStars')
review = reviewOver.find('span', class_='sr-only')
review = review.get_text(strip=True, separator='').split(' ')
img = s.find('img', class_='MediaWrapper__Image_img')

if price is None:
    print(title.text, url, brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1], salePrice.text, orginalPrice.text, productDem.text, review[0], review[5] + ' ' + review[6], img['src'])
    sh.update('D' + str(2) + ':N' + str(2), [[brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1],  orginalPrice.text, salePrice.text, productDem.text, review[0], review[5] + ' ' + review[6], title.text, url, img['src']]])
else:
    print(title.text, url, brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1], price.text, productDem.text, img['src'])
    sh.update('D' + str(2) + ':N' + str(2), [[brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1], 'N/A', price.text, productDem.text, review[0], review[5] + ' ' + review[6], title.text, url, img['src']]])
    