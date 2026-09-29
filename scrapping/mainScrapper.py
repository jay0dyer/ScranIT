import re
import requests
from bs4 import BeautifulSoup
import json
import urllib

class Scrapper:
    def __init__(self):
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

    def scrap(self, url):
        raw = requests.get(url, headers=self.headers).content
        soup = BeautifulSoup(raw, "html.parser")
        parsed = self.parse(soup)
        MetaData = self.MetaDataExtact(soup)
        MenuSample = self.DataExtact(parsed, soup)
        finaljson = {"metadata": MetaData, "menu": MenuSample}
        if MenuSample == []:
            return "No data scrapable"
        elif MetaData["address"]["postalCode"][:4] != "NE1 ":
            return "Not in NE1"
        else:
            return finaljson

    def parse(self, soup):
        return soup.get_text(separator="\n")

    def DataExtact(self, text, soup):
        element = soup.select_one('[data-qa="address-indicator-content"]')
        address = element.get_text(strip=True) if element else None

        MenuSampleRegex = r'([^\n]+)\n(?:([^\n£]+)\n)?\s*(£\d+\.\d{2})'
        raw_matches = re.findall(MenuSampleRegex, text)

        MenuSample = []
        for desc, name, price in raw_matches:
            clean_name = name.strip()

            # Skip garbage names (empty, just a comma, or UI words like "from")
            if len(clean_name) < 2 or clean_name.lower() in ["from", "add", "select"]:
                continue

            MenuSample.append({
                "name": clean_name,
                "description": desc.strip() if desc else None,
                "price": price
            })

        return MenuSample

    def MetaDataExtact(self, soup):
        json_ld_scripts = soup.find_all("script", type="application/ld+json")
        name, address, menu = None, None, []

        for script in json_ld_scripts:
            if not script.string:
                pass
            else:
                data = json.loads(script.string)
                return {"name":data["name"], "address": data["address"], "image": data["image"]}


scrapper = Scrapper()
with open("ne1_all_restaurants.json", "r") as f:
    restaurantUrls = json.loads(f.read())
    numofrestaurants = len(restaurantUrls)

i = 0
dropped = 0
NoData = 0
OutOfNE1 = 0

for url in restaurantUrls:
    i+=1
    scrapedData = scrapper.scrap(url)
    if scrapedData == "No data scrapable":
        NoData += 1
        print("no data scrapable")
    elif scrapedData == "Not in NE1":
        OutOfNE1 += 1
        print("Not in NE1")
    else:
        print(f"{url} : {scrapedData['menu']}")
        with open(f'menus/{scrapedData["metadata"]["name"].replace(" ","-")}.json', "w+") as f:
            json.dump(scrapedData, f, indent=4)

    dropped = NoData + OutOfNE1
    print("item num :",i, "/", numofrestaurants, "\n vaild :",i-dropped, "dropped :",dropped,
          "Reasons dropped :","Was outside NE1 :",OutOfNE1,"No menu data :",NoData)