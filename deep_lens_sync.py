import json

def deep_lens_sync():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 2026 新旗艦鏡頭與深度數據
    deep_data = {
        # --- Canon L-Series ---
        "RF 14mm f/1.4 L VCM": {
            "opticalDesign": "15 groups, 19 elements",
            "specialElements": "2 UD, 3 Aspherical, 1 BR element",
            "coatings": "ASC, SWC, Fluorine Coating",
            "motorType": "VCM (Voice Coil Motor) + Nano USM",
            "hasApertureRing": True,
            "hasWeatherSeal": True,
            "brand": "Canon",
            "gearType": "LENS",
            "releaseYear": 2026,
            "launchPrice": 72900,
            "focalLengthMinMm": 14,
            "focalLengthMaxMm": 14,
            "apertureMax": "1.4",
            "filterSizeMm": 0 # Rear filter
        },
        "RF 24-70mm F2.8L IS USM": {
            "opticalDesign": "15 groups, 21 elements",
            "specialElements": "3 UD, 3 Aspherical",
            "coatings": "ASC, Fluorine Coating",
            "motorType": "Nano USM",
            "hasApertureRing": False, # Has Control Ring
            "hasWeatherSeal": True
        },
        # --- Nikon S-Line ---
        "Z 70-200mm f/2.8 VR S II": {
            "opticalDesign": "18 groups, 21 elements",
            "specialElements": "2 Fluorite, 1 SR, 6 ED, 2 Aspherical",
            "coatings": "Meso Amorphous, Arneo, Nano Crystal",
            "motorType": "VCM + Multi-focusing System",
            "hasApertureRing": True,
            "hasWeatherSeal": True,
            "brand": "Nikon",
            "gearType": "LENS",
            "releaseYear": 2026,
            "launchPrice": 82900,
            "focalLengthMinMm": 70,
            "focalLengthMaxMm": 200,
            "apertureMax": "2.8"
        },
        "Z 85mm f/1.2 S": {
            "opticalDesign": "10 groups, 15 elements",
            "specialElements": "2 Aspherical, 1 ED",
            "coatings": "Nano Crystal Coating",
            "motorType": "Multi-focusing System (STM)",
            "hasApertureRing": True,
            "hasWeatherSeal": True
        },
        # --- Fujifilm WR/LM ---
        "XF 16-55mm F2.8 R LM WR II": {
            "opticalDesign": "12 groups, 17 elements",
            "specialElements": "3 ED, 4 Aspherical",
            "coatings": "Nano GI Coating",
            "motorType": "Linear Motor (LM)",
            "hasApertureRing": True,
            "hasWeatherSeal": True,
            "brand": "Fujifilm",
            "gearType": "LENS",
            "releaseYear": 2026,
            "launchPrice": 38900,
            "focalLengthMinMm": 16,
            "focalLengthMaxMm": 55,
            "apertureMax": "2.8"
        }
    }

    updated_count = 0
    added_count = 0
    
    # 首先更新現有鏡頭
    for item in products:
        name = item['modelName']
        if name in deep_data:
            item.update(deep_data[name])
            updated_count += 1

    # 然後加入 2026 新鏡頭
    existing_names = {p['modelName'] for p in products}
    for name, data in deep_data.items():
        if name not in existing_names:
            data['modelName'] = name
            data['slug'] = name.lower().replace(' ', '-')
            data['id'] = data['slug']
            products.append(data)
            added_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"DEEP_LENS_SYNC_COMPLETE: Updated {updated_count} lenses, Added {added_count} new 2026 flagship lenses.")

if __name__ == "__main__":
    deep_lens_sync()
