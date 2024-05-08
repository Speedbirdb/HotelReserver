from datetime import datetime, timedelta
from workbenchgui import city, checkin_date, checkout_date, url

base_url = "https://www.booking.com/searchresults.html?ss={}&ssne={}&ssne_untouched={}&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4YzkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id={}&dest_type=city&checkin={}&checkout={}&group_adults={}&no_rooms={}&group_children={}"

checkin_date = datetime.now().strftime("%Y-%m-%d")
checkout_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

num_adults = 2
num_rooms = 1
num_children = 0

url = base_url.format(city, city, city, city, checkin_date, checkout_date, num_adults, num_rooms, num_children)
print(url)