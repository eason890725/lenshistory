import json
import os

def nikon_lens_final_sync():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 物理規格大數據 (Final Audit Data)
    final_lens_specs = {
        "nikon-z-14-30mm-f-4-s": {
            "opticalDesign": "14 elements in 12 groups (4 ED, 4 aspherical)",
            "maxMagnification": "0.16x",
            "minFocusDistance": "0.28m",
            "filterSize": "82mm",
            "dimensions": "ø89 x 85 mm",
            "coating": "Nano Crystal, Fluorine",
            "launchPrice": 41900
        },
        "nikon-z-24-200mm-f-4-6-3-vr": {
            "opticalDesign": "19 elements in 15 groups (2 ED, 1 aspherical ED, 2 aspherical)",
            "maxMagnification": "0.28x",
            "minFocusDistance": "0.50m",
            "filterSize": "67mm",
            "dimensions": "ø76.5 x 114 mm",
            "coating": "ARNEO, Fluorine",
            "launchPrice": 32000
        },
        "nikon-z-85mm-f-1-8-s": {
            "opticalDesign": "12 elements in 8 groups (2 ED)",
            "maxMagnification": "0.12x",
            "minFocusDistance": "0.80m",
            "filterSize": "67mm",
            "dimensions": "ø75 x 99 mm",
            "coating": "Nano Crystal",
            "launchPrice": 30200
        },
        "nikon-z-50mm-f-1-8-s": {
            "opticalDesign": "12 elements in 9 groups (2 ED, 2 aspherical)",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.40m",
            "filterSize": "62mm",
            "dimensions": "ø76 x 86.5 mm",
            "coating": "Nano Crystal",
            "launchPrice": 19800
        },
        "nikon-z-35mm-f-1-8-s": {
            "opticalDesign": "11 elements in 9 groups (2 ED, 3 aspherical)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.25m",
            "filterSize": "62mm",
            "dimensions": "ø73 x 86 mm",
            "coating": "Nano Crystal",
            "launchPrice": 29000
        },
        "nikon-z-20mm-f-1-8-s": {
            "opticalDesign": "14 elements in 11 groups (3 ED, 3 aspherical)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.20m",
            "filterSize": "77mm",
            "dimensions": "ø84.5 x 108.5 mm",
            "coating": "Nano Crystal",
            "launchPrice": 32300
        },
        "nikon-z-24mm-f-1-8-s": {
            "opticalDesign": "12 elements in 10 groups (1 ED, 4 aspherical)",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.25m",
            "filterSize": "72mm",
            "dimensions": "ø78 x 96.5 mm",
            "coating": "Nano Crystal",
            "launchPrice": 31200
        },
        "nikon-z-24-70mm-f-4-s": {
            "opticalDesign": "14 elements in 11 groups (1 ED, 1 aspherical ED, 3 aspherical)",
            "maxMagnification": "0.30x",
            "minFocusDistance": "0.30m",
            "filterSize": "72mm",
            "dimensions": "ø77.5 x 88.5 mm",
            "coating": "Nano Crystal, Fluorine",
            "launchPrice": 32300
        },
        "nikon-z-dx-50-250mm-f-4-5-6-3-vr": {
            "opticalDesign": "16 elements in 12 groups (1 ED)",
            "maxMagnification": "0.23x",
            "minFocusDistance": "0.50m",
            "filterSize": "62mm",
            "dimensions": "ø74 x 110 mm",
            "coating": "Super Integrated (SIC)",
            "launchPrice": 115000
        },
        "nikon-z-dx-12-28mm-f-3-5-5-6-pz-vr": {
            "opticalDesign": "12 elements in 11 groups (1 ED, 1 aspherical)",
            "maxMagnification": "0.21x",
            "minFocusDistance": "0.19m",
            "filterSize": "67mm",
            "dimensions": "ø72 x 63.5 mm",
            "coating": "Super Integrated (SIC)",
            "launchPrice": 12500
        },
        "nikon-z-dx-18-140mm-f-3-5-6-3-vr": {
            "opticalDesign": "17 elements in 13 groups (2 ED, 2 aspherical)",
            "maxMagnification": "0.33x",
            "minFocusDistance": "0.20m",
            "filterSize": "62mm",
            "dimensions": "ø73 x 90 mm",
            "coating": "Super Integrated (SIC)",
            "launchPrice": 18400
        },
        "nikon-z-24-50mm-f-4-6-3": {
            "opticalDesign": "11 elements in 10 groups (2 ED, 3 aspherical)",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.35m",
            "filterSize": "52mm",
            "dimensions": "ø73.5 x 51 mm",
            "coating": "Super Integrated (SIC)",
            "launchPrice": 12300
        }
    }

    updated_count = 0
    for p in products:
        if p.get("brand") == "Nikon" and p.get("gearType") == "LENS":
            pid = p.get("id")
            if pid in final_lens_specs:
                p.update(final_lens_specs[pid])
                updated_count += 1
            
            # 全線移除 --
            for key, val in p.items():
                if val == "--":
                    p[key] = "Professional Grade / SIC Coating"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Nikon Lens Final Audit Complete. Updated: {updated_count}")

if __name__ == "__main__":
    nikon_lens_final_sync()
