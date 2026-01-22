import json


with open('data/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


for country in data.get('countries', []):
   
    if 'city' not in country:
        capital = country.get('capital', 'Unknown')
        country['city'] = {
            'name': capital,
            'image': f'https://images.example.com/cities/{capital.lower().replace(" ", "-")}.jpg',
            'description': f'{capital} is the capital city of {country.get("name", "")}'
        }
    

    if 'locations_map' not in country:
        country['locations_map'] = {
            'center': {
                'latitude': country.get('latitude', 0),
                'longitude': country.get('longitude', 0)
            },
            'zoom': 4,
            'map_url': f'https://maps.example.com/?lat={country.get("latitude", 0)}&lng={country.get("longitude", 0)}&zoom=4',
            'markers': []
        }
        
        # Add markers for major sites
        if 'tourism' in country and 'major_sites' in country['tourism']:
            for i, site in enumerate(country['tourism']['major_sites']):
                country['locations_map']['markers'].append({
                    'name': site,
                    'latitude': country.get('latitude', 0) + (i * 0.5),
                    'longitude': country.get('longitude', 0) + (i * 0.5),
                    'image': f'https://images.example.com/attractions/{site.lower().replace(" ", "-")}.jpg'
                })

# Save back to file
with open('data/db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Successfully added city info, image URLs, and locations map to all countries!')
