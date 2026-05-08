import json
import os

def nikon_19_lens_final_sync():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 物理規格大數據 (V59.3 Harvested Data)
    final_19_lens_specs = {
        "nikon-z-180-600mm-f-5-6-6-3-vr": {
            "opticalDesign": "25 elements in 17 groups (6 ED, 1 aspherical)",
            "maxMagnification": "0.25x",
            "minFocusDistance": "1.3m",
            "filterSize": "95mm",
            "dimensions": "ø110 x 315.5 mm",
            "coating": "Fluorine Coating",
            "launchPrice": 57880
        },
        "nikon-z-26mm-f-2-8": {
            "opticalDesign": "8 elements in 6 groups (3 aspherical)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.2m",
            "filterSize": "52mm (via HB-111)",
            "dimensions": "ø70 x 23.5 mm",
            "coating": "Super Integrated (SIC)",
            "launchPrice": 15900
        },
        "nikon-z-dx-12-28mm-f-3-5-5-6-pz-vr": {
            "opticalDesign": "12 elements in 11 groups (1 ED, 1 aspherical)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.19m",
            "filterSize": "67mm",
            "dimensions": "ø72 x 63.5 mm",
            "coating": "Standard SIC",
            "launchPrice": 10990
        },
        "nikon-z-105mm-f-2-8-vr-s-micro": {
            "opticalDesign": "16 elements in 11 groups (3 ED, 1 aspherical)",
            "maxMagnification": "1.0x",
            "minFocusDistance": "0.29m",
            "filterSize": "62mm",
            "dimensions": "ø85 x 140 mm",
            "coating": "Nano Crystal, ARNEO, Fluorine",
            "launchPrice": 34400
        },
        "nikon-z-28mm-f-2-8": {
            "opticalDesign": "9 elements in 8 groups (2 aspherical)",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.19m",
            "filterSize": "52mm",
            "dimensions": "ø70 x 43 mm",
            "coating": "Standard SIC",
            "launchPrice": 9900
        },
        "nikon-z-40mm-f-2": {
            "opticalDesign": "6 elements in 4 groups (2 aspherical)",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.29m",
            "filterSize": "52mm",
            "dimensions": "ø70 x 45.5 mm",
            "coating": "Standard SIC",
            "launchPrice": 8800
        },
        "nikon-z-dx-18-140mm-f-3-5-6-3-vr": {
            "opticalDesign": "17 elements in 13 groups (2 ED, 2 aspherical)",
            "maxMagnification": "0.33x",
            "minFocusDistance": "0.2m",
            "filterSize": "62mm",
            "dimensions": "ø73 x 90 mm",
            "coating": "Standard SIC",
            "launchPrice": 19300
        },
        "nikon-z-28-75mm-f-2-8": {
            "opticalDesign": "15 elements in 12 groups (1 Super ED, 1 ED, 3 aspherical)",
            "maxMagnification": "0.34x",
            "minFocusDistance": "0.19m",
            "filterSize": "67mm",
            "dimensions": "ø75 x 120.5 mm",
            "coating": "Standard SIC",
            "launchPrice": 28900
        },
        "nikon-z-24-200mm-f-4-6-3-vr": {
            "opticalDesign": "19 elements in 15 groups (2 ED, 1 aspherical ED, 2 aspherical)",
            "maxMagnification": "0.28x",
            "minFocusDistance": "0.5m",
            "filterSize": "72mm",
            "dimensions": "ø76.5 x 114 mm",
            "coating": "ARNEO, Fluorine",
            "launchPrice": 28900
        },
        "nikon-z-20mm-f-1-8-s": {
            "opticalDesign": "14 elements in 11 groups (3 ED, 3 aspherical)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.2m",
            "filterSize": "77mm",
            "dimensions": "ø84.5 x 108.5 mm",
            "coating": "Nano Crystal",
            "launchPrice": 31900
        },
        "nikon-z-24-50mm-f-4-6-3": {
            "opticalDesign": "11 elements in 10 groups (2 ED, 3 aspherical)",
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.35m",
            "filterSize": "52mm",
            "dimensions": "ø73.5 x 51 mm",
            "coating": "Standard SIC",
            "launchPrice": 13400
        },
        "nikon-z-14-30mm-f-4-s": {
            "opticalDesign": "14 elements in 12 groups (4 ED, 4 aspherical)",
            "maxMagnification": "0.16x",
            "minFocusDistance": "0.28m",
            "filterSize": "82mm",
            "dimensions": "ø89 x 85 mm",
            "coating": "Nano Crystal, Fluorine",
            "launchPrice": 38400
        },
        "nikon-z-85mm-f-1-8-s": {
            "opticalDesign": "12 elements in 8 groups (2 ED)",
            "maxMagnification": "0.12x",
            "minFocusDistance": "0.8m",
            "filterSize": "67mm",
            "dimensions": "ø75 x 99 mm",
            "coating": "Nano Crystal",
            "launchPrice": 24900
        },
        "nikon-z-24mm-f-1-8-s": {
            "opticalDesign": "12 elements in 10 groups (1 ED, 4 aspherical)",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.25m",
            "filterSize": "72mm",
            "dimensions": "ø75 x 96.5 mm",
            "coating": "Nano Crystal",
            "launchPrice": 31400
        },
        "nikon-z-dx-16-50mm-f-3-5-6-3-vr": {
            "opticalDesign": "9 elements in 7 groups (1 ED, 4 aspherical)",
            "maxMagnification": "0.2x",
            "minFocusDistance": "0.2m",
            "filterSize": "46mm",
            "dimensions": "ø70 x 32 mm",
            "coating": "Standard SIC",
            "launchPrice": 8800
        },
        "nikon-z-dx-50-250mm-f-4-5-6-3-vr": {
            "opticalDesign": "16 elements in 12 groups (1 ED)",
            "maxMagnification": "0.23x",
            "minFocusDistance": "0.5m",
            "filterSize": "62mm",
            "dimensions": "ø74 x 110 mm",
            "coating": "Standard SIC",
            "launchPrice": 10800
        },
        "nikon-z-50mm-f-1-8-s": {
            "opticalDesign": "12 elements in 9 groups (2 ED, 2 aspherical)",
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.4m",
            "filterSize": "62mm",
            "dimensions": "ø75 x 86.5 mm",
            "coating": "Nano Crystal",
            "launchPrice": 17900
        },
        "nikon-z-35mm-f-1-8-s": {
            "opticalDesign": "11 elements in 9 groups (2 ED, 3 aspherical)",
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.25m",
            "filterSize": "62mm",
            "dimensions": "ø73 x 86 mm",
            "coating": "Nano Crystal",
            "launchPrice": 24400
        },
        "nikon-z-24-70mm-f-4-s": {
            "opticalDesign": "14 elements in 11 groups (1 ED, 1 aspherical ED, 3 aspherical)",
            "maxMagnification": "0.3x",
            "minFocusDistance": "0.3m",
            "filterSize": "72mm",
            "dimensions": "ø77.5 x 88.5 mm",
            "coating": "Nano Crystal, Fluorine",
            "launchPrice": 28400
        }
    }

    updated_count = 0
    for p in products:
        if p.get("brand") == "Nikon":
            pid = p.get("id")
            if pid in final_19_lens_specs:
                p.update(final_19_lens_specs[pid])
                updated_count += 1
            
            # 確保價格為數字
            if "launchPrice" in p and isinstance(p["launchPrice"], str):
                try:
                    p["launchPrice"] = int(p["launchPrice"].replace(",", "").replace("NT$", "").strip())
                except:
                    pass

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Nikon 19 Lenses Final Audit Complete. Updated: {updated_count}")

if __name__ == "__main__":
    nikon_19_lens_final_sync()
