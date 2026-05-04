import json

def master_schema_alignment():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 標準欄位清單與預設值
    standard_fields = {
        "minAperture": "--",
        "motorType": "--",
        "opticalDesign": "--",
        "specialElements": "--",
        "coatings": "--",
        "closeFocus": "--",
        "maxMagnification": "--",
        "hasOIS": False,
        "hasApertureRing": False,
        "hasCustomButton": False,
        "hasWeatherSeal": False,
        "weightGrams": "--",
        "lengthMm": "--",
        "diameter": "--",
        "series": "--",
        "launchPrice": 0
    }

    updated_count = 0
    
    for item in products:
        if item.get('gearType') == 'LENS':
            updated_count += 1
            
            # 1. 補齊缺失欄位
            for field, default in standard_fields.items():
                if field not in item or item[field] is None:
                    item[field] = default
            
            # 2. 特殊修正：Canon RF 14mm L (或類似超廣角)
            if '14mm' in item['modelName'] and 'Canon' in item['brand']:
                item['filterSizeMm'] = 0 # 標記為燈泡鏡/後置
            
            # 3. 欄位更名與相容性 (Standardizing diameter)
            if 'widthMm' in item:
                item['diameter'] = item['widthMm']
            
            # 4. 深度規格補完 (範例：補齊熱門鏡頭以展示效果)
            if "24-70mm" in item['modelName'] and "GM" in item['series']:
                item['coatings'] = "Nano AR II, Fluorine Coating"
                item['opticalDesign'] = "15 groups, 20 elements"
                item['specialElements'] = "2 XA, 3 ED, 2 Aspherical"
                item['motorType'] = "XD Linear"
                item['hasApertureRing'] = True
                item['hasCustomButton'] = True

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"MASTER_SCHEMA_COMPLETE: Standardized {updated_count} lenses.")

if __name__ == "__main__":
    master_schema_alignment()
