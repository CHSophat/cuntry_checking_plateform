import json

# Read the JSON file
with open('data/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add image and recommendations to countries
for country in data.get('countries', []):
    if 'image' not in country:
        country['image'] = f'https://images.example.com/countries/{country.get("iso_code", "unknown").lower()}.jpg'
    if 'recommendations' not in country:
        country['recommendations'] = [
            'Visit the local museums',
            'Explore traditional markets',
            'Taste local cuisine',
            'Experience cultural festivals',
            'Interact with local communities'
        ]

# Add image and recommendations to attractions in tourism section
for country in data.get('countries', []):
    if 'tourism' in country and 'major_sites' in country['tourism']:
        if 'sites_with_images' not in country['tourism']:
            country['tourism']['sites_with_images'] = []
            for site in country['tourism']['major_sites']:
                site_slug = site.lower().replace(' ', '-')
                country['tourism']['sites_with_images'].append({
                    'name': site,
                    'image': f'https://images.example.com/attractions/{site_slug}.jpg',
                    'recommendations': ['Take guided tour', 'Visit at sunrise', 'Hire local guide']
                })

# Save back to file
with open('data/db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Successfully added image and recommendations fields to all data!')
