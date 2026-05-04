import json
import re

def normalize_name(name):
    # 統一將 Alpha 替換為 A
    name = name.replace('Alpha ', 'A').replace('alpha ', 'A')
    # 移除多餘空格，例如 A7C II -> A7C II, A7CII -> A7C II
    name = re.sub(r'([A-Z]+\d+[A-Z]*)([IV]+)', r'\1 \2', name) # A7CII -> A7C II
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def merge_products():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    merged = {}
    
    for item in products:
        raw_name = item['modelName']
        norm_name = normalize_name(raw_name)
        
        if norm_name not in merged:
            item['modelName'] = norm_name
            merged[norm_name] = item
        else:
            # 智慧合併：保留較完整的資料
            existing = merged[norm_name]
            for key, value in item.items():
                if key not in existing or existing[key] in [None, "--", 0, ""]:
                    existing[key] = value
            # 確保 gearType 一致
            if existing['gearType'] == 'LENS' and 'apertureMax' in item:
                existing['gearType'] = 'LENS'

    final_list = list(merged.values())
    
    # 統計機身數量
    bodies = [p for p in final_list if p['gearType'] == 'CAMERA_BODY']
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"MERGE_COMPLETE: Original={len(products)}, Final={len(final_list)}")
    print(f"TOTAL_BODIES: {len(bodies)}")
    print(f"A7C_II_CHECK: {'A7C II' in merged}")

if __name__ == "__main__":
    merge_products()
