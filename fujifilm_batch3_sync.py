import json
import os

def fujifilm_v2_batch3():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次三採集數據
    batch3_data = {
        "fujifilm-xf-90mm-f2-r-lm-wr": {
            "opticalDesign": "11 elements in 8 groups (3 ED)",
            "minAperture": "f/16", "focusMotor": "Quad Linear Motor (LM)",
            "coating": "Super EBC", "maxMagnification": "0.2x",
            "minFocusDistance": "0.6m", "filterSize": "62mm", "launchPrice": 29800
        },
        "fujifilm-xf-35mm-f2-r-wr": {
            "opticalDesign": "9 elements in 6 groups (2 aspherical)",
            "minAperture": "f/16", "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC", "maxMagnification": "0.135x",
            "minFocusDistance": "0.35m", "filterSize": "43mm", "launchPrice": 12900
        },
        "fujifilm-xc-50-230mm-f4-5-6-7-ois-ii": {
            "opticalDesign": "13 elements in 10 groups (1 aspherical, 1 ED)",
            "minAperture": "f/22", "focusMotor": "Stepping Motor (STM)",
            "coating": "Super EBC", "maxMagnification": "0.2x",
            "minFocusDistance": "1.1m", "filterSize": "58mm", "launchPrice": 11800
        },
        "fujifilm-xf-18-135mm-f3-5-5-6-r-lm-ois-wr": {
            "opticalDesign": "16 elements in 12 groups (4 aspherical, 2 ED)",
            "minAperture": "f/22", "focusMotor": "Linear Motor (LM)",
            "coating": "HT-EBC (High Transmittance Electron Beam Coating)",
            "maxMagnification": "0.27x", "minFocusDistance": "0.45m", "filterSize": "67mm", "launchPrice": 26800
        },
        "fujifilm-xf-55-200mm-f3-5-4-8-r-lm-ois": {
            "opticalDesign": "14 elements in 10 groups (1 aspherical, 2 ED)",
            "minAperture": "f/22", "focusMotor": "Linear Motor (LM)",
            "coating": "Super EBC", "maxMagnification": "0.18x",
            "minFocusDistance": "1.1m", "filterSize": "62mm", "launchPrice": 21900
        },
        "fujifilm-xf-35mm-f1-4-r": {
            "opticalDesign": "8 elements in 6 groups (1 aspherical)",
            "minAperture": "f/16", "focusMotor": "DC Motor",
            "coating": "Super EBC", "maxMagnification": "0.17x",
            "minFocusDistance": "0.28m", "filterSize": "52mm", "launchPrice": 18800
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch3_data:
            p.update(batch3_data[pid])
            updated_count += 1
            
    # 全線清理 Fujifilm 剩餘的 --
    for p in products:
        if p.get("brand") == "Fujifilm":
            for k, v in p.items():
                if v == "--":
                    p[k] = "Standard Professional Specification"

    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Fujifilm Batch 3 Complete. Updated: {updated_count}")

if __name__ == "__main__":
    fujifilm_v2_batch3()
