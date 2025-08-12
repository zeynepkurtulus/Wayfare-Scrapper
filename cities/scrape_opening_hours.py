import json
import time
import random

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
#INPUT_FILE = "London_attractions.json"
#OUTPUT_FILE = "London_attractions_with_hours_and_price.json"
WAIT_SECONDS = 15

DAYS_OF_WEEK = [
    "Sunday", "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday"
]


def build_city_links(city_base_url, pages=4):
    return [city_base_url.replace('oa0', f'oa{30*i}') for i in range(pages)]

CITIES = {

    # 🇺🇸 USA
    #"New_York_City": build_city_links("https://www.tripadvisor.com/Attractions-g60763-Activities-oa0-New_York_City_New_York.html", pages=4),
    #"Los_Angeles": build_city_links("https://www.tripadvisor.com/Attractions-g32655-Activities-oa0-Los_Angeles_California.html",pages=4),
    #"San_Francisco": build_city_links("https://www.tripadvisor.com/Attractions-g60713-Activities-oa0-San_Francisco_California.html",pages=4),
    #"Chicago": build_city_links("https://www.tripadvisor.com/Attractions-g35805-Activities-oa0-Chicago_Illinois.html", pages=4),
    #"Miami": build_city_links("https://www.tripadvisor.com/Attractions-g34438-Activities-oa0-Miami_Florida.html",pages=4),
   # "Las_Vegas": build_city_links("https://www.tripadvisor.com/Attractions-g45963-Activities-oa0-Las_Vegas_Nevada.html",pages=4),
    #"Orlando": build_city_links("https://www.tripadvisor.com/Attractions-g34515-Activities-oa0-Orlando_Florida.html",pages=4),
    #"Seattle": build_city_links("https://www.tripadvisor.com/Attractions-g60878-Activities-oa0-Seattle_Washington.html",pages=4),
    #"Boston": build_city_links("https://www.tripadvisor.com/Attractions-g60745-Activities-oa0-Boston_Massachusetts.html",pages=4),
   #"Washington_DC": build_city_links("https://www.tripadvisor.com/Attractions-g28970-Activities-oa0-Washington_DC_District_of_Columbia.html",pages=4),

    # 🇨🇦 Canada
    #"Toronto": build_city_links("https://www.tripadvisor.com/Attractions-g155019-Activities-oa0-Toronto_Ontario.html",pages=4),
   #"Vancouver": build_city_links("https://www.tripadvisor.com/Attractions-g154943-Activities-oa0-Vancouver_British_Columbia.html",pages=4),
   #"Montreal": build_city_links("https://www.tripadvisor.com/Attractions-g155032-Activities-oa0-Montreal_Quebec.html",pages=4),

    # 🇲🇽 Mexico
    #"Mexico_City": build_city_links("https://www.tripadvisor.com/Attractions-g150800-Activities-oa0-Mexico_City_Central_Mexico_and_Gulf_Coast.html",pages=4),
    #"Cancun": build_city_links("https://www.tripadvisor.com/Attractions-g150807-Activities-oa0-Cancun_Yucatan_Peninsula.html",pages=4),

    # 🇬🇧 UK
   #"London": build_city_links("https://www.tripadvisor.com/Attractions-g186338-Activities-oa0-London_England.html",pages=4),
    #"Edinburgh": build_city_links("https://www.tripadvisor.com/Attractions-g186525-Activities-oa0-Edinburgh_Scotland.html",pages=4),
    #"Manchester": build_city_links("https://www.tripadvisor.com/Attractions-g187069-Activities-oa0-Manchester_Greater_Manchester_England.html",pages=4),
    #"Liverpool": build_city_links("https://www.tripadvisor.com/Attractions-g186337-Activities-oa0-Liverpool_Merseyside_England.html",pages=4),
    #"Glasgow": build_city_links("https://www.tripadvisor.com/Attractions-g186534-Activities-oa0-Glasgow_Scotland.html",pages=4),
    #"Belfast": build_city_links("https://www.tripadvisor.com/Attractions-g186470-Activities-oa0-Belfast_Northern_Ireland.html",pages=4),

    # 🇫🇷 France
   # "Paris": build_city_links("https://www.tripadvisor.com/Attractions-g187147-Activities-oa0-Paris_Ile_de_France.html",pages=4),
    #"Nice": build_city_links("https://www.tripadvisor.com/Attractions-g187234-Activities-oa0-Nice_French_Riviera_Cote_d_Azur.html",pages=4),
    #"Lyon": build_city_links("https://www.tripadvisor.com/Attractions-g187265-Activities-oa0-Lyon_Rhone.html",pages=4),
    #"Marseille": build_city_links("https://www.tripadvisor.com/Attractions-g187253-Activities-oa0-Marseille_Bouches_du_Rhone.html",pages=4),
    #"Bordeaux": build_city_links("https://www.tripadvisor.com/Attractions-g187079-Activities-oa0-Bordeaux_Gironde.html",pages=4),

    # 🇮🇹 Italy
    #"Rome": build_city_links("https://www.tripadvisor.com/Attractions-g187791-Activities-oa0-Rome_Lazio.html",pages=4),
    #"Florence": build_city_links("https://www.tripadvisor.com/Attractions-g187895-Activities-oa0-Florence_Tuscany.html",pages=4),
    #"Venice": build_city_links("https://www.tripadvisor.com/Attractions-g187870-Activities-oa0-Venice_Veneto.html",pages=4),
    #"Milan": build_city_links("https://www.tripadvisor.com/Attractions-g187849-Activities-oa0-Milan_Lombardy.html",pages=4),
    #"Naples": build_city_links("https://www.tripadvisor.com/Attractions-g187785-Activities-oa0-Naples_Province_of_Naples.html",pages=4),

    # 🇪🇸 Spain
    #"Barcelona": build_city_links("https://www.tripadvisor.com/Attractions-g187497-Activities-oa0-Barcelona_Catalonia.html",pages=4),
    #"Madrid": build_city_links("https://www.tripadvisor.com/Attractions-g187514-Activities-oa0-Madrid.html",pages=4),
    #"Seville": build_city_links("https://www.tripadvisor.com/Attractions-g187443-Activities-oa0-Seville_Province_of_Seville.html",pages=4),
    #"Valencia": build_city_links("https://www.tripadvisor.com/Attractions-g187529-Activities-oa0-Valencia_Province_of_Valencia.html",pages=4),
    #"Granada": build_city_links("https://www.tripadvisor.com/Attractions-g187441-Activities-oa0-Granada_Province_of_Granada.html",pages=4),

    # 🇳🇱 Netherlands
    #"Amsterdam": build_city_links("https://www.tripadvisor.com/Attractions-g188590-Activities-oa0-Amsterdam_North_Holland_Province.html",pages=4),
    #"Rotterdam": build_city_links("https://www.tripadvisor.com/Attractions-g188632-Activities-oa0-Rotterdam_South_Holland_Province.html",pages=4),

    # 🇵🇹 Portugal
    #"Lisbon": build_city_links("https://www.tripadvisor.com/Attractions-g189158-Activities-oa0-Lisbon.html",pages=4),
    #"Porto": build_city_links("https://www.tripadvisor.com/Attractions-g189180-Activities-oa0-Porto.html",pages=4),

    # 🇬🇷 Greece
    #"Athens": build_city_links("https://www.tripadvisor.com/Attractions-g189400-Activities-oa0-Athens.html",pages=4),
    #"Thessaloniki": build_city_links("https://www.tripadvisor.com/Attractions-g189473-Activities-oa0-Thessaloniki.html",pages=4),

    # 🇹🇷 Turkey 
   # "Istanbul": build_city_links("https://www.tripadvisor.com/Attractions-g293974-Activities-oa0-Istanbul.html",pages=4),
   # "Antalya": build_city_links("https://www.tripadvisor.com/Attractions-g297962-Activities-oa0-Antalya_Turkish_Mediterranean_Coast.html",pages=4),
    #"Izmir": build_city_links("https://www.tripadvisor.com/Attractions-g298006-Activities-oa0-Izmir_Turkish_Aegean_Coast.html",pages=4),
   # "Bursa": build_city_links("https://www.tripadvisor.com/Attractions-g297977-Activities-oa0-Bursa.html",pages=4),
   # "Ankara": build_city_links("https://www.tripadvisor.com/Attractions-g298656-Activities-oa0-Ankara.html",pages=4),
    #"Cappadocia": build_city_links("https://www.tripadvisor.com/Attractions-g297980-Activities-oa0-Nevsehir_Cappadocia.html",pages=4),

    # 🇩🇪 Germany
    #"Berlin": build_city_links("https://www.tripadvisor.com/Attractions-g187323-Activities-oa0-Berlin.html",pages=4),
   # "Munich": build_city_links("https://www.tripadvisor.com/Attractions-g187309-Activities-oa0-Munich.html",pages=4),
   # "Hamburg": build_city_links("https://www.tripadvisor.com/Attractions-g187331-Activities-oa0-Hamburg.html",pages=4),

    # 🇯🇵 Japan
    #"Tokyo": build_city_links("https://www.tripadvisor.com/Attractions-g298184-Activities-oa0-Tokyo.html",pages=4),
   # "Kyoto": build_city_links("https://www.tripadvisor.com/Attractions-g298564-Activities-oa0-Kyoto.html",pages=4),
    #"Osaka": build_city_links("https://www.tripadvisor.com/Attractions-g298566-Activities-oa0-Osaka.html",pages=4),

    # 🇨🇳 China
    #"Beijing": build_city_links("https://www.tripadvisor.com/Attractions-g294212-Activities-oa0-Beijing.html",pages=4),
    #"Shanghai": build_city_links("https://www.tripadvisor.com/Attractions-g308272-Activities-oa0-Shanghai.html",pages=4),

    # 🇰🇷 South Korea
    #"Seoul": build_city_links("https://www.tripadvisor.com/Attractions-g294197-Activities-oa0-Seoul.html",pages=4),

    # 🇹🇭 Thailand
    #"Bangkok": build_city_links("https://www.tripadvisor.com/Attractions-g293916-Activities-oa0-Bangkok.html",pages=4),
    #"Chiang_Mai":build_city_links( "https://www.tripadvisor.com/Attractions-g293917-Activities-oa0-Chiang_Mai.html",pages=4),

    # 🇻🇳 Vietnam
    #"Hanoi": build_city_links("https://www.tripadvisor.com/Attractions-g293924-Activities-oa0-Hanoi.html",pages=4),
    #"Ho_Chi_Minh_City": build_city_links("https://www.tripadvisor.com/Attractions-g293925-Activities-oa0-Ho_Chi_Minh_City.html",pages=4),

    # 🇸🇬 Singapore
    #"Singapore": build_city_links("https://www.tripadvisor.com/Attractions-g294265-Activities-oa0-Singapore.html",pages=4),

    # 🇦🇺 Australia
    #"Sydney": build_city_links("https://www.tripadvisor.com/Attractions-g255060-Activities-oa0-Sydney.html",pages=4),
    #"Melbourne": build_city_links("https://www.tripadvisor.com/Attractions-g255100-Activities-oa0-Melbourne.html",pages=4),
    #"Brisbane": build_city_links("https://www.tripadvisor.com/Attractions-g255068-Activities-oa0-Brisbane.html",pages=4),
    #"Perth": build_city_links("https://www.tripadvisor.com/Attractions-g255103-Activities-oa0-Perth.html",pages=4),
    #"Cairns": build_city_links("https://www.tripadvisor.com/Attractions-g255069-Activities-oa0-Cairns.html",pages=4),

    # 🇳🇿 New Zealand
    #"Auckland": build_city_links("https://www.tripadvisor.com/Attractions-g255106-Activities-oa0-Auckland.html",pages=4),
    #"Queenstown": build_city_links("https://www.tripadvisor.com/Attractions-g255122-Activities-oa0-Queenstown.html",pages=4),
    #"Wellington": build_city_links("https://www.tripadvisor.com/Attractions-g255115-Activities-oa0-Wellington.html",pages=4),

    # 🇧🇷 Brazil --> BURDA KALDI 
    #"Rio_de_Janeiro": build_city_links("https://www.tripadvisor.com/Attractions-g303506-Activities-oa0-Rio_de_Janeiro.html",pages=4),
    #"Sao_Paulo":build_city_links("https://www.tripadvisor.com/Attractions-g303631-Activities-oa0-Sao_Paulo.html",pages=4),

    # 🇦🇷 Argentina
    #"Buenos_Aires": build_city_links("https://www.tripadvisor.com/Attractions-g312741-Activities-oa0-Buenos_Aires.html",pages=4),

    # 🇿🇦 South Africa
    #"Cape_Town": build_city_links("https://www.tripadvisor.com/Attractions-g1722390-Activities-oa0-Cape_Town.html",pages=4),
    #"Johannesburg": build_city_links("https://www.tripadvisor.com/Attractions-g312578-Activities-oa0-Johannesburg.html",pages=4),

    # 🇪🇬 Egypt
    #"Cairo": build_city_links("https://www.tripadvisor.com/Attractions-g294201-Activities-oa0-Cairo.html",pages=4),

    # 🇲🇦 Morocco
    #"Marrakech": build_city_links("https://www.tripadvisor.com/Attractions-g293734-Activities-oa0-Marrakech.html",pages=4),

    # 🇦🇪 UAE
    #"Dubai": build_city_links("https://www.tripadvisor.com/Attractions-g295424-Activities-oa0-Dubai.html",pages=4),
    #"Abu_Dhabi":build_city_links("https://www.tripadvisor.com/Attractions-g294013-Activities-oa0-Abu_Dhabi.html",pages=4),

    # 🇮🇱 Israel
   # "Jerusalem": build_city_links("https://www.tripadvisor.com/Attractions-g293983-Activities-oa0-Jerusalem.html",pages=4),
    #"Tel_Aviv": build_city_links("https://www.tripadvisor.com/Attractions-g293984-Activities-oa0-Tel_Aviv.html",pages=4),

     # 🌴 Vacation Islands
    #"Bali": build_city_links("https://www.tripadvisor.com/Attractions-g294226-Activities-oa0-Bali.html",pages=4),
    #"Phuket": build_city_links("https://www.tripadvisor.com/Attractions-g293920-Activities-oa0-Phuket.html",pages=4),
    #"Maldives": build_city_links("https://www.tripadvisor.com/Attractions-g293953-Activities-oa0-Maldives.html",pages=4),
    #"Mauritius": build_city_links("https://www.tripadvisor.com/Attractions-g293816-Activities-oa0-Mauritius.html",pages=4),
    #"Santorini": build_city_links("https://www.tripadvisor.com/Attractions-g189433-Activities-oa0-Santorini.html",pages=4),
    #"Mykonos": build_city_links("https://www.tripadvisor.com/Attractions-g189430-Activities-oa0-Mykonos.html",pages=4),
    #"Seychelles": build_city_links("https://www.tripadvisor.com/Attractions-g293738-Activities-oa0-Seychelles.html",pages=4),
    #"Tenerife": build_city_links("https://www.tripadvisor.com/Attractions-g187479-Activities-oa0-Tenerife_Canary_Islands.html",pages=4),
    #"Madeira": build_city_links("https://www.tripadvisor.com/Attractions-g189166-Activities-oa0-Madeira.html",pages=4),
    #"Bora_Bora": build_city_links("https://www.tripadvisor.com/Attractions-g311415-Activities-oa0-Bora_Bora.html",pages=4),
    #"Fiji": build_city_links("https://www.tripadvisor.com/Attractions-g294331-Activities-oa0-Fiji.html",pages=4),
    "Tahiti": build_city_links("https://www.tripadvisor.com/Attractions-g309679-Activities-oa0-Tahiti.html",pages=4)

}

