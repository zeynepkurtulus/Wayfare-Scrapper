import os
import json

def main():
    cities_dir = 'cities'
    missing = {}
    for filename in os.listdir(cities_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(cities_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue
            for i, entry in enumerate(data):
                if 'popularity' not in entry:
                    if filename not in missing:
                        missing[filename] = []
                    missing[filename].append(i)
    if missing:
        print("Entries missing 'popularity' field:")
        for fname, indices in missing.items():
            print(f"{fname}: entries {indices}")
    else:
        print("All entries in all files have the 'popularity' field.")

if __name__ == "__main__":
    main() 