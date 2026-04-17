import json
from pathlib import Path

# Path to your updated JSON file
file_path = Path(r'D:\hotel-comparison\static\hotels-merged-updated.json')

# Load JSON data
with open(file_path, 'r', encoding='utf-8') as f:
    hotels_data = json.load(f)

# Replace Hotels.com source links with general Hotels.com homepage
for hotel in hotels_data:
    if 'sources' in hotel:
        for source in hotel['sources']:
            if source.get('provider') == 'Hotels.com':
                source['link'] = "https://www.hotels.com"

# Save the modified JSON file (overwrite or new file)
output_path = file_path.parent / 'hotels-merged-hotelscom-homepage.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(hotels_data, f, ensure_ascii=False, indent=2)

print(f"Updated JSON saved to: {output_path}")
