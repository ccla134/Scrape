import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as exceptions
import gspread

gc = gspread.service_account(filename='Creds.json')
sh = gc.open('TestScrapeSheet1')
sh = sh.get_worksheet(5)

# url = "https://www.gdit.com/careers/search/?q=bossier%20city"
# html_text = requests.get(url).text
# soup = BeautifulSoup(html_text, "html.parser")
# print(soup.prettify)
# for job in soup.find_all('h3'):
#     print(job)

gdit_url = "https://www.nike.com/w/mens-basketball-shoes-3glsmznik1zy7ok"
# ["https://www.gdit.com/careers/search/?q=bossier%20city",
#              "https://www.gdit.com/careers/search/?q=bossier%20city&page=2&",
#              "https://www.gdit.com/careers/search/?q=bossier%20city&page=3&",
#              "https://www.gdit.com/careers/search/?q=bossier%20city&page=4&"]
# length = len(gdit_urls)
# for i in range(length):
#     gdit_url = gdit_urls[i]
global driver
options = Options()
options.add_argument("start-maximized")
# options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option('useAutomationExtension', False)
try:
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(gdit_url)
    previous_height = 0
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # time.sleep(7)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # previous_height = driver.execute_script("return document.body.scrollHeight")
    # print(previous_height)
    time.sleep(5)
    while True: 
        previous_height = driver.execute_script('return document.body.scrollHeight')
        print(previous_height)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if previous_height == new_height:
            break
        
    #     # count = count + 1
    #     # print(count)


    page_source = driver.page_source
    s = BeautifulSoup(page_source, 'html.parser')
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
        

        if pic is None:
            print()
        else:
            pic = pic.find_all('img')
            if len(variation) == 0:
                if price is None:
                    price = s.find('div', class_='product-price is--current-price css-s56yt7 css-xq7tty')
                    orignalPrice = s.find('div', class_='product-price is--striked-out css-tpaepq')
                    percent = s.find('span', class_='css-1umcwok')
                    if percent is None:
                        if subtitle is None:
                            print(results.text, '', style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], shoe_link[i]['href'], pic[1]['src'])
                            sh.update('C' + str(count) + ':N' + str(count), [['', color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), 'N/A', '', '', '', results.text.strip(), shoe_link[i]['href'], pic[1]['src']]])
                            count = count + 1
                        else:
                            print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], shoe_link[i]['href'], pic[1]['src'])
                            sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), 'N/A', '', '', '', results.text.strip(), shoe_link[i]['href'], pic[1]['src']]])
                            count = count + 1
                    else:
                        if subtitle is None:
                            print(results.text, '', style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
                            sh.update('C' + str(count) + ':N' + str(count), [['', color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), percent.text.strip(), '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                            count = count + 1
                        else:
                            print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
                            sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), percent.text.strip(), '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                            count = count + 1
                else:
                    if subtitle is None:
                        print(results.text, '', style.text, color.text, price.text, shoe_link[i]['href'], pic[1]['src'])
                        sh.update('C' + str(count) + ':N' + str(count), [['', color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], 'N/A' ,  price.text.strip(), 'No Advertised Discount', '', '', '', results.text.strip(), shoe_link[i]['href'], pic[1]['src']]])
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
                            if subtitle is None:
                                print(results.text, '', style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], var['href'], pic[1]['src'])
                                sh.update('C' + str(count) + ':N' + str(count), [['', color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), 'N/A', '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                                count = count + 1
                            else:
                                print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], var['href'], pic[1]['src'])
                                sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), 'N/A', '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                                count = count + 1
                        else:
                            if subtitle is None:
                                print(results.text, '', style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
                                sh.update('C' + str(count) + ':N' + str(count), [['', color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), percent.text.strip(), '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                                count = count + 1
                            else:
                                print(results.text, subtitle.text, style.text, color.text, price.text, '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2], percent.text, var['href'], pic[1]['src'])
                                sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], '$' + orignalPrice.get_text(strip=True, separator='$').split('$')[2],  price.text.strip(), percent.text.strip(), '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                                count = count + 1
                    else:
                        if subtitle is None:
                            print(results.text, '', style.text, color.text, price.text, var['href'], pic[1]['src'])
                            sh.update('C' + str(count) + ':N' + str(count), [['', color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], 'N/A' ,  price.text.strip(), 'No Advertised Discount', '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                            count = count + 1
                        else:
                            print(results.text, subtitle.text, style.text, color.text, price.text, var['href'], pic[1]['src'])
                            sh.update('C' + str(count) + ':N' + str(count), [[subtitle.text.strip(), color.get_text(strip=True, separator='').split(': ')[1], style.get_text(strip=True, separator=':').split(' ')[1], 'N/A' ,  price.text.strip(), 'No Advertised Discount', '', '', '', results.text.strip(), var['href'], pic[1]['src']]])
                            count = count + 1
    driver.close()
except exceptions.WebDriverException:
    print('You need to download the new webdriver')
    