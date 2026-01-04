import json

# Read the JSON file
with open('data/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add flag image URL to each country
for country in data.get('countries', []):
    if 'flag' not in country:
        iso_code = country.get('iso_code', '').lower()
        country['flag'] = f'https://flagcdn.com/w320/{iso_code}.png'

# Save back to file
with open('data/db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Successfully added flag image URLs to all countries!')
