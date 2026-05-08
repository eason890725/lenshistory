import requests
import json
import os

def harvest_persistence_v34_2_4_2():
    targets = [
        {"id": "rf-28-70mm-f2l-usm", "url": "https://cdn11.bigcommerce.com/s-745x53acpn/images/stencil/1280x1280/products/7505/14301/canon-rf-24-70-f2L-1__64946.1743785050.jpg?c=2"},
        {"id": "rf-50mm-f1-2l-usm", "url": "https://www.bhphotovideo.com/images/images1000x1000/canon_rf_50mm_f_1_2l_usm_1536121266_1433715.jpg"},
        {"id": "rf-14mm-f-1-4-l-vcm", "url": "https://www.bhphotovideo.com/images/images1000x1000/canon_rf_14mm_f_1_4_l_1947744.jpg"}
    ]
    
    json_path = "frontend/src/data/products.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    results = []
    
    for t in targets:
        id = t["id"]
        url = t["url"]
        target_file = f"frontend/public/images/products/canon/{id}.jpg"
        
        try:
            print(f"Downloading {id} from {url}...")
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "wb") as f:
                f.write(resp.content)
            
            # 更新 JSON
            for p in products:
                if p.get("id") == id:
                    p["image_url"] = f"/images/products/canon/{id}.jpg"
                    break
            
            results.append(f"{id} | {url} | Success")
        except Exception as e:
            results.append(f"{id} | {url} | Fail ({str(e)})")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("\n".join(results))

if __name__ == "__main__":
    harvest_persistence_v34_2_4_2()
