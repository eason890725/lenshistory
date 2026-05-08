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

def canon_mass_expansion_p1_1():
    new_lenses = [
        {
            "id": "rf-16mm-f2-8-stm",
            "brand": "Canon",
            "modelName": "Canon RF 16mm F2.8 STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 16,
            "focalLengthMaxMm": 16,
            "apertureMax": 2.8,
            "releaseYear": 2021,
            "weightGrams": 165,
            "launchPrice": 8900,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car1628.jpg"
        },
        {
            "id": "rf-24mm-f1-8-macro-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 24mm F1.8 Macro IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 24,
            "apertureMax": 1.8,
            "releaseYear": 2022,
            "weightGrams": 270,
            "launchPrice": 17900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car2418.jpg"
        },
        {
            "id": "rf-28mm-f2-8-stm",
            "brand": "Canon",
            "modelName": "Canon RF 28mm F2.8 STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 28,
            "focalLengthMaxMm": 28,
            "apertureMax": 2.8,
            "releaseYear": 2023,
            "weightGrams": 120,
            "launchPrice": 8900,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car2828.jpg"
        },
        {
            "id": "rf-35mm-f1-8-macro-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 35mm F1.8 Macro IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 35,
            "focalLengthMaxMm": 35,
            "apertureMax": 1.8,
            "releaseYear": 2018,
            "weightGrams": 305,
            "launchPrice": 14900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car3518.jpg"
        },
        {
            "id": "rf-100-400mm-f5-6-8-is-usm",
            "brand": "Canon",
            "modelName": "Canon RF 100-400mm F5.6-8 IS USM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 100,
            "focalLengthMaxMm": 400,
            "apertureMax": 5.6,
            "releaseYear": 2021,
            "weightGrams": 635,
            "launchPrice": 19900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "USM",
            "url": "https://www.adorama.com/images/Large/car100400.jpg"
        }
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/canon"
    os.makedirs(target_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    existing_ids = [p.get("id") for p in products]
    
    for lens in new_lenses:
        lens_id = lens["id"]
        url = lens.pop("url")
        temp_file = os.path.join(target_dir, f"{lens_id}_temp.jpg")
        final_file = os.path.join(target_dir, f"{lens_id}.jpg")
        
        try:
            print(f"Processing {lens_id}...")
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            with open(temp_file, "wb") as f_img:
                f_img.write(resp.content)
            
            if transform_to_black_bg(temp_file, final_file):
                lens["image_url"] = f"/images/products/canon/{lens_id}.jpg"
                if lens_id not in existing_ids:
                    products.append(lens)
                else:
                    for p in products:
                        if p["id"] == lens_id:
                            p.update(lens)
                            break
                os.remove(temp_file)
        except Exception as e:
            print(f"Error expanding {lens_id}: {e}")
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Expanded Canon lineup with {len(new_lenses)} consumer lenses.")

if __name__ == "__main__":
    canon_mass_expansion_p1_1()
