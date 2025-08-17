import json
import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
WAIT_SECONDS = 15
DELAY_RANGE = (3, 6)  # Random delay between requests

DAYS_OF_WEEK = [
    "Sunday", "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday"
]

# Setup logging
log_filename = f"opening_hours_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log_and_print(message):
    """Print to console and save to log file"""
    print(message)
    with open(log_filename, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")

def extract_opening_hours(driver, detail_url, name):
    """Extract opening hours from TripAdvisor detail page"""
    try:
        driver.get(detail_url)
        sleep_time = random.uniform(*DELAY_RANGE)
        log_and_print(f"⏳ Waiting {sleep_time:.2f}s for page load...")
        time.sleep(sleep_time)

        # === SCRAPE OPENING HOURS ===
        try:
            GRID_SELECTOR = '[data-automation="attractionsPoiHoursForDay"]'
            log_and_print("🕑 Waiting for the opening hours grid...")
            WebDriverWait(driver, WAIT_SECONDS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, GRID_SELECTOR))
            )
            grid_div = driver.find_element(By.CSS_SELECTOR, GRID_SELECTOR)
            driver.execute_script("arguments[0].scrollIntoView(true);", grid_div)
            time.sleep(2)

            children = grid_div.find_elements(By.XPATH, './*')
            log_and_print(f"✅ Found {len(children)} children in grid.")

            opening_hours = {}

            for i in range(0, len(children), 2):
                day_div = children[i]
                time_container = children[i + 1]
                day_attr = day_div.get_attribute('data-automation')
                day = day_attr.split('.')[0].strip() if day_attr else ""

                try:
                    hours_element = time_container.find_element(By.XPATH, './/div')
                    hours_attr = hours_element.get_attribute('data-automation')
                    hours = hours_attr.split('.')[0].strip() if hours_attr else ""
                except Exception as e:
                    log_and_print(f"⚠️ Could not extract hours for {day}: {e}")
                    hours = ""

                if day in DAYS_OF_WEEK and hours:
                    opening_hours[day] = hours
                else:
                    log_and_print(f"⚠️ Skipped pair: '{day}' / '{hours}'")

            # Fill in missing days
            for day in DAYS_OF_WEEK:
                if day not in opening_hours:
                    opening_hours[day] = ""

            log_and_print(f"✅ Extracted opening_hours: {opening_hours}")
            return opening_hours

        except Exception as e:
            log_and_print(f"❌ Could not scrape opening hours for {name}: {e}")
            return {day: "" for day in DAYS_OF_WEEK}

    except Exception as e:
        log_and_print(f"❌ Error accessing {detail_url}: {e}")
        return {day: "" for day in DAYS_OF_WEEK}

def process_all_cities():
    """Process all cities in the cities directory"""
    cities_dir = 'cities'
    total_files_processed = 0
    total_hours_updated = 0
    successful_cities = []
    failed_cities = []
    
    log_and_print("🕑 OPENING HOURS SCRAPING")
    log_and_print("Scraping opening hours from TripAdvisor detail pages")
    log_and_print("="*60)
    log_and_print(f"📝 Log file: {log_filename}")
    
    # Get total number of files to process
    files_to_process = [f for f in os.listdir(cities_dir) if f.endswith('_attractions_with_hours_and_price.json')]
    total_files = len(files_to_process)
    
    # Setup browser
    log_and_print("🚀 Launching browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        for file_index, filename in enumerate(files_to_process, 1):
            city_name = filename.replace('_attractions_with_hours_and_price.json', '')
            log_and_print(f"\n🌍 [{file_index}/{total_files}] Scraping opening hours for: {city_name}")

            file_path = os.path.join(cities_dir, filename)
            try:
                with open(file_path, encoding="utf-8") as f:
                    existing_data = json.load(f)
                log_and_print(f"✅ Loaded {len(existing_data)} existing places from file")
            except Exception as e:
                log_and_print(f"❌ Could not load file: {e}")
                failed_cities.append(city_name)
                continue

            hours_updated = 0
            hours_found = 0
            hours_missing = 0
            
            try:
                for i, entry in enumerate(existing_data):
                    name = entry.get("name", "")
                    detail_url = entry.get("detail_url", "")

                    if not detail_url:
                        log_and_print(f"❌ No detail URL for: {name}")
                        hours_missing += 1
                        continue

                    # Show progress without too much detail
                    if i % 10 == 0 or i == len(existing_data) - 1:
                        log_and_print(f"  [{i+1}/{len(existing_data)}] 🕑 Processing: {name[:30]}...")
                    
                    opening_hours = extract_opening_hours(driver, detail_url, name)
                    
                    if opening_hours and any(opening_hours.values()):  # Check if any hours were found
                        old_hours = entry.get("opening_hours", {})
                        existing_data[i]["opening_hours"] = opening_hours
                        hours_updated += 1
                        hours_found += 1
                        
                        # Only show updates for every 10th item
                        if i % 10 == 0 or i == len(existing_data) - 1:
                            if old_hours and any(old_hours.values()):
                                log_and_print(f"    ✅ Hours updated for {name[:30]}")
                            else:
                                log_and_print(f"    ✅ Hours added for {name[:30]}")
                    else:
                        hours_missing += 1
                        # Only show missing hours for every 10th item
                        if i % 10 == 0 or i == len(existing_data) - 1:
                            log_and_print(f"    ❌ No hours found for {name[:30]}")

                # Save to the same file (overwrite)
                if hours_updated > 0:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(existing_data, f, ensure_ascii=False, indent=2)
                    log_and_print(f"💾 File updated: {file_path} ({hours_updated} hours updated)")
                    total_files_processed += 1
                    total_hours_updated += hours_updated
                    successful_cities.append(city_name)
                else:
                    log_and_print(f"ℹ️  No hours updates needed for {city_name}")
                    successful_cities.append(city_name)
                
                # Progress summary for this city
                log_and_print(f"📊 {city_name} Summary: {hours_found} found, {hours_missing} missing")

            except Exception as e:
                log_and_print(f"❌ Error during scraping: {e}")
                failed_cities.append(city_name)
    
    finally:
        driver.quit()
        log_and_print("🔒 Browser closed")
    
    # Final Summary
    log_and_print("\n" + "="*60)
    log_and_print("OPENING HOURS SCRAPING SUMMARY")
    log_and_print("="*60)
    log_and_print(f"Files processed: {total_files_processed}")
    log_and_print(f"Total hours updated: {total_hours_updated}")
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
