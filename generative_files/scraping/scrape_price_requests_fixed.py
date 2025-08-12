import requests
from bs4 import BeautifulSoup
import json
import time
import re
import random
from urllib.parse import urljoin
import os
from datetime import datetime

# === CONFIG ===
BASE_URL = "https://www.tripadvisor.co.uk"

# User agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
]

# Proxy configuration (use real proxy here if needed)
PROXIES = None  # Example: {"http": "http://proxy:port", "https": "http://proxy:port"}

RETRIES = 3
DELAY_RANGE = (1, 3)  # Random delay between requests

# Setup logging
log_filename = f"price_scraping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log_and_print(message):
    """Print to console and save to log file"""
    print(message)
    with open(log_filename, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")

def clean_attraction_name(name):
    name = re.sub(r'^\d+\.\s*', '', name)
    return name.strip().lower()

def safe_get(url):
    for attempt in range(RETRIES):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            response = requests.get(url, headers=headers, proxies=PROXIES, timeout=15)
            response.raise_for_status()
            return response
        except Exception as e:
            log_and_print(f"⚠️ Request failed ({attempt + 1}/{RETRIES}): {e}")
            if attempt < RETRIES - 1:  # Don't sleep on last attempt
                time.sleep(random.uniform(*DELAY_RANGE))
    return None

def extract_price_from_detail_page(url, name):
    """Extract price from TripAdvisor detail page using the specific selector"""
    response = safe_get(url)
    if not response:
        log_and_print(f"❌ Failed to fetch detail page: {url}")
        return None
    
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Use the specific selector from browser inspection
        price_elem = soup.select_one('[data-automation="dtFromPrice"]')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            if price_text:
                # Return the original price text as string
                return price_text
        
        return None
        
    except Exception as e:
        log_and_print(f"❌ Error parsing detail page: {e}")
        return None

def extract_numerical_price(price_text):
    """Extract numerical price from text like 'From $36' or '$25'"""
    if not price_text:
        return None
    
    # Remove common prefixes
    price_text = price_text.replace('From ', '').replace('from ', '')
    
    # Extract the first number found (usually the price)
    price_match = re.search(r'[\$€£¥]?\s*(\d+(?:\.\d{2})?)', price_text)
    if price_match:
        try:
            price = float(price_match.group(1))
            return price
        except ValueError:
            return None
    
    return None

def process_all_cities():
    cities_dir = 'cities'
    total_files_processed = 0
    total_prices_updated = 0
    successful_cities = []
    failed_cities = []
    
    log_and_print("🔍 REQUESTS-BASED PRICE SCRAPING")
    log_and_print("Using specific selector: [data-automation='dtFromPrice']")
    log_and_print("="*60)
    log_and_print(f"📝 Log file: {log_filename}")
    
    # Get total number of files to process (sorted alphabetically)
    files_to_process = sorted([f for f in os.listdir(cities_dir) if f.endswith('_attractions_with_hours_and_price.json')])
    total_files = len(files_to_process)
    
    for file_index, filename in enumerate(files_to_process, 1):
        city_name = filename.replace('_attractions_with_hours_and_price.json', '')
        log_and_print(f"\n🌍 [{file_index}/{total_files}] Scraping price info for: {city_name}")

        file_path = os.path.join(cities_dir, filename)
        try:
            with open(file_path, encoding="utf-8") as f:
                existing_data = json.load(f)
            log_and_print(f"✅ Loaded {len(existing_data)} existing places from file")
        except Exception as e:
            log_and_print(f"❌ Could not load file: {e}")
            failed_cities.append(city_name)
            continue

        prices_updated = 0
        prices_found = 0
        prices_missing = 0
        
        try:
            for i, entry in enumerate(existing_data):
                name = entry.get("name", "")
                detail_url = entry.get("detail_url", "")

                if not detail_url:
                    print(f"❌ No detail URL for: {name}")
                    prices_missing += 1
                    continue

                # Show progress without too much detail
                if i % 10 == 0 or i == len(existing_data) - 1:  # Show every 10th item or last item
                    log_and_print(f"  [{i+1}/{len(existing_data)}] 🔎 Processing: {name[:30]}...")
                
                price = extract_price_from_detail_page(detail_url, name)
                
                if price is not None:
                    old_price = entry.get("price", None)
                    existing_data[i]["price"] = price
                    prices_updated += 1
                    prices_found += 1
                    
                    # Only show price updates for every 10th item to reduce output
                    if i % 10 == 0 or i == len(existing_data) - 1:
                        if old_price is not None:
                            log_and_print(f"    ✅ Price updated: {old_price} → {price}")
                        else:
                            log_and_print(f"    ✅ Price added: {price}")
                else:
                    prices_missing += 1
                    # Only show missing prices for every 10th item
                    if i % 10 == 0 or i == len(existing_data) - 1:
                        log_and_print(f"    ❌ No price found")

                # Delay between requests (silent)
                delay = random.uniform(*DELAY_RANGE)
                time.sleep(delay)

            # Save to the same file (overwrite)
            if prices_updated > 0:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=2)
                log_and_print(f"💾 File updated: {file_path} ({prices_updated} prices updated)")
                total_files_processed += 1
                total_prices_updated += prices_updated
                successful_cities.append(city_name)
            else:
                log_and_print(f"ℹ️  No price updates needed for {city_name}")
                successful_cities.append(city_name)
            
            # Progress summary for this city
            log_and_print(f"📊 {city_name} Summary: {prices_found} found, {prices_missing} missing")

        except Exception as e:
            log_and_print(f"❌ Error during scraping: {e}")
            failed_cities.append(city_name)
    
    # Final Summary
    log_and_print("\n" + "="*60)
    log_and_print("REQUESTS-BASED PRICE SCRAPING SUMMARY")
    log_and_print("="*60)
    log_and_print(f"Files processed: {total_files_processed}")
    log_and_print(f"Total prices updated: {total_prices_updated}")
    log_and_print(f"Successful cities: {len(successful_cities)}")
    log_and_print(f"Failed cities: {len(failed_cities)}")
    
    if successful_cities:
        log_and_print(f"\n✅ SUCCESSFUL CITIES ({len(successful_cities)}):")
        for city in successful_cities:
            log_and_print(f"  ✓ {city}")
    
    if failed_cities:
        log_and_print(f"\n❌ FAILED CITIES ({len(failed_cities)}):")
        for city in failed_cities:
            log_and_print(f"  ✗ {city}")
    
    log_and_print("="*60)
    log_and_print(f"📝 Complete log saved to: {log_filename}")

if __name__ == "__main__":
    process_all_cities() 