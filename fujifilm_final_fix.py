import json
import os
import requests
from PIL import Image
import io

def process_and_save(url, save_path):
    try:
        response = requests.get(url, timeout=15)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] > 220 and item[1] > 220 and item[2] > 220:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])
        background.save(save_path, "JPEG", quality=95)
        print(f"Saved: {save_path}")
    except Exception as e:
        print(f"Failed to save {save_path}: {e}")

def fujifilm_final_fix():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/fujifilm"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 1. 修正 X100VI
    for p in products:
        if "x100v-i" in p.get("id", ""):
            p["id"] = "fujifilm-x100vi"
            p["image_url"] = "/images/products/fujifilm/fujifilm-x100vi.jpg"

    # 2. 注入 X-E5
    ids = [p["id"] for p in products]
    if "fujifilm-x-e5" not in ids:
        products.append({
            "brand": "Fujifilm",
            "modelName": "Fujifilm X-E5",
            "gearType": "CAMERA_BODY",
            "sensorFormat": "APS-C",
            "megapixels": "40.2MP",
            "releaseYear": 2025,
            "id": "fujifilm-x-e5",
            "image_url": "/images/products/fujifilm/fujifilm-x-e5.jpg",
            "launchPrice": 52900,
            "sensorType": "X-Trans CMOS 5 HR (BSI)",
            "processor": "X-Processor 5",
            "hasIBIS": True,
            "ibisRating": "7.0 stops",
            "videoResolution": "6.2K 30p / 4K 60p",
            "afTargets": "Human, Animal, Bird, Vehicle, Airplane, Train",
            "weightGrams": "Approx. 400g",
            "mounts": [{"mount": {"name": "Fujifilm X"}}]
        })

    # 3. 視覺糾偏 (Rule 17)
    visual_targets = {
        "fujifilm-x-e5.jpg": "https://www.fujifilm.com/jp/en/consumer/support/digitalcameras/x-e5/image_01.jpg",
        "fujifilm-x-m5.jpg": "https://eshop.fujifilm-x.com/media/catalog/product/x/m/xm5_body_front.jpg",
        "fujifilm-gfx-50s-ii.jpg": "https://fujifilm-x.com/wp-content/uploads/2021/08/gfx50s-ii_main-scaled.jpg",
        "fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr.jpg": "https://m.media-amazon.com/images/I/71pE4fC2SML._AC_SL1500_.jpg",
        "fujifilm-x100vi.jpg": "https://fujifilm-x.com/wp-content/uploads/2024/02/x100vi_silver_front.jpg"
    }
    
    for filename, url in visual_targets.items():
        save_path = os.path.join(img_dir, filename)
        process_and_save(url, save_path)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("Fujifilm Final Fix Complete.")

if __name__ == "__main__":
    fujifilm_final_fix()
