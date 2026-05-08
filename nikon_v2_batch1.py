import json
import os
import requests
from PIL import Image
import io

def process_image_to_black(img_url, save_path):
    try:
        response = requests.get(img_url, timeout=10)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        
        # 簡單的白轉黑邏輯：將接近白色的像素變為透明，然後貼在黑色背景上
        # 或者更精確地使用門檻值
        datas = img.getdata()
        newData = []
        for item in datas:
            # 如果像素接近白色 (R>240, G>240, B>240)
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((0, 0, 0, 0)) # 變透明
            else:
                newData.append(item)
        img.putdata(newData)
        
        # 創建純黑背景
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3]) # 使用透明度作為 mask
        background.save(save_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"Image Error: {e}")
        return False

def nikon_v2_batch1():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次一採集數據
    batch1_data = {
        "nikon-z-180-600mm-f-5-6-6-3-vr": {
            "opticalDesign": "25 elements in 17 groups (6 ED, 1 aspherical)",
            "minAperture": "f/32 - f/36",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Fluorine Coating (Front Element)",
            "maxMagnification": "0.25x",
            "minFocusDistance": "1.3m",
            "filterSize": "95mm",
            "dimensions": "ø110 x 315.5 mm",
            "launchPrice": 57880
        },
        "nikon-z-26mm-f-2-8": {
            "opticalDesign": "8 elements in 6 groups (3 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.2m",
            "filterSize": "52mm (via HB-111)",
            "dimensions": "ø70 x 23.5 mm",
            "launchPrice": 15900
        },
        "nikon-z-dx-12-28mm-f-3-5-5-6-pz-vr": {
            "opticalDesign": "12 elements in 11 groups (1 ED, 1 aspherical)",
            "minAperture": "f/16 - f/25",
            "focusMotor": "STM (Power Zoom Integrated)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.19m",
            "filterSize": "67mm",
            "dimensions": "ø72 x 63.5 mm",
            "launchPrice": 10990
        },
        "nikon-z-105mm-f-2-8-vr-s-micro": {
            "opticalDesign": "16 elements in 11 groups (3 ED, 1 aspherical)",
            "minAperture": "f/32",
            "focusMotor": "Dual STM (Multi-focus system)",
            "coating": "Nano Crystal, ARNEO, Fluorine",
            "maxMagnification": "1.0x",
            "minFocusDistance": "0.29m",
            "filterSize": "62mm",
            "dimensions": "ø85 x 140 mm",
            "launchPrice": 29400
        },
        "nikon-z-28mm-f-2-8": {
            "opticalDesign": "9 elements in 8 groups (2 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "Dual STM (Multi-focus system)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.19m",
            "filterSize": "52mm",
            "dimensions": "ø70 x 43 mm",
            "launchPrice": 7900
        },
        "nikon-z-40mm-f-2": {
            "opticalDesign": "6 elements in 4 groups (2 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.29m",
            "filterSize": "52mm",
            "dimensions": "ø70 x 45.5 mm",
            "launchPrice": 9180
        },
        "nikon-z-dx-18-140mm-f-3-5-6-3-vr": {
            "opticalDesign": "17 elements in 13 groups (2 ED, 2 aspherical)",
            "minAperture": "f/22 - f/40",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.33x",
            "minFocusDistance": "0.2m",
            "filterSize": "62mm",
            "dimensions": "ø73 x 90 mm",
            "launchPrice": 18900
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch1_data:
            p.update(batch1_data[pid])
            updated_count += 1
            
    # 數量防呆 (Rule 3)
    if len(products) < 230: # 預期總數應在 238 左右
        print("ERROR: DATA LOSS DETECTED")
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Nikon V2.0 Batch 1 Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    nikon_v2_batch1()
