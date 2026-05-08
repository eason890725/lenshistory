import json
import os

def sony_data_purification():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    initial_count = len(products)
    sony_products = [p for p in products if p.get("brand") == "Sony"]
    print(f"Initial Sony Count: {len(sony_products)}")

    # 1. 處理重複 A7C II (保留第一個)
    new_products = []
    seen_ids = set()
    for p in products:
        pid = p.get("id")
        if pid == "sony-a7c-ii" or p.get("modelName") == "Sony Alpha 7C II":
            if "a7c2" in seen_ids:
                continue
            seen_ids.add("a7c2")
        
        # 2. 修復 "Sony Sony" 命名
        if p.get("brand") == "Sony":
            name = p.get("modelName", "")
            if name.lower().startswith("sony sony"):
                p["modelName"] = name.replace("Sony Sony", "Sony", 1).replace("sony sony", "Sony", 1)
            
            # 3. ID 規範化
            old_id = p["id"]
            clean_id = old_id.replace("sony-", "").lower().replace("/", "-").replace(" ", "-").replace("--", "-")
            p["id"] = f"sony-{clean_id}"
            p["image_url"] = f"/images/products/sony/{p['id']}.jpg"
            
        new_products.append(p)

    final_count = len(new_products)
    print(f"Final Total Count: {final_count} (Reduced: {initial_count - final_count})")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(new_products, f, indent=2, ensure_ascii=False)
    
    return True

if __name__ == "__main__":
    sony_data_purification()
