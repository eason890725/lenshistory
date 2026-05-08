import json
import os
import shutil

def final_sync_canon():
    # Paths to source screenshots
    src_dir = r"C:\Users\eason\.gemini\antigravity\brain\c02609d0-36ed-440a-8e76-b5302abbe265"
    dest_dir = "frontend/public/images/products/canon"
    json_path = "frontend/src/data/products.json"
    
    mapping = {
        "eos_r100_element_v2_1777994007398.png": "eos-r100.png",
        "rf_24_70mm_element_1777994140272.png": "rf-24-70mm-f2-8l-is-usm.png",
        "rf_70_200mm_element_1777994162110.png": "rf-70-200mm-f2-8l-is-usm.png"
    }
    
    # 1. Copy files
    for src, dest in mapping.items():
        src_path = os.path.join(src_dir, src)
        dest_path = os.path.join(dest_dir, dest)
        if os.path.exists(src_path):
            print(f"Copying {src} to {dest}...")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Warning: Source {src} not found!")
            
    # 2. Update JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    updates = {
        "eos-r100": "/images/products/canon/eos-r100.png",
        "rf-24-70mm-f2-8l-is-usm": "/images/products/canon/rf-24-70mm-f2-8l-is-usm.png",
        "rf-70-200mm-f2-8l-is-usm": "/images/products/canon/rf-70-200mm-f2-8l-is-usm.png",
        "eos-r1": "/images/products/canon/eos-r1.jpg"
    }
    
    count = 0
    for p in data:
        if p.get("id") in updates:
            p["image_url"] = updates[p["id"]]
            count += 1
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Updated {count} records in JSON.")

if __name__ == "__main__":
    final_sync_canon()
