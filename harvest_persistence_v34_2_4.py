import requests
import json
import os

def harvest_persistence_v34_2_4():
    targets = [
        {"id": "eos-r50", "url": "https://assets.cathayphoto.com.sg/product/EOS-R50-White-Kit-1845-55210_1.jpg"},
        {"id": "eos-r100", "url": "https://hk.canon/media/image/2023/05/19/b89bed4e21e540f985dedebe80166def_EOS%2BR100%2BRF-S18-45mm%2BFront%2BSlant.png"},
        {"id": "rf-15-35mm-f2-8l-is-usm", "url": "https://www.lcegroup.co.uk/Images/Products/New-Canon-RF-15-35mm-F2.8L-IS-USM.jpg"},
        {"id": "rf-24-70mm-f2-8l-is-usm", "url": "https://asia.canon/media/image/2023/11/01/95b9d3752e504c609c958448555198e3_RF24-70mm-f2.8L-IS-USM-Front-Slant.png"},
        {"id": "rf-70-200mm-f2-8l-is-usm", "url": "https://tw.canon/media/image/2024/10/30/0333ce942d9943f9a7444c1d6baef76e_RF70-200mm-f2.8L-IS-USM-Z-White-Front.png"},
        {"id": "rf-28-70mm-f2l-usm", "url": "https://bccamera.com/product_images/z/459/Canon-RF-28-70mm-f2L-USM__18663_zoom.jpg"},
        {"id": "rf-50mm-f1-2l-usm", "url": "https://www.canon.com.au/-/media/images/canon/products/camera-lenses/rf-lenses/rf-50mm-f12l-usm/rf-50mm-f12l-usm-slant.jpg"},
        {"id": "rf-14mm-f-1-4-l-vcm", "url": "https://tw.canon/media/image/2024/05/29/e56238b975874c76b9dfa3e9c6a1e3a6_RF14mm-f1.4L-VCM-Front.png"}
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
    harvest_persistence_v34_2_4()
