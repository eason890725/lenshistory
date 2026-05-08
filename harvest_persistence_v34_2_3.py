import requests
import json
import os

def harvest_persistence_v34_2_3():
    targets = [
        {"id": "eos-r8", "url": "https://s7d1.scene7.com/is/image/canon/eos_r8_body_primary?fmt=jpg&wid=800&hei=800"},
        {"id": "eos-r", "url": "https://www.photoreview.com.au/wp-content/uploads/2018/11/EOS-R_FrontSlantLeft_RF24-105LIS.jpg"},
        {"id": "eos-rp", "url": "https://reefphoto.com/cdn/shop/products/1550097912_IMG_1138466_730x.jpg?v=1574012503"},
        {"id": "eos-r7", "url": "https://cdn-next.cybassets.com/media/W1siZiIsIjkwODAvcHJvZHVjdHMvYWI5Zjc2NTBjNWE2ZDdmNTJhZTU3ODY1MGRlNGJiYjZmZGU4MjEzMDA2YjYyOTUyZmZiMTI3YTk2NGEyOWMwMy5qcGVnIl0sWyJwIiwidGh1bWIiLCI2MDB4NjAwIl1d.jpeg?sha=b31deafab590bdb9"},
        {"id": "eos-r10", "url": "https://i1.adis.ws/i/canon/eos-r10-frt_range_9feaf965e90e48d3a164d106d9939020?fmt=jpg&wid=800&hei=800"},
        {"id": "eos-r6-ii", "url": "https://www.ephotozine.com/articles/canon-eos-r6-mark-ii-announced-36245/images/highres-01_Product-1_Front_BODYjpg_1667310614.jpg"}
    ]
    
    json_path = "frontend/src/data/products.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    results = []
    
    for t in targets:
        id = t["id"]
        url = t["url"]
        # Standardize extension to .jpg as per user request
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
    harvest_persistence_v34_2_3()
