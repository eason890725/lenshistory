import json
import os

def inject_mount_data():
    json_path = "frontend/src/data/products.json"
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    updated_count = 0
    for p in products:
        brand = p.get("brand", "")
        model = p.get("modelName", "").upper()
        
        # 決定接環名稱
        mount_name = ""
        if brand == "Sony":
            mount_name = "Sony E"
        elif brand == "Canon":
            mount_name = "Canon RF"
        elif brand == "Nikon":
            mount_name = "Nikon Z"
        elif brand == "Fujifilm":
            if "GFX" in model or " G " in model or "GF" in model:
                mount_name = "Fujifilm G"
            else:
                mount_name = "Fujifilm X"
        elif brand == "Panasonic" or brand == "Leica":
            mount_name = "L-Mount"
        
        if mount_name:
            # 依照前端 GearGrid.tsx 的預期結構注入
            p["mounts"] = [{"mount": {"name": mount_name}}]
            updated_count += 1
            
        # 同時修正 sensorFormat 的連字號問題 (確保統一為 "Full Frame" 或 "APS-C")
        fmt = p.get("sensorFormat", "")
        if "Full-frame" in fmt or "Fullframe" in fmt:
            p["sensorFormat"] = "Full Frame"
        elif "Medium" in fmt:
            p["sensorFormat"] = "Medium Format"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Mount and SensorFormat data injected. Updated: {updated_count}")

if __name__ == "__main__":
    inject_mount_data()
