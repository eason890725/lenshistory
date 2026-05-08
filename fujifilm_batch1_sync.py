import json
import os

def fujifilm_v2_batch1():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次一採集數據
    batch1_data = {
        "fujifilm-xf-23mm-f1-4-r-lm-wr": {
            "opticalDesign": "15 elements in 10 groups (2 aspherical, 3 ED)",
            "minAperture": "f/16",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.19m",
            "filterSize": "58mm",
            "launchPrice": 27300
        },
        "fujifilm-xf-18mm-f1-4-r-lm-wr": {
            "opticalDesign": "15 elements in 9 groups (3 aspherical, 1 ED)",
            "minAperture": "f/16",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.2m",
            "filterSize": "62mm",
            "launchPrice": 28500
        },
        "fujifilm-gf-80mm-f1-7-r-wr": {
            "opticalDesign": "12 elements in 9 groups (1 aspherical, 2 Super ED)",
            "minAperture": "f/22",
            "focusMotor": "High-torque DC Motor",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.7m",
            "filterSize": "77mm",
            "launchPrice": 67000
        },
        "fujifilm-xf-27mm-f2-8-r-wr": {
            "opticalDesign": "7 elements in 5 groups (1 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "High-torque DC Motor",
            "coating": "Super EBC",
            "maxMagnification": "0.1x",
            "minFocusDistance": "0.34m",
            "filterSize": "39mm",
            "launchPrice": 11500
        },
        "fujifilm-xf-70-300mm-f4-5-6-r-lm-ois-wr": {
            "opticalDesign": "17 elements in 12 groups (1 aspherical, 2 ED)",
            "minAperture": "f/22",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.33x",
            "minFocusDistance": "0.83m",
            "filterSize": "67mm",
            "launchPrice": 23000
        },
        "fujifilm-gf-45-100mm-f4-r-lm-ois-wr": {
            "opticalDesign": "16 elements in 12 groups (3 aspherical, 1 Super ED, 1 ED)",
            "minAperture": "f/32",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.13x",
            "minFocusDistance": "0.65m",
            "filterSize": "82mm",
            "launchPrice": 64000
        },
        "fujifilm-xf-16mm-f2-8-r-wr": {
            "opticalDesign": "10 elements in 8 groups (2 aspherical)",
            "minAperture": "f/22",
            "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC",
            "maxMagnification": "0.13x",
            "minFocusDistance": "0.17m",
            "filterSize": "49mm",
            "launchPrice": 11000
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch1_data:
            p.update(batch1_data[pid])
            updated_count += 1
            
    # 數量防呆
    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Fujifilm Batch 1 Update Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    fujifilm_v2_batch1()
