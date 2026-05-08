import json

def nikon_legacy_correction_v32():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0

    # Nikon 經典機型精確規格庫
    nikon_legacy_db = {
        "z7": {
            "modelName": "Nikon Z 7",
            "processor": "EXPEED 6",
            "weightGrams": "Approx. 675 g (including battery and card)",
            "dimensions": "134.0 x 100.5 x 67.5 mm",
            "launchPrice": 105000,
            "ibisRating": "5.0 stops (CIPA)",
            "videoColorDepth": "10-bit (via HDMI)",
            "logSupport": "N-Log (External)"
        },
        "z6": {
            "modelName": "Nikon Z 6",
            "processor": "EXPEED 6",
            "weightGrams": "Approx. 675 g (including battery and card)",
            "dimensions": "134.0 x 100.5 x 67.5 mm",
            "launchPrice": 63000,
            "ibisRating": "5.0 stops (CIPA)",
            "videoColorDepth": "10-bit (via HDMI)",
            "logSupport": "N-Log (External)"
        },
        "z50": {
            "modelName": "Nikon Z 50",
            "processor": "EXPEED 6",
            "weightGrams": "Approx. 450 g (including battery and card)",
            "dimensions": "126.5 x 93.5 x 60.0 mm",
            "launchPrice": 28900,
            "ibisRating": "No (Lens OIS support)",
            "videoColorDepth": "8-bit",
            "logSupport": "No",
            "afTargets": "Human, Animal"
        }
    }

    for item in products:
        item_id = item.get('id', '')
        if item_id in nikon_legacy_db:
            specs = nikon_legacy_db[item_id]
            for key, val in specs.items():
                item[key] = val
                fixed_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"NIKON_LEGACY_CORRECTION_V32_COMPLETE: Successfully calibrated {fixed_count} fields for Z 50, Z 7, and Z 6.")

if __name__ == "__main__":
    nikon_legacy_correction_v32()
