import json
import re

def upgrade_schema_and_add_2026():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 2. 2026 新機身資料
    new_2026_gear = [
        {
            "brand": "Sony",
            "modelName": "A1 II",
            "gearType": "CAMERA_BODY",
            "sensorType": "Stacked CMOS",
            "megapixels": 50.1,
            "videoResolution": "8K 30p / 4K 120p 10-bit",
            "afPoints": "759 Phase-detection",
            "evfResolution": "9.44M-dot OLED",
            "burstSpeed": "30 fps",
            "releaseYear": 2024,
            "launchPrice": 210000,
            "hasIBIS": True,
            "sensorFormat": "Full Frame",
            "slug": "a1-ii"
        },
        {
            "brand": "Sony",
            "modelName": "A7 V",
            "gearType": "CAMERA_BODY",
            "sensorType": "Partially Stacked CMOS",
            "megapixels": 33.0,
            "videoResolution": "4K 60p (Oversampled 7K) / 4K 120p",
            "afPoints": "759 Phase-detection",
            "evfResolution": "3.68M-dot OLED",
            "burstSpeed": "10+ fps",
            "releaseYear": 2025,
            "launchPrice": 92980,
            "hasIBIS": True,
            "sensorFormat": "Full Frame",
            "slug": "a7-v"
        }
    ]

    # 合併並確保欄位齊全
    existing_names = {p['modelName'] for p in products}
    for item in new_2026_gear:
        if item['modelName'] not in existing_names:
            products.append(item)

    for item in products:
        # 機身專屬欄位初始化
        if item['gearType'] == 'CAMERA_BODY':
            item.setdefault('videoResolution', item.get('videoResolution', '--'))
            item.setdefault('afPoints', '--')
            item.setdefault('evfResolution', '--')
            item.setdefault('burstSpeed', '--')
            item.setdefault('logSupport', 'S-Log3 / S-Cinetone')
            # 清除可能誤植的鏡頭欄位
            item.pop('focalLengthMinMm', None)
            item.pop('focalLengthMaxMm', None)
            item.pop('apertureMax', None)
        # 鏡頭專屬欄位初始化
        elif item['gearType'] == 'LENS':
            item.setdefault('motorType', 'XD Linear' if 'GM' in item['modelName'] else '--')
            item.setdefault('opticalDesign', '--')
            item.setdefault('minAperture', '--')
            item.setdefault('specialElements', '--')

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"UPGRADE_COMPLETE: Added 2026 gear and expanded schema fields.")

if __name__ == "__main__":
    upgrade_schema_and_add_2026()
