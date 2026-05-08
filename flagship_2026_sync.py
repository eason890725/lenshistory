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

def flagship_2026_sync():
    new_items = [
        {
            "id": "eos-r6-mark-iii",
            "brand": "Canon",
            "modelName": "Canon EOS R6 Mark III",
            "gearType": "CAMERA",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "megapixels": 32.5,
            "maxVideoResolution": "7K RAW",
            "releaseYear": 2025,
            "weightGrams": 609,
            "launchPrice": 79000,
            "hasIBIS": True,
            "url": "https://www.adorama.com/images/Large/car6m3.jpg"
        },
        {
            "id": "nikon-zr",
            "brand": "Nikon",
            "modelName": "Nikon ZR (Cinema Camera)",
            "gearType": "CAMERA",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "megapixels": 24.5,
            "maxVideoResolution": "8K REDCODE",
            "releaseYear": 2025,
            "weightGrams": 650,
            "launchPrice": 69000,
            "hasIBIS": True,
            "url": "https://www.adorama.com/images/Large/nkzr.jpg"
        },
        {
            "id": "nikon-z6-iii",
            "brand": "Nikon",
            "modelName": "Nikon Z6 III",
            "gearType": "CAMERA",
            "mount": "Nikon Z",
            "sensorFormat": "Full Frame",
            "megapixels": 24.5,
            "maxVideoResolution": "6K RAW",
            "releaseYear": 2024,
            "weightGrams": 670,
            "launchPrice": 79000,
            "hasIBIS": True,
            "url": "https://www.adorama.com/images/Large/nkz6m3.jpg"
        },
        {
            "id": "rf-28-70mm-f2-8-is-stm",
            "brand": "Canon",
            "modelName": "Canon RF 28-70mm F2.8 IS STM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 28,
            "focalLengthMaxMm": 70,
            "apertureMax": 2.8,
            "releaseYear": 2024,
            "weightGrams": 495,
            "launchPrice": 34900,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "STM",
            "url": "https://www.adorama.com/images/Large/ca2870rf.jpg"
        },
        {
            "id": "rf-24mm-f1-4l-vcm",
            "brand": "Canon",
            "modelName": "Canon RF 24mm F1.4 L VCM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 24,
            "focalLengthMaxMm": 24,
            "apertureMax": 1.4,
            "releaseYear": 2025,
            "weightGrams": 520,
            "launchPrice": 46900,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "L-VCM",
            "url": "https://www.adorama.com/images/Large/ca2414rf.jpg"
        },
        {
            "id": "rf-50mm-f1-4l-vcm",
            "brand": "Canon",
            "modelName": "Canon RF 50mm F1.4 L VCM",
            "gearType": "LENS",
            "mount": "Canon RF",
            "sensorFormat": "Full Frame",
            "focalLengthMinMm": 50,
            "focalLengthMaxMm": 50,
            "apertureMax": 1.4,
            "releaseYear": 2025,
            "weightGrams": 580,
            "launchPrice": 43900,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "L-VCM",
            "url": "https://www.adorama.com/images/Large/ca5014rf.jpg"
        }
    ]
    
    json_path = "frontend/src/data/products.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    existing_ids = [p.get("id") for p in products]
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for item in new_items:
        item_id = item["id"]
        brand = item["brand"].lower()
        url = item.pop("url")
        target_dir = f"frontend/public/images/products/{brand}"
        os.makedirs(target_dir, exist_ok=True)
        
        temp_file = os.path.join(target_dir, f"{item_id}_temp.jpg")
        final_file = os.path.join(target_dir, f"{item_id}.jpg")
        
        try:
            print(f"Processing 2026 Flagship: {item_id}...")
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            with open(temp_file, "wb") as f_img:
                f_img.write(resp.content)
            
            if transform_to_black_bg(temp_file, final_file):
                item["image_url"] = f"/images/products/{brand}/{item_id}.jpg"
                if item_id not in existing_ids:
                    products.append(item)
                else:
                    for p in products:
                        if p["id"] == item_id:
                            p.update(item)
                            break
                os.remove(temp_file)
        except Exception as e:
            print(f"Error syncing {item_id}: {e}")
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Synced 2026 Flagship Lineup (Canon R6 III, Nikon ZR, etc.)")

if __name__ == "__main__":
    flagship_2026_sync()
