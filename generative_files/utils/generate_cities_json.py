import os
import json
import uuid
import random
import time

# Generates a MongoDB-like ObjectId (24 hex chars)
def generate_object_id():
    timestamp = int(time.time())
    oid = hex(timestamp)[2:].zfill(8)
    oid += ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return oid

CITY_COUNTRY = {
    # USA
    "New_York_City": "USA", "Los_Angeles": "USA", "San_Francisco": "USA", "Chicago": "USA", "Miami": "USA",
    "Las_Vegas": "USA", "Orlando": "USA", "Seattle": "USA", "Boston": "USA", "Washington_DC": "USA",
    # Canada
    "Toronto": "Canada", "Vancouver": "Canada", "Montreal": "Canada",
    # Mexico
    "Mexico_City": "Mexico", "Cancun": "Mexico",
    # UK
    "London": "UK", "Edinburgh": "UK", "Manchester": "UK", "Liverpool": "UK", "Glasgow": "UK", "Belfast": "UK",
    # France
    "Paris": "France", "Nice": "France", "Lyon": "France", "Marseille": "France", "Bordeaux": "France",
    # Italy
    "Rome": "Italy", "Florence": "Italy", "Venice": "Italy", "Milan": "Italy", "Naples": "Italy",
    # Spain
    "Barcelona": "Spain", "Madrid": "Spain", "Seville": "Spain", "Valencia": "Spain", "Granada": "Spain",
    # Netherlands
    "Amsterdam": "Netherlands", "Rotterdam": "Netherlands",
    # Portugal
    "Lisbon": "Portugal", "Porto": "Portugal", "Madeira": "Portugal",
    # Greece
    "Athens": "Greece", "Thessaloniki": "Greece", "Santorini": "Greece", "Mykonos": "Greece",
    # Turkey
    "Istanbul": "Turkey", "Antalya": "Turkey", "Izmir": "Turkey", "Bursa": "Turkey", "Ankara": "Turkey", "Cappadocia": "Turkey",
    # Germany
    "Berlin": "Germany", "Munich": "Germany", "Hamburg": "Germany",
    # Japan
    "Tokyo": "Japan", "Kyoto": "Japan", "Osaka": "Japan",
    # China
    "Beijing": "China", "Shanghai": "China",
    # South Korea
    "Seoul": "South Korea",
    # Thailand
    "Bangkok": "Thailand", "Chiang_Mai": "Thailand", "Phuket": "Thailand",
    # Vietnam
    "Hanoi": "Vietnam", "Ho_Chi_Minh_City": "Vietnam",
    # Singapore
    "Singapore": "Singapore",
    # Australia
    "Sydney": "Australia", "Melbourne": "Australia", "Brisbane": "Australia", "Perth": "Australia", "Cairns": "Australia",
    # New Zealand
    "Auckland": "New Zealand", "Queenstown": "New Zealand", "Wellington": "New Zealand",
    # Brazil
    "Rio_de_Janeiro": "Brazil", "Sao_Paulo": "Brazil",
    # Argentina
    "Buenos_Aires": "Argentina",
    # South Africa
    "Cape_Town": "South Africa", "Johannesburg": "South Africa",
    # Egypt
    "Cairo": "Egypt",
    # Morocco
    "Marrakech": "Morocco",
    # UAE
    "Dubai": "UAE", "Abu_Dhabi": "UAE",
    # Israel
    "Jerusalem": "Israel", "Tel_Aviv": "Israel",
    # Islands
    "Bali": "Indonesia", "Maldives": "Maldives", "Mauritius": "Mauritius", "Seychelles": "Seychelles",
    "Tenerife": "Spain", "Bora_Bora": "French Polynesia", "Fiji": "Fiji", "Tahiti": "French Polynesia",
    # Others (add as needed)
}

COUNTRY_ID = {
    "USA": "US",
    "Canada": "CA",
    "Mexico": "MX",
    "UK": "GB",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",
    "Portugal": "PT",
    "Greece": "GR",
    "Turkey": "TR",
    "Germany": "DE",
    "Japan": "JP",
    "China": "CN",
    "South Korea": "KR",
    "Thailand": "TH",
    "Vietnam": "VN",
    "Singapore": "SG",
    "Australia": "AU",
    "New Zealand": "NZ",
    "Brazil": "BR",
    "Argentina": "AR",
    "South Africa": "ZA",
    "Egypt": "EG",
    "Morocco": "MA",
    "UAE": "AE",
    "Israel": "IL",
    "Indonesia": "ID",
    "Maldives": "MV",
    "Mauritius": "MU",
    "Seychelles": "SC",
    "French Polynesia": "PF",
    "Fiji": "FJ",
    # Add more as needed
}

COUNTRY_ID = {
    "USA": "US",
    "Canada": "CA",
    "Mexico": "MX",
    "UK": "GB",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",
    "Portugal": "PT",
    "Greece": "GR",
    "Turkey": "TR",
    "Germany": "DE",
    "Japan": "JP",
    "China": "CN",
    "South Korea": "KR",
    "Thailand": "TH",
    "Vietnam": "VN",
    "Singapore": "SG",
    "Australia": "AU",
    "New Zealand": "NZ",
    "Brazil": "BR",
    "Argentina": "AR",
    "South Africa": "ZA",
    "Egypt": "EG",
    "Morocco": "MA",
    "UAE": "AE",
    "Israel": "IL",
    "Indonesia": "ID",
    "Maldives": "MV",
    "Mauritius": "MU",
    "Seychelles": "SC",
    "French Polynesia": "PF",
    "Fiji": "FJ",
   
}

def get_city_from_filename(filename):
    return filename.split('_attractions_with_hours_and_price.json')[0]

def main():
    cities_dir = "cities"
    city_entries = []
    for filename in os.listdir(cities_dir):
        if filename.endswith("_attractions_with_hours_and_price.json"):
            city_key = get_city_from_filename(filename)
            country = CITY_COUNTRY.get(city_key)
            country_id = COUNTRY_ID.get(country)
            if not country or not country_id:
                print(f"Warning: Missing mapping for city '{city_key}'. Skipping.")
                continue
            entry = {
                "_id": generate_object_id(),
                "city_id": str(uuid.uuid4()),
                "name": city_key.replace("_", " "),
                "country": country,
                "country_id": country_id,
                "active": True
            }
            city_entries.append(entry)
    # Save to file
    with open("cities.json", "w", encoding="utf-8") as f:
        json.dump(city_entries, f, ensure_ascii=False, indent=2)
    print(f"Created cities.json with {len(city_entries)} cities.")

if __name__ == "__main__":
    main() 