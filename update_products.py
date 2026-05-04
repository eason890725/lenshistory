import json
import sys

def update():
    file_path = 'frontend/src/data/products.json'
    new_camera = {
        "brand": "TestBrand",
        "modelName": "Test Camera",
        "gearType": "CAMERA_BODY",
        "sensorFormat": "Full Frame",
        "megapixels": 24.2,
        "releaseYear": 2024,
        "launchPrice": 9999
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    old_count = len(products)
    products.append(new_camera)
    new_count = len(products)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"Old count: {old_count}, New count: {new_count}")

if __name__ == "__main__":
    update()
