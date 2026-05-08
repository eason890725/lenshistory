import json
import os

def fujifilm_id_standardization():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/fujifilm"
    
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    initial_count = len([p for p in products if p.get("brand") == "Fujifilm"])
    print(f"Initial Fujifilm Count: {initial_count}")
    
    for p in products:
        if p.get("brand") == "Fujifilm":
            old_id = p["id"]
            # 生成新 ID: fujifilm- + 型號
            clean_id = old_id.replace("fujifilm-", "").lower().replace("/", "-").replace(" ", "-").replace("--", "-")
            new_id = f"fujifilm-{clean_id}"
            
            p["id"] = new_id
            
            # 同步圖片路徑 (預設為 ID.jpg)
            p["image_url"] = f"/images/products/fujifilm/{new_id}.jpg"

    # 數量防呆
    final_count = len([p for p in products if p.get("brand") == "Fujifilm"])
    if final_count < initial_count:
        print("ERROR: DATA LOSS")
        return False
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SUCCESS: Fujifilm ID Standardization complete. Total: {final_count}")
    return True

if __name__ == "__main__":
    fujifilm_id_standardization()
