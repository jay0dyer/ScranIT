import sqlite3
import os
import json


conn = sqlite3.connect("ItemInfo.db")
cursor = conn.cursor()

restaurant_table_creation_query = """
    CREATE TABLE IF NOT EXISTS RestaurantInfo (
        ScranHash TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        StreetAddress TEXT NOT NULL,
        Postcode TEXT NOT NULL,
        Image TEXT NOT NULL
    );
"""
cursor.execute(restaurant_table_creation_query)

item_table_creation_query = """
    CREATE TABLE IF NOT EXISTS ItemInfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Description TEXT NOT NULL,
        Price REAL NOT NULL,
        ScranHash TEXT NOT NULL,
        FOREIGN KEY (ScranHash) REFERENCES RestaurantInfo(ScranHash)
    );
"""
cursor.execute(item_table_creation_query)

def ScranHasher(Postcode, name):
    ScranHash = Postcode.replace(" ", (name[:2].lower()+name[-2:].lower()))[3:]
    ScranHash = ScranHash.replace(" ", "-")
    return ScranHash

p = r"menus/"
for e in os.scandir(p):
    with open(e.path, "r") as f:
        restaurantInfo = json.loads(f.read())
        metadata = restaurantInfo["metadata"]
        menu = restaurantInfo["menu"]
        ScranHash = ScranHasher(metadata["address"]["postalCode"], metadata["name"])
        print(ScranHash)
        cursor.execute("""INSERT INTO RestaurantInfo (
         Name,
         StreetAddress,
         Postcode,
         Image,
         ScranHash) VALUES (?,?,?,?,?)
         """,(
            metadata["name"],
            metadata["address"]["streetAddress"],
            metadata["address"]["postalCode"],
            metadata["image"],
            ScranHash ))
        for item in menu:
            cursor.execute("""INSERT INTO ItemInfo (
            Name,
            Description,
            Price,
            scranHash) VALUES (?,?,?,?)
            """, (item["name"], item["description"], item["price"], ScranHash))

cursor.close()
conn.commit()