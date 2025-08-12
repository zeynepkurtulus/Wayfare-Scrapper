import os
import json

def get_city_from_filename(filename):
    return filename.split('_attractions_with_hours_and_price.json')[0]

def main():
    # Load city_id mapping from cities.json
    with open("cities.json", "r", encoding="utf-8") as f:
        cities = json.load(f)
    # Build mapping: normalized city name -> city_id
    city_name_to_id = {city["name"].replace(" ", "_"): city["city_id"] for city in cities}

    cities_dir = "cities"
    for filename in os.listdir(cities_dir):
        if filename.endswith("_attractions_with_hours_and_price.json"):
            city_key = get_city_from_filename(filename)
            city_id = city_name_to_id.get(city_key)
            if not city_id:
                print(f"Warning: No city_id found for city '{city_key}' in file '{filename}'. Skipping.")
                continue
            file_path = os.path.join(cities_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entity in data:
                entity["city_id"] = city_id
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {filename} with city_id '{city_id}'.")

if __name__ == "__main__":
    main()
