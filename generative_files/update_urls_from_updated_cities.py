import os
import json

def update_urls_from_updated_cities():
    """
    Update detail_url fields in cities/ files with correct URLs from updated_cities/ files.
    Only updates the detail_url field, leaving all other fields unchanged.
    """
    
    cities_dir = "cities"
    updated_cities_dir = "updated_cities"
    
    # Check if directories exist
    if not os.path.exists(cities_dir):
        print(f"Error: {cities_dir} directory not found")
        return
    
    if not os.path.exists(updated_cities_dir):
        print(f"Error: {updated_cities_dir} directory not found")
        return
    
    # Get list of files in both directories
    cities_files = [f for f in os.listdir(cities_dir) if f.endswith('_attractions_with_hours_and_price.json')]
    updated_cities_files = [f for f in os.listdir(updated_cities_dir) if f.endswith('_attractions_with_hours_and_price.json')]
    
    print(f"Found {len(cities_files)} files in {cities_dir}")
    print(f"Found {len(updated_cities_files)} files in {updated_cities_dir}")
    
    total_files_processed = 0
    total_urls_updated = 0
    
    # Process each file in cities directory
    for filename in cities_files:
        cities_file_path = os.path.join(cities_dir, filename)
        updated_cities_file_path = os.path.join(updated_cities_dir, filename)
        
        # Check if corresponding file exists in updated_cities
        if not os.path.exists(updated_cities_file_path):
            print(f"Warning: No corresponding file found in {updated_cities_dir} for {filename}. Skipping.")
            continue
        
        print(f"\nProcessing {filename}...")
        
        try:
            # Load cities data
            with open(cities_file_path, 'r', encoding='utf-8') as f:
                cities_data = json.load(f)
            
            # Load updated cities data
            with open(updated_cities_file_path, 'r', encoding='utf-8') as f:
                updated_cities_data = json.load(f)
            
            print(f"  Cities file: {len(cities_data)} attractions")
            print(f"  Updated cities file: {len(updated_cities_data)} attractions")
            
            # Update detail_url fields
            urls_updated = 0
            
            # Use the minimum length to avoid index errors
            min_length = min(len(cities_data), len(updated_cities_data))
            
            for i in range(min_length):
                cities_entry = cities_data[i]
                updated_entry = updated_cities_data[i]
                
                # Get the attraction names for verification
                cities_name = cities_entry.get('name', '')
                updated_name = updated_entry.get('name', '')
                
                # Get the URLs
                cities_url = cities_entry.get('detail_url', '')
                updated_url = updated_entry.get('detail_url', '')
                
                # Only update if URLs are different and updated URL is not empty
                if cities_url != updated_url and updated_url:
                    cities_data[i]['detail_url'] = updated_url
                    urls_updated += 1
                    print(f"    Updated URL for '{cities_name}': {updated_url}")
            
            # Save the updated cities file
            with open(cities_file_path, 'w', encoding='utf-8') as f:
                json.dump(cities_data, f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ Updated {urls_updated} URLs in {filename}")
            total_files_processed += 1
            total_urls_updated += urls_updated
            
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
            continue
    
    # Summary
    print(f"\n{'='*60}")
    print("UPDATE SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {total_files_processed}")
    print(f"Total URLs updated: {total_urls_updated}")
    print(f"✓ URL update process completed!")

if __name__ == "__main__":
    update_urls_from_updated_cities() 