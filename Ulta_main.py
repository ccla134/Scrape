import requests
from bs4 import BeautifulSoup
import gspread

url = 'https://www.ulta.com/promotion/sale'
html = requests.get(url)

gc = gspread.service_account(filename='Creds.json')
sh = gc.open('TestScrapeSheet1')
sh = sh.get_worksheet(7)

count = 2
s = BeautifulSoup(html.content, 'html.parser')
results = s.find('ul', class_='ProductListingResults__productList ProductListingResults__productList--space--top')
product_link = results.find_all('a',  class_='Link_Huge Link_Huge--secondary')

for i in range (0, len(product_link)):
    print(product_link[i]['href'])
    html = requests.get(product_link[i]['href'])
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
    productVar = s.find_all('div', class_='ProductDimension')
    if len(productVar) == 0:
        productDem = 'N/A'
    else:
        productDem = productVar[len(productVar) - 1].find('span', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--black')
    reviewOver = s.find('div', class_='ReviewStars')
    review = reviewOver.find('span', class_='sr-only')
    review = review.get_text(strip=True, separator='').split(' ')
    imgDiv = s.find('div', class_='MediaWrapper__Image')
    print(imgDiv)
    if imgDiv is None:
        img = s.find('img', class_='MediaWrapper__Image_img')
    else:
        img = imgDiv.find('img', class_='MediaWrapper__Image_img')
    if price is None:
        # print(title.text, url, brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1], salePrice.text, orginalPrice.text, productDem.text, review[0], review[5] + ' ' + review[6], img['src'])
        print(title.text)
        print(brand.text)
        print(category[len(category) - 1].text)
        print(productNum.get_text(strip=True, separator='').split(' ')[1])
        print(salePrice.text)
        print(orginalPrice.text)
        print(productVar)
        print(review[0])
        print(review[5] + ' ' + review[6])
        print(img)
        if img is None:
            print()
        else:
            if len(productVar) == 0:
                sh.update('D' + str(count) + ':N' + str(count), [[brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1],  orginalPrice.text, salePrice.text, 'N/A', review[0], review[5] + ' ' + review[6], title.text, product_link[i]['href'], img['src']]])
                count = count + 1
            else:
                productDem = productVar[len(productVar) - 1].find('span', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--black')
                sh.update('D' + str(count) + ':N' + str(count), [[brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1],  orginalPrice.text, salePrice.text, productDem.text, review[0], review[5] + ' ' + review[6], title.text, product_link[i]['href'], img['src']]])
                count = count + 1
    else:
        print(title.text, url, brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1], price.text, productDem.text, img['src'])
        sh.update('D' + str(count) + ':N' + str(count), [[brand.text, category[len(category) - 1].text, productNum.get_text(strip=True, separator='').split(' ')[1], 'N/A', price.text, productDem.text, review[0], review[5] + ' ' + review[6], title.text, product_link[i]['href'], img['src']]])
        count = count + 1