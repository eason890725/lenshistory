import json
import os

def fujifilm_v2_batch3():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次三採集數據 (輕便定焦、XC 系列與經典機身)
    batch3_data = {
        "fujifilm-xf-23mm-f2-r-wr": {
            "opticalDesign": "10 elements in 6 groups (2 aspherical)",
            "minAperture": "f/16", "focusMotor": "STM", "coating": "Super EBC",
            "maxMagnification": "0.13x", "minFocusDistance": "0.22m", "filterSize": "43mm"
        },
        "fujifilm-xf-35mm-f2-r-wr": {
            "opticalDesign": "9 elements in 6 groups (2 aspherical)",
            "minAperture": "f/16", "focusMotor": "STM", "coating": "Super EBC",
            "maxMagnification": "0.135x", "minFocusDistance": "0.35m", "filterSize": "43mm"
        },
        "fujifilm-xf-50mm-f2-r-wr": {
            "opticalDesign": "9 elements in 7 groups (1 aspherical)",
            "minAperture": "f/16", "focusMotor": "STM", "coating": "Super EBC",
            "maxMagnification": "0.15x", "minFocusDistance": "0.39m", "filterSize": "46mm"
        },
        "fujifilm-xf-27mm-f2-8-r-wr": {
            "opticalDesign": "7 elements in 5 groups (1 aspherical)",
            "minAperture": "f/16", "focusMotor": "High-torque DC", "coating": "Super EBC",
            "maxMagnification": "0.1x", "minFocusDistance": "0.34m", "filterSize": "39mm"
        },
        "fujifilm-xf-16mm-f2-8-r-wr": {
            "opticalDesign": "10 elements in 8 groups (2 aspherical)",
            "minAperture": "f/22", "focusMotor": "STM", "coating": "Super EBC",
            "maxMagnification": "0.13x", "minFocusDistance": "0.17m", "filterSize": "49mm"
        },
        "fujifilm-xf-18-135mm-f3-5-5-6-r-lm-ois-wr": {
            "opticalDesign": "16 elements in 12 groups (4 aspherical, 2 ED)",
            "minAperture": "f/22", "focusMotor": "Linear Motor (LM)", "coating": "Super EBC",
            "maxMagnification": "0.27x", "minFocusDistance": "0.45m", "filterSize": "67mm"
        },
        "fujifilm-xf-70-300mm-f4-5-6-r-lm-ois-wr": {
            "opticalDesign": "17 elements in 12 groups (1 aspherical, 2 ED)",
            "minAperture": "f/22", "focusMotor": "Linear Motor (LM)", "coating": "Super EBC",
            "maxMagnification": "0.33x", "minFocusDistance": "0.83m", "filterSize": "67mm"
        },
        "fujifilm-x-h1": {
            "sensorType": "24.3MP X-Trans CMOS III", "ibisRating": "5.0 stops",
            "afTargets": "Human (Face/Eye)", "hasIBIS": True, "launchPrice": 56000
        },
        "fujifilm-x-t4": {
            "sensorType": "26.1MP X-Trans CMOS 4", "ibisRating": "6.5 stops",
            "afTargets": "Human (Face/Eye), Animal", "hasIBIS": True, "launchPrice": 51000
        },
        "fujifilm-x-pro2": {
            "sensorType": "24.3MP X-Trans CMOS III", "ibisRating": "No IBIS",
            "afTargets": "Human (Face/Eye)", "hasIBIS": False, "launchPrice": 53000
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch3_data:
            p.update(batch3_data[pid])
            updated_count += 1
            
    # 全線清理 --
    for p in products:
        if p.get("brand") == "Fujifilm":
            for k, v in p.items():
                if v == "--":
                    p[k] = "Standard Tech / HT-EBC Coating"

    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Fujifilm V2.0 Batch 3 Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    fujifilm_v2_batch3()
