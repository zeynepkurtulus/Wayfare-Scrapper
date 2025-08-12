import os
import json
import re
import unicodedata
import string

def normalize_name(name):
    # Remove leading number and dot, lowercase, strip, remove punctuation, normalize spaces
    name = re.sub(r'^\d+\.\s*', '', name)
    name = name.lower().strip()
    name = ''.join(ch for ch in unicodedata.normalize('NFD', name) if unicodedata.category(ch) != 'Mn')  # Remove accents
    name = name.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    name = re.sub(r'\s+', ' ', name)  # Normalize spaces
    return name

def main():
    raw_dir = 'raw_data'
    cities_dir = 'cities'
    for filename in os.listdir(raw_dir):
        if filename.endswith('.json'):
            raw_path = os.path.join(raw_dir, filename)
            cities_filename = filename  # Use the same filename
            cities_path = os.path.join(cities_dir, cities_filename)
            if not os.path.exists(cities_path):
                print(f"Warning: No matching cities file for {filename}. Skipping.")
                continue
            # Load both files
            with open(raw_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            with open(cities_path, 'r', encoding='utf-8') as f:
                cities_data = json.load(f)
            # Assign popularity by order
            min_len = min(len(raw_data), len(cities_data))
            for i in range(min_len):
                cities_data[i]['popularity'] = str(i + 1)
            # Optionally warn if lengths differ
            if len(raw_data) != len(cities_data):
                print(f"Warning: {filename} - raw_data and cities file have different lengths ({len(raw_data)} vs {len(cities_data)})")
            with open(cities_path, 'w', encoding='utf-8') as f:
                json.dump(cities_data, f, ensure_ascii=False, indent=2)
            print(f"Updated {cities_filename} with popularity values by order.")

if __name__ == "__main__":
    main() 