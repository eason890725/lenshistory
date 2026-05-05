import json
import os

def force_persistence_v22():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # Canon 機身物理規格與別名庫
    canon_physics = {
        "eos-r1": {
            "weightGrams": "Approx. 922 g (including battery and card)",
            "dimensions": "157.6 x 149.5 x 87.3 mm",
            "aliases": ["R1", "EOSR1", "CanonR1"]
        },
        "eos-r3": {
            "weightGrams": "Approx. 1015 g (including battery and card)",
            "dimensions": "150.0 x 142.6 x 87.2 mm",
            "aliases": ["R3", "EOSR3", "CanonR3"]
        },
        "eos-r5-ii": {
            "weightGrams": "Approx. 746 g (including battery and card)",
            "dimensions": "138.5 x 101.2 x 93.5 mm",
            "aliases": ["R5II", "R5MarkII", "EOSR5II"]
        },
        "eos-r5": {
            "weightGrams": "Approx. 738 g (including battery and card)",
            "dimensions": "138.5 x 97.5 x 88.0 mm",
            "aliases": ["R5", "EOSR5"]
        },
        "eos-r6-ii": {
            "weightGrams": "Approx. 670 g (including battery and card)",
            "dimensions": "138.4 x 98.4 x 88.4 mm",
            "aliases": ["R6II", "R6MarkII", "EOSR6II"]
        },
        "eos-r6": {
            "weightGrams": "Approx. 680 g (including battery and card)",
            "dimensions": "138.4 x 97.5 x 88.4 mm",
            "aliases": ["R6", "EOSR6"]
        },
        "eos-r8": {
            "weightGrams": "Approx. 461 g (including battery and card)",
            "dimensions": "132.5 x 86.1 x 70.0 mm",
            "aliases": ["R8", "EOSR8"]
        },
        "eos-r": {
            "weightGrams": "Approx. 660 g (including battery and card)",
            "dimensions": "135.8 x 98.3 x 84.4 mm",
            "aliases": ["EOSR", "CanonR"]
        },
        "eos-rp": {
            "weightGrams": "Approx. 485 g (including battery and card)",
            "dimensions": "132.5 x 85.0 x 70.0 mm",
            "aliases": ["EOSRP", "CanonRP"]
        }
    }

    modified_count = 0
    for item in products:
        item_id = item.get('id', '')
        if item_id in canon_physics:
            specs = canon_physics[item_id]
            for key, val in specs.items():
                item[key] = val
                modified_count += 1
        
        # Sony A7C II 命名與別名校驗
        if item_id == "a7c-ii":
            item['modelName'] = "Sony Alpha 7C II"
            if "A7C2" not in item.get('aliases', []):
                item['aliases'] = item.get('aliases', []) + ["A7C2", "A7CII"]
                modified_count += 1

    # 強制完全覆蓋寫入
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"FORCE_WRITE_BACK_COMPLETE: Modified {modified_count} fields in products.json.")

if __name__ == "__main__":
    force_persistence_v22()
