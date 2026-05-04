import json
import os

def merge_data():
    backend_path = 'backend/src/main/resources'
    frontend_data_path = 'frontend/src/data'
    
    with open(os.path.join(backend_path, 'bodies.json'), 'r', encoding='utf-8-sig') as f:
        bodies = json.load(f)
    with open(os.path.join(backend_path, 'lenses.json'), 'r', encoding='utf-8-sig') as f:
        lenses = json.load(f)
        
    products = bodies + lenses
    
    os.makedirs(frontend_data_path, exist_ok=True)
    with open(os.path.join(frontend_data_path, 'products.json'), 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"Merge successful: {len(products)} items moved.")

if __name__ == "__main__":
    merge_data()
