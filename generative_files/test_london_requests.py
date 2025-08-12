import requests
from bs4 import BeautifulSoup
import json
import time
import re
import random

# User agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def safe_get(url):
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def extract_price_from_detail_page(url, name):
    """Extract price from TripAdvisor detail page with multiple methods"""
    print(f"🔍 Testing URL: {url}")
    
    response = safe_get(url)
    if not response:
        print(f"❌ Failed to fetch detail page")
        return None
    
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Method 1: Primary selector (most reliable)
        print("🔍 Trying Method 1: [data-automation='dtFromPrice']")
        price_elem = soup.select_one('[data-automation="dtFromPrice"]')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            if price_text:
                print(f"💰 Method 1 - Found price: {price_text}")
                price = extract_numerical_price(price_text)
                if price is not None:
                    return price
        else:
            print("❌ Method 1: No element found with [data-automation='dtFromPrice']")
        
        # Method 2: Look for admission tickets section
        print("🔍 Trying Method 2: Admission section search")
        admission_elements = soup.find_all(text=re.compile(r'admission|ticket', re.IGNORECASE))
        for elem in admission_elements:
            parent = elem.parent
            if parent:
                text = parent.get_text()
                if '$' in text or '€' in text or '£' in text:
                    print(f"💰 Method 2 - Found in admission section: {text[:100]}...")
                    price = extract_numerical_price(text)
                    if price is not None:
                        return price
        
        # Method 3: Search entire page for price patterns
        print("🔍 Trying Method 3: Pattern matching")
        page_text = soup.get_text()
        price_patterns = [
            r'From \$[\d,]+',
            r'\$[\d,]+',
            r'From €[\d,]+',
            r'€[\d,]+',
            r'From £[\d,]+',
            r'£[\d,]+'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, page_text)
            if matches:
                for match in matches:
                    price = extract_numerical_price(match)
                    if price is not None and 1 <= price <= 1000:  # Reasonable price range
                        print(f"💰 Method 3 - Found price pattern: {match}")
                        return price
        
        # Method 4: Check if it's free
        print("🔍 Trying Method 4: Free admission check")
        free_indicators = ['free', 'no admission fee', 'no charge', 'free admission']
        page_text_lower = page_text.lower()
        for indicator in free_indicators:
            if indicator in page_text_lower:
                print(f"💰 Method 4 - Found free admission indicator: {indicator}")
                return 0.0
        
        print(f"❌ No price found for {name}")
        
        # Debug: Show what we found in the page
        print("\n🔍 DEBUG: Checking page content...")
        if 'dtFromPrice' in response.text:
            print("✅ Found 'dtFromPrice' in page source")
        else:
            print("❌ 'dtFromPrice' NOT found in page source")
        
        if '$' in response.text:
            print("✅ Found '$' symbol in page source")
        else:
            print("❌ '$' symbol NOT found in page source")
        
        return None
        
    except Exception as e:
        print(f"❌ Error parsing detail page: {e}")
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

def test_london_eye():
    """Test the London Eye URL from the image"""
    print("🧪 TESTING LONDON EYE PRICE SCRAPING")
    print("="*60)
    
    # London Eye URL from the image
    london_eye_url = "https://www.tripadvisor.com/Attraction_Review-g186338-d553603-Reviews-London_Eye-London_England.html"
    
    price = extract_price_from_detail_page(london_eye_url, "London Eye")
    
    if price is not None:
        print(f"\n✅ SUCCESS! Found price: ${price}")
    else:
        print(f"\n❌ FAILED! No price found")
    
    print("="*60)

if __name__ == "__main__":
    test_london_eye() 