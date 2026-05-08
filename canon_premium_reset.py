import requests
import json
import os
from PIL import Image, ImageDraw

def transform_to_black_bg(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        # 從四個角進行洪水填充，容差設為 40 以適應 Adorama 的純白背景
        seed_points = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        for pt in seed_points:
            ImageDraw.floodfill(img, pt, (0, 0, 0, 0), thresh=40)
        
        datas = img.getdata()
        new_data = []
        for item in datas:
            # 識別背景或極接近白的像素
            if item[3] == 0 or (item[0] > 245 and item[1] > 245 and item[2] > 245):
                new_data.append((0, 0, 0, 255))
            else:
                new_data.append(item)
        img.putdata(new_data)
        final_img = img.convert("RGB")
        # 覆蓋原檔，儲存為 JPEG 品質 90
        final_img.save(output_path, "JPEG", quality=90)
        return True
    except Exception as e:
        print(f"Error blackening {input_path}: {e}")
        return False

def canon_premium_reset():
    targets = [
        {"id": "eos-r100", "url": "https://www.adorama.com/images/Large/car100.jpg"},
        {"id": "eos-r6", "url": "https://www.adorama.com/images/Large/car6.jpg"},
        {"id": "eos-r3", "url": "https://www.adorama.com/images/Large/car3.jpg"},
        {"id": "rf-24-70mm-f2-8l-is-usm", "url": "https://www.adorama.com/images/Large/ca2470rf.jpg"},
        {"id": "rf-15-35mm-f2-8l-is-usm", "url": "https://www.adorama.com/images/Large/ca1535rf.jpg"},
        {"id": "rf-70-200mm-f2-8l-is-usm", "url": "https://www.adorama.com/images/Large/ca70200rf.jpg"},
        {"id": "rf-50mm-f1-2l-usm", "url": "https://www.adorama.com/images/Large/car5012.jpg"}
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/canon"
    os.makedirs(target_dir, exist_ok=True)
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    for t in targets:
        id = t["id"]
        url = t["url"]
        temp_file = os.path.join(target_dir, f"{id}_premium_temp.jpg")
        final_file = os.path.join(target_dir, f"{id}.jpg")
        
        try:
            print(f"Downloading Premium {id}...")
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            with open(temp_file, "wb") as f_img:
                f_img.write(resp.content)
            
            print(f"Applying Professional Blackout to {id}...")
            if transform_to_black_bg(temp_file, final_file):
                # 更新 JSON 確保路徑指向 .jpg (有些之前可能是 .png)
                for p in products:
                    if p.get("id") == id:
                        p["image_url"] = f"/images/products/canon/{id}.jpg"
                        break
                os.remove(temp_file)
            else:
                print(f"Failed to blacken {id}")
        except Exception as e:
            print(f"Failed to reset {id}: {e}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("CANON PREMIUM RESET COMPLETE")

if __name__ == "__main__":
    canon_premium_reset()
