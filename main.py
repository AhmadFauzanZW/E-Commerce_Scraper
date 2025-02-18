# Program Web Scraper - Bukalapak

# Import Modules
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Deklarasi Variable
URL = f'https://www.bukalapak.com/c/handphone/hp-smartphone/hp-android?page={str(1)}&search%5Bsort_by%5D=weekly_sales_ratio%3Adesc'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

Links = []
Names = []

# Inisialisasi Get Request dan BeautifulSoup ke url website
r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html5lib')

# Selected Box untuk di scrape (main canvas)
box = soup.find('div', class_ = 'bl-flex-item bl-product-list-wrapper')

# Products link
links = box.find_all('a', class_ = 'slide')

for i in links:
    link = i.get('href')
    Links.append(link)
print(len(Links))

# Products name
names = box.find_all('a', class_ = 'bl-link')

for i in names[0]:
    name = i.text.strip()
    Names.append(name)
print(Names)

# print(box)