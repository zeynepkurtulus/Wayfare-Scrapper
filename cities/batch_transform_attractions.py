import os
import json
import time
import uuid
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Helper for MongoDB ObjectId-like string
def generate_object_id():
    return uuid.uuid4().hex[:24]

def clean_name(name):
    # Remove leading numbers and dot, e.g., '1. Tower of London' -> 'Tower of London'
    return name.split('. ', 1)[-1] if '. ' in name else name

def geocode_place(geolocator, name, city):
    try:
        location = geolocator.geocode(f"{name}, {city}")
        if location:
            return {
                'lat': location.latitude,
                'lng': location.longitude
            }, location.address
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Geocoding error for {name}, {city}: {e}")
    return None, None

def transform_file(filepath, city):
    geolocator = Nominatim(user_agent="travel_planner_batch")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    transformed = []
    for place in data:
        name = clean_name(place.get('name', ''))
        # Geocode
        coords, address = geocode_place(geolocator, name, city)
        if coords is None:
            print(f"[WARN] Could not geocode: {name} ({city})")
            coords = {'lat': None, 'lng': None}
            address = None
        # Generate IDs and timestamps
        place_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + 'Z'
        # Build new structure
        new_place = {
            '_id': generate_object_id(),
            'place_id': place_id,
            'city': city,
            'name': name,
            'category': place.get('category', ''),
            'price': place.get('price', ''),
            'rating': place.get('rating', ''),
            'image': place.get('image', ''),
            'detail_url': place.get('detail_url', ''),
            'opening_hours': place.get('opening_hours', {}),
            'coordinates': coords,
            'address': address,
            'source': 'tripadvisor',
            'created_at': now,
            'updated_at': now
        }
        transformed.append(new_place)
        print(f"[INFO] Processed: {name} ({city}) -> {coords}")
        time.sleep(1)  # Respect Nominatim rate limit
    # Overwrite file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)
    print(f"[DONE] Overwrote {filepath} with {len(transformed)} places.")

def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            city = filename.split('_')[0].replace('_', ' ')
            filepath = os.path.join(folder, filename)
            print(f"[START] Processing {filename} for city: {city}")
            transform_file(filepath, city)

if __name__ == "__main__":
    main() 