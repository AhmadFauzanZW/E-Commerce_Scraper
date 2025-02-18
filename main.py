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
Products = []
Names = []
Ratings = []
Sales = []
Prices = []
Places = []

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

# Products name, rating, and seller
products = box.find_all('a', class_ = 'bl-link')

for i in products:
    product = i.text.strip()
    Products.append(product)
# print(Products)

# Products name
Names = [Products[i] for i in range(0, len(Products), 3)]
print(len(Names))

# Products rating
Ratings = [Products[i] for i in range(1, len(Products), 3)]
print(len(Ratings))

# Products sold volume
sales = box.find_all('p', class_ = 'bl-text bl-text--body-14 bl-text--subdued')

for i in sales:
    sold = i.text.strip()
    Sales.append(sold)

Solds = [Sales[i] for i in range(1, len(Sales), 2)]
print(len(Solds))

# Products price
prices = box.find_all('p', class_ = 'bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1')

for i in prices:
    price = i.text.strip()
    Prices.append(price)

print(len(Prices))

# Products seller location
places = box.find_all('div', class_ = 'bl-product-card__description-store')

for i in places:
    place = i.text.strip()
    Places.append(place)

print(len(Places))
