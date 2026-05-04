import json

def sony_precision_sync_v2():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    sync_count = 0

    # 專業數據定義 (以 ID 為準，確保 100% 命中)
    deep_data = {
        "a7c-ii": {
            "modelName": "A7C2",
            "sensorType": "Exmor R BSI CMOS",
            "megapixels": "33MP",
            "processor": "BIONZ XR",
            "ibisRating": "7.0 stops (CIPA)",
            "isoRange": "100-51200 (Ext: 50-204800)",
            "afPoints": "759 Phase-detection",
            "afTargets": "Human, Animal, Bird, Insect, Car, Train, Airplane",
            "afRange": "-4 to +20 EV",
            "videoResolution": "4K 60p (Super 35) / 4K 30p (Full Frame)",
            "videoColorDepth": "10-bit 4:2:2 (H.265/XAVC HS)",
            "evfResolution": "2.36M-dot OLED",
            "evfMagnification": "0.70x",
            "lcdSpec": "3.0-inch 1.03M-dot Vari-angle LCD",
            "cardSlots": "1x SD (UHS-I/II)",
            "batterySpec": "NP-FZ100 (Approx. 530 shots)",
            "ports": "USB-C (USB 3.2 Gen 2), HDMI (Type-D), 3.5mm Mic/Headphone",
            "dimensions": "124.0 x 71.1 x 63.4 mm",
            "weightGrams": "Approx. 514 g",
            "official_name": "Sony Alpha 7C II"
        },
        "a7r-v": {
            "modelName": "A7R5",
            "sensorType": "Exmor R BSI CMOS",
            "megapixels": "61MP",
            "processor": "BIONZ XR (with AI Processing Unit)",
            "ibisRating": "8.0 stops (CIPA)",
            "isoRange": "100-32000 (Ext: 50-102400)",
            "afPoints": "693 Phase-detection",
            "afTargets": "Human, Animal, Bird, Insect, Car, Train, Airplane",
            "afRange": "-4 to +20 EV",
            "videoResolution": "8K 24p / 4K 60p",
            "videoColorDepth": "10-bit 4:2:2",
            "evfResolution": "9.44M-dot OLED",
            "evfMagnification": "0.90x",
            "lcdSpec": "3.2-inch 2.1M-dot 4-axis Multi-angle LCD",
            "cardSlots": "2x CFexpress Type A / SD (UHS-II)",
            "batterySpec": "NP-FZ100 (Approx. 530 shots)",
            "ports": "USB-C (USB 3.2 Gen 2), Full HDMI (Type-A), PC Sync, Ethernet",
            "dimensions": "131.3 x 96.9 x 82.4 mm",
            "weightGrams": "Approx. 723 g",
            "official_name": "Sony Alpha 7R V"
        },
        "a1-ii": {
            "modelName": "A1 II",
            "sensorType": "Exmor R BSI Stacked CMOS",
            "megapixels": "50.1MP",
            "processor": "BIONZ XR (with AI Processing Unit)",
            "ibisRating": "8.5 stops (CIPA)",
            "isoRange": "100-32000 (Ext: 50-102400)",
            "afPoints": "759 Phase-detection",
            "afTargets": "Human, Animal, Bird, Insect, Car, Train, Airplane",
            "afRange": "-4 to +20 EV",
            "videoResolution": "8K 30p / 4K 120p",
            "videoColorDepth": "10-bit 4:2:2",
            "evfResolution": "9.44M-dot OLED",
            "evfMagnification": "0.90x",
            "lcdSpec": "3.2-inch 2.1M-dot 4-axis Multi-angle LCD",
            "cardSlots": "2x CFexpress Type A / SD (UHS-II)",
            "batterySpec": "NP-FZ100",
            "ports": "USB-C (10 Gbps), Full HDMI, 2.5G Ethernet",
            "dimensions": "136.1 x 96.9 x 82.9 mm",
            "weightGrams": "Approx. 746 g",
            "official_name": "Sony Alpha 1 II"
        }
    }

    for item in products:
        item_id = item.get('id', '')
        
        # --- 1. 命中精確數據 ---
        if item_id in deep_data:
            data = deep_data[item_id]
            official = data['official_name']
            
            # 更新 modelName 為簡稱
            item['modelName'] = data['modelName']
            
            # 確保官方全名在別名中
            if 'aliases' not in item: item['aliases'] = []
            if official not in item['aliases']:
                item['aliases'].append(official)
            
            # 回填所有技術參數
            for key, val in data.items():
                if key not in ['modelName', 'official_name']:
                    item[key] = val
            sync_count += 1
            
        # --- 2. 通用簡稱翻轉邏輯 (其他 Sony 機型) ---
        elif item.get('brand') == 'Sony' and item.get('gearType') == 'CAMERA_BODY':
            current = item.get('modelName', '')
            aliases = item.get('aliases', [])
            
            # 如果目前是長名，嘗試翻轉
            if "Sony Alpha" in current:
                # 簡單生成簡稱 (Alpha 7 IV -> A74)
                short = current.replace("Sony Alpha ", "A").replace(" ", "")
                item['modelName'] = short
                if current not in item['aliases']:
                    item['aliases'].append(current)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SONY_PRECISION_V2_COMPLETE: Synced {sync_count} flagship models.")

if __name__ == "__main__":
    sony_precision_sync_v2()
