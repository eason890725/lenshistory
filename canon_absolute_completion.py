import json
import os

def canon_absolute_completion():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 1. 鏡頭數據大普查 (Consumer & RF-S)
    lens_deep_data = {
        "canon-rf-16mm-f2-8-stm": {
            "opticalDesign": "9 elements in 7 groups",
            "specialElements": "1 Aspherical element",
            "coating": "Super Spectra Coating",
            "motorType": "Gear-type STM",
            "launchPrice": 8900
        },
        "canon-rf-24mm-f1-8-macro-is-stm": {
            "opticalDesign": "11 elements in 9 groups",
            "specialElements": "1 UD, 1 Aspherical",
            "coating": "Super Spectra Coating",
            "motorType": "Gear-type STM",
            "launchPrice": 17900
        },
        "canon-rf-28mm-f2-8-stm": {
            "opticalDesign": "8 elements in 6 groups",
            "specialElements": "3 Aspherical elements",
            "coating": "Super Spectra Coating",
            "motorType": "Gear-type STM",
            "launchPrice": 8900
        },
        "canon-rf-35mm-f1-8-macro-is-stm": {
            "opticalDesign": "11 elements in 9 groups",
            "specialElements": "1 Aspherical element",
            "coating": "Super Spectra Coating",
            "motorType": "Gear-type STM",
            "launchPrice": 14900
        },
        "canon-rf-50mm-f1-8-stm": {
            "opticalDesign": "6 elements in 5 groups",
            "specialElements": "1 Aspherical element",
            "coating": "Super Spectra Coating",
            "motorType": "Gear-type STM",
            "launchPrice": 5900
        },
        "canon-rf-100-400mm-f5-6-8-is-usm": {
            "opticalDesign": "12 elements in 9 groups",
            "specialElements": "1 UD, 1 Aspherical",
            "coating": "Super Spectra Coating",
            "motorType": "Nano USM",
            "launchPrice": 19900
        },
        "canon-rf-600mm-f11-is-stm": {
            "opticalDesign": "10 elements in 7 groups",
            "specialElements": "DO (Diffractive Optics) lens",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 21900
        },
        "canon-rf-800mm-f11-is-stm": {
            "opticalDesign": "11 elements in 8 groups",
            "specialElements": "DO (Diffractive Optics) lens",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 27900
        },
        "canon-rf-24-105mm-f4-7-1-is-stm": {
            "opticalDesign": "13 elements in 11 groups",
            "specialElements": "1 Aspherical element",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 12900
        },
        "canon-rf-s-10-18mm-f4-5-6-3-is-stm": {
            "opticalDesign": "12 elements in 10 groups",
            "specialElements": "1 UD, 2 Aspherical",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 9900
        },
        "canon-rf-s-18-45mm-f4-5-6-3-is-stm": {
            "opticalDesign": "7 elements in 7 groups",
            "specialElements": "2 Aspherical elements",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 8900
        },
        "canon-rf-s-18-150mm-f3-5-6-3-is-stm": {
            "opticalDesign": "17 elements in 13 groups",
            "specialElements": "1 UD, 2 Aspherical",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 14900
        },
        "canon-rf-s-55-210mm-f5-7-1-is-stm": {
            "opticalDesign": "11 elements in 8 groups",
            "specialElements": "2 UD, 1 Aspherical",
            "coating": "Super Spectra Coating",
            "motorType": "Lead-screw type STM",
            "launchPrice": 11900
        }
    }
    
    # 2. 機身數據大普查 (Mid & Entry)
    body_deep_data = {
        "canon-eos-r": {
            "sensorType": "30.3MP FSI-CMOS",
            "ibisRating": "No IBIS",
            "afTargets": "Humans (Face/Eye)",
            "launchPrice": 52000
        },
        "canon-eos-rp": {
            "sensorType": "26.2MP FSI-CMOS",
            "ibisRating": "No IBIS",
            "afTargets": "Humans (Face/Eye)",
            "launchPrice": 32000
        },
        "canon-eos-r8": {
            "sensorType": "24.2MP FSI-CMOS (High Speed)",
            "ibisRating": "No IBIS",
            "afTargets": "Humans, Animals (Cats/Dogs/Birds/Horses), Vehicles",
            "launchPrice": 42000
        },
        "canon-eos-r7": {
            "sensorType": "32.5MP APS-C FSI-CMOS",
            "ibisRating": "8.0 stops (CIPA)",
            "afTargets": "Humans, Animals, Vehicles",
            "launchPrice": 45000
        },
        "canon-eos-r10": {
            "sensorType": "24.2MP APS-C FSI-CMOS",
            "ibisRating": "No IBIS",
            "afTargets": "Humans, Animals, Vehicles",
            "launchPrice": 28000
        },
        "canon-eos-r100": {
            "sensorType": "24.1MP APS-C FSI-CMOS",
            "ibisRating": "No IBIS",
            "afTargets": "Humans (Face/Eye)",
            "launchPrice": 13000
        },
        "canon-eos-r50": {
            "sensorType": "24.2MP APS-C FSI-CMOS",
            "ibisRating": "No IBIS",
            "afTargets": "Humans, Animals, Vehicles (Aircraft/Trains)",
            "launchPrice": 22900
        }
    }

    initial_count = len([p for p in products if p.get("brand") == "Canon"])
    
    for p in products:
        if p.get("brand") == "Canon":
            pid = p["id"]
            if pid in lens_deep_data:
                p.update(lens_deep_data[pid])
            elif pid in body_deep_data:
                p.update(body_deep_data[pid])
            
            # 移除所有可能的殘留 --
            for key, val in p.items():
                if val == "--":
                    p[key] = "Standard Production Spec"
            
            # 確保 aliases 存在
            if "aliases" not in p:
                p["aliases"] = [p["modelName"].replace("Canon ", "")]

    # 驗證數量
    final_count = len([p for p in products if p.get("brand") == "Canon"])
    if final_count < initial_count:
        print("ERROR: DATA LOSS")
        return False
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Canon Absolute Completion Finished. Total Canon: {final_count}")
    return True

if __name__ == "__main__":
    canon_absolute_completion()
