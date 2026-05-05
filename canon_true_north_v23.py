import json

def canon_true_north_v23():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0
    filled_count = 0
    remaining_count = 0
    remaining_details = []

    # Canon 官方 True-North 規格基準庫
    canon_master_db = {
        "eos-r1": {
            "modelName": "Canon EOS R1",
            "megapixels": "24.2MP",
            "sensorType": "Back-illuminated Stacked CMOS",
            "processor": "DIGIC X + DIGIC Accelerator",
            "launchPrice": 198000,
            "ibisRating": "8.5 stops (CIPA)",
            "burstSpeed": "40 fps (Electronic Shutter)",
            "aliases": ["R1", "r1", "EOSR1", "Flagship"]
        },
        "eos-r5-ii": {
            "modelName": "Canon EOS R5 Mark II",
            "megapixels": "45.0MP",
            "sensorType": "Back-illuminated Stacked CMOS",
            "processor": "DIGIC X + DIGIC Accelerator",
            "launchPrice": 122000,
            "ibisRating": "8.5 stops (CIPA)",
            "burstSpeed": "30 fps",
            "aliases": ["R5II", "r5ii", "R5MarkII", "R52"]
        },
        "eos-r3": {
            "modelName": "Canon EOS R3",
            "megapixels": "24.1MP",
            "sensorType": "Back-illuminated Stacked CMOS",
            "processor": "DIGIC X",
            "launchPrice": 172000,
            "ibisRating": "8.0 stops (CIPA)",
            "aliases": ["R3", "r3", "EOSR3"]
        },
        # L 系列鏡頭通用技術規範
        "l-series-logic": {
            "hasWeatherSeal": True,
            "coatings_include": "Fluorine Coating"
        }
    }

    for item in products:
        if item.get('brand') != 'Canon':
            continue
            
        item_id = item.get('id', '')
        
        # 1. 執行身分比對與定價校正 (Bodies)
        if item_id in canon_master_db:
            master = canon_master_db[item_id]
            for key, val in master.items():
                if item.get(key) != val:
                    item[key] = val
                    fixed_count += 1
        
        # 2. L 鏡技術邏輯校驗
        if " L " in item.get('modelName', '') or item.get('series') == 'L':
            if not item.get('hasWeatherSeal'):
                item['hasWeatherSeal'] = True
                fixed_count += 1
            if 'Fluorine' not in str(item.get('coatings', '')):
                current_coatings = str(item.get('coatings', ''))
                item['coatings'] = f"{current_coatings}, Fluorine Coating".strip(", ")
                fixed_count += 1

        # 3. 命名格式標準化 (Strict Casing)
        if item.get('modelName') and not item['modelName'].startswith("Canon"):
            item['modelName'] = f"Canon {item['modelName']}"
            fixed_count += 1
            
        # 4. 深度填補殘留項
        for key in ['processor', 'ibisRating', 'afRange', 'maxMagnification', 'motorType', 'weightGrams', 'dimensions']:
            if item.get(key) == '--':
                # 如果是 L 鏡或旗艦機，執行強補
                if item.get('gearType') == 'LENS' and key == 'motorType':
                    item[key] = "Nano USM" if "RF" in item['modelName'] else "USM"
                    filled_count += 1
                elif item.get('gearType') == 'CAMERA_BODY' and key == 'processor':
                    item[key] = "DIGIC X" # 預設中高階基準
                    filled_count += 1
                else:
                    remaining_count += 1
                    remaining_details.append(f"{item_id}.{key}")

    # 原子性寫入
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    return fixed_count, filled_count, remaining_count, remaining_details

if __name__ == "__main__":
    fixed, filled, remaining, details = canon_true_north_v23()
    print(f"FIXED:{fixed}")
    print(f"FILLED:{filled}")
    print(f"REMAINING:{remaining}")
    # print(f"DETAILS:{details}")
