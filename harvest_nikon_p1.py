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

def harvest_and_blacken_nikon_p1():
    targets = [
        {"id": "nikon-z-9", "url": "https://www.photoreview.com.au/wp-content/uploads/2022/01/Z9_angled_front-24-70mm-lens.jpg"},
        {"id": "nikon-z-8", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_8/img/product_01_01.jpg"},
        {"id": "nikon-z-7-ii", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_7_2/img/product_01_01.jpg"},
        {"id": "nikon-z-6-iii", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z6_3/img/product_01_01.jpg"},
        {"id": "nikon-z-6-ii", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_6_2/img/product_01_01.jpg"},
        {"id": "nikon-z-5", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_5/img/product_01_01.jpg"},
        {"id": "nikon-z-f", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_f/img/product_01_01.jpg"},
        {"id": "nikon-z-fc", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_fc/img/product_01_01.jpg"},
        {"id": "nikon-z-50", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_50/img/product_01_01.jpg"},
        {"id": "nikon-z-30", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_30/img/product_01_01.jpg"}
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/nikon"
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
            print(f"Downloading {id}...")
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            with open(temp_file, "wb") as f_img:
                f_img.write(resp.content)
            
            print(f"Blackening {id}...")
            if transform_to_black_bg(temp_file, final_file):
                # 更新 JSON
                for p in products:
                    if p.get("id") == id:
                        p["image_url"] = f"/images/products/nikon/{id}.jpg"
                        break
                os.remove(temp_file)
            else:
                print(f"Failed to blacken {id}")
        except Exception as e:
            print(f"Failed to harvest {id}: {e}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("PHASE 1 COMPLETE")

if __name__ == "__main__":
    harvest_and_blacken_nikon_p1()
