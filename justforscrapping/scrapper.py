from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
#from workbenchgui import checker, url
import subprocess

base_url = "https://www.booking.com/searchresults.html?ss={}&ssne={}&ssne_untouched={}&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4YzkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id={}&dest_type=city&checkin={}&checkout={}&group_adults={}&no_rooms={}&group_children={}"

checkin_date = datetime.now().strftime("%Y-%m-%d")
checkout_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

num_adults = 2
num_rooms = 1
num_children = 0
city = "Prague"

url = base_url.format(city, city, city, city, checkin_date, checkout_date, num_adults, num_rooms, num_children)
print(url)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5'
}

response = requests.get(url, headers= headers)
soup = BeautifulSoup(response.content, 'html.parser')

hotels = soup.findAll('div', {'data-testid': 'property-card'})

hotels_data = []
for hotel in hotels:
    name_element = hotel.find('div', {'data-testid': 'title'})
    name = name_element.text.strip() if name_element else "N/A"

    location_element = hotel.find('span', {'data-testid': 'address'})
    location = location_element.text.strip() if location_element else "N/A"

    distance_element = hotel.find('span', {'data-testid': 'distance'})
    distance = distance_element.text.strip() if distance_element else "N/A"

    rating_element = hotel.find('div', {'data-testid': 'review-score'})
    rating = rating_element.text.strip() if rating_element else "N/A"

    price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
    price = price_element.text.strip() if price_element else "N/A"


    hotels_data.append({
        'name': name,
        'location': location,
        'distance': distance,
        'rating': rating,
        'price': price
    })

df = pd.DataFrame(hotels_data)
df = df.rename(columns={'price': 'price_TRY'})

df.to_csv('hotel_data.csv', index=False)
print(hotels_data)

subprocess.run(["python", "secondarygui.py"])
