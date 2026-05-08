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

def fuji_mass_expansion_p3_1():
    new_lenses = [
        {
            "id": "xf-23mm-f2-r-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 23mm F2 R WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 23,
            "focalLengthMaxMm": 23,
            "apertureMax": 2.0,
            "releaseYear": 2016,
            "weightGrams": 180,
            "launchPrice": 13000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "R WR",
            "url": "https://www.adorama.com/images/Large/ifj232b.jpg"
        },
        {
            "id": "xf-35mm-f2-r-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 35mm F2 R WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 35,
            "focalLengthMaxMm": 35,
            "apertureMax": 2.0,
            "releaseYear": 2015,
            "weightGrams": 170,
            "launchPrice": 11500,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "R WR",
            "url": "https://www.adorama.com/images/Large/ifj352xf.jpg"
        },
        {
            "id": "xf-50mm-f2-r-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 50mm F2 R WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 50,
            "focalLengthMaxMm": 50,
            "apertureMax": 2.0,
            "releaseYear": 2017,
            "weightGrams": 200,
            "launchPrice": 13000,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "R WR",
            "url": "https://www.adorama.com/images/Large/ifj502xfb.jpg"
        },
        {
            "id": "xf-27mm-f2-8-r-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 27mm F2.8 R WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 27,
            "focalLengthMaxMm": 27,
            "apertureMax": 2.8,
            "releaseYear": 2021,
            "weightGrams": 84,
            "launchPrice": 11500,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "R WR",
            "url": "https://www.adorama.com/images/Large/ifj27xfwr.jpg"
        },
        {
            "id": "xf-16mm-f2-8-r-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 16mm F2.8 R WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 16,
            "focalLengthMaxMm": 16,
            "apertureMax": 2.8,
            "releaseYear": 2019,
            "weightGrams": 155,
            "launchPrice": 11500,
            "hasOIS": False,
            "hasWeatherSeal": True,
            "series": "R WR",
            "url": "https://www.adorama.com/images/Large/ifj1628b.jpg"
        },
        {
            "id": "xf-18-135mm-f3-5-5-6-r-lm-ois-wr",
            "brand": "Fujifilm",
            "modelName": "Fujifilm XF 18-135mm F3.5-5.6 R LM OIS WR",
            "gearType": "LENS",
            "mount": "Fujifilm X",
            "sensorFormat": "APS-C",
            "focalLengthMinMm": 18,
            "focalLengthMaxMm": 135,
            "apertureMax": 3.5,
            "releaseYear": 2014,
            "weightGrams": 490,
            "launchPrice": 26000,
            "hasOIS": True,
            "hasWeatherSeal": True,
            "series": "LM WR",
            "url": "https://www.adorama.com/images/Large/ifj18135.jpg"
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
        
    print(f"SUCCESS: Expanded Fujifilm lineup with {len(new_lenses)} consumer lenses.")

if __name__ == "__main__":
    fuji_mass_expansion_p3_1()
