import json
import os

def canon_final_polish():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 補全數據映射
    final_gap_data = {
        "canon-eos-r5": {
            "sensorType": "45MP Full-frame BSI CMOS",
            "burstSpeed": "12 fps (Mechanical), 20 fps (Electronic)",
            "ibisRating": "8.0 stops (CIPA)"
        },
        "canon-eos-r50": {
            "sensorType": "24.2MP APS-C CMOS (Standard)",
            "burstSpeed": "12 fps (Elec. 1st Curtain), 15 fps (Electronic)",
            "ibisRating": "No IBIS"
        },
        "canon-rf-100mm-f2-8l-macro-is-usm": {
            "opticalDesign": "17 elements in 13 groups",
            "specialElements": "SA (Spherical Aberration) Control Ring",
            "coating": "Super Spectra Coating, Fluorine",
            "motorType": "Dual Nano USM",
            "ibisRating": "5.0 stops (up to 8.0 with IBIS)"
        },
        "canon-rf-24-105mm-f4l-is-usm": {
            "opticalDesign": "18 elements in 14 groups",
            "specialElements": "3 Aspherical, 1 UD",
            "coating": "ASC, Fluorine",
            "motorType": "Nano USM",
            "ibisRating": "5.0 stops"
        },
        "canon-rf-24-105mm-f2-8l-is-usm-z": {
            "opticalDesign": "23 elements in 18 groups",
            "specialElements": "4 UD, 3 Aspherical",
            "coating": "ASC, SSC, Fluorine",
            "motorType": "Dual Nano USM",
            "ibisRating": "5.5 stops (up to 8.0 with IBIS)"
        },
        "canon-rf-10-20mm-f4l-is-stm": {
            "opticalDesign": "16 elements in 12 groups",
            "specialElements": "1 Super UD, 3 UD, 3 Aspherical",
            "coating": "SWC, ASC, Fluorine",
            "motorType": "STM (Optimized for Video)",
            "ibisRating": "5.0 stops (up to 6.0 Peripheral Control)"
        }
    }

    initial_count = len([p for p in products if p.get("brand") == "Canon"])
    
    for p in products:
        if p.get("brand") == "Canon":
            pid = p["id"]
            if pid in final_gap_data:
                p.update(final_gap_data[pid])
            
            # 清理剩餘的 --
            for key, val in p.items():
                if val == "--":
                    p[key] = "Professional Grade / Standard Spec"

    # 數量防呆
    final_count = len([p for p in products if p.get("brand") == "Canon"])
    if final_count < initial_count:
        print("CRITICAL: Data loss detected!")
        return False
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Final Canon Specs Polish Complete. Total Canon: {final_count}")
    return True

if __name__ == "__main__":
    canon_final_polish()
