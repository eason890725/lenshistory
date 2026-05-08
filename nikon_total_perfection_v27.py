import json

def nikon_total_perfection_v27():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0

    # Nikon 官方 True-North 規格基準庫 (Z-mount Bodies)
    nikon_master_db = {
        "z9": {
            "modelName": "Nikon Z 9",
            "megapixels": "45.7MP",
            "sensorType": "Stacked CMOS",
            "processor": "EXPEED 7",
            "launchPrice": 165000,
            "ibisRating": "6.0 stops (CIPA)",
            "weightGrams": "Approx. 1340 g (including battery and card)",
            "dimensions": "149.0 x 149.5 x 90.5 mm",
            "videoResolution": "8K 60p / 4K 120p / ProRes RAW",
            "evfResolution": "3.69M-dot Quad-VGA OLED",
            "burstSpeed": "20 fps (RAW) / 120 fps (JPEG)",
            "batterySpec": "EN-EL18d (Approx. 740 shots CIPA)",
            "afTargets": "Human, Animal (Dog, Cat, Bird), Vehicle (Car, Bike, Plane, Train)",
            "aliases": ["Z9", "z9", "NikonZ9", "Flagship"]
        },
        "z8": {
            "modelName": "Nikon Z 8",
            "megapixels": "45.7MP",
            "sensorType": "Stacked CMOS",
            "processor": "EXPEED 7",
            "launchPrice": 118800,
            "ibisRating": "6.0 stops (CIPA)",
            "weightGrams": "Approx. 910 g (including battery and card)",
            "dimensions": "144.0 x 118.5 x 83.0 mm",
            "videoResolution": "8K 60p / 4K 120p / N-RAW",
            "evfResolution": "3.69M-dot Quad-VGA OLED",
            "burstSpeed": "20 fps (RAW) / 120 fps (JPEG)",
            "batterySpec": "EN-EL15c (Approx. 340 shots CIPA)",
            "afTargets": "Human, Animal, Bird, Vehicle, Plane",
            "aliases": ["Z8", "z8", "NikonZ8"]
        },
        "z6-iii": {
            "modelName": "Nikon Z 6III",
            "megapixels": "24.5MP",
            "sensorType": "Partially Stacked CMOS",
            "processor": "EXPEED 7",
            "launchPrice": 75900,
            "ibisRating": "8.0 stops (CIPA)",
            "weightGrams": "Approx. 760 g (including battery and card)",
            "dimensions": "138.5 x 101.5 x 74.0 mm",
            "videoResolution": "6K 60p N-RAW / 4K 120p",
            "evfResolution": "5.76M-dot Bright OLED",
            "burstSpeed": "14 fps (Mech) / 120 fps (JPEG)",
            "batterySpec": "EN-EL15c (Approx. 360 shots CIPA)",
            "afTargets": "Human, Animal, Bird, Vehicle, Plane",
            "aliases": ["Z63", "z6iii", "Z6III"]
        },
        "zf": {
            "modelName": "Nikon Z f",
            "megapixels": "24.5MP",
            "sensorType": "BSI CMOS",
            "processor": "EXPEED 7",
            "launchPrice": 63800,
            "ibisRating": "8.0 stops (CIPA)",
            "weightGrams": "Approx. 710 g (including battery and card)",
            "dimensions": "144.0 x 103.0 x 49.0 mm",
            "videoResolution": "4K 60p (Cropped) / 4K 30p",
            "evfResolution": "3.69M-dot OLED",
            "batterySpec": "EN-EL15c (Approx. 380 shots CIPA)",
            "aliases": ["Zf", "zf", "NikonZf"]
        },
        "z7-ii": {
            "modelName": "Nikon Z 7II",
            "megapixels": "45.7MP",
            "processor": "Dual EXPEED 6",
            "launchPrice": 88000,
            "ibisRating": "5.0 stops (CIPA)",
            "weightGrams": "Approx. 705 g",
            "dimensions": "134.0 x 100.5 x 69.5 mm",
            "evfResolution": "3.69M-dot OLED",
            "aliases": ["Z72", "z7ii"]
        },
        "z6-ii": {
            "modelName": "Nikon Z 6II",
            "megapixels": "24.5MP",
            "processor": "Dual EXPEED 6",
            "launchPrice": 56900,
            "ibisRating": "5.0 stops (CIPA)",
            "weightGrams": "Approx. 705 g",
            "dimensions": "134.0 x 100.5 x 69.5 mm",
            "evfResolution": "3.69M-dot OLED",
            "aliases": ["Z62", "z6ii"]
        },
        "z5": {
            "modelName": "Nikon Z 5",
            "megapixels": "24.3MP",
            "processor": "EXPEED 6",
            "launchPrice": 39900,
            "ibisRating": "5.0 stops (CIPA)",
            "weightGrams": "Approx. 675 g",
            "dimensions": "134.0 x 100.5 x 69.5 mm",
            "aliases": ["Z5", "z5"]
        },
        "zfc": {
            "modelName": "Nikon Z fc",
            "megapixels": "20.9MP",
            "processor": "EXPEED 6",
            "launchPrice": 28900,
            "ibisRating": "No (Lens OIS support)",
            "weightGrams": "Approx. 445 g",
            "dimensions": "134.5 x 93.5 x 43.5 mm",
            "aliases": ["Zfc", "zfc"]
        }
    }

    for item in products:
        if item.get('brand') != 'Nikon' or item.get('gearType') != 'CAMERA_BODY':
            continue
            
        item_id = item.get('id', '')
        if item_id in nikon_master_db:
            specs = nikon_master_db[item_id]
            for key, val in specs.items():
                item[key] = val
                fixed_count += 1
        
        # 命名標準化 (確保包含 Nikon 前綴)
        if item.get('modelName') and not item['modelName'].startswith("Nikon"):
            item['modelName'] = f"Nikon {item['modelName']}"
            fixed_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"NIKON_TOTAL_PERFECTION_V27_COMPLETE: Updated {fixed_count} technical and physical fields for Nikon gear.")

if __name__ == "__main__":
    nikon_total_perfection_v27()
