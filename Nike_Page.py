import requests
from bs4 import BeautifulSoup

url = 'https://www.nike.com/t/air-max-terrascape-97-mens-shoes-DCLQCN/DJ5019-004'
html = requests.get(url)


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
            print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], pic[1]['src'])
        else:
            print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, pic[1]['src'])
    else:
        print(results.text, subtitle.text, style.text, color.text, price.text, pic[1]['src'])
else:
    for i in range(0, len(variation)):
        var = variation[i].find('a')
        pic = variation[i].find('img')
        html = requests.get(var['href'])
        s = BeautifulSoup(html.content, 'html.parser')
        results = s.find('h1', id='pdp_product_title')
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
                print(results.text, subtitle.text, style.get_text(strip=True, separator=':').split(' ')[1], color.get_text(strip=True, separator='').split(': ')[1], price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], var['href'], pic[1]['src'])
            else:
                if subtitle is None:
                    print(results.text, style.get_text(strip=True, separator=':').split(' ')[1], color.get_text(strip=True, separator='').split(': ')[1], price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
                else:
                    print(results.text, subtitle.text, style.get_text(strip=True, separator=':').split(' ')[1], color.get_text(strip=True, separator='').split(': ')[1], price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
        else:
            print(results.text, subtitle.text, style.get_text(strip=True, separator=':').split(' ')[1], color.get_text(strip=True, separator='').split(': ')[1], price.text, var['href'], pic[1]['src'])