import json

def normalize():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    brand_map = {
        'sony': 'Sony', 'canon': 'Canon', 'nikon': 'Nikon', 'fujifilm': 'Fujifilm',
        'sigma': 'Sigma', 'tamron': 'Tamron', 'samyang': 'Samyang', 'viltrox': 'Viltrox',
        'laowa': 'Laowa', 'venus optics': 'Laowa', 'tokina': 'Tokina', 'zeiss': 'Zeiss',
        'panasonic': 'Panasonic', 'leica': 'Leica', 'pentax': 'Pentax', 'om system': 'OM System',
        'olympus': 'OM System', 'voigtlander': 'Voigtlander'
    }

    for item in products:
        b_raw = str(item.get('brand', '')).strip()
        b_lower = b_raw.lower()
        
        if b_lower in brand_map:
            item['brand'] = brand_map[b_lower]
        elif b_raw:
            item['brand'] = b_raw[0].upper() + b_raw[1:]
            
        # Fix obvious errors
        if len(item['brand']) > 15 or any(c.isdigit() for c in item['brand']):
            name = item.get('modelName', '')
            for key in brand_map.values():
                if key.lower() in name.lower():
                    item['brand'] = key
                    break

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print('Normalization complete.')

if __name__ == "__main__":
    normalize()
