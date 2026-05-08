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

def harvest_nikon():
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/nikon"
    os.makedirs(target_dir, exist_ok=True)
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    nikon_items = [p for p in products if p.get("brand") == "Nikon" and (not p.get("image_url") or p.get("image_url") == "--")]
    
    print(f"Targeting {len(nikon_items)} Nikon items...")
    
    # 注意：這裡我將列出型號，稍後由 Browser Subagent 尋找網址
    for item in nikon_items:
        print(f"SEARCH_TARGET: Nikon {item['modelName']}")

if __name__ == "__main__":
    harvest_nikon()
