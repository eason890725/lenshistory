import json
import re

def purge():
    file_path = 'frontend/src/data/products.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    old_count = len(products)
    
    def is_valid(item):
        name = item.get('modelName', '')
        brand = item.get('brand', '')
        
        # 1. 包含 "Model" 及流水號
        if re.search(r'Model \d+', name):
            return False
            
        # 2. 包含 "DG DN Series"
        if "DG DN Series" in name:
            return False
            
        # 3. 邏輯一致性：Tamron 鏡頭不應有 Sigma 的 DG DN 標示
        if brand == 'Tamron' and 'DG DN' in name:
            return False
            
        # 4. 測試相機
        if name == 'Test Camera':
            return False
            
        return True

    clean_products = [p for p in products if is_valid(p)]
    new_count = len(clean_products)
    deleted_count = old_count - new_count
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(clean_products, f, indent=2, ensure_ascii=False)
    
    print(f"Purge complete: Deleted {deleted_count} fake/invalid items.")
    print(f"Remaining: {new_count} real items.")

if __name__ == "__main__":
    purge()
