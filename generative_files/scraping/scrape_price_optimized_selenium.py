import os
import json
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def extract_price_from_text(price_text):
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

def setup_driver():
    """Setup optimized headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # Don't load images for speed
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Set Chrome binary path for macOS
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Trying to install chromedriver automatically...")
        
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e2:
            print(f"Failed to install chromedriver automatically: {e2}")
            return None

def scrape_price_optimized(driver, detail_url, name):
    """Optimized price scraping with Selenium using specific selector"""
    if not detail_url or not driver:
        return None
    
    try:
        driver.get(detail_url)
        
        # Wait for page load
        time.sleep(2)
        
        # Use the specific selector you provided
        try:
            price_selector = '[data-automation="dtFromPrice"]'
            
            # Wait for the element to be present (up to 10 seconds)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            wait = WebDriverWait(driver, 10)
            price_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
            
            price_text = price_elem.text.strip()
            print(f"💰 Found price: {price_text}")
            
            # Extract numerical price
            price = extract_price_from_text(price_text)
            return price
            
        except Exception as e:
            print(f"⚠️ Could not extract price for {name}: {e}")
            
            # Try alternative approach - look for price in page source
            try:
                page_source = driver.page_source
                if 'dtFromPrice' in page_source:
                    print(f"🔍 Found 'dtFromPrice' in page source, but element not accessible")
                if '$' in page_source:
                    print(f"🔍 Found '$' symbol in page source")
            except:
                pass
            
            return None
        
    except Exception as e:
        print(f"Error accessing {detail_url}: {e}")
        return None

def main():
    """Main function with optimized Selenium performance"""
    cities_dir = 'cities'
    total_files_processed = 0
    total_prices_updated = 0
    
    print("⚡ OPTIMIZED SELENIUM PRICE SCRAPING")
    print("This version is optimized for speed while maintaining reliability")
    print("="*60)
    
    # Setup driver once
    print("🚀 Setting up browser...")
    driver = setup_driver()
    if not driver:
        print("❌ Failed to setup browser driver. Exiting.")
        return
    
    try:
        # Process all cities
        files_to_process = [f for f in os.listdir(cities_dir) if f.endswith('_attractions_with_hours_and_price.json')]
        
        for filename in files_to_process:
            file_path = os.path.join(cities_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                prices_updated = 0
                total_entries = len(data)
                
                print(f"\n📁 Processing: {filename} ({total_entries} attractions)")
                
                for i, entry in enumerate(data):
                    detail_url = entry.get('detail_url', '')
                    
                    if detail_url:
                        name = entry.get('name', 'Unknown')
                        print(f"  [{i+1}/{total_entries}] Optimized scrape: '{name}'...")
                        price = scrape_price_optimized(driver, detail_url, name)
                        
                        if price is not None:
                            old_price = entry.get('price', None)
                            data[i]['price'] = price
                            prices_updated += 1
                            
                            if old_price is not None:
                                print(f"    ✅ Price updated: ${old_price} → ${price}")
                            else:
                                print(f"    ✅ Price added: ${price}")
                        else:
                            print(f"    ❌ No price found")
                        
                        # Optimized delay - faster but still safe
                        delay = random.uniform(0.8, 2.0)  # 0.8-2 seconds
                        print(f"    ⏳ Waiting {delay:.1f} seconds...")
                        time.sleep(delay)
                
                # Save the updated file
                if prices_updated > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ Updated {prices_updated} prices in {filename}")
                    total_files_processed += 1
                    total_prices_updated += prices_updated
                else:
                    print(f"ℹ️  No price updates needed for {filename}")
                    
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
                continue
    
    finally:
        # Always close the driver
        driver.quit()
    
    # Summary
    print("\n" + "="*60)
    print("OPTIMIZED SELENIUM PRICE SCRAPING SUMMARY")
    print("="*60)
    print(f"Files processed: {total_files_processed}")
    print(f"Total prices updated: {total_prices_updated}")
    print("="*60)

if __name__ == "__main__":
    main() 