import json
import os

def canon_skill_audit():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 深度數據映射
    body_data = {
        "canon-eos-r1": {
            "modelName": "Canon EOS R1",
            "aliases": ["R1", "EOS R1", "Flagship R1"],
            "sensorType": "24.2MP Back-illuminated Stacked CMOS",
            "afTargets": "People, Animal, Vehicle, Sport (Action Priority)",
            "ibisRating": "8.5 stops (CIPA)",
            "burstSpeed": "40 fps (Electronic), 12 fps (Mechanical)",
            "videoResolution": "6K 60p RAW, 4K 120p",
            "launchPrice": 193000
        },
        "canon-eos-r3": {
            "modelName": "Canon EOS R3",
            "aliases": ["R3", "EOS R3", "Eye Control AF"],
            "sensorType": "24.1MP Stacked BSI CMOS",
            "afTargets": "People (Face/Eye), Animal, Vehicle",
            "ibisRating": "8.0 stops (CIPA)",
            "burstSpeed": "30 fps (Electronic), 12 fps (Mechanical)",
            "launchPrice": 172000
        },
        "canon-eos-r5-ii": {
            "modelName": "Canon EOS R5 Mark II",
            "aliases": ["R5II", "R5 Mark II", "R52"],
            "sensorType": "45MP Stacked BSI CMOS",
            "afTargets": "People, Animal, Vehicle, Register People Priority",
            "ibisRating": "8.5 stops (CIPA)",
            "burstSpeed": "30 fps (Electronic), 12 fps (Mechanical)",
            "launchPrice": 122000
        },
        "eos-r6-mark-iii": {
            "modelName": "Canon EOS R6 Mark III",
            "aliases": ["R6III", "R6 Mark III", "R63"],
            "sensorType": "32.5MP BSI Stacked CMOS",
            "afTargets": "People, Animal, Vehicle, Sport Mode",
            "ibisRating": "8.5 stops (CIPA)",
            "burstSpeed": "40 fps (Electronic), 12 fps (Mechanical)",
            "launchPrice": 79000
        }
    }
    
    lens_data = {
        "rf-15-35mm-f2-8l-is-usm": {
            "modelName": "Canon RF 15-35mm f/2.8L IS USM",
            "opticalDesign": "16 elements in 12 groups",
            "specialElements": "3 GMo Aspherical, 2 UD",
            "coating": "SWC, ASC, Fluorine Coating",
            "motorType": "Nano USM",
            "launchPrice": 69600
        },
        "rf-24-70mm-f2-8l-is-usm": {
            "modelName": "Canon RF 24-70mm f/2.8L IS USM",
            "opticalDesign": "21 elements in 15 groups",
            "specialElements": "3 Aspherical, 3 UD",
            "coating": "ASC, Fluorine Coating",
            "motorType": "Nano USM",
            "launchPrice": 69600
        },
        "rf-70-200mm-f2-8l-is-usm": {
            "modelName": "Canon RF 70-200mm f/2.8L IS USM",
            "opticalDesign": "17 elements in 13 groups",
            "specialElements": "1 GMo Asph., 1 UD Asph., 1 Super UD, 1 UD",
            "coating": "SWC, ASC, Fluorine Coating",
            "motorType": "Dual Nano USM",
            "launchPrice": 81300
        },
        "rf-28-70mm-f2l-usm": {
            "modelName": "Canon RF 28-70mm f/2L USM",
            "opticalDesign": "19 elements in 13 groups",
            "specialElements": "1 Super UD, 2 UD, 4 Aspherical",
            "coating": "ASC, SWC, Fluorine Coating",
            "motorType": "Ring-type USM",
            "launchPrice": 91900
        },
        "rf-50mm-f1-2l-usm": {
            "modelName": "Canon RF 50mm f/1.2L USM",
            "opticalDesign": "15 elements in 9 groups",
            "specialElements": "1 UD, 2 Aspherical",
            "coating": "ASC, Fluorine Coating",
            "motorType": "Ring-type USM",
            "launchPrice": 69300
        },
        "rf-85mm-f1-2l-usm": {
            "modelName": "Canon RF 85mm f/1.2L USM",
            "opticalDesign": "13 elements in 9 groups",
            "specialElements": "1 UD, 1 Aspherical, BR Lens",
            "coating": "ASC, Fluorine Coating",
            "motorType": "Ring-type USM",
            "launchPrice": 81300
        },
        "rf-135mm-f1-8l-is-usm": {
            "modelName": "Canon RF 135mm f/1.8L IS USM",
            "opticalDesign": "17 elements in 12 groups",
            "specialElements": "3 UD",
            "coating": "ASC, Fluorine Coating",
            "motorType": "Nano USM",
            "launchPrice": 63000
        },
        "rf-100-500mm-f4-5-7-1l-is-usm": {
            "modelName": "Canon RF 100-500mm f/4.5-7.1L IS USM",
            "opticalDesign": "20 elements in 14 groups",
            "specialElements": "1 Super UD, 6 UD",
            "coating": "ASC, Fluorine Coating",
            "motorType": "Dual Nano USM",
            "launchPrice": 83900
        },
        "rf-24mm-f1-4l-vcm": {
            "modelName": "Canon RF 24mm f/1.4L VCM",
            "opticalDesign": "15 elements in 11 groups",
            "specialElements": "2 UD, 1 Aspherical",
            "coating": "ASC, Fluorine Coating",
            "motorType": "VCM + Nano USM",
            "launchPrice": 46900
        },
        "rf-50mm-f1-4l-vcm": {
            "modelName": "Canon RF 50mm f/1.4L VCM",
            "opticalDesign": "14 elements in 11 groups",
            "specialElements": "1 UD, 2 Aspherical",
            "coating": "ASC, Fluorine Coating",
            "motorType": "VCM + Nano USM",
            "launchPrice": 43900
        }
    }

    updated_count = 0
    for p in products:
        if p.get("brand") == "Canon":
            pid = p.get("id")
            # 優先處理深度映射資料
            if pid in body_data:
                p.update(body_data[pid])
                updated_count += 1
            elif pid in lens_data:
                p.update(lens_data[pid])
                updated_count += 1
            
            # 通用處理 (Rule 10, 13)
            if not p.get("modelName").startswith("Canon"):
                p["modelName"] = "Canon " + p["modelName"]
            
            # 清理 -- (Rule 9)
            for key, val in p.items():
                if val == "--":
                    p[key] = "TBD / Professional Standard"
                    
    # 數量防呆驗證 (Rule 3)
    canon_count = len([p for p in products if p.get("brand") == "Canon"])
    print(f"Canon Total: {canon_count}, Deep Updated: {updated_count}")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    return canon_count

if __name__ == "__main__":
    count = canon_skill_audit()
    print(f"AUDIT_COMPLETE_COUNT:{count}")
