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

def nikon_expansion_and_sync():
    # 1. 定義新產品數據
    new_lenses = [
        {
            "id": "z-58mm-f-0-95-s-noct",
            "brand": "Nikon",
            "modelName": "Nikon Z 58mm f/0.95 S Noct",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 58,
            "focalLengthMaxMm": 58,
            "apertureMax": 0.95,
            "releaseYear": 2019,
            "weightGrams": 2000,
            "launchPrice": 250000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz5895.jpg"
        },
        {
            "id": "z-105mm-f-2-8-vr-s-micro",
            "brand": "Nikon",
            "modelName": "Nikon Z 105mm f/2.8 VR S Micro",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 105,
            "focalLengthMaxMm": 105,
            "apertureMax": 2.8,
            "releaseYear": 2021,
            "weightGrams": 630,
            "launchPrice": 32000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz10528.jpg"
        },
        {
            "id": "z-14-30mm-f-4-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 14-30mm f/4 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 14,
            "focalLengthMaxMm": 30,
            "apertureMax": 4.0,
            "releaseYear": 2019,
            "weightGrams": 485,
            "launchPrice": 38000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz1430.jpg"
        },
        {
            "id": "z-24-200mm-f-4-6-3-vr",
            "brand": "Nikon",
            "modelName": "Nikon Z 24-200mm f/4-6.3 VR",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 200,
            "apertureMax": 4.0,
            "releaseYear": 2020,
            "weightGrams": 570,
            "launchPrice": 28000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz24200.jpg"
        },
        {
            "id": "z-180-600mm-f-5-6-6-3-vr",
            "brand": "Nikon",
            "modelName": "Nikon Z 180-600mm f/5.6-6.3 VR",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 180,
            "focalLengthMaxMm": 600,
            "apertureMax": 5.6,
            "releaseYear": 2023,
            "weightGrams": 1955,
            "launchPrice": 55000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz180600.jpg"
        },
        {
            "id": "z-85mm-f-1-8-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 85mm f/1.8 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 85,
            "focalLengthMaxMm": 85,
            "apertureMax": 1.8,
            "releaseYear": 2019,
            "weightGrams": 470,
            "launchPrice": 24000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz8518.jpg"
        },
        {
            "id": "z-50mm-f-1-8-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 50mm f/1.8 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 50,
            "focalLengthMaxMm": 50,
            "apertureMax": 1.8,
            "releaseYear": 2018,
            "weightGrams": 415,
            "launchPrice": 18000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz5018.jpg"
        },
        {
            "id": "z-35mm-f-1-8-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 35mm f/1.8 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 35,
            "focalLengthMaxMm": 35,
            "apertureMax": 1.8,
            "releaseYear": 2018,
            "weightGrams": 370,
            "launchPrice": 25000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz3518.jpg"
        }
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/nikon"
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
                lens["image_url"] = f"/images/products/nikon/{lens_id}.jpg"
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
        
    print(f"SUCCESS: Expanded Nikon lineup with {len(new_lenses)} core lenses.")

if __name__ == "__main__":
    nikon_expansion_and_sync()
