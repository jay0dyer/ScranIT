import re
import json
from bs4 import BeautifulSoup
from curl_cffi import requests


def get_ne1_restaurant_urls():
    # Just Eat's dedicated NE1 area directory page
    with open("RestaurantsNE1.htm", encoding='utf-8', errors='ignore', mode="r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    # Extract all restaurant menu links matching Just Eat's URL structure
    links = set()
    for a in soup.find_all("a", href=True):
        href = a['href']
        if "/menu" in href:
            links.add(href)

    return list(links)


# Get the full list
ne1_all_restaurants = get_ne1_restaurant_urls()
with open(f'ne1_all_restaurants.json', "w+") as f:
    json.dump(ne1_all_restaurants, f, indent=4)