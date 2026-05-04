import json

def mass_update():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 規格查找表
    spec_map = {
        "Z9": {"videoResolution": "8K 60p / 4K 120p", "afPoints": "493", "evfResolution": "3.69M-dot OLED", "burstSpeed": "20 fps (RAW) / 120 fps (JPEG)", "logSupport": "N-Log / ProRes RAW", "sensorType": "Stacked CMOS", "weightGrams": 1340},
        "Z8": {"videoResolution": "8K 60p / 4K 120p", "afPoints": "493", "evfResolution": "3.69M-dot OLED", "burstSpeed": "20 fps (RAW)", "logSupport": "N-Log / ProRes RAW", "sensorType": "Stacked CMOS", "weightGrams": 910},
        "Z6 III": {"videoResolution": "6K 60p / 4K 120p", "afPoints": "299", "evfResolution": "5.76M-dot OLED", "burstSpeed": "20 fps", "logSupport": "N-Log", "sensorType": "Partially Stacked CMOS", "weightGrams": 670},
        "EOS R5 II": {"videoResolution": "8K 60p / 4K 120p", "afPoints": "5850", "evfResolution": "5.76M-dot OLED", "burstSpeed": "30 fps", "logSupport": "C-Log 2/3", "sensorType": "Stacked CMOS", "weightGrams": 746},
        "EOS R1": {"videoResolution": "6K 60p / 4K 120p", "afPoints": "1053", "evfResolution": "9.44M-dot OLED", "burstSpeed": "40 fps", "logSupport": "C-Log 2/3", "sensorType": "Stacked CMOS", "weightGrams": 1115},
        "X-T5": {"videoResolution": "6.2K 30p / 4K 60p", "afPoints": "425", "evfResolution": "3.69M-dot OLED", "burstSpeed": "15 fps (Mech)", "logSupport": "F-Log2", "sensorType": "X-Trans CMOS 5 HR", "weightGrams": 557},
        "X-H2S": {"videoResolution": "6.2K 30p / 4K 120p", "afPoints": "425", "evfResolution": "5.76M-dot OLED", "burstSpeed": "40 fps", "logSupport": "F-Log2", "sensorType": "Stacked X-Trans CMOS 5 HS", "weightGrams": 660},
        "GFX 100 II": {"videoResolution": "8K 30p / 4K 60p", "afPoints": "425", "evfResolution": "9.44M-dot OLED", "burstSpeed": "8 fps", "logSupport": "F-Log2", "sensorType": "CMOS II HS", "weightGrams": 1030},
        "EOS R3": {"videoResolution": "6K 60p / 4K 120p", "afPoints": "1053", "evfResolution": "5.76M-dot OLED", "burstSpeed": "30 fps", "logSupport": "C-Log 3", "sensorType": "Stacked CMOS", "weightGrams": 1015},
        "Zf": {"videoResolution": "4K 60p", "afPoints": "299", "evfResolution": "3.69M-dot OLED", "burstSpeed": "14 fps", "logSupport": "N-Log", "sensorType": "CMOS", "weightGrams": 710},
    }

    updated_count = 0
    for item in products:
        name = item['modelName']
        # 模糊匹配
        match_key = next((k for k in spec_map.keys() if k in name), None)
        if match_key and item['gearType'] == 'CAMERA_BODY':
            specs = spec_map[match_key]
            for key, val in specs.items():
                item[key] = val
            updated_count += 1
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"MASS_UPDATE_COMPLETE: Updated {updated_count} major camera bodies with deep specs.")

if __name__ == "__main__":
    mass_update()
