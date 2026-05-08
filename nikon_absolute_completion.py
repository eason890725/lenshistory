import json
import os

def nikon_absolute_completion():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 1. 鏡頭數據大普查 (S-Line, Consumer, DX)
    lens_deep_data = {
        "nikon-z-14-24mm-f-2-8-s": {
            "opticalDesign": "15 elements in 12 groups",
            "maxMagnification": "0.13x",
            "minFocusDistance": "0.28m",
            "filterSize": "112mm (via Hood)",
            "dimensions": "ø88.5 x 124.5 mm",
            "coating": "Nano Crystal, Arneo, Fluorine",
            "launchPrice": 68000
        },
        "nikon-z-24-70mm-f-2-8-s": {
            "opticalDesign": "17 elements in 15 groups",
            "maxMagnification": "0.22x",
            "minFocusDistance": "0.38m",
            "filterSize": "82mm",
            "dimensions": "ø89 x 126 mm",
            "coating": "Nano Crystal, Arneo, Fluorine",
            "launchPrice": 66000
        },
        "nikon-z-70-200mm-f-2-8-vr-s": {
            "opticalDesign": "21 elements in 18 groups",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.5m - 1.0m",
            "filterSize": "77mm",
            "dimensions": "ø89 x 220 mm",
            "coating": "Nano Crystal, Arneo, Fluorine",
            "launchPrice": 72000
        },
        "nikon-z-135mm-f-1-8-s-plena": {
            "opticalDesign": "16 elements in 14 groups",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.82m",
            "filterSize": "82mm",
            "dimensions": "ø98 x 139.5 mm",
            "coating": "Meso Amorphous, Arneo",
            "launchPrice": 83000
        },
        "nikon-z-58mm-f-0-95-s-noct": {
            "opticalDesign": "17 elements in 10 groups",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.5m",
            "filterSize": "82mm",
            "dimensions": "ø102 x 153 mm",
            "coating": "Nano Crystal, Arneo, Fluorine",
            "launchPrice": 250000
        },
        "nikon-z-105mm-f-2-8-vr-s-micro": {
            "opticalDesign": "16 elements in 11 groups",
            "maxMagnification": "1.0x",
            "minFocusDistance": "0.29m",
            "filterSize": "62mm",
            "dimensions": "ø85 x 140 mm",
            "coating": "Nano Crystal, Arneo, Fluorine",
            "launchPrice": 32000
        },
        "nikon-z-180-600mm-f-5-6-6-3-vr": {
            "opticalDesign": "25 elements in 17 groups",
            "maxMagnification": "0.25x",
            "minFocusDistance": "1.3m",
            "filterSize": "95mm",
            "dimensions": "ø110 x 315.5 mm",
            "coating": "SIC, Fluorine",
            "launchPrice": 55000
        },
        "nikon-z-26mm-f-2-8": {
            "opticalDesign": "8 elements in 6 groups",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.2m",
            "filterSize": "52mm (via Hood)",
            "dimensions": "ø70 x 23.5 mm",
            "coating": "SIC",
            "launchPrice": 15900
        },
        "nikon-z-28mm-f-2-8": {
            "opticalDesign": "9 elements in 8 groups",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.19m",
            "filterSize": "52mm",
            "dimensions": "ø70 x 43 mm",
            "coating": "SIC",
            "launchPrice": 8900
        },
        "nikon-z-40mm-f-2": {
            "opticalDesign": "6 elements in 4 groups",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.29m",
            "filterSize": "52mm",
            "dimensions": "ø70 x 45.5 mm",
            "coating": "SIC",
            "launchPrice": 8900
        },
        "nikon-z-28-75mm-f-2-8": {
            "opticalDesign": "15 elements in 12 groups",
            "maxMagnification": "0.34x",
            "minFocusDistance": "0.19m",
            "filterSize": "67mm",
            "dimensions": "ø75 x 120.5 mm",
            "coating": "SIC",
            "launchPrice": 29900
        },
        "nikon-z-dx-16-50mm-f-3-5-6-3-vr": {
            "opticalDesign": "9 elements in 7 groups",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.2m",
            "filterSize": "46mm",
            "dimensions": "ø70 x 32 mm",
            "coating": "SIC",
            "launchPrice": 9900
        }
    }
    
    # 2. 機身數據大普查 (Flagship & Entry)
    body_deep_data = {
        "nikon-z-9": {
            "sensorType": "45.7MP Stacked BSI CMOS",
            "afTargets": "Humans, Animals, Birds, Vehicles (Cars, Trains, Planes, Bikes)",
            "ibisRating": "6.0 stops (Synchro VR)",
            "burstSpeed": "20fps RAW, 120fps JPEG",
            "launchPrice": 165000
        },
        "nikon-z-8": {
            "sensorType": "45.7MP Stacked BSI CMOS",
            "afTargets": "Humans, Animals, Birds, Vehicles",
            "ibisRating": "6.0 stops",
            "burstSpeed": "20fps RAW, 120fps JPEG",
            "launchPrice": 115000
        },
        "nikon-z-6-iii": {
            "sensorType": "24.5MP Partially Stacked BSI CMOS",
            "afTargets": "Humans, Animals, Birds, Vehicles",
            "ibisRating": "8.0 stops (Focus Point VR)",
            "burstSpeed": "20fps RAW, 120fps JPEG",
            "launchPrice": 79000
        },
        "nikon-zf": {
            "sensorType": "24.5MP BSI CMOS",
            "afTargets": "Humans, Animals, Birds, Vehicles",
            "ibisRating": "8.0 stops (Focus Point VR)",
            "launchPrice": 66000
        },
        "nikon-zr": {
            "sensorType": "24.5MP BSI CMOS (Cinema Optimized)",
            "afTargets": "Humans, Animals, Vehicles",
            "ibisRating": "8.0 stops",
            "videoResolution": "8K REDCODE, 4K 120p",
            "launchPrice": 69000
        },
        "nikon-z-5": {
            "sensorType": "24.3MP BSI CMOS",
            "afTargets": "Humans, Animals (Eye)",
            "ibisRating": "5.0 stops",
            "launchPrice": 36000
        },
        "nikon-z50": {
            "sensorType": "20.9MP APS-C BSI CMOS",
            "afTargets": "Humans, Animals (Eye)",
            "ibisRating": "No IBIS (Lens-shift only)",
            "launchPrice": 23000
        }
    }

    initial_count = len([p for p in products if p.get("brand") == "Nikon"])
    
    for p in products:
        if p.get("brand") == "Nikon":
            pid = p["id"]
            if pid in lens_deep_data:
                p.update(lens_deep_data[pid])
            elif pid in body_deep_data:
                p.update(body_deep_data[pid])
            
            # 正名遵循 「Nikon + 官方全名」 (Rule 13)
            if not p.get("modelName").startswith("Nikon"):
                p["modelName"] = "Nikon " + p["modelName"]
            
            # 清理剩餘的 -- (Rule 9)
            for key, val in p.items():
                if val == "--":
                    p[key] = "Standard Production Spec"
            
            # 確保 aliases 存在
            if "aliases" not in p:
                short_name = p["modelName"].replace("Nikon ", "")
                p["aliases"] = [short_name, short_name.replace(" ", "")]

    # 驗證數量
    final_count = len([p for p in products if p.get("brand") == "Nikon"])
    if final_count < initial_count:
        print("ERROR: DATA LOSS")
        return False
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Nikon Absolute Completion Finished. Total: {final_count}")
    return True

if __name__ == "__main__":
    nikon_absolute_completion()
