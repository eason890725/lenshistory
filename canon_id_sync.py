import json
import os

def canon_id_standardization():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/canon"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    initial_canon_count = len([p for p in products if p.get("brand") == "Canon"])
    print(f"Initial Canon Count: {initial_canon_count}")
    
    for p in products:
        if p.get("brand") == "Canon":
            old_id = p["id"]
            # 生成新 ID: canon- + 移除舊 id 中已有的 canon- 前綴
            suffix = old_id.replace("canon-", "")
            new_id = f"canon-{suffix}".lower().replace("/", "-").replace(" ", "-")
            
            # 更新 ID
            p["id"] = new_id
            
            # 處理圖片路徑與重新命名檔案
            if "image_url" in p and p["image_url"]:
                old_img_path = os.path.join("frontend/public", p["image_url"].lstrip("/"))
                new_img_name = f"{new_id}.jpg"
                new_img_url = f"/images/products/canon/{new_img_name}"
                new_img_path = os.path.join(img_dir, new_img_name)
                
                if os.path.exists(old_img_path) and old_img_path != new_img_path:
                    try:
                        os.rename(old_img_path, new_img_path)
                        p["image_url"] = new_img_url
                    except Exception as e:
                        print(f"Error renaming {old_img_path} to {new_img_path}: {e}")
                else:
                    p["image_url"] = new_img_url # 即使檔案不存在也先更新 URL 以便後續抓取

    # 數量驗證 (Rule 3)
    final_canon_count = len([p for p in products if p.get("brand") == "Canon"])
    if final_canon_count < initial_canon_count:
        print("ERROR: Quantity reduction detected! Restoring...")
        return False
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SUCCESS: ID Standardization complete. Total Canon: {final_canon_count}")
    return True

if __name__ == "__main__":
    canon_id_standardization()
