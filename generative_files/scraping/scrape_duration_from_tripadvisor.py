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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

def setup_chrome_driver(headless=True):
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")  # Run in headless mode
    else:
        print("Running Chrome in visible mode for debugging...")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Add additional options to avoid detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        print("Initializing Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✓ Chrome driver initialized successfully")
        return driver
        
    except Exception as e:
        print(f"✗ Error setting up Chrome driver: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Chrome browser is installed")
        print("2. Run the setup script: python setup_chromedriver.py")
        print("3. Or manually download ChromeDriver from: https://chromedriver.chromium.org/")
        print("4. Make sure ChromeDriver is in your PATH")
        return None

def parse_duration_to_minutes(duration_text):
    """Parse duration text like '2-3 hours' to average minutes"""
    duration_text = duration_text.strip().lower()
    
    # Handle ranges like "2-3 hours"
    if '-' in duration_text:
        parts = duration_text.split('-')
        if len(parts) == 2:
            try:
                # Extract numbers and units
                first_part = parts[0].strip()
                second_part = parts[1].strip()
                
                # Parse first number
                first_num = float(re.findall(r'\d+(?:\.\d+)?', first_part)[0])
                
                # Parse second number
                second_num = float(re.findall(r'\d+(?:\.\d+)?', second_part)[0])
                
                # Determine units
                if 'hour' in first_part or 'hour' in second_part:
                    # Convert to minutes and return average
                    return int((first_num + second_num) * 30)  # Average of range
                elif 'minute' in first_part or 'minute' in second_part:
                    return int((first_num + second_num) / 2)  # Average of range
            except:
                pass
    
    # Handle single values like "2 hours" or "30 minutes"
    try:
        numbers = re.findall(r'\d+(?:\.\d+)?', duration_text)
        if numbers:
            num = float(numbers[0])
            if 'hour' in duration_text:
                return int(num * 60)
            elif 'minute' in duration_text:
                return int(num)
    except:
        pass
    
    return None

def scrape_duration_from_tripadvisor(driver, detail_url):
    """Scrape duration from TripAdvisor detail page using Selenium"""
    if not detail_url or not detail_url.strip():
        return None
    
    try:
        print(f"    Navigating to: {detail_url}")
        
        # Navigate to the page
        driver.get(detail_url)
        
        # Wait for page to load
        wait_time = random.uniform(3, 6)
        print(f"    Waiting {wait_time:.1f} seconds for page to load...")
        time.sleep(wait_time)
        
        # Try multiple selectors for duration information
        duration_selectors = [
            'div.biGQs_P.pZUbB.AWdfh',  # Based on the HTML structure you showed
            'div[class*="duration"]',
            'span[class*="duration"]',
            'div:contains("Duration:")',
            'span:contains("Duration:")',
            '//div[contains(text(), "Duration:")]',  # XPath
            '//span[contains(text(), "Duration:")]',  # XPath
        ]
        
        duration_text = None
        
        # Try CSS selectors first
        for i, selector in enumerate(duration_selectors[:4]):
            try:
                print(f"    Trying CSS selector {i+1}: {selector}")
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if 'Duration:' in element.text:
                        duration_text = element.text
                        print(f"    ✓ Found duration with CSS selector: {duration_text}")
                        break
                if duration_text:
                    break
            except Exception as e:
                print(f"    ✗ CSS selector failed: {e}")
                continue
        
        # Try XPath selectors if CSS didn't work
        if not duration_text:
            for i, xpath in enumerate(duration_selectors[4:]):
                try:
                    print(f"    Trying XPath selector {i+1}: {xpath}")
                    elements = driver.find_elements(By.XPATH, xpath)
                    for element in elements:
                        if 'Duration:' in element.text:
                            duration_text = element.text
                            print(f"    ✓ Found duration with XPath: {duration_text}")
                            break
                    if duration_text:
                        break
                except Exception as e:
                    print(f"    ✗ XPath selector failed: {e}")
                    continue
        
        # Also try searching by text content in all elements
        if not duration_text:
            try:
                print("    Searching all div elements for 'Duration:' text...")
                all_elements = driver.find_elements(By.TAG_NAME, "div")
                for element in all_elements:
                    if element.text and 'Duration:' in element.text:
                        duration_text = element.text
                        print(f"    ✓ Found duration in div: {duration_text}")
                        break
            except Exception as e:
                print(f"    ✗ Text search failed: {e}")
        
        if duration_text:
            # Extract just the duration part
            duration_match = re.search(r'Duration:\s*(.+?)(?:\n|$)', duration_text)
            if duration_match:
                duration_part = duration_match.group(1).strip()
                parsed_duration = parse_duration_to_minutes(duration_part)
                if parsed_duration:
                    print(f"    ✓ Parsed duration: {parsed_duration} minutes")
                    return parsed_duration
                else:
                    print(f"    ✗ Could not parse duration from: {duration_part}")
            else:
                print(f"    ✗ Could not extract duration from: {duration_text}")
        else:
            print("    ✗ No duration information found on page")
        
        return None
        
    except Exception as e:
        print(f"    ✗ Error scraping {detail_url}: {e}")
        return None

def main():
    cities_dir = 'cities'
    
    # Ask user if they want to run in visible mode for debugging
    print("Chrome Driver Duration Scraper")
    print("=" * 40)
    
    headless = True
    try:
        response = input("Run Chrome in visible mode for debugging? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            headless = False
    except KeyboardInterrupt:
        print("\nExiting...")
        return
    
    # Setup Chrome driver
    driver = setup_chrome_driver(headless=headless)
    if not driver:
        print("Failed to setup Chrome driver. Exiting.")
        return
    
    try:
        for filename in os.listdir(cities_dir):
            if filename.endswith('_attractions_with_hours_and_price.json'):
                file_path = os.path.join(cities_dir, filename)
                print(f"\nProcessing {filename}...")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    updated_count = 0
                    for i, entry in enumerate(data):
                        detail_url = entry.get('detail_url', '')
                        if detail_url:
                            print(f"\n  Scraping duration for entry {i+1}/{len(data)}: {entry.get('name', 'Unknown')}")
                            
                            duration = scrape_duration_from_tripadvisor(driver, detail_url)
                            if duration:
                                entry['duration'] = duration
                                updated_count += 1
                                print(f"    ✓ Updated with duration: {duration} minutes")
                            else:
                                print(f"    ✗ No duration found")
                            
                            # Add delay to be respectful to TripAdvisor
                            delay = random.uniform(3, 7)
                            print(f"    Waiting {delay:.1f} seconds before next request...")
                            time.sleep(delay)
                        else:
                            print(f"  Skipping entry {i+1}: No detail_url")
                    
                    # Save updated file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"\n✓ Updated {filename} with {updated_count} durations")
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue
    finally:
        # Always close the driver
        print("\nClosing Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main() 