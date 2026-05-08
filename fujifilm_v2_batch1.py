import json
import os

def fujifilm_v2_batch1():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 批次一採集數據 (旗艦機身與 X100 系列)
    batch1_data = {
        "fujifilm-x-h2s": {
            "sensorType": "26.1MP X-Trans CMOS 5 HS (Stacked BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "7.0 stops",
            "weightGrams": "660g",
            "launchPrice": 74900,
            "videoResolution": "6.2K 30p / 4K 120p",
            "hasIBIS": True
        },
        "fujifilm-x-h2": {
            "sensorType": "40.2MP X-Trans CMOS 5 HR (BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "7.0 stops",
            "weightGrams": "660g",
            "launchPrice": 56900,
            "videoResolution": "8K 30p / 4K 60p",
            "hasIBIS": True
        },
        "fujifilm-x-t5": {
            "sensorType": "40.2MP X-Trans CMOS 5 HR (BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "7.0 stops",
            "weightGrams": "557g",
            "launchPrice": 52900,
            "videoResolution": "6.2K 30p / 4K 60p",
            "hasIBIS": True
        },
        "fujifilm-x-t50": {
            "sensorType": "40.2MP X-Trans CMOS 5 HR (BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "7.0 stops",
            "weightGrams": "438g",
            "launchPrice": 43900,
            "videoResolution": "6.2K 30p / 4K 60p",
            "hasIBIS": True
        },
        "fujifilm-x-s20": {
            "sensorType": "26.1MP X-Trans CMOS 4 (BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "7.0 stops",
            "weightGrams": "491g",
            "launchPrice": 39900,
            "videoResolution": "6.2K 30p / 4K 60p",
            "hasIBIS": True
        },
        "fujifilm-x100vi": {
            "sensorType": "40.2MP X-Trans CMOS 5 HR (BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "6.0 stops",
            "weightGrams": "521g",
            "launchPrice": 51800,
            "videoResolution": "6.2K 30p",
            "hasIBIS": True
        },
        "fujifilm-gfx-100-ii": {
            "sensorType": "102MP GFX CMOS II HS (Medium Format Stacked)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "8.0 stops",
            "weightGrams": "1030g",
            "launchPrice": 225000,
            "videoResolution": "8K 30p / 4K 60p",
            "hasIBIS": True
        },
        "fujifilm-gfx-100s-ii": {
            "sensorType": "102MP GFX CMOS II (Medium Format BSI)",
            "afTargets": "Human (Face/Eye), Animal, Bird, Car, Motorcycle, Bicycle, Airplane, Train",
            "ibisRating": "8.0 stops",
            "weightGrams": "883g",
            "launchPrice": 169000,
            "videoResolution": "4K 60p",
            "hasIBIS": True
        },
        "fujifilm-x-pro3": {
            "sensorType": "26.1MP X-Trans CMOS 4 (BSI)",
            "afTargets": "Human (Face/Eye)",
            "ibisRating": "No IBIS",
            "weightGrams": "497g",
            "launchPrice": 54900,
            "hasIBIS": False
        },
        "fujifilm-x100v": {
            "sensorType": "26.1MP X-Trans CMOS 4 (BSI)",
            "afTargets": "Human (Face/Eye)",
            "ibisRating": "No IBIS",
            "weightGrams": "478g",
            "launchPrice": 41900,
            "hasIBIS": False
        }
    }

    updated_count = 0
    for p in products:
        pid = p.get("id")
        if pid in batch1_data:
            p.update(batch1_data[pid])
            updated_count += 1
            
    # 數量防呆 (Rule 3)
    if len(products) < 230:
        return False

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Fujifilm V2.0 Batch 1 Complete. Updated: {updated_count}")
    return True

if __name__ == "__main__":
    fujifilm_v2_batch1()
