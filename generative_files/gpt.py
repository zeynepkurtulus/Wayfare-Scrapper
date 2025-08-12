import requests
from bs4 import BeautifulSoup
import time
import re

BASE_URL = "https://www.tripadvisor.com"
CITY_URL_TEMPLATE = BASE_URL + "/Attractions-g293974-Activities-oa{offset}-Istanbul.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def extract_detail_urls(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    urls = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/Attraction_Review"):
            full_url = BASE_URL + href.split("?")[0]  # remove query params
            urls.add(full_url)
    return urls

def scrape_tripadvisor_urls(total=120, per_page=30):
    all_urls = set()
    for offset in range(0, total, per_page):
        url = CITY_URL_TEMPLATE.format(offset=offset)
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch: {url}")
            continue
        page_urls = extract_detail_urls(response.text)
        all_urls.update(page_urls)
        time.sleep(1.5)  # be nice to servers
    return list(all_urls)[:total]

if __name__ == "__main__":
    result = scrape_tripadvisor_urls()
    for idx, url in enumerate(result, 1):
        print(f"{idx:03d}: {url}")
