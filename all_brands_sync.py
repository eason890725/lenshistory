import json
import re

def add_all_brands_gear():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    existing_names = {p['modelName'].lower() for p in products}
    
    new_items = [
        # --- Canon Bodies ---
        {"brand": "Canon", "modelName": "EOS R1", "gearType": "CAMERA_BODY", "megapixels": 24.2, "weightGrams": 1115, "releaseYear": 2024, "launchPrice": 210000, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Stacked CMOS", "videoResolution": "6K 60p / 4K 120p", "afPoints": "1053 Zones"},
        {"brand": "Canon", "modelName": "EOS R5 II", "gearType": "CAMERA_BODY", "megapixels": 45.0, "weightGrams": 746, "releaseYear": 2024, "launchPrice": 119980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Stacked CMOS", "videoResolution": "8K 60p / 4K 120p"},
        {"brand": "Canon", "modelName": "EOS R6 II", "gearType": "CAMERA_BODY", "megapixels": 24.2, "weightGrams": 670, "releaseYear": 2022, "launchPrice": 69980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "CMOS", "videoResolution": "4K 60p"},
        {"brand": "Canon", "modelName": "EOS R7", "gearType": "CAMERA_BODY", "megapixels": 32.5, "weightGrams": 612, "releaseYear": 2022, "launchPrice": 44980, "hasIBIS": True, "sensorFormat": "APS-C", "sensorType": "CMOS", "videoResolution": "4K 60p"},
        
        # --- Nikon Bodies ---
        {"brand": "Nikon", "modelName": "Z9", "gearType": "CAMERA_BODY", "megapixels": 45.7, "weightGrams": 1340, "releaseYear": 2021, "launchPrice": 165000, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Stacked CMOS", "videoResolution": "8K 60p / 4K 120p", "afPoints": "493"},
        {"brand": "Nikon", "modelName": "Z8", "gearType": "CAMERA_BODY", "megapixels": 45.7, "weightGrams": 910, "releaseYear": 2023, "launchPrice": 124980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Stacked CMOS", "videoResolution": "8K 60p / 4K 120p"},
        {"brand": "Nikon", "modelName": "Z6 III", "gearType": "CAMERA_BODY", "megapixels": 24.5, "weightGrams": 670, "releaseYear": 2024, "launchPrice": 79980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "Partially Stacked CMOS", "videoResolution": "6K 60p / 4K 120p"},
        {"brand": "Nikon", "modelName": "Zf", "gearType": "CAMERA_BODY", "megapixels": 24.5, "weightGrams": 710, "releaseYear": 2023, "launchPrice": 66980, "hasIBIS": True, "sensorFormat": "Full Frame", "sensorType": "CMOS", "videoResolution": "4K 60p"},
        
        # --- Fujifilm Bodies ---
        {"brand": "Fujifilm", "modelName": "X-T5", "gearType": "CAMERA_BODY", "megapixels": 40.2, "weightGrams": 557, "releaseYear": 2022, "launchPrice": 52980, "hasIBIS": True, "sensorFormat": "APS-C", "sensorType": "X-Trans CMOS 5 HR", "videoResolution": "6.2K 30p"},
        {"brand": "Fujifilm", "modelName": "X-H2s", "gearType": "CAMERA_BODY", "megapixels": 26.1, "weightGrams": 660, "releaseYear": 2022, "launchPrice": 74980, "hasIBIS": True, "sensorFormat": "APS-C", "sensorType": "Stacked X-Trans CMOS 5 HS", "videoResolution": "6.2K 30p / 4K 120p"},
        {"brand": "Fujifilm", "modelName": "GFX 100 II", "gearType": "CAMERA_BODY", "megapixels": 102.0, "weightGrams": 1030, "releaseYear": 2023, "launchPrice": 249800, "hasIBIS": True, "sensorFormat": "Medium Format", "sensorType": "CMOS II HS", "videoResolution": "8K 30p / 4K 60p"},
        
        # --- Sigma / Tamron Lenses ---
        {"brand": "Sigma", "modelName": "24-70mm F2.8 DG DN II Art", "gearType": "LENS", "apertureMax": "2.8", "weightGrams": 745, "filterSizeMm": 82, "releaseYear": 2024, "launchPrice": 36980, "hasOIS": False, "hasWeatherSeal": True, "hasApertureRing": True, "focalLengthMinMm": 24, "focalLengthMaxMm": 70, "motorType": "HLA (High-response Linear Actuator)"},
        {"brand": "Tamron", "modelName": "28-75mm F2.8 Di III VXD G2", "gearType": "LENS", "apertureMax": "2.8", "weightGrams": 540, "filterSizeMm": 67, "releaseYear": 2021, "launchPrice": 28800, "hasOIS": False, "hasWeatherSeal": True, "hasApertureRing": False, "focalLengthMinMm": 28, "focalLengthMaxMm": 75, "motorType": "VXD Linear"},
        {"brand": "Tamron", "modelName": "35-150mm F2-2.8 Di III VXD", "gearType": "LENS", "apertureMax": "2.0-2.8", "weightGrams": 1165, "filterSizeMm": 82, "releaseYear": 2021, "launchPrice": 52800, "hasOIS": False, "hasWeatherSeal": True, "hasApertureRing": False, "focalLengthMinMm": 35, "focalLengthMaxMm": 150, "motorType": "VXD Linear"}
    ]
    
    added_count = 0
    for item in new_items:
        if item['modelName'].lower() not in existing_names:
            slug = re.sub(r'[^\w\s-]', '', item['modelName'].lower()).replace(' ', '-')
            item['slug'] = slug
            item['id'] = slug
            # Initialize common fields
            if item['gearType'] == 'CAMERA_BODY':
                item.setdefault('logSupport', 'Log Support')
                item.setdefault('evfResolution', '--')
                item.setdefault('burstSpeed', '--')
            products.append(item)
            added_count += 1
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"ALL_BRANDS_SYNC_COMPLETE: Added {added_count} new products from Canon, Nikon, Fujifilm, Sigma, and Tamron.")

if __name__ == "__main__":
    add_all_brands_gear()
