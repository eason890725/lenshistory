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

def fuji_expansion_and_sync():
    # 1. 定義新產品數據 (XF Primes & GF Lenses)
    new_lenses = [
        {
            "id": "xf-35mm-f1-4-r",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 35mm F1.4 R",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 35,
            "focalLengthMaxMm": 35,
            "apertureMax": 1.4,
            "releaseYear": 2012,
            "weightGrams": 187,
            "launchPrice": 18000,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "R-Series",
            "url": "https://www.adorama.com/images/Large/ifj35xf.jpg"
        },
        {
            "id": "xf-23mm-f1-4-r-lm-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 23mm F1.4 R LM WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 23,
            "focalLengthMaxMm": 23,
            "apertureMax": 1.4,
            "releaseYear": 2021,
            "weightGrams": 375,
            "launchPrice": 26000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "LM WR",
            "url": "https://www.adorama.com/images/Large/ifj23xflm.jpg"
        },
        {
            "id": "xf-18mm-f1-4-r-lm-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 18mm F1.4 R LM WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 18,
            "focalLengthMaxMm": 18,
            "apertureMax": 1.4,
            "releaseYear": 2021,
            "weightGrams": 370,
            "launchPrice": 29000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "LM WR",
            "url": "https://www.adorama.com/images/Large/ifj1814.jpg"
        },
        {
            "id": "xf-90mm-f2-r-lm-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 90mm F2 R LM WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 90,
            "focalLengthMaxMm": 90,
            "apertureMax": 2.0,
            "releaseYear": 2015,
            "weightGrams": 540,
            "launchPrice": 28000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "LM WR",
            "url": "https://www.adorama.com/images/Large/ifj902.jpg"
        },
        {
            "id": "gf-32-64mm-f4-r-lm-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm GF 32-64mm F4 R LM WR",
            "gearType": "LENS",
            "mount": "Fujifilm G",
            "sensorFormat": "Medium Format",
            "focalLengthMinMm": 32,
            "focalLengthMaxMm": 64,
            "apertureMax": 4.0,
            "releaseYear": 2017,
            "weightGrams": 875,
            "launchPrice": 72000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "GF-Series",
            "url": "https://www.adorama.com/images/Large/ifjgf3264.jpg"
        },
        {
            "id": "gf-110mm-f2-r-lm-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm GF 110mm F2 R LM WR",
            "gearType": "LENS",
            "mount": "Fujifilm G",
            "sensorFormat": "Medium Format",
            "focalLengthMinMm": 110,
            "focalLengthMaxMm": 110,
            "apertureMax": 2.0,
            "releaseYear": 2017,
            "weightGrams": 1010,
            "launchPrice": 85000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "GF-Series",
            "url": "https://www.adorama.com/images/Large/ifjgf1102.jpg"
        },
        {
            "id": "gf-80mm-f1-7-r-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm GF 80mm F1.7 R WR",
            "gearType": "LENS",
            "mount": "Fujifilm G",
            "sensorFormat": "Medium Format",
            "focalLengthMinMm": 80,
            "focalLengthMaxMm": 80,
            "apertureMax": 1.7,
            "releaseYear": 2021,
            "weightGrams": 795,
            "launchPrice": 69000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "GF-Series",
            "url": "https://www.adorama.com/images/Large/ifjgf80.jpg"
        },
        {
            "id": "gf-45-100mm-f4-r-lm-ois-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm GF 45-100mm F4 R LM OIS WR",
            "gearType": "LENS",
            "mount": "Fujifilm G",
            "sensorFormat": "Medium Format",
            "focalLengthMinMm": 45,
            "focalLengthMaxMm": 100,
            "apertureMax": 4.0,
            "releaseYear": 2020,
            "weightGrams": 1005,
            "launchPrice": 72000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "GF-Series",
            "url": "https://www.adorama.com/images/Large/ifjgf45100.jpg"
        }
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/fujifilm"
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
                lens["image_url"] = f"/images/products/fujifilm/{lens_id}.jpg"
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
        
    print(f"SUCCESS: Expanded Fujifilm lineup with {len(new_lenses)} core lenses.")

if __name__ == "__main__":
    fuji_expansion_and_sync()
