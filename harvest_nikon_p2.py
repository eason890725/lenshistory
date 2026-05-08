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

def harvest_and_blacken_nikon_p2():
    targets = [
        {"id": "z7", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_7/img/product_01_01.jpg"},
        {"id": "z6", "url": "https://imaging.nikon.com/imaging/lineup/mirrorless/z_6/img/product_01_01.jpg"},
        {"id": "z-14-24mm-f-2-8-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_14-24mmf28s/img/product_01.jpg"},
        {"id": "z-24-70mm-f-2-8-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_24-70mmf28s/img/product_01.jpg"},
        {"id": "z-70-200mm-f-2-8-vr-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_70_200mmf28_vr_s/img/product_01.jpg"},
        {"id": "z-135mm-f-1-8-s-plena", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_135mmf18s/img/product_01.jpg"},
        {"id": "z-50mm-f-1-2-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_50mmf12s/img/product_01.jpg"},
        {"id": "z-85mm-f-1-2-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_85mmf12s/img/product_01.jpg"},
        {"id": "z-24-120mm-f-4-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_24-120mmf4s/img/product_01.jpg"},
        {"id": "z-100-400mm-f-4-5-5-6-vr-s", "url": "https://imaging.nikon.com/imaging/lineup/lens/z-mount/z_100-400mmf45-56_vr_s/img/product_01.jpg"}
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
    
    print("PHASE 2 COMPLETE")

if __name__ == "__main__":
    harvest_and_blacken_nikon_p2()
