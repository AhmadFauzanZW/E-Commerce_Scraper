# Program Web Scraper - Bukalapak
# Import Modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Deklarasi Variable
Products = []
Links = []
Names = []
Ratings = []
Sales = []
Prices = []
Places = []

for i in range(1, 3):
    URL = f'https://www.bukalapak.com/c/handphone/hp-smartphone/hp-android?page={str(i)}&search%5Bsort_by%5D=weekly_sales_ratio%3Adesc'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    # Inisialisasi Get Request dan BeautifulSoup ke url website
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html5lib')

    # Selected Box untuk di scrape (main canvas)
    box = soup.find('div', class_='bl-flex-item bl-product-list-wrapper')

    # Products link
    links = box.find_all('a', class_='slide')

    for i in links:
        link = i.get('href')
        Links.append(link)

    # Products name, rating, and seller
    products = box.find_all('a', class_='bl-link')

    for i in products:
        product = i.text.strip()
        Products.append(product)

    # Products name
    Names = [Products[i] for i in range(0, len(Products), 3)]

    # Products rating
    Ratings = [Products[i] for i in range(1, len(Products), 3)]

    # Products sold volume
    sales = box.find_all('p', class_='bl-text bl-text--body-14 bl-text--subdued')

    for i in sales:
        sold = i.text.strip()
        Sales.append(sold)

    Sales = [Sales[i] for i in range(1, len(Sales), 2)]

    # Products price
    prices = box.find_all('p', class_='bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1')

    for i in prices:
        price = i.text.strip()
        Prices.append(price)

    # Products seller location
    places = box.find_all('div', class_='bl-product-card__description-store')

    for i in places:
        place = i.text.strip()
        Places.append(place)

# Ensure all lists are of the same length
max_length = max(len(Names), len(Ratings), len(Sales), len(Prices), len(Places), len(Links))

# Extend lists to the maximum length with None or empty strings
Names.extend([None] * (max_length - len(Names)))
Ratings.extend([None] * (max_length - len(Ratings)))
Sales.extend([None] * (max_length - len(Sales)))
Prices.extend([None] * (max_length - len(Prices)))
Places.extend([None] * (max_length - len(Places)))
Links.extend([None] * (max_length - len(Links)))

# Create clickable links using HTML
clickable_links = []
for link in Links:
    if link:
        clickable_links.append(f'<a href="{link}" target="_blank">View Product</a>')
    else:
        clickable_links.append(None)

# Create a DataFrame from the dictionary
data = {
    'Nama Produk': Names,
    'Penjual': Places,
    'Rating': Ratings,
    'Total Terjual': Sales,
    'Harga': Prices,
    'Link Pembelian': clickable_links
}

df = pd.DataFrame(data, index=range(1, len(Links) + 1))

# Save to CSV (optional)
df_to_csv = df.copy()
df_to_csv['Link Pembelian'] = Links  # Use raw links for CSV
df_to_csv.to_csv('Bukalapak-Handphones.csv')

# Streamlit app
st.set_page_config(page_title="Bukalapak Product Scraper",
                   page_icon="🛒",
                   layout='wide')
st.title("Bukalapak Product Scraping")
st.subheader("By Ahmad Fauzan")
st.divider()

# Display DataFrame with clickable links
st.write(df.to_html(escape=False), unsafe_allow_html=True)

# Add a download button for the CSV
csv = df_to_csv.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Bukalapak-Handphones.csv',
    mime='text/csv',
)