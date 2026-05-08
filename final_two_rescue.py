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

def final_two_reset():
    targets = [
        {
            "id": "rf-35mm-f-1-4-l-vcm", 
            "url": "https://www.adorama.com/images/Large/car3514.jpg",
            "dir": "frontend/public/images/products/canon"
        },
        {
            "id": "z-70-200mm-f-2-8-vr-s", 
            "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_70-200mmf28_vr_s/img/product_01_01.jpg",
            "dir": "frontend/public/images/products/nikon"
        }
    ]
    
    json_path = "frontend/src/data/products.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    for t in targets:
        id = t["id"]
        url = t["url"]
        target_dir = t["dir"]
        os.makedirs(target_dir, exist_ok=True)
        
        temp_file = os.path.join(target_dir, f"{id}_rescue_temp.jpg")
        final_file = os.path.join(target_dir, f"{id}.jpg")
        
        try:
            print(f"Downloading Premium {id}...")
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            with open(temp_file, "wb") as f_img:
                f_img.write(resp.content)
            
            print(f"Applying Blackout to {id}...")
            if transform_to_black_bg(temp_file, final_file):
                for p in products:
                    if p.get("id") == id:
                        # 修正可能的路徑偏差
                        brand_folder = "canon" if "canon" in target_dir else "nikon"
                        p["image_url"] = f"/images/products/{brand_folder}/{id}.jpg"
                        break
                os.remove(temp_file)
            else:
                print(f"Failed to blacken {id}")
        except Exception as e:
            print(f"Failed to reset {id}: {e}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("FINAL TWO RESCUE COMPLETE")

if __name__ == "__main__":
    final_two_reset()
