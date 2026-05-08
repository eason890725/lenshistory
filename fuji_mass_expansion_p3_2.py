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

def fuji_mass_expansion_p3_2():
    new_lenses = [
        {
            "id": "xf-70-300mm-f4-5-6-r-lm-ois-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 70-300mm F4-5.6 R LM OIS WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 70,
            "focalLengthMaxMm": 300,
            "apertureMax": 4.0,
            "releaseYear": 2021,
            "weightGrams": 580,
            "launchPrice": 23500,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "LM WR",
            "url": "https://www.adorama.com/images/Large/ifj70300xf.jpg"
        },
        {
            "id": "xf-100-400mm-f4-5-5-6-r-lm-ois-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 100-400mm F4.5-5.6 R LM OIS WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 100,
            "focalLengthMaxMm": 400,
            "apertureMax": 4.5,
            "releaseYear": 2016,
            "weightGrams": 1375,
            "launchPrice": 55000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "LM WR",
            "url": "https://www.adorama.com/images/Large/ifj100400xfa.jpg"
        },
        {
            "id": "xf-55-200mm-f3-5-4-8-r-lm-ois",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 55-200mm F3.5-4.8 R LM OIS",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 55,
            "focalLengthMaxMm": 200,
            "apertureMax": 3.5,
            "releaseYear": 2013,
            "weightGrams": 580,
            "launchPrice": 20000,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "LM",
            "url": "https://www.adorama.com/images/Large/ifj555200xf.jpg"
        },
        {
            "id": "xc-15-45mm-f3-5-5-6-ois-pz",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XC 15-45mm F3.5-5.6 OIS PZ",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 15,
            "focalLengthMaxMm": 45,
            "apertureMax": 3.5,
            "releaseYear": 2018,
            "weightGrams": 135,
            "launchPrice": 8500,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "XC-Series",
            "url": "https://www.adorama.com/images/Large/ifj1545b.jpg"
        },
        {
            "id": "xc-35mm-f2",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XC 35mm F2",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 35,
            "focalLengthMaxMm": 35,
            "apertureMax": 2.0,
            "releaseYear": 2019,
            "weightGrams": 130,
            "launchPrice": 5800,
            "hasOIS": False,
            "hasWeatherSeal": False,
            "series": "XC-Series",
            "url": "https://www.adorama.com/images/Large/ifj352xc.jpg"
        },
        {
            "id": "xc-50-230mm-f4-5-6-7-ois-ii",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XC 50-230mm F4.5-6.7 OIS II",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 50,
            "focalLengthMaxMm": 230,
            "apertureMax": 4.5,
            "releaseYear": 2015,
            "weightGrams": 375,
            "launchPrice": 11500,
            "hasOIS": True,
            "hasWeatherSeal": False,
            "series": "XC-Series",
            "url": "https://www.adorama.com/images/Large/ifj502302b.jpg"
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
        
    print(f"SUCCESS: Expanded Fujifilm lineup with {len(new_lenses)} consumer/tele lenses.")

if __name__ == "__main__":
    fuji_mass_expansion_p3_2()
