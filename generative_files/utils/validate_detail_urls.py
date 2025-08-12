import os
import json
import re
import urllib.parse

def normalize_text(text):
    """Normalize text for comparison by removing special characters and converting to lowercase"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove common words that might not be in URLs
    common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
    words = text.split()
    words = [word for word in words if word not in common_words]
    
    return ' '.join(words)

def extract_name_from_url(url):
    """Extract the attraction name from a TripAdvisor URL"""
    if not url:
        return ""
    
    try:
        # Parse the URL
        parsed = urllib.parse.urlparse(url)
        
        # Extract the path and decode URL encoding
        path = urllib.parse.unquote(parsed.path)
        
        # Look for the attraction name in the path
        # TripAdvisor URLs typically have format: /Attraction_Review-...-Reviews-{Attraction_Name}-{Location}.html
        if 'Reviews-' in path:
            # Extract everything between 'Reviews-' and the last '-'
            reviews_part = path.split('Reviews-')[-1]
            if reviews_part.endswith('.html'):
                reviews_part = reviews_part[:-5]  # Remove .html
            
            # Split by '-' and take the first part (attraction name)
            parts = reviews_part.split('-')
            if parts:
                attraction_name = parts[0]
                return attraction_name
        
        return ""
    except:
        return ""

def validate_detail_urls():
    """Validate detail URLs by checking if attraction names appear in the URLs"""
    cities_dir = 'cities'
    total_entries = 0
    mismatched_entries = []
    
    for filename in os.listdir(cities_dir):
        if filename.endswith('_attractions_with_hours_and_price.json'):
            file_path = os.path.join(cities_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_mismatches = []
                for i, entry in enumerate(data):
                    total_entries += 1
                    name = entry.get('name', '')
                    detail_url = entry.get('detail_url', '')
                    
                    if not detail_url or not name:
                        continue
                    
                    # Normalize the attraction name
                    normalized_name = normalize_text(name)
                    
                    # Extract name from URL
                    url_name = extract_name_from_url(detail_url)
                    normalized_url_name = normalize_text(url_name)
                    
                    # Check if names match
                    if normalized_name and normalized_url_name:
                        # Check if any significant part of the name appears in the URL
                        name_words = normalized_name.split()
                        url_words = normalized_url_name.split()
                        
                        # Check for overlap
                        name_set = set(name_words)
                        url_set = set(url_words)
                        overlap = name_set.intersection(url_set)
                        
                        # If no significant overlap, flag as mismatch
                        if len(overlap) < min(len(name_set), len(url_set)) * 0.5:  # Less than 50% overlap
                            mismatch_info = {
                                'file': filename,
                                'index': i,
                                'name': name,
                                'url_name': url_name,
                                'detail_url': detail_url,
                                'normalized_name': normalized_name,
                                'normalized_url_name': normalized_url_name
                            }
                            file_mismatches.append(mismatch_info)
                            mismatched_entries.append(mismatch_info)
                
                # Only print if there are mismatches
                if file_mismatches:
                    print(f"⚠️  Found {len(file_mismatches)} potential mismatches in {filename}")
                    for mismatch in file_mismatches:
                        print(f"  Entry {mismatch['index']}: '{mismatch['name']}' vs URL: '{mismatch['url_name']}'")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
    
    # Summary report
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total entries checked: {total_entries}")
    print(f"Potential mismatches found: {len(mismatched_entries)}")
    
    if mismatched_entries:
        print(f"\nMismatch rate: {len(mismatched_entries)/total_entries*100:.1f}%")
        print("\nDetailed mismatch report:")
        print("-" * 60)
        
        for mismatch in mismatched_entries:
            print(f"File: {mismatch['file']}")
            print(f"Entry {mismatch['index']}: {mismatch['name']}")
            print(f"URL suggests: {mismatch['url_name']}")
            print(f"URL: {mismatch['detail_url']}")
            print("-" * 40)
    else:
        print("✓ All detail URLs appear to be correctly matched!")

if __name__ == "__main__":
    validate_detail_urls() 