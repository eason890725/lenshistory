import requests
import json
import os

def harvest_persistence_v34_2_2():
    targets = [
        {"id": "eos-r3", "url": "https://tw.canon/media/image/2021/09/13/833d03bdb5e64e8aba8dce604cdd499f_R3_top.png"},
        {"id": "eos-r5-ii", "url": "https://www.photoreview.com.au/wp-content/uploads/2024/09/12_EOS-R5II_FrontSlantLeft_RF24-105F4L.jpg"},
        {"id": "eos-r5", "url": "https://www.canon.ca/dam/products/BUSINESS-UNIT/ITCG/Cameras/EOS-Cameras/Mirrorless/EOS-R5/Canon_EOS-R5_Side_580x580.png"},
        {"id": "eos-r6-ii", "url": "https://www.photoreview.com.au/wp-content/uploads/2022/11/Canon-EOS-R6-II_FrontSlantLeft_RF24-105F4L-scaled.jpg"},
        {"id": "eos-r6", "url": "https://as2.ftcdn.net/v2/jpg/04/22/84/10/1000_F_422841016_ymP46o83bxzQz1epz1E7WstGUXZPiemX.jpg"}
    ]
    
    json_path = "frontend/src/data/products.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    results = []
    
    for t in targets:
        id = t["id"]
        url = t["url"]
        ext = ".jpg" if ".jpg" in url.lower() or ".jpeg" in url.lower() else ".png"
        target_file = f"frontend/public/images/products/canon/{id}{ext}"
        
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
                    p["image_url"] = f"/images/products/canon/{id}{ext}"
                    break
            
            results.append(f"{id} | {url} | Success")
        except Exception as e:
            results.append(f"{id} | {url} | Fail ({str(e)})")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("\n".join(results))

if __name__ == "__main__":
    harvest_persistence_v34_2_2()
