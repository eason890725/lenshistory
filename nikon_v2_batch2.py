import json
import os

def nikon_v2_batch2():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次二採集數據
    batch2_data = {
        "nikon-z-28-75mm-f-2-8": {
            "opticalDesign": "15 elements in 12 groups (1 Super ED, 1 ED, 3 aspherical)",
            "minAperture": "f/22",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.34x",
            "minFocusDistance": "0.19m",
            "filterSize": "67mm",
            "dimensions": "ø75 x 120.5 mm",
            "launchPrice": 33500
        },
        "nikon-z-24-200mm-f-4-6-3-vr": {
            "opticalDesign": "19 elements in 15 groups (2 ED, 1 aspherical ED, 2 aspherical)",
            "minAperture": "f/22 - f/36",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "ARNEO, Fluorine",
            "maxMagnification": "0.28x",
            "minFocusDistance": "0.5m",
            "filterSize": "67mm",
            "dimensions": "ø76.5 x 114 mm",
            "launchPrice": 32000
        },
        "nikon-z-20mm-f-1-8-s": {
            "opticalDesign": "14 elements in 11 groups (3 ED, 3 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "Dual STM (Multi-focus system)",
            "coating": "Nano Crystal, Fluorine",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.20m",
            "filterSize": "77mm",
            "dimensions": "ø84.5 x 108.5 mm",
            "launchPrice": 35900
        },
        "nikon-z-24-50mm-f-4-6-3": {
            "opticalDesign": "11 elements in 10 groups (2 ED, 3 aspherical)",
            "minAperture": "f/22 - f/36",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated Coating (SIC)",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.35m",
            "filterSize": "52mm",
            "dimensions": "ø73.5 x 51 mm",
            "launchPrice": 13500
        },
        "nikon-z-14-30mm-f-4-s": {
            "opticalDesign": "14 elements in 12 groups (4 ED, 4 aspherical)",
            "minAperture": "f/22",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Nano Crystal, Fluorine",
            "maxMagnification": "0.16x",
            "minFocusDistance": "0.28m",
            "filterSize": "82mm",
            "dimensions": "ø89 x 85 mm",
            "launchPrice": 41900
        },
        "nikon-z-85mm-f-1-8-s": {
            "opticalDesign": "12 elements in 8 groups (2 ED)",
            "minAperture": "f/16",
            "focusMotor": "Dual STM (Multi-focus system)",
            "coating": "Nano Crystal",
            "maxMagnification": "0.12x",
            "minFocusDistance": "0.8m",
            "filterSize": "67mm",
            "dimensions": "ø75 x 99 mm",
            "launchPrice": 30200
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch2_data:
            p.update(batch2_data[pid])
            updated_count += 1
            
    # 數量防呆 (Rule 3)
    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Nikon V2.0 Batch 2 Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    nikon_v2_batch2()
