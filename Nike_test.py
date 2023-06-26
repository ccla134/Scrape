import requests
from bs4 import BeautifulSoup
import gspread

url = 'https://www.nike.com/w/mens-summer-ready-sale-over-150-jordan-low-top-shoes-37eefz44tviz7hf8ezabwsqznik1zy7ok'
html = requests.get(url)
gc = gspread.service_account(filename='Creds.json')
sh = gc.open('TestScrapeSheet1').sheet1

s = BeautifulSoup(html.content, 'html.parser')
count = 2
results = s.find(id='skip-to-products')
shoe_link = results.find_all('a',  class_='product-card__img-link-overlay')
# shoe_title = results.find_all('div', class_='product-card__title')
# shoe_subtitle = results.find_all('div', class_='product-card__subtitle')
# shoe_colors = results.find_all('div', class_='product-card__product-count font-override__body1')
# shoe_currentprice = results.find_all('div', class_='product-price us__styling is--current-price css-11s12ax')
# shoe_currentprice2 = results.find_all('div', class_='product-price is--current-price css-1ydfahe')

for i in range(0, len(shoe_link)):
    html = requests.get(shoe_link[i]['href'])
    s = BeautifulSoup(html.content, 'html.parser')
    results = s.find('h1', id='pdp_product_title')
    subtitle = s.find('h2', class_='headline-5 pb1-sm d-sm-ib')
    style = s.find('li', class_='description-preview__style-color ncss-li')
    color = s.find('li', class_='description-preview__color-description ncss-li')
    price = s.find('div', class_='product-price css-11s12ax is--current-price css-tpaepq')
    variation = s.find_all('div', class_='css-b8rwz8 tooltip-component-container')

    pic = s.find('div', class_='css-1rayx7p')
    pic = pic.find_all('img')

    if len(variation) == 0:
        if price is None:
            price = s.find('div', class_='product-price is--current-price css-s56yt7 css-xq7tty')
            orignalPrice = s.find('div', class_='product-price is--striked-out css-tpaepq')
            percent = s.find('span', class_='css-1umcwok')
            if percent is None:
                print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], shoe_link[i]['href'], pic[1]['src'])
                sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), 'N/A', '', '', '', results.text.strip(), shoe_link[i]['href'], pic[1]['src']]])
                count = count + 1
            else:
                print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, shoe_link[i]['href'], pic[1]['src'])
                sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), percent.text.strip(), '', '', '', results.text.strip(), shoe_link[i]['href'], pic[1]['src']]])
                count = count + 1
        else:
            print(results.text, subtitle.text, style.text, color.text, price.text, shoe_link[i]['href'], pic[1]['src'])
            sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], 'N/A' ,  price.text.strip(), 'No Advertised Discount', '', '', '', results.text.strip(), shoe_link[i]['href'], pic[1]['src']]])
            count = count + 1
    else:
        for j in range(0, len(variation)):
            var = variation[j].find('a')
            pic = variation[j].find('img')
            html = requests.get(var['href'])
            s = BeautifulSoup(html.content, 'html.parser')
            results = s.find('h1', id='pdp_product_title')
            subttile = s.find('h2', class_='headline-5 pb1-sm d-sm-ib')
            style = s.find('li', class_='description-preview__style-color ncss-li')
            color = s.find('li', class_='description-preview__color-description ncss-li')
            price = s.find('div', class_='product-price css-11s12ax is--current-price css-tpaepq')
            pic = s.find('div', class_='css-1rayx7p')
            pic = pic.find_all('img')
            if price is None:
                price = s.find('div', class_='product-price is--current-price css-s56yt7 css-xq7tty')
                orignalPrice = s.find('div', class_='product-price is--striked-out css-tpaepq')
                percent = s.find('span', class_='css-1umcwok')
                if percent is None:
                    print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], var['href'], pic[1]['src'])
                    sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), 'N/A', '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                    count = count + 1
                else:
                    print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
                    sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), percent.text.strip(), '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                    count = count + 1
            else:
                print(results.text, subtitle.text, style.text, color.text, price.text, var['href'], pic[1]['src'])
                sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], 'N/A' ,  price.text.strip(), 'No Advertised Discount', '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                count = count + 1