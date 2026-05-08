import requests
import json
import os

def harvest_persistence_v34_2_4_4():
    # 使用 The Digital Picture 的高品質直連網址
    url = "https://www.the-digital-picture.com/Images/Products/Canon-RF-14mm-F1.4-L-VCM-Lens.jpg"
    id = "rf-14mm-f-1-4-l-vcm"
    
    json_path = "frontend/src/data/products.json"
    target_file = f"frontend/public/images/products/canon/{id}.jpg"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.the-digital-picture.com/"
    }
    
    try:
        print(f"DEBUG: Attempting final rescue for {id} from {url}...")
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "wb") as f:
            f.write(resp.content)
        
        # 更新 JSON
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
            
        for p in products:
            if p.get("id") == id:
                p["image_url"] = f"/images/products/canon/{id}.jpg"
                break
                
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
            
        print(f"SUCCESS: {id} has been harvested.")
    except Exception as e:
        print(f"FAIL: {id} harvest failed again ({str(e)}).")

if __name__ == "__main__":
    harvest_persistence_v34_2_4_4()