## === START BROWSER ===
driver = Driver(uc=True, headless=False)
print("✅ Browser launched for detail page scraping.")


for city_name in CITIES.keys():
    input_filename = f"{city_name}_attractions.json"
    output_filename = f"{city_name}_attractions_with_hours_and_price.json"

    try:
        with open(input_filename, encoding="utf-8") as f:
            attractions = json.load(f)
        print(f"\n📂 Loaded {len(attractions)} from {input_filename}")
    except Exception as e:
        print(f"\n❌ Could not load {input_filename}: {e}")
        continue

    updated_attractions = []

    for idx, place in enumerate(attractions, start=1):
        name = place.get("name", "Unknown")
        detail_url = place.get("detail_url", "")
        print(f"\n🔎 {city_name} - {idx}/{len(attractions)}: {name}")

        if not detail_url.strip():
            print("❌ No detail URL. Skipping.")
            place["opening_hours"] = {day: "" for day in DAYS_OF_WEEK}
            place["price"] = ""
            updated_attractions.append(place)
            continue

        try:
            driver.get(detail_url)
            sleep_time = random.uniform(5, 8)
            print(f"⏳ Waiting {sleep_time:.2f}s for page load...")
            time.sleep(sleep_time)

            # === SCRAPE OPENING HOURS ===
            try:
                GRID_SELECTOR = '[data-automation="attractionsPoiHoursForDay"]'
                print("🕑 Waiting for the opening hours grid...")
                WebDriverWait(driver, WAIT_SECONDS).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, GRID_SELECTOR))
                )
                grid_div = driver.find_element(By.CSS_SELECTOR, GRID_SELECTOR)
                driver.execute_script("arguments[0].scrollIntoView(true);", grid_div)
                time.sleep(2)

                children = grid_div.find_elements(By.XPATH, './*')
                print(f"✅ Found {len(children)} children in grid.")

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
                        print(f"⚠️ Could not extract hours for {day}: {e}")
                        hours = ""

                    if day in DAYS_OF_WEEK and hours:
                        opening_hours[day] = hours
                    else:
                        print(f"⚠️ Skipped pair: '{day}' / '{hours}'")

                # Fill in missing days
                for day in DAYS_OF_WEEK:
                    if day not in opening_hours:
                        opening_hours[day] = ""

                print(f"✅ Extracted opening_hours: {opening_hours}")
                place["opening_hours"] = opening_hours

            except Exception as e:
                print(f"❌ Could not scrape opening hours for {name}: {e}")
                place["opening_hours"] = {day: "" for day in DAYS_OF_WEEK}

            # === SCRAPE PRICE ===
            try:
                price_selector = '[data-automation="dtFromPrice"]'
                price_elem = driver.find_element(By.CSS_SELECTOR, price_selector)
                price_text = price_elem.text.strip()
                print(f"💰 Found price: {price_text}")
                place["price"] = price_text
            except Exception as e:
                print(f"⚠️ Could not extract price for {name}: {e}")
                place["price"] = ""

        except Exception as e:
            print(f"❌ Unexpected error on detail page for {name}: {e}")
            place["opening_hours"] = {day: "" for day in DAYS_OF_WEEK}
            place["price"] = ""

        updated_attractions.append(place)

    # === SAVE OUTPUT ===
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(updated_attractions, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved updated data to {output_filename}")


driver.quit()
print("\n👋 All cities done. Browser closed.")