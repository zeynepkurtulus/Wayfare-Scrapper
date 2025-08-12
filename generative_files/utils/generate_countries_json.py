import json
import time
import random

# List of countries and their codes (from your mappings)
COUNTRIES = [
    ("USA", "US", "North America"),
    ("Canada", "CA", "North America"),
    ("Mexico", "MX", "North America"),
    ("UK", "GB", "Europe"),
    ("France", "FR", "Europe"),
    ("Italy", "IT", "Europe"),
    ("Spain", "ES", "Europe"),
    ("Netherlands", "NL", "Europe"),
    ("Portugal", "PT", "Europe"),
    ("Greece", "GR", "Europe"),
    ("Turkey", "TR", "Europe/Asia"),
    ("Germany", "DE", "Europe"),
    ("Japan", "JP", "Asia"),
    ("China", "CN", "Asia"),
    ("South Korea", "KR", "Asia"),
    ("Thailand", "TH", "Asia"),
    ("Vietnam", "VN", "Asia"),
    ("Singapore", "SG", "Asia"),
    ("Australia", "AU", "Oceania"),
    ("New Zealand", "NZ", "Oceania"),
    ("Brazil", "BR", "South America"),
    ("Argentina", "AR", "South America"),
    ("South Africa", "ZA", "Africa"),
    ("Egypt", "EG", "Africa"),
    ("Morocco", "MA", "Africa"),
    ("UAE", "AE", "Asia"),
    ("Israel", "IL", "Asia"),
    ("Indonesia", "ID", "Asia"),
    ("Maldives", "MV", "Asia"),
    ("Mauritius", "MU", "Africa"),
    ("Seychelles", "SC", "Africa"),
    ("French Polynesia", "PF", "Oceania"),
    ("Fiji", "FJ", "Oceania"),
]

def generate_object_id():
    timestamp = int(time.time())
    oid = hex(timestamp)[2:].zfill(8)
    oid += ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return oid

def main():
    country_entries = []
    for name, code, region in COUNTRIES:
        entry = {
            "_id": generate_object_id(),
            "name": name,
            "country_id": code,
            "active": True,
            "region": region
        }
        country_entries.append(entry)
    with open("countries.json", "w", encoding="utf-8") as f:
        json.dump(country_entries, f, ensure_ascii=False, indent=2)
    print(f"Created countries.json with {len(country_entries)} countries.")

if __name__ == "__main__":
    main() 