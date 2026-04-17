import requests
from bs4 import BeautifulSoup
import json
import time
import urllib.parse
from pathlib import Path

def fetch_hotel_link(hotel_name, city):
    query = f"{hotel_name} {city}"
    search_url = f"https://www.hotels.com/search.do?q-destination={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = requests.get(search_url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Find the first hotel link in search results
        hotel_link_tag = soup.select_one('a.property-name-link')
        if hotel_link_tag and hotel_link_tag['href']:
            # Construct absolute URL
            return urllib.parse.urljoin("https://www.hotels.com", hotel_link_tag['href'])
    return None

def main():
    # Path to your JSON file
    file_path = Path(r'D:\hotel-comparison\static\hotels-merged.json')

    # Load JSON data
    with open(file_path, 'r', encoding='utf-8') as f:
        hotels_data = json.load(f)

    # Process each hotel entry
    for hotel in hotels_data:
        name = hotel.get('hotelName')
        city = hotel.get('city')
        if name and city:
            print(f"Searching link for: {name} in {city}")
            link = fetch_hotel_link(name, city)
            if link:
                print(f"Found link: {link}")
                hotel['link'] = link
            else:
                print(f"No link found for: {name}")
            time.sleep(1)  # polite delay between requests
    
    # Save updated JSON file
    output_path = file_path.parent / 'hotels-merged-updated.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(hotels_data, f, ensure_ascii=False, indent=2)
    print(f"Updated JSON saved to: {output_path}")

if __name__ == "__main__":
    main()
