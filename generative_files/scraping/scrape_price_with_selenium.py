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
    """Setup headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
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
        
        # Try to install chromedriver using webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e2:
            print(f"Failed to install chromedriver automatically: {e2}")
            print("Please install chromedriver manually or use: pip install webdriver-manager")
            return None

def scrape_price_with_selenium(driver, detail_url):
    """Scrape price using Selenium"""
    if not detail_url or not driver:
        return None
    
    try:
        driver.get(detail_url)
        
        # Wait for page to load
        time.sleep(random.uniform(2, 4))
        
        # Try multiple selectors for price
        price_selectors = [
            '[data-automation="dtFromPrice"]',
            '.biGQs._P.fiohW.XARtZ.iktvT.ezezH',
            '[class*="price"]',
            '[class*="admission"]',
            'div:contains("$")',
            'span:contains("$")'
        ]
        
        price_text = None
        
        for selector in price_selectors:
            try:
                # Wait for element to be present
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                price_text = element.text.strip()
                if price_text and ('$' in price_text or '€' in price_text or '£' in price_text):
                    break
            except:
                continue
        
        # If no specific selector worked, search for price patterns in page text
        if not price_text:
            page_text = driver.page_source
            price_patterns = [
                r'From \$[\d,]+',
                r'\$[\d,]+',
                r'From €[\d,]+',
                r'€[\d,]+',
                r'From £[\d,]+',
                r'£[\d,]+'
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, page_text)
                if match:
                    price_text = match.group(0)
                    break
        
        if price_text:
            price = extract_price_from_text(price_text)
            return price
        
        return None
        
    except Exception as e:
        print(f"  Selenium error for {detail_url}: {e}")
        return None

def main():
    """Main function using Selenium"""
    cities_dir = 'cities'
    total_files_processed = 0
    total_prices_updated = 0
    
    print("🤖 SELENIUM-BASED PRICE SCRAPING")
    print("This version uses headless browser for more reliable scraping")
    print("="*60)
    
    # Setup driver
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
                        print(f"  [{i+1}/{total_entries}] Browser: '{entry.get('name', 'Unknown')}'...")
                        price = scrape_price_with_selenium(driver, detail_url)
                        
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
                        
                        # Optimized delay for browser requests
                        time.sleep(random.uniform(0.8, 2.0))  # Faster but still safe
                
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
    print("SELENIUM PRICE SCRAPING SUMMARY")
    print("="*60)
    print(f"Files processed: {total_files_processed}")
    print(f"Total prices updated: {total_prices_updated}")
    print("="*60)

if __name__ == "__main__":
    main() 