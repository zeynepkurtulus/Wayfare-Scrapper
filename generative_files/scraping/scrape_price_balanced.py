import os
import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup

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

def scrape_price_balanced(detail_url):
    """Balanced price scraping - faster than Selenium but safe"""
    if not detail_url:
        return None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        response = requests.get(detail_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Try data-automation attribute first (most reliable)
        price_element = soup.find('div', {'data-automation': 'dtFromPrice'})
        
        # Method 2: Try specific CSS classes if data-automation not found
        if not price_element:
            price_element = soup.find('div', class_=['biGQs', 'fiohW', 'XARtZ', 'iktvT', 'ezezH'])
        
        # Method 3: Look for price patterns in text
        if not price_element:
            # Look for any element containing price patterns
            price_patterns = [
                r'From \$[\d,]+',
                r'\$[\d,]+',
                r'From €[\d,]+',
                r'€[\d,]+',
                r'From £[\d,]+',
                r'£[\d,]+'
            ]
            
            for pattern in price_patterns:
                price_element = soup.find(text=re.compile(pattern))
                if price_element:
                    break
        
        if price_element:
            price_text = price_element.get_text().strip() if hasattr(price_element, 'get_text') else str(price_element).strip()
            price = extract_price_from_text(price_text)
            return price
        
        return None
        
    except requests.RequestException as e:
        print(f"  Request error for {detail_url}: {e}")
        return None
    except Exception as e:
        print(f"  Error scraping {detail_url}: {e}")
        return None

def main():
    """Main function with balanced speed and safety"""
    cities_dir = 'cities'
    total_files_processed = 0
    total_prices_updated = 0
    
    print("⚖️ BALANCED PRICE SCRAPING")
    print("This version balances speed with safety to avoid IP blocking")
    print("="*60)
    
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
                    print(f"  [{i+1}/{total_entries}] Balanced scrape: '{entry.get('name', 'Unknown')}'...")
                    price = scrape_price_balanced(detail_url)
                    
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
                    
                    # Balanced delay - faster than Selenium but safe
                    delay = random.uniform(1.5, 3.0)  # 1.5-3 seconds
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
    
    # Summary
    print("\n" + "="*60)
    print("BALANCED PRICE SCRAPING SUMMARY")
    print("="*60)
    print(f"Files processed: {total_files_processed}")
    print(f"Total prices updated: {total_prices_updated}")
    print("="*60)

if __name__ == "__main__":
    main() 