from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from workbenchgui import checker, url

base_url = "https://www.booking.com/searchresults.html?ss={}&ssne={}&ssne_untouched={}&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4YzkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id={}&dest_type=city&checkin={}&checkout={}&group_adults={}&no_rooms={}&group_children={}"

checkin_date = datetime.now().strftime("%Y-%m-%d")
checkout_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
global secondwindowstarter
secondwindowstarter = 0

num_adults = 2
num_rooms = 1
num_children = 0

#for testing since gui can not handle the data properly
url = "https://www.booking.com/searchresults.html?ss=London&ssne=Prague&ssne_untouched=London&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEXyAEP2AEB6AEB-AECiAIBqAIDuAK-o-qxBsACAdICJDY3ZjkzNjUxLWU2MTMtNDhhOC05N2IxLWJhMzEyZDIwNjIwMNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=-553173&dest_type=city&checkin=2024-05-10&checkout=2024-05-24&group_adults=2&no_rooms=1&group_children=0&efdco=1"

"""url = base_url.format(city, city, city, city, checkin_date, checkout_date, num_adults, num_rooms, num_children)
print(url)"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5'
}

if checker == True:
    response = requests.get(url, headers= headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    hotels = soup.findAll('div', {'data-testid': 'property-card'})

    hotels_data = []
    for hotel in hotels:
    
        name_element = hotel.find('div', {'data-testid': 'title'})
        name = name_element.text.strip() if name_element else "N/A"

        location_element = hotel.find('span', {'data-testid': 'address'})
        location = location_element.text.strip() if location_element else "N/A"

        price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        price = price_element.text.strip() if price_element else "N/A"

        rating_element = hotel.find('div', {'data-testid': 'review-score'})
        rating = rating_element.text.strip() if rating_element else "N/A"

        review_score_element = hotel.find('div', {'class': lambda x: x and 'ac4a7896c7' in x})
        review_score = review_score_element.text.strip() if review_score_element else "N/A"

    
        hotels_data.append({
            'name': name,
            'location': location,
            'price': price,
            'rating': rating,
            'review_score': review_score
        })


# Call the function with the base URL
#hotel_data = extract_hotel_info(base_url.format('Goa', 'Goa', 'Goa', '4127', '2023-08-28', '2023-08-30', '2', '1', '0'))

df = pd.DataFrame(hotels_data) # Creating a dataframe

df.to_csv('hotel_data.csv', index=False) # Save to CSV file
print(hotels_data)
secondwindowstarter+= 1