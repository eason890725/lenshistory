import json
import os

def fujifilm_id_fix_and_new_models():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/fujifilm"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 1. 修正 X100VI ID 與圖片
    for p in products:
        if p.get("id") == "fujifilm-x100v-i":
            p["id"] = "fujifilm-x100vi"
            p["image_url"] = "/images/products/fujifilm/fujifilm-x100vi.jpg"
            
            # 同步重命名物理圖檔
            old_img = os.path.join(img_dir, "fujifilm-x100v-i.jpg")
            new_img = os.path.join(img_dir, "fujifilm-x100vi.jpg")
            if os.path.exists(old_img):
                os.rename(old_img, new_img)
            print("Fixed X100VI ID and Image path.")

    # 2. 檢查是否缺 X-M5 (最新機型)
    ids = [p["id"] for p in products]
    if "fujifilm-x-m5" not in ids:
        products.append({
            "brand": "Fujifilm",
            "modelName": "Fujifilm X-M5",
            "gearType": "CAMERA_BODY",
            "sensorFormat": "APS-C",
            "megapixels": "26.1MP",
            "releaseYear": 2024,
            "id": "fujifilm-x-m5",
            "image_url": "/images/products/fujifilm/fujifilm-x-m5.jpg",
            "launchPrice": 25900,
            "sensorType": "X-Trans CMOS 4",
            "hasIBIS": False,
            "videoResolution": "6.2K 30p / 4K 60p",
            "afTargets": "Human, Animal, Bird, Vehicle"
        })
        print("Added missing X-M5.")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fujifilm_id_fix_and_new_models()
