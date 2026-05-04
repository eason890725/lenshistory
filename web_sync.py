import json
import re

def add_new_gear():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    existing_names = {p['modelName'].lower() for p in products}
    
    new_items = [
        # --- Bodies ---
        {"brand": "Sony", "modelName": "Alpha 1 II", "gearType": "CAMERA_BODY", "megapixels": 50.1, "weightGrams": 746, "releaseYear": 2024, "launchPrice": 210000, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Stacked CMOS"},
        {"brand": "Sony", "modelName": "Alpha 9 III", "gearType": "CAMERA_BODY", "megapixels": 24.6, "weightGrams": 617, "releaseYear": 2024, "launchPrice": 184980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Global Shutter Stacked CMOS"},
        {"brand": "Sony", "modelName": "Alpha 7R V", "gearType": "CAMERA_BODY", "megapixels": 61.0, "weightGrams": 723, "releaseYear": 2022, "launchPrice": 109980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "BSI CMOS"},
        {"brand": "Sony", "modelName": "Alpha 7 IV", "gearType": "CAMERA_BODY", "megapixels": 33.0, "weightGrams": 658, "releaseYear": 2021, "launchPrice": 64980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "BSI CMOS"},
        {"brand": "Sony", "modelName": "Alpha 7C II", "gearType": "CAMERA_BODY", "megapixels": 33.0, "weightGrams": 514, "releaseYear": 2023, "launchPrice": 59980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "BSI CMOS"},
        {"brand": "Sony", "modelName": "Alpha 6700", "gearType": "CAMERA_BODY", "megapixels": 26.0, "weightGrams": 493, "releaseYear": 2023, "launchPrice": 44980, "hasIBIS": True, "sensorFormat": "APS-C", "sensorType": "BSI CMOS"},
        {"brand": "Sony", "modelName": "FX3", "gearType": "CAMERA_BODY", "megapixels": 12.1, "weightGrams": 630, "releaseYear": 2021, "launchPrice": 109980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "BSI CMOS"},
        {"brand": "Sony", "modelName": "FX30", "gearType": "CAMERA_BODY", "megapixels": 26.0, "weightGrams": 562, "releaseYear": 2022, "launchPrice": 59980, "hasIBIS": True, "sensorFormat": "APS-C", "sensorType": "BSI CMOS"},
        
        # --- Lenses ---
        {"brand": "Sony", "modelName": "FE 28-70mm F2 GM", "gearType": "LENS", "apertureMax": "2.0", "weightGrams": 918, "filterSizeMm": 86, "releaseYear": 2024, "launchPrice": 92980, "hasOIS": False, "hasWeatherSeal": True, "hasApertureRing": True, "focalLengthMinMm": 28, "focalLengthMaxMm": 70, "series": "GM"},
        {"brand": "Sony", "modelName": "FE 85mm F1.4 GM II", "gearType": "LENS", "apertureMax": "1.4", "weightGrams": 642, "filterSizeMm": 77, "releaseYear": 2024, "launchPrice": 56980, "hasOIS": False, "hasWeatherSeal": True, "hasApertureRing": True, "focalLengthMinMm": 85, "focalLengthMaxMm": 85, "series": "GM"},
        {"brand": "Sony", "modelName": "E 11mm F1.8", "gearType": "LENS", "apertureMax": "1.8", "weightGrams": 181, "filterSizeMm": 55, "releaseYear": 2022, "launchPrice": 13980, "hasOIS": False, "hasWeatherSeal": True, "hasApertureRing": False, "focalLengthMinMm": 11, "focalLengthMaxMm": 11, "series": "G"}
    ]
    
    added_count = 0
    for item in new_items:
        if item['modelName'].lower() not in existing_names:
            # Generate Slug
            slug = re.sub(r'[^\w\s-]', '', item['modelName'].lower()).replace(' ', '-')
            item['slug'] = slug
            item['id'] = slug
            products.append(item)
            added_count += 1
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"WEB_SYNC_COMPLETE: Added {added_count} new Sony products.")

if __name__ == "__main__":
    add_new_gear()
