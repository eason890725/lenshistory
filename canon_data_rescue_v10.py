import json
import re

def canon_data_rescue_v10():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0
    filled_fields_count = 0

    # Canon 官方技術與售價基準庫 (2026)
    canon_master_data = {
        "eos-r1": {
            "modelName": "Canon EOS R1",
            "launchPrice": 198000,
            "megapixels": "24.2MP",
            "sensorType": "Back-illuminated Stacked CMOS",
            "processor": "DIGIC Accelerator + DIGIC X",
            "ibisRating": "8.5 stops (CIPA)",
            "afRange": "EV -7.5 to 21",
            "afTargets": "People, Animals, Vehicles (including Train/Plane)",
            "evfResolution": "9.44M-dot OLED",
            "evfMagnification": "0.90x",
            "batterySpec": "LP-E19",
            "dimensions": "157.6 x 149.2 x 87.3 mm",
            "weightGrams": "Approx. 1115 g (including battery and card)"
        },
        "eos-r5-ii": {
            "modelName": "Canon EOS R5 Mark II",
            "launchPrice": 128000,
            "megapixels": "45.0MP",
            "sensorType": "Back-illuminated Stacked CMOS",
            "processor": "DIGIC Accelerator + DIGIC X",
            "ibisRating": "8.5 stops (CIPA center)",
            "afTargets": "People, Animals, Vehicles",
            "evfResolution": "5.76M-dot OLED",
            "batterySpec": "LP-E6P",
            "dimensions": "138.5 x 101.2 x 93.5 mm"
        },
        "rf-15-35mm-f2-8-l-is-usm": {
            "modelName": "Canon RF 15-35mm F2.8 L IS USM",
            "opticalDesign": "16 elements in 12 groups",
            "specialElements": "3 Aspherical, 2 UD",
            "coatings": "ASC (Air Sphere Coating), SWC, Fluorine",
            "motorType": "Nano USM",
            "ibisRating": "5.0 stops (OIS only) / 8.0 stops (Coordinated)",
            "closeFocus": "0.28m",
            "maxMagnification": "0.21x",
            "filterSizeMm": "82mm"
        }
    }

    for item in products:
        if item.get('brand') != 'Canon':
            continue
            
        item_id = item.get('id', '')
        old_name = item.get('modelName', '')

        # --- 1. 正名計畫 (Canon Standard) ---
        new_name = old_name.replace("canon", "Canon").replace("eos", "EOS").replace("mark", "Mark")
        # 修正連寫錯誤
        new_name = re.sub(r'^(Canon\s+)+', 'Canon ', new_name)
        new_name = re.sub(r'R(\d)M(\d)', r'R\1 Mark \2', new_name)
        item['modelName'] = new_name

        # --- 2. 深度補全 ---
        if item_id in canon_master_data:
            specs = canon_master_data[item_id]
            for key, val in specs.items():
                item[key] = val
                filled_fields_count += 1
        
        # --- 3. 建立專業別名 ---
        aliases = set(item.get('aliases', []))
        # 提取簡稱 (如 R1, R5II)
        short = new_name.replace("Canon EOS ", "").replace(" Mark ", "")
        aliases.add(short)
        aliases.add(short.replace(" ", ""))
        if "Mark" in new_name:
            # 處理 Mark II -> II 或 2
            match = re.search(r'Mark\s+(I+)', new_name)
            if match:
                rom = match.group(1)
                num = str(len(rom))
                base = new_name.split(" Mark")[0].replace("Canon EOS ", "")
                aliases.add(f"{base}{rom}")
                aliases.add(f"{base}{num}")
        
        item['aliases'] = sorted(list(aliases))
        fixed_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"CANON_RESCUE_COMPLETE: Processed {fixed_count} Canon products.")
    print(f"FIELDS_FILLED_COUNT: {filled_fields_count}")

if __name__ == "__main__":
    canon_data_rescue_v10()
