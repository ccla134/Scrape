from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized")
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("htps://www.shreveporttimes.com")

print('finished')