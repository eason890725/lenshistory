import json
import os

def nikon_dedup_and_audit():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    initial_len = len(products)
    
    # 1. 去重 (基於 ID)
    seen_ids = set()
    deduped = []
    for p in products:
        pid = p.get("id")
        if pid not in seen_ids:
            deduped.append(p)
            seen_ids.add(pid)
    
    # 2. 針對 Z6III 的特殊檢查 (可能 ID 不同但型號相同)
    final_list = []
    names_seen = set()
    for p in deduped:
        name = p.get("modelName")
        if "Z 6III" in name or "Z6 III" in name:
            if name not in names_seen:
                final_list.append(p)
                names_seen.add(name)
        else:
            final_list.append(p)
            
    # 3. 確保 19 款鏡頭存在且 ID 規範化
    target_lenses = [
        "nikon-z-180-600mm-f-5-6-6-3-vr", "nikon-z-26mm-f-2-8", "nikon-z-dx-12-28mm-f-3-5-5-6-pz-vr",
        "nikon-z-105mm-f-2-8-vr-s-micro", "nikon-z-28mm-f-2-8", "nikon-z-40mm-f-2",
        "nikon-z-dx-18-140mm-f-3-5-6-3-vr", "nikon-z-28-75mm-f-2-8", "nikon-z-24-200mm-f-4-6-3-vr",
        "nikon-z-20mm-f-1-8-s", "nikon-z-24-50mm-f-4-6-3", "nikon-z-14-30mm-f-4-s",
        "nikon-z-85mm-f-1-8-s", "nikon-z-24mm-f-1-8-s", "nikon-z-dx-16-50mm-f-3-5-6-3-vr",
        "nikon-z-dx-50-250mm-f-4-5-6-3-vr", "nikon-z-50mm-f-1-8-s", "nikon-z-35mm-f-1-8-s",
        "nikon-z-24-70mm-f-4-s"
    ]
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"Dedup complete. Removed: {initial_len - len(final_list)}")

if __name__ == "__main__":
    nikon_dedup_and_audit()
