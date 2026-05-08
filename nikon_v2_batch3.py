import json
import os

def nikon_v2_batch3():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次三採集數據
    batch3_data = {
        "nikon-z-24mm-f-1-8-s": {
            "opticalDesign": "12 elements in 10 groups (1 ED, 4 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "Dual STM (Multi-focus system)",
            "coating": "Nano Crystal, Super Integrated (SIC)",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.25m",
            "filterSize": "72mm",
            "dimensions": "ø75 x 96.5 mm",
            "launchPrice": 31900
        },
        "nikon-z-dx-16-50mm-f-3-5-6-3-vr": {
            "opticalDesign": "9 elements in 7 groups (1 ED, 4 aspherical)",
            "minAperture": "f/22 - f/40",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated (SIC)",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.2m",
            "filterSize": "46mm",
            "dimensions": "ø70 x 32 mm",
            "launchPrice": 9900
        },
        "nikon-z-dx-50-250mm-f-4-5-6-3-vr": {
            "opticalDesign": "16 elements in 12 groups (1 ED)",
            "minAperture": "f/22 - f/32",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Super Integrated (SIC)",
            "maxMagnification": "0.23x",
            "minFocusDistance": "0.5m",
            "filterSize": "62mm",
            "dimensions": "ø74 x 110 mm",
            "launchPrice": 11800
        },
        "nikon-z-50mm-f-1-8-s": {
            "opticalDesign": "12 elements in 9 groups (2 ED, 2 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Nano Crystal, Super Integrated (SIC)",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.4m",
            "filterSize": "62mm",
            "dimensions": "ø75 x 86.5 mm",
            "launchPrice": 20400
        },
        "nikon-z-35mm-f-1-8-s": {
            "opticalDesign": "11 elements in 9 groups (2 ED, 3 aspherical)",
            "minAperture": "f/16",
            "focusMotor": "Dual STM (Multi-focus system)",
            "coating": "Nano Crystal, Super Integrated (SIC)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.25m",
            "filterSize": "62mm",
            "dimensions": "ø73 x 86 mm",
            "launchPrice": 29000
        },
        "nikon-z-24-70mm-f-4-s": {
            "opticalDesign": "14 elements in 11 groups (1 ED, 1 aspherical ED, 3 aspherical)",
            "minAperture": "f/22",
            "focusMotor": "STM (Stepping Motor)",
            "coating": "Nano Crystal, Fluorine, SIC",
            "maxMagnification": "0.3x",
            "minFocusDistance": "0.3m",
            "filterSize": "72mm",
            "dimensions": "ø77.5 x 88.5 mm",
            "launchPrice": 26500
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch3_data:
            p.update(batch3_data[pid])
            updated_count += 1
            
    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Nikon V2.0 Batch 3 Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    nikon_v2_batch3()
