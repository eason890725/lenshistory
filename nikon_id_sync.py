import json
import os

def nikon_id_standardization():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/nikon"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    initial_count = len([p for p in products if p.get("brand") == "Nikon"])
    print(f"Initial Nikon Count: {initial_count}")
    
    for p in products:
        if p.get("brand") == "Nikon":
            old_id = p["id"]
            # 生成新 ID: nikon- + 移除舊 id 中已有的 nikon- 或 z- 前綴
            suffix = old_id.replace("nikon-", "").replace("z-", "z-") # 保留 z- 作為型號一部分
            new_id = f"nikon-{suffix}".lower().replace("/", "-").replace(" ", "-").replace("--", "-")
            
            p["id"] = new_id
            
            if "image_url" in p and p["image_url"]:
                old_img_path = os.path.join("frontend/public", p["image_url"].lstrip("/"))
                new_img_name = f"{new_id}.jpg"
                new_img_url = f"/images/products/nikon/{new_img_name}"
                new_img_path = os.path.join(img_dir, new_img_name)
                
                if os.path.exists(old_img_path) and old_img_path != new_img_path:
                    try:
                        os.rename(old_img_path, new_img_path)
                        p["image_url"] = new_img_url
                    except Exception as e:
                        print(f"Error renaming {old_id}: {e}")
                else:
                    p["image_url"] = new_img_url

    final_count = len([p for p in products if p.get("brand") == "Nikon"])
    if final_count < initial_count:
        print("ERROR: DATA LOSS")
        return False
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SUCCESS: Nikon ID Standardization complete. Total: {final_count}")
    return True

if __name__ == "__main__":
    nikon_id_standardization()
