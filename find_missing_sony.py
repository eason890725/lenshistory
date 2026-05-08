import os
import json

def find_missing_sony_images():
    db_path = "frontend/src/data/products.json"
    img_dir = "frontend/public/images/products/sony"
    
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    missing = []
    for item in data:
        if item.get("brand", "").lower() == "sony":
            img_filename = item.get("id") + ".jpg"
            if not os.path.exists(os.path.join(img_dir, img_filename)):
                missing.append(item.get("modelName"))

    print(f"Total missing Sony images: {len(missing)}")
    for name in missing:
        print(f"- {name}")

if __name__ == "__main__":
    find_missing_sony_images()
