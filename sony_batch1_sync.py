import json
import os
import requests
from PIL import Image
import io

def process_to_pure_black(img_url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(img_url, headers=headers, timeout=15)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] > 220 and item[1] > 220 and item[2] > 220:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])
        background.save(save_path, "JPEG", quality=95)
        print(f"SUCCESS: Saved {save_path}")
        return True
    except Exception as e:
        print(f"IMG ERROR {save_path}: {e}")
        return False

def sony_v2_batch1():
    json_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/sony"
    if not os.path.exists(img_dir): os.makedirs(img_dir)
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次一採集數據 (2026 旗艦與 GM 組)
    batch1_data = {
        "sony-a1-ii": {
            "sensorType": "50.1MP Full-frame Stacked BSI CMOS (Exmor RS)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "8.5 stops (Center)", "launchPrice": 189980, "hasIBIS": True,
            "videoResolution": "8K 30p / 4K 120p", "burstSpeed": "30fps"
        },
        "sony-a9-iii": {
            "sensorType": "24.6MP Full-frame Stacked CMOS (Global Shutter)",
            "afTargets": "Real-time Recognition AF (AI Unit)",
            "ibisRating": "8.0 stops", "launchPrice": 184980, "hasIBIS": True,
            "videoResolution": "4K 120p (No Crop)", "burstSpeed": "120fps"
        },
        "sony-a7r-v": {
            "sensorType": "61.0MP Full-frame BSI CMOS (Exmor R)",
            "afTargets": "Human, Animal, Bird, Insect, Car, Train, Airplane",
            "ibisRating": "8.0 stops", "launchPrice": 106980, "hasIBIS": True
        },
        "sony-a7-v": {
            "sensorType": "33.0MP Full-frame Partially Stacked CMOS (Exmor RS)",
            "afTargets": "Next-gen AI Recognition", "ibisRating": "7.5 stops",
            "launchPrice": 78990, "hasIBIS": True, "videoResolution": "4K 60p (7K Oversampled)"
        },
        "sony-a7c-ii": {
            "sensorType": "33.0MP Full-frame BSI CMOS", "ibisRating": "7.0 stops",
            "afTargets": "Human, Animal, Bird, Insect, Car, Train, Airplane", "launchPrice": 56980
        },
        "sony-fe-28-70mm-f2-gm": {
            "opticalDesign": "20 elements in 14 groups", "focusMotor": "4 XD Linear Motors",
            "coating": "Nano AR II, Fluorine", "minFocusDistance": "0.38m", "filterSize": "86mm", "launchPrice": 87980
        },
        "sony-fe-24-70mm-f2-8-gm-ii": {
            "opticalDesign": "20 elements in 15 groups", "focusMotor": "4 XD Linear Motors",
            "coating": "Nano AR II", "minFocusDistance": "0.21m", "filterSize": "82mm", "launchPrice": 51280
        },
        "sony-fe-70-200mm-f2-8-gm-oss-ii": {
            "opticalDesign": "17 elements in 14 groups", "focusMotor": "4 XD Linear Motors",
            "coating": "Nano AR II", "minFocusDistance": "0.4m", "filterSize": "77mm", "launchPrice": 76980
        }
        # ... 其他產品規格與影像 URL 映射
    }

    # 影像抓取清單
    img_targets = {
        "sony-a1-ii": "https://www.sony.com.tw/image/ff8080819323f93d019324205c3b0010?fmt=png-alpha",
        "sony-a9-iii": "https://www.sony.com.tw/image/ff8080818c8be844018c9f7f44ff06c1?fmt=png-alpha",
        "sony-fe-28-70mm-f2-gm": "https://www.sony.com.tw/image/ff8080819323f93d0193295de80c0480?fmt=png-alpha"
    }

    for name, url in img_targets.items():
        process_to_pure_black(url, os.path.join(img_dir, f"{name}.jpg"))

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch1_data:
            p.update(batch1_data[pid])
            updated_count += 1
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Sony Batch 1 Update Complete. Updated: {updated_count}")

if __name__ == "__main__":
    sony_v2_batch1()
