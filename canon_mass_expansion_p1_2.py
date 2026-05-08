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

def canon_mass_expansion_p1_2():
    new_lenses = [
        {
            "id": "rf-600mm-f11-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 600mm F11 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 600,
            "focalLengthMaxMm": 600,
            "apertureMax": 11.0,
            "releaseYear": 2020,
            "weightGrams": 930,
            "launchPrice": 21900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/ca60011.jpg"
        },
        {
            "id": "rf-800mm-f11-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 800mm F11 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 800,
            "focalLengthMaxMm": 800,
            "apertureMax": 11.0,
            "releaseYear": 2020,
            "weightGrams": 1260,
            "launchPrice": 27900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/ca80011.jpg"
        },
        {
            "id": "rf-24-105mm-f4-7-1-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 24-105mm F4-7.1 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 105,
            "apertureMax": 4.0,
            "releaseYear": 2020,
            "weightGrams": 395,
            "launchPrice": 12900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car24105.jpg"
        },
        {
            "id": "rf-s-18-45mm-f4-5-6-3-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF-S 18-45mm F4.5-6.3 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF-S",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 18,
            "focalLengthMaxMm": 45,
            "apertureMax": 4.5,
            "releaseYear": 2022,
            "weightGrams": 130,
            "launchPrice": 8900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car1845.jpg"
        },
        {
            "id": "rf-s-10-18mm-f4-5-6-3-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF-S 10-18mm F4.5-6.3 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF-S",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 10,
            "focalLengthMaxMm": 18,
            "apertureMax": 4.5,
            "releaseYear": 2023,
            "weightGrams": 150,
            "launchPrice": 9900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car1018.jpg"
        },
        {
            "id": "rf-s-18-150mm-f3-5-6-3-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF-S 18-150mm F3.5-6.3 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF-S",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 18,
            "focalLengthMaxMm": 150,
            "apertureMax": 3.5,
            "releaseYear": 2022,
            "weightGrams": 310,
            "launchPrice": 14900,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car18150.jpg"
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
        
    print(f"SUCCESS: Expanded Canon lineup with {len(new_lenses)} kit/tele lenses.")

if __name__ == "__main__":
    canon_mass_expansion_p1_2()
