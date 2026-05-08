import json
import os

def fujifilm_v2_batch2():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次二採集數據 (XF/GF 旗艦與定焦組)
    batch2_data = {
        "fujifilm-xf-8-16mm-f2-8-r-lm-wr": {
            "opticalDesign": "20 elements in 13 groups (4 ASPH, 3 ED, 3 Super ED)",
            "minAperture": "f/22",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Nano-GI, Fluorine",
            "maxMagnification": "0.1x",
            "minFocusDistance": "0.25m",
            "filterSize": "N/A",
            "launchPrice": 58000
        },
        "fujifilm-xf-16-55mm-f2-8-r-lm-wr": {
            "opticalDesign": "17 elements in 12 groups (3 ASPH, 3 ED)",
            "minAperture": "f/22",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Nano-GI, HT-EBC",
            "maxMagnification": "0.16x",
            "minFocusDistance": "0.3m",
            "filterSize": "77mm",
            "launchPrice": 33000
        },
        "fujifilm-xf-16-55mm-f2-8-r-lm-wr-ii": {
            "opticalDesign": "16 elements in 11 groups (4 ASPH, 3 ED, 1 Super ED)",
            "minAperture": "f/22",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.21x",
            "minFocusDistance": "0.3m",
            "filterSize": "72mm",
            "launchPrice": 38900
        },
        "fujifilm-xf-50-140mm-f2-8-r-lm-ois-wr": {
            "opticalDesign": "23 elements in 16 groups (5 ED, 1 Super ED)",
            "minAperture": "f/22",
            "focusMotor": "Triple Linear Motor (LM)",
            "coating": "Nano-GI, HT-EBC",
            "maxMagnification": "0.12x",
            "minFocusDistance": "1.0m",
            "filterSize": "72mm",
            "launchPrice": 42000
        },
        "fujifilm-xf-10-24mm-f4-r-ois-wr": {
            "opticalDesign": "14 elements in 10 groups (4 ASPH, 4 ED)",
            "minAperture": "f/22",
            "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.16x",
            "minFocusDistance": "0.24m",
            "filterSize": "72mm",
            "launchPrice": 28300
        },
        "fujifilm-xf-18-55mm-f2-8-4-r-lm-ois": {
            "opticalDesign": "14 elements in 10 groups (3 ASPH, 1 ED)",
            "minAperture": "f/22",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.3m",
            "filterSize": "58mm",
            "launchPrice": 12000
        },
        "fujifilm-xf-18mm-f1-4-r-lm-wr": {
            "opticalDesign": "15 elements in 9 groups (3 ASPH, 1 Super ED)",
            "minAperture": "f/16",
            "focusMotor": "Linear Motor (LM)",
            "coating": "HT-EBC",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.2m",
            "filterSize": "62mm",
            "launchPrice": 26000
        },
        "fujifilm-xf-23mm-f1-4-r-lm-wr": {
            "opticalDesign": "15 elements in 10 groups (2 ASPH, 3 ED)",
            "minAperture": "f/16",
            "focusMotor": "Linear Motor (LM)",
            "coating": "HT-EBC",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.19m",
            "filterSize": "58mm",
            "launchPrice": 24500
        },
        "fujifilm-xf-33mm-f1-4-r-lm-wr": {
            "opticalDesign": "15 elements in 10 groups (2 ASPH, 3 ED)",
            "minAperture": "f/16",
            "focusMotor": "Linear Motor (LM)",
            "coating": "HT-EBC",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.3m",
            "filterSize": "58mm",
            "launchPrice": 23300
        },
        "fujifilm-xf-35mm-f1-4-r": {
            "opticalDesign": "8 elements in 6 groups (1 ASPH)",
            "minAperture": "f/16",
            "focusMotor": "DC Motor",
            "coating": "Super EBC",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.28m",
            "filterSize": "52mm",
            "launchPrice": 16500
        },
        "fujifilm-xf-56mm-f1-2-r-wr": {
            "opticalDesign": "13 elements in 8 groups (2 ASPH, 1 ED)",
            "minAperture": "f/16",
            "focusMotor": "High-torque DC Motor",
            "coating": "HT-EBC, Fluorine",
            "maxMagnification": "0.14x",
            "minFocusDistance": "0.5m",
            "filterSize": "67mm",
            "launchPrice": 31000
        },
        "fujifilm-xf-90mm-f2-r-lm-wr": {
            "opticalDesign": "11 elements in 8 groups (3 ED)",
            "minAperture": "f/16",
            "focusMotor": "Quad Linear Motor (LM)",
            "coating": "Super EBC",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.6m",
            "filterSize": "62mm",
            "launchPrice": 26000
        },
        "fujifilm-gf-32-64mm-f4-r-lm-wr": {
            "opticalDesign": "14 elements in 11 groups (3 ASPH, 1 ED, 1 Super ED)",
            "minAperture": "f/32",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.12x",
            "minFocusDistance": "0.5m",
            "filterSize": "77mm",
            "launchPrice": 68000
        },
        "fujifilm-gf-45-100mm-f4-r-lm-ois-wr": {
            "opticalDesign": "16 elements in 12 groups (3 ASPH, 1 ED, 1 Super ED)",
            "minAperture": "f/32",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.13x",
            "minFocusDistance": "0.65m",
            "filterSize": "82mm",
            "launchPrice": 68000
        },
        "fujifilm-gf-80mm-f1-7-r-wr": {
            "opticalDesign": "12 elements in 9 groups (1 ASPH, 2 Super ED)",
            "minAperture": "f/22",
            "focusMotor": "High-torque DC Motor",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.7m",
            "filterSize": "77mm",
            "launchPrice": 64000
        },
        "fujifilm-gf-110mm-f2-r-lm-wr": {
            "opticalDesign": "14 elements in 9 groups (4 ED)",
            "minAperture": "f/22",
            "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC, Fluorine",
            "maxMagnification": "0.16x",
            "minFocusDistance": "0.9m",
            "filterSize": "77mm",
            "launchPrice": 82000
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch2_data:
            p.update(batch2_data[pid])
            updated_count += 1
            
    # 數量防呆
    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Fujifilm V2.0 Batch 2 Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    fujifilm_v2_batch2()
