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

def nikon_mass_expansion_p2_2():
    new_lenses = [
        {
            "id": "z-dx-16-50mm-f-3-5-6-3-vr",
            "brand": "Nikon",
            "modelName": "Nikon Z DX 16-50mm f/3.5-6.3 VR",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 16,
            "focalLengthMaxMm": 50,
            "apertureMax": 3.5,
            "releaseYear": 2019,
            "weightGrams": 135,
            "launchPrice": 9000,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "DX-Series",
            "url": "https://www.adorama.com/images/Large/nkz1650.jpg"
        },
        {
            "id": "z-dx-50-250mm-f-4-5-6-3-vr",
            "brand": "Nikon",
            "modelName": "Nikon Z DX 50-250mm f/4.5-6.3 VR",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 50,
            "focalLengthMaxMm": 250,
            "apertureMax": 4.5,
            "releaseYear": 2019,
            "weightGrams": 405,
            "launchPrice": 11000,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "DX-Series",
            "url": "https://www.adorama.com/images/Large/nkz50250.jpg"
        },
        {
            "id": "z-dx-12-28mm-f-3-5-5-6-pz-vr",
            "brand": "Nikon",
            "modelName": "Nikon Z DX 12-28mm f/3.5-5.6 PZ VR",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 12,
            "focalLengthMaxMm": 28,
            "apertureMax": 3.5,
            "releaseYear": 2023,
            "weightGrams": 205,
            "launchPrice": 11000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "DX-Series",
            "url": "https://www.adorama.com/images/Large/nkz1228.jpg"
        },
        {
            "id": "z-dx-18-140mm-f-3-5-6-3-vr",
            "brand": "Nikon",
            "modelName": "Nikon Z DX 18-140mm f/3.5-6.3 VR",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 18,
            "focalLengthMaxMm": 140,
            "apertureMax": 3.5,
            "releaseYear": 2021,
            "weightGrams": 315,
            "launchPrice": 18000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "DX-Series",
            "url": "https://www.adorama.com/images/Large/nkz18140.jpg"
        },
        {
            "id": "z-24-50mm-f-4-6-3",
            "brand": "Nikon",
            "modelName": "Nikon Z 24-50mm f/4-6.3",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 50,
            "apertureMax": 4.0,
            "releaseYear": 2020,
            "weightGrams": 195,
            "launchPrice": 12000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz2450.jpg"
        },
        {
            "id": "z-28-75mm-f-2-8",
            "brand": "Nikon",
            "modelName": "Nikon Z 28-75mm f/2.8",
            "gearType": "LENS",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 28,
            "focalLengthMaxMm": 75,
            "apertureMax": 2.8,
            "releaseYear": 2021,
            "weightGrams": 565,
            "launchPrice": 29000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "Z-Series",
            "url": "https://www.adorama.com/images/Large/nkz2875n.jpg"
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
        
    print(f"SUCCESS: Expanded Nikon lineup with {len(new_lenses)} kit/DX lenses.")

if __name__ == "__main__":
    nikon_mass_expansion_p2_2()
