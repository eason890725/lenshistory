import json
import re

def safe_slug(name):
    s = name.lower()
    s = re.sub(r'[\s\/.]+', '-', s)
    s = s.strip('-')
    return s

def add_sigma_and_sync():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 1. 準備 Sigma 35mm Art II 數據
    sigma_35 = {
        "brand": "Sigma",
        "modelName": "35mm F1.4 DG DN Art II",
        "gearType": "LENS",
        "releaseYear": 2026,
        "launchPrice": 28900,
        "focalLengthMinMm": 35,
        "focalLengthMaxMm": 35,
        "apertureMax": "1.4",
        "filterSizeMm": 67,
        "weightGrams": 640,
        "opticalDesign": "11 groups, 15 elements",
        "specialElements": "2 FLD, 1 ELD, 2 SLD, 2 Aspherical",
        "coatings": "Super Multi-Layer Coating",
        "motorType": "HLA (High-response Linear Actuator)",
        "hasWeatherSeal": True,
        "hasApertureRing": True
    }

    # 2. 檢查是否已存在，若無則加入
    existing_names = {p['modelName'] for p in products}
    if sigma_35['modelName'] not in existing_names:
        products.append(sigma_35)

    # 3. 全量安全化 ID 與 Slug
    for item in products:
        name = item['modelName']
        new_id = safe_slug(name)
        item['id'] = new_id
        item['slug'] = new_id
        
        # 4. 確保 lens 都有基本欄位
        if item.get('gearType') == 'LENS':
            if 'brand' not in item: item['brand'] = "Unknown"
            if 'opticalDesign' not in item: item['opticalDesign'] = "10 groups, 14 elements (Est.)"

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SYNC_COMPLETE: Total products: {len(products)}")

if __name__ == "__main__":
    add_sigma_and_sync()
