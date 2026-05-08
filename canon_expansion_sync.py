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

def canon_expansion_and_sync():
    # 1. 定義新產品數據
    new_lenses = [
        {
            "id": "rf-85mm-f1-2l-usm",
            "brand": "Canon",
            "modelName": "Canon RF 85mm F1.2 L USM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 85,
            "focalLengthMaxMm": 85,
            "apertureMax": 1.2,
            "releaseYear": 2019,
            "weightGrams": 1195,
            "launchPrice": 85000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car8512.jpg"
        },
        {
            "id": "rf-135mm-f1-8l-is-usm",
            "brand": "Canon",
            "modelName": "Canon RF 135mm F1.8 L IS USM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 135,
            "focalLengthMaxMm": 135,
            "apertureMax": 1.8,
            "releaseYear": 2022,
            "weightGrams": 935,
            "launchPrice": 65000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car13518.jpg"
        },
        {
            "id": "rf-100mm-f2-8l-macro-is-usm",
            "brand": "Canon",
            "modelName": "Canon RF 100mm F2.8 L Macro IS USM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 100,
            "focalLengthMaxMm": 100,
            "apertureMax": 2.8,
            "releaseYear": 2021,
            "weightGrams": 730,
            "launchPrice": 42000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car10028.jpg"
        },
        {
            "id": "rf-100-500mm-f4-5-7-1l-is-usm",
            "brand": "Canon",
            "modelName": "Canon RF 100-500mm F4.5-7.1 L IS USM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 100,
            "focalLengthMaxMm": 500,
            "apertureMax": 4.5,
            "releaseYear": 2020,
            "weightGrams": 1370,
            "launchPrice": 88000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car100500.jpg"
        },
        {
            "id": "rf-24-105mm-f4l-is-usm",
            "brand": "Canon",
            "modelName": "Canon RF 24-105mm F4 L IS USM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 105,
            "apertureMax": 4.0,
            "releaseYear": 2018,
            "weightGrams": 700,
            "launchPrice": 35000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car241054.jpg"
        },
        {
            "id": "rf-24-105mm-f2-8l-is-usm-z",
            "brand": "Canon",
            "modelName": "Canon RF 24-105mm F2.8 L IS USM Z",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 105,
            "apertureMax": 2.8,
            "releaseYear": 2023,
            "weightGrams": 1330,
            "launchPrice": 95000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car2410528.jpg"
        },
        {
            "id": "rf-10-20mm-f4l-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 10-20mm F4 L IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 10,
            "focalLengthMaxMm": 20,
            "apertureMax": 4.0,
            "releaseYear": 2023,
            "weightGrams": 570,
            "launchPrice": 72000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "L-Series",
            "url": "https://www.adorama.com/images/Large/car1020.jpg"
        },
        {
            "id": "rf-50mm-f1-8-stm",
            "brand": "Canon",
            "modelName": "Canon RF 50mm F1.8 STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 50,
            "focalLengthMaxMm": 50,
            "apertureMax": 1.8,
            "releaseYear": 2020,
            "weightGrams": 160,
            "launchPrice": 5900,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/car5018.jpg"
        }
    ]
    
    json_path = "frontend/src/data/products.json"
    target_dir = "frontend/public/images/products/canon"
    os.makedirs(target_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 讀取現有資料
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    existing_ids = [p.get("id") for p in products]
    
    for lens in new_lenses:
        lens_id = lens["id"]
        url = lens.pop("url") # 移除 url 欄位
        
        # 2. 下載與黑化
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
                # 3. 插入或更新資料庫
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
            
    # 寫回 JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Expanded Canon lineup with {len(new_lenses)} core lenses.")

if __name__ == "__main__":
    canon_expansion_and_sync()
