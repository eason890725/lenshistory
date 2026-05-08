import json
import os

def canon_physical_sync():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 物理規格大數據 (L-Series & Consumer)
    physical_specs = {
        "canon-rf-15-35mm-f2-8l-is-usm": {
            "maxMagnification": "0.21x",
            "minFocusDistance": "0.28m",
            "filterSize": "82mm",
            "dimensions": "ø88.5 x 126.8 mm",
            "coating": "SWC, ASC, Fluorine"
        },
        "canon-rf-24-70mm-f2-8l-is-usm": {
            "maxMagnification": "0.30x",
            "minFocusDistance": "0.21m",
            "filterSize": "82mm",
            "dimensions": "ø88.5 x 125.7 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-70-200mm-f2-8l-is-usm": {
            "maxMagnification": "0.23x",
            "minFocusDistance": "0.70m",
            "filterSize": "77mm",
            "dimensions": "ø89.9 x 146.0 mm",
            "coating": "SWC, ASC, Fluorine"
        },
        "canon-rf-28-70mm-f2l-usm": {
            "maxMagnification": "0.18x",
            "minFocusDistance": "0.39m",
            "filterSize": "95mm",
            "dimensions": "ø103.8 x 139.8 mm",
            "coating": "ASC, SWC, Fluorine"
        },
        "canon-rf-50mm-f1-2l-usm": {
            "maxMagnification": "0.19x",
            "minFocusDistance": "0.40m",
            "filterSize": "77mm",
            "dimensions": "ø89.8 x 108.0 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-85mm-f1-2l-usm": {
            "maxMagnification": "0.12x",
            "minFocusDistance": "0.85m",
            "filterSize": "82mm",
            "dimensions": "ø103.2 x 117.3 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-135mm-f1-8l-is-usm": {
            "maxMagnification": "0.26x",
            "minFocusDistance": "0.70m",
            "filterSize": "82mm",
            "dimensions": "ø89.2 x 130.3 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-100mm-f2-8l-macro-is-usm": {
            "maxMagnification": "1.4x",
            "minFocusDistance": "0.26m",
            "filterSize": "67mm",
            "dimensions": "ø81.5 x 148.0 mm",
            "coating": "Super Spectra, Fluorine"
        },
        "canon-rf-100-500mm-f4-5-7-1l-is-usm": {
            "maxMagnification": "0.33x",
            "minFocusDistance": "0.90m",
            "filterSize": "77mm",
            "dimensions": "ø93.8 x 207.6 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-24mm-f1-4l-vcm": {
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.24m",
            "filterSize": "67mm",
            "dimensions": "ø76.5 x 99.3 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-50mm-f1-4l-vcm": {
            "maxMagnification": "0.15x",
            "minFocusDistance": "0.37m",
            "filterSize": "67mm",
            "dimensions": "ø76.5 x 99.3 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-35mm-f-1-4-l-vcm": {
            "maxMagnification": "0.18x",
            "minFocusDistance": "0.28m",
            "filterSize": "67mm",
            "dimensions": "ø76.5 x 99.3 mm",
            "coating": "ASC, Fluorine"
        },
        "canon-rf-16mm-f2-8-stm": {
            "maxMagnification": "0.26x",
            "minFocusDistance": "0.13m",
            "filterSize": "43mm",
            "dimensions": "ø69.2 x 40.1 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-24mm-f1-8-macro-is-stm": {
            "maxMagnification": "0.50x",
            "minFocusDistance": "0.14m",
            "filterSize": "52mm",
            "dimensions": "ø74.4 x 63.1 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-28mm-f2-8-stm": {
            "maxMagnification": "0.17x",
            "minFocusDistance": "0.23m",
            "filterSize": "55mm",
            "dimensions": "ø69.2 x 24.7 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-35mm-f1-8-macro-is-stm": {
            "maxMagnification": "0.50x",
            "minFocusDistance": "0.17m",
            "filterSize": "52mm",
            "dimensions": "ø74.4 x 62.8 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-50mm-f1-8-stm": {
            "maxMagnification": "0.25x",
            "minFocusDistance": "0.30m",
            "filterSize": "43mm",
            "dimensions": "ø69.2 x 40.5 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-100-400mm-f5-6-8-is-usm": {
            "maxMagnification": "0.41x",
            "minFocusDistance": "0.88m",
            "filterSize": "67mm",
            "dimensions": "ø79.5 x 164.7 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-600mm-f11-is-stm": {
            "maxMagnification": "0.14x",
            "minFocusDistance": "4.50m",
            "filterSize": "82mm",
            "dimensions": "ø93.0 x 199.5 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-800mm-f11-is-stm": {
            "maxMagnification": "0.14x",
            "minFocusDistance": "6.00m",
            "filterSize": "95mm",
            "dimensions": "ø101.6 x 281.8 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-24-105mm-f4-7-1-is-stm": {
            "maxMagnification": "0.4x (AF) / 0.5x (MF)",
            "minFocusDistance": "0.20m (AF) / 0.13m (MF)",
            "filterSize": "67mm",
            "dimensions": "ø76.6 x 88.8 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-s-18-45mm-f4-5-6-3-is-stm": {
            "maxMagnification": "0.16x (AF) / 0.26x (MF)",
            "minFocusDistance": "0.20m (AF) / 0.15m (MF)",
            "filterSize": "49mm",
            "dimensions": "ø69.0 x 44.3 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-s-10-18mm-f4-5-6-3-is-stm": {
            "maxMagnification": "0.23x (AF) / 0.50x (MF)",
            "minFocusDistance": "0.14m (AF) / 0.086m (MF)",
            "filterSize": "49mm",
            "dimensions": "ø69.0 x 44.9 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-s-18-150mm-f3-5-6-3-is-stm": {
            "maxMagnification": "0.44x (AF) / 0.59x (MF)",
            "minFocusDistance": "0.17m (AF) / 0.12m (MF)",
            "filterSize": "55mm",
            "dimensions": "ø69.0 x 84.5 mm",
            "coating": "Super Spectra (SSC)"
        },
        "canon-rf-s-55-210mm-f5-7-1-is-stm": {
            "maxMagnification": "0.28x",
            "minFocusDistance": "0.73m",
            "filterSize": "55mm",
            "dimensions": "ø69.0 x 92.9 mm",
            "coating": "Super Spectra (SSC)"
        }
    }

    updated_count = 0
    for p in products:
        if p.get("brand") == "Canon":
            pid = p.get("id")
            if pid in physical_specs:
                p.update(physical_specs[pid])
                updated_count += 1
                
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Canon Physical Specs Synced. Updated: {updated_count}")

if __name__ == "__main__":
    canon_physical_sync()
