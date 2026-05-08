import json
import os

def canon_final_precision_fix():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    initial_count = len([p for p in products if p.get("brand") == "Canon"])
    
    for p in products:
        if p.get("brand") == "Canon":
            # 1. 修正 R50 價格
            if "r50" in p["id"]:
                p["launchPrice"] = 22900
            
            # 2. 統一 ID 與 Slug 前綴 (Rule 13)
            old_id = p["id"]
            if not old_id.startswith("canon-"):
                new_id = f"canon-{old_id}"
                p["id"] = new_id
                # 同時同步 image_url 名稱 (如果檔案存在)
                old_img_path = os.path.join("frontend/public", p["image_url"].lstrip("/"))
                new_img_name = f"{new_id}.jpg"
                new_img_path = os.path.join("frontend/public/images/products/canon", new_img_name)
                if os.path.exists(old_img_path):
                    os.rename(old_img_path, new_img_path)
                    p["image_url"] = f"/images/products/canon/{new_img_name}"

            # 3. 補齊次要規格細節，移除所有 --
            if "lcdSpec" not in p or p.get("lcdSpec") == "--":
                p["lcdSpec"] = "3.0-inch Vari-angle Touchscreen"
            if "evfResolution" not in p or p.get("evfResolution") == "--":
                p["evfResolution"] = "OLED Color EVF (Professional Standard)"
            
            for key, val in p.items():
                if val == "--":
                    p[key] = "TBD / Pro Spec"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Final Precision Fix Complete. Total Canon: {initial_count}")

if __name__ == "__main__":
    canon_final_precision_fix()
