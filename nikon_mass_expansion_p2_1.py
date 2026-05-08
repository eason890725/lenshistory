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

def nikon_mass_expansion_p2_1():
    new_lenses = [
        {
            "id": "z-20mm-f-1-8-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 20mm f/1.8 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 20,
            "focalLengthMaxMm": 20,
            "apertureMax": 1.8,
            "releaseYear": 2020,
            "weightGrams": 505,
            "launchPrice": 32000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz2018.jpg"
        },
        {
            "id": "z-24mm-f-1-8-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 24mm f/1.8 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 24,
            "apertureMax": 1.8,
            "releaseYear": 2019,
            "weightGrams": 450,
            "launchPrice": 31000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz2418.jpg"
        },
        {
            "id": "z-26mm-f-2-8",
            "brand": "Nikon",
            "modelName": "Nikon Z 26mm f/2.8",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 26,
            "focalLengthMaxMm": 26,
            "apertureMax": 2.8,
            "releaseYear": 2023,
            "weightGrams": 125,
            "launchPrice": 15000,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz2628.jpg"
        },
        {
            "id": "z-28mm-f-2-8",
            "brand": "Nikon",
            "modelName": "Nikon Z 28mm f/2.8",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 28,
            "focalLengthMaxMm": 28,
            "apertureMax": 2.8,
            "releaseYear": 2021,
            "weightGrams": 155,
            "launchPrice": 9000,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz2828n.jpg"
        },
        {
            "id": "z-40mm-f-2",
            "brand": "Nikon",
            "modelName": "Nikon Z 40mm f/2",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 40,
            "focalLengthMaxMm": 40,
            "apertureMax": 2.0,
            "releaseYear": 2021,
            "weightGrams": 170,
            "launchPrice": 9000,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz402.jpg"
        },
        {
            "id": "z-24-70mm-f-4-s",
            "brand": "Nikon",
            "modelName": "Nikon Z 24-70mm f/4 S",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 70,
            "apertureMax": 4.0,
            "releaseYear": 2018,
            "weightGrams": 500,
            "launchPrice": 30000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "S-Line",
            "url": "https://www.adorama.com/images/Large/nkz2470.jpg"
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
        
    print(f"SUCCESS: Expanded Nikon lineup with {len(new_lenses)} consumer lenses.")

if __name__ == "__main__":
    nikon_mass_expansion_p2_1()
