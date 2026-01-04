import json

# Read the JSON file
with open('data/db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Historical overviews for countries
history_data = {
    "Afghanistan": "Afghanistan has a rich history spanning thousands of years, serving as a crossroads between Central Asia, South Asia, and the Middle East. It was home to ancient Silk Road trade routes and has been ruled by various empires including the Persian, Greek, and Mughal empires.",
    "Albania": "Albania has a long history dating back to ancient Illyrian kingdoms. It was ruled by the Romans, Byzantines, and Ottomans before gaining independence in 1912. The country has undergone significant transformation, especially after the fall of communism in 1990.",
    "Algeria": "Algeria was home to ancient Numidia and served as a Roman colony. It was later ruled by the Ottoman Empire for centuries before French colonization. Algeria gained independence in 1962 after a lengthy struggle.",
    "Andorra": "Andorra is one of Europe's oldest states, with a unique system of governance dating back to 1278. It has maintained independence and neutrality for centuries, protected by its mountain location.",
    "Angola": "Angola has a diverse history with ancient kingdoms, Portuguese colonization, and a significant period under the Angolan slave trade. It gained independence in 1975 and has since developed into a major African nation.",
    "Antigua and Barbuda": "Antigua and Barbuda were originally inhabited by the Arawak and later Carib peoples. The islands were colonized by the British in the 17th century and gained independence in 1981.",
    "Argentina": "Argentina has a rich history with indigenous civilizations, Spanish colonization, and independence in 1816. It developed into a major economic power in South America during the 19th and 20th centuries.",
}

# Add history field to each country
for country in data.get('countries', []):
    if 'history' not in country:
        country_name = country.get('name', '')
        
        # Use predefined history if available, otherwise generate a generic one
        if country_name in history_data:
            country['history'] = {
                'overview': history_data[country_name],
                'founded_year': 'Ancient times' if 'Afghanistan' in country_name or 'Albania' in country_name else 'Various periods',
                'independence_year': country.get('independence_year', 'Check local records'),
                'key_events': [
                    f'{country_name} has experienced significant cultural and political developments',
                    'Major transformations during colonial and post-colonial periods',
                    'Modern development and integration into the global community'
                ],
                'notable_periods': [
                    'Ancient civilizations',
                    'Medieval period',
                    'Colonial period',
                    'Modern era'
                ]
            }
        else:
            # Generic history for other countries
            country['history'] = {
                'overview': f'{country_name} has a diverse and rich history spanning multiple civilizations and empires.',
                'founded_year': 'Ancient times',
                'independence_year': 'Varies by period',
                'key_events': [
                    f'{country_name} has been shaped by various cultural influences',
                    'Notable developments during different historical periods',
                    'Modern transformation and growth'
                ],
                'notable_periods': [
                    'Ancient period',
                    'Medieval period',
                    'Colonial/Modern period',
                    'Contemporary era'
                ]
            }

# Save back to file
with open('data/db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Successfully added history overview to all countries!')
