# Program Web Scraper - Bukalapak

# Import Modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Deklarasi Variable
Products = []
Links = []
Names = []
Ratings = []
Sales = []
Prices = []
Places = []

for i in range(1, 21):
    URL = f'https://www.bukalapak.com/c/handphone/hp-smartphone/hp-android?page={str(i)}&search%5Bsort_by%5D=weekly_sales_ratio%3Adesc'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

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

    # print(len(Links))

    # Products name, rating, and seller
    products = box.find_all('a', class_ = 'bl-link')

    for i in products:
        product = i.text.strip()
        Products.append(product)
    # print(Products)

    # Products name
    Names = [Products[i] for i in range(0, len(Products), 3)]

    # print(len(Names))

    # Products rating
    Ratings = [Products[i] for i in range(1, len(Products), 3)]

    # print(len(Ratings))

    # Products sold volume
    sales = box.find_all('p', class_ = 'bl-text bl-text--body-14 bl-text--subdued')

    for i in sales:
        sold = i.text.strip()
        sale = sold[7:]
        Sales.append(sale)

    Sales = [Sales[i] for i in range(1, len(Sales), 2)]

    # print(len(Solds))

    # Products price
    prices = box.find_all('p', class_ = 'bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1')

    for i in prices:
        price = i.text.strip()
        Prices.append(price)

    # print(len(Prices))

    # Products seller location
    places = box.find_all('div', class_ = 'bl-product-card__description-store')

    for i in places:
        place = i.text.strip()
        Places.append(place)

    # print(len(Places))
    time.sleep(2)

# Ensure all lists are of the same length
max_length = max(len(Names), len(Ratings), len(Sales), len(Prices), len(Places), len(Links))

# Extend lists to the maximum length with None or empty strings
Names.extend([None] * (max_length - len(Names)))
Ratings.extend([None] * (max_length - len(Ratings)))
Sales.extend([None] * (max_length - len(Sales)))
Prices.extend([None] * (max_length - len(Prices)))
Places.extend([None] * (max_length - len(Places)))
Links.extend([None] * (max_length - len(Links)))


# Create a DataFrame from the dictionary
data = {
    'Nama Produk': Names,
    'Penjual': Places,
    'Rating': Ratings,
    'Total Terjual': Sales,
    'Harga': Prices,
    'Link Pembelian': Links
}

df = pd.DataFrame(data, index=range(1, len(Links) + 1))

# Print the DataFrame
print(df)

df.to_csv('Bukalapak-Handphones.csv')

print(len(Links), len(Names), len(Ratings), len(Sales), len(Prices), len(Places))
