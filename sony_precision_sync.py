import json
import re

def sony_precision_sync():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    sync_count = 0

    # 專業數據定義 (以 A7C2 為標竿)
    deep_data = {
        "Sony Alpha 7C II": {
            "short": "A7C2",
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
            "weightGrams": "Approx. 514 g"
        },
        "Sony Alpha 7R V": {
            "short": "A7R5",
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
            "weightGrams": "Approx. 723 g"
        }
    }

    for item in products:
        if item.get('gearType') == 'CAMERA_BODY':
            brand = item.get('brand', '')
            aliases = item.get('aliases', [])
            current_model = item.get('modelName', '')
            
            # --- 1. 名稱翻轉與簡稱優化 ---
            # 獲取官方全名 (從別名中提取最長者)
            official_name = current_model
            if aliases:
                official_name = max(aliases, key=len)
            
            # 如果目前顯示的是全名，則尋找對應簡稱
            shorthand = current_model
            for full, data in deep_data.items():
                if full == official_name:
                    shorthand = data['short']
                    break
            
            # 翻轉邏輯：modelName = 簡稱, aliases 包含全名
            item['modelName'] = shorthand
            if official_name not in item.get('aliases', []):
                item.setdefault('aliases', []).append(official_name)
            
            # --- 2. 精確數據回填 ---
            if official_name in deep_data:
                data = deep_data[official_name]
                for key, val in data.items():
                    if key != 'short':
                        item[key] = val
                sync_count += 1
            
            # --- 3. 格式校準 (通用) ---
            if 'weightGrams' in item and isinstance(item['weightGrams'], (int, float)):
                item['weightGrams'] = f"Approx. {item['weightGrams']} g"
            if 'widthMm' in item and 'heightMm' in item and 'depthMm' in item:
                item['dimensions'] = f"{item['widthMm']} x {item['heightMm']} x {item['depthMm']} mm"

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SONY_PRECISION_SYNC_COMPLETE: Synced {sync_count} high-precision models.")

if __name__ == "__main__":
    sony_precision_sync()
