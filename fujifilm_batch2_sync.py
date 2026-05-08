import json
import os
import requests
from PIL import Image
import io

def process_to_pure_black(img_url, save_path):
    try:
        response = requests.get(img_url, timeout=15)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        
        # 影像黑化邏輯 (V2.0 高強度)
        datas = img.getdata()
        newData = []
        for item in datas:
            # 判斷是否為白色背景 (R,G,B > 220)
            if item[0] > 220 and item[1] > 220 and item[2] > 220:
                newData.append((0, 0, 0, 0)) # 變透明
            else:
                newData.append(item)
        img.putdata(newData)
        
        # 建立純黑背景 (RGB 0,0,0)
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])
        background.save(save_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"Image Error: {e}")
        return False

def fujifilm_v2_batch2():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/fujifilm"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次二採集數據
    batch2_data = {
        "fujifilm-xc-35mm-f2": {
            "opticalDesign": "9 elements in 6 groups (2 aspherical)",
            "minAperture": "f/16", "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC", "maxMagnification": "0.14x",
            "minFocusDistance": "0.35m", "filterSize": "43mm", "launchPrice": 6000
        },
        "fujifilm-xc-15-45mm-f3-5-5-6-ois-pz": {
            "opticalDesign": "10 elements in 9 groups (3 aspherical, 2 ED)",
            "minAperture": "f/22", "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC", "maxMagnification": "0.24x",
            "minFocusDistance": "0.13m", "filterSize": "52mm", "launchPrice": 5500
        },
        "fujifilm-gf-32-64mm-f4-r-lm-wr": {
            "opticalDesign": "14 elements in 11 groups (3 aspherical, 1 ED, 1 Super ED)",
            "minAperture": "f/32", "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine", "maxMagnification": "0.12x",
            "minFocusDistance": "0.5m", "filterSize": "77mm", "launchPrice": 65000
        },
        "fujifilm-gf-110mm-f2-r-lm-wr": {
            "opticalDesign": "14 elements in 9 groups (4 ED)",
            "minAperture": "f/22", "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine", "maxMagnification": "0.16x",
            "minFocusDistance": "0.9m", "filterSize": "77mm", "launchPrice": 85000
        },
        "fujifilm-xf-50mm-f2-r-wr": {
            "opticalDesign": "9 elements in 7 groups (1 aspherical ED)",
            "minAperture": "f/16", "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC", "maxMagnification": "0.15x",
            "minFocusDistance": "0.39m", "filterSize": "46mm", "launchPrice": 14000
        },
        "fujifilm-xf-23mm-f2-r-wr": {
            "opticalDesign": "10 elements in 6 groups (2 aspherical)",
            "minAperture": "f/16", "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC", "maxMagnification": "0.13x",
            "minFocusDistance": "0.22m", "filterSize": "43mm", "launchPrice": 13500
        },
        "fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr": {
            "opticalDesign": "21 elements in 14 groups (5 ED, 1 Super ED)",
            "minAperture": "f/22", "focusMotor": "Twin Linear Motor (LM)",
            "coating": "Super EBC, Fluorine", "maxMagnification": "0.19x",
            "minFocusDistance": "1.75m", "filterSize": "77mm", "launchPrice": 55000
        }
    }

    # 更換 XF 100-400mm 影像 (Rule 17)
    img_url_100_400 = "http://thepixelconnection.com/cdn/shop/products/100-400.jpg?v=1691166026"
    save_path_100_400 = os.path.join(img_dir, "fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr.jpg")
    process_to_pure_black(img_url_100_400, save_path_100_400)

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch2_data:
            p.update(batch2_data[pid])
            updated_count += 1
            
    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Fujifilm Batch 2 Update Complete. Updated: {updated_count}")

if __name__ == "__main__":
    fujifilm_v2_batch2()
