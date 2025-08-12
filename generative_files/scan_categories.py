import os
import json

def main():
    cities_dir = 'cities'
    categories = set()
    
    for filename in os.listdir(cities_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(cities_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for entry in data:
                    category = entry.get('category', '')
                    if category:  # Only add non-empty categories
                        categories.add(category)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    # Print sorted list of unique categories
    print("All unique category values found:")
    print("=" * 50)
    for category in sorted(categories):
        print(f"- {category}")
    print(f"\nTotal unique categories: {len(categories)}")

if __name__ == "__main__":
    main() 