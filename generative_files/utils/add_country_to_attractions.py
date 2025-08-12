import os
import json

# 1. City-to-country mapping (expand as needed)
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

def get_city_from_filename(filename):
    # Extracts the city part from the filename
    return filename.split('_attractions_with_hours_and_price.json')[0]

def main():
    cities_dir = "cities"
    for filename in os.listdir(cities_dir):
        if filename.endswith("_attractions_with_hours_and_price.json"):
            city_key = get_city_from_filename(filename)
            country = CITY_COUNTRY.get(city_key)
            if not country:
                print(f"Warning: No country mapping for city '{city_key}' in file '{filename}'. Skipping.")
                continue
            country_id = COUNTRY_ID.get(country)
            if not country_id:
                print(f"Warning: No country_id mapping for country '{country}' (city '{city_key}'). Skipping.")
                continue
            file_path = os.path.join(cities_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entity in data:
                entity["country"] = country
                entity["country_id"] = country_id
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {filename} with country '{country}' and country_id '{country_id}'.")

if __name__ == "__main__":
    main()
