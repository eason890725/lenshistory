import json
import os

def fix_nikon():
    p_path = 'frontend/src/data/products.json'
    base_dir = 'frontend/public/images/products/nikon'
    
    mapping = {
        'nikon-z-9': 'z9',
        'nikon-z-8': 'z8',
        'nikon-z-7-ii': 'z7-ii',
        'nikon-z-6-iii': 'z6-iii',
        'nikon-z-6-ii': 'z6-ii',
        'nikon-z-5': 'z5',
        'nikon-z-f': 'zf',
        'nikon-z-fc': 'zfc',
        'nikon-z-50': 'z50',
        'nikon-z-30': 'z30'
    }
    
    # 1. Rename files
    for old_id, new_id in mapping.items():
        old_path = os.path.join(base_dir, f"{old_id}.jpg")
        new_path = os.path.join(base_dir, f"{new_id}.jpg")
        if os.path.exists(old_path):
            print(f"Renaming {old_id} -> {new_id}...")
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(old_path, new_path)
            
    # 2. Update JSON
    with open(p_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    count = 0
    for p in data:
        pid = p.get('id')
        for old_id, new_id in mapping.items():
            if pid == new_id:
                p['image_url'] = f"/images/products/nikon/{new_id}.jpg"
                count += 1
                break
                
    with open(p_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Updated {count} records in JSON.")

if __name__ == "__main__":
    fix_nikon()
