import os
import json
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import time
import random

def normalize_text(text):
    """Normalize text for comparison"""
    if not text:
        return ""
    
    text = text.lower()
    text = text.replace('_', ' ')
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
    words = text.split()
    words = [word for word in words if word not in common_words]
    
    return ' '.join(words)

def extract_name_from_url(url):
    """Extract attraction name from TripAdvisor URL"""
    if not url:
        return ""
    
    try:
        parsed = urllib.parse.urlparse(url)
        path = urllib.parse.unquote(parsed.path)
        
        if 'Reviews-' in path:
            reviews_part = path.split('Reviews-')[-1]
            if reviews_part.endswith('.html'):
                reviews_part = reviews_part[:-5]
            
            parts = reviews_part.split('-')
            if parts:
                return parts[0]
        
        return ""
    except:
        return ""

def validate_url_correctness(attraction_name, url):
    """Validate if a URL is correct for the given attraction name"""
    if not url or not attraction_name:
        return False
    
    try:
        url_name = extract_name_from_url(url)
        if not url_name:
            return False
        
        normalized_attraction = normalize_text(attraction_name)
        normalized_url = normalize_text(url_name)
        
        if not normalized_attraction or not normalized_url:
            return False
        
        attraction_words = set(normalized_attraction.split())
        url_words = set(normalized_url.split())
        overlap = attraction_words.intersection(url_words)
        
        min_overlap = min(len(attraction_words), len(url_words)) * 0.5
        return len(overlap) >= min_overlap
        
    except Exception as e:
        return False

def get_city_urls():
    """Get main URLs for cities"""
    return {
        "Istanbul": "https://www.tripadvisor.com/Attractions-g293974-Activities-oa0-Istanbul.html",
        "London": "https://www.tripadvisor.com/Attractions-g186338-Activities-oa0-London_England.html",
        "Paris": "https://www.tripadvisor.com/Attractions-g187147-Activities-oa0-Paris_Ile_de_France.html",
        "Rome": "https://www.tripadvisor.com/Attractions-g187791-Activities-oa0-Rome_Lazio.html",
        "Barcelona": "https://www.tripadvisor.com/Attractions-g187497-Activities-oa0-Barcelona_Catalonia.html",
        "Amsterdam": "https://www.tripadvisor.com/Attractions-g188590-Activities-oa0-Amsterdam_North_Holland_Province.html",
        "New York City": "https://www.tripadvisor.com/Attractions-g60763-Activities-oa0-New_York_City_New_York.html",
        "Tokyo": "https://www.tripadvisor.com/Attractions-g1066443-Activities-oa0-Tokyo_Tokyo_Prefecture_Kanto.html",
        "Sydney": "https://www.tripadvisor.com/Attractions-g255060-Activities-oa0-Sydney_New_South_Wales.html",
        "Dubai": "https://www.tripadvisor.com/Attractions-g295424-Activities-oa0-Dubai_Emirate_of_Dubai.html"
    }

def scrape_city_urls(city_name, max_pages=3):
    """Scrape attraction URLs from a city's main page and pagination"""
    city_urls = get_city_urls()
    main_url = city_urls.get(city_name)
    
    if not main_url:
        print(f"  No URL found for {city_name}")
        return {}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_attraction_links = {}
    
    for page in range(max_pages):
        if page == 0:
            url = main_url
        else:
            # Add pagination parameter
            url = main_url.replace('-oa0-', f'-oa{page*30}-')
        
        print(f"  Scraping page {page + 1}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            page_attractions = 0
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if 'Attraction_Review' in href and 'Reviews-' in href:
                    attraction_name = extract_name_from_url(href)
                    if attraction_name:
                        if href.startswith('/'):
                            href = 'https://www.tripadvisor.com' + href
                        
                        all_attraction_links[attraction_name] = href
                        page_attractions += 1
            
            print(f"    Found {page_attractions} attractions on page {page + 1}")
            
            # If we found very few attractions, stop pagination
            if page_attractions < 10:
                break
            
            # Add delay between pages
            time.sleep(2 + random.uniform(1, 3))
            
        except Exception as e:
            print(f"    Error scraping page {page + 1}: {e}")
            break
    
    print(f"  Total unique attractions found: {len(all_attraction_links)}")
    return all_attraction_links

def fix_city_urls(city_name):
    """Fix URLs for a specific city"""
    print(f"\nProcessing {city_name}...")
    
    # Load city data
    filename = f"{city_name.replace(' ', '_')}_attractions_with_hours_and_price.json"
    file_path = os.path.join('cities', filename)
    
    if not os.path.exists(file_path):
        print(f"  File not found: {filename}")
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"  Loaded {len(data)} attractions")
    
    # Scrape correct URLs
    scraped_urls = scrape_city_urls(city_name)
    
    if not scraped_urls:
        print(f"  No URLs scraped for {city_name}")
        return 0
    
    # Fix URLs
    fixed_count = 0
    for i, entry in enumerate(data):
        name = entry.get('name', '')
        current_url = entry.get('detail_url', '')
        
        if name and current_url:
            if not validate_url_correctness(name, current_url):
                # Try to find correct URL from scraped data
                normalized_name = normalize_text(name)
                
                for scraped_name, scraped_url in scraped_urls.items():
                    normalized_scraped = normalize_text(scraped_name)
                    if normalized_name == normalized_scraped:
                        data[i]['detail_url'] = scraped_url
                        fixed_count += 1
                        print(f"    Fixed: '{name}' -> {scraped_url}")
                        break
    
    # Save the updated file
    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Fixed {fixed_count} URLs in {city_name}")
    else:
        print(f"  No URLs could be fixed in {city_name}")
    
    return fixed_count

def main():
    """Main function to fix URLs for multiple cities"""
    print("Comprehensive URL Fixing by Scraping Main Pages")
    print("This will scrape TripAdvisor main pages to get correct URLs")
    
    # Cities to process (starting with a few for testing)
    cities_to_process = [
        "Istanbul",
        "London", 
        "Paris",
        "Rome",
        "Barcelona"
    ]
    
    total_fixed = 0
    
    for city in cities_to_process:
        fixed = fix_city_urls(city)
        total_fixed += fixed
        
        # Add delay between cities
        time.sleep(5 + random.uniform(2, 5))
    
    print(f"\n✓ Total URLs fixed: {total_fixed}")

if __name__ == "__main__":
    main() 