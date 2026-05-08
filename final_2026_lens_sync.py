import requests
import json
import os
from PIL import Image, ImageDraw

def transform_to_black_bg(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        seed_points = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        for pt in seed_points:
            ImageDraw.floodfill(img, pt, (0, 0, 0, 0), thresh=40)
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[3] == 0 or (item[0] > 245 and item[1] > 245 and item[2] > 245):
                new_data.append((0, 0, 0, 255))
            else:
                new_data.append(item)
        img.putdata(new_data)
        final_img = img.convert("RGB")
        final_img.save(output_path, "JPEG", quality=90)
        return True
    except Exception as e:
        print(f"Error blackening {input_path}: {e}")
        return False

def final_2026_lens_sync():
    targets = [
        {"id": "rf-28-70mm-f2-8-is-stm", "url": "https://www.adorama.com/images/Large/car287028.jpg"},
        {"id": "rf-24mm-f1-4l-vcm", "url": "https://www.adorama.com/images/Large/car2414.jpg"},
        {"id": "rf-50mm-f1-4l-vcm", "url": "https://www.adorama.com/images/Large/car5014.jpg"}
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/canon"
    os.makedirs(target_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    for t in targets:
        id = t["id"]
        url = t["url"]
        temp_file = os.path.join(target_dir, f"{id}_temp.jpg")
        final_file = os.path.join(target_dir, f"{id}.jpg")
        
        try:
            print(f"Processing {id}...")
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            with open(temp_file, "wb") as f_img:
                f_img.write(resp.content)
            
            if transform_to_black_bg(temp_file, final_file):
                for p in products:
                    if p.get("id") == id:
                        p["image_url"] = f"/images/products/canon/{id}.jpg"
                        break
                os.remove(temp_file)
        except Exception as e:
            print(f"Error syncing {id}: {e}")
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print("SUCCESS: 2026 Lens Assets Synced & Blackened.")

if __name__ == "__main__":
    final_2026_lens_sync()
