from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('chromedriver.exe')
# 예금상품 url
url = 'https://www.kfcc.co.kr/goods/goods01_main.do'
driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())