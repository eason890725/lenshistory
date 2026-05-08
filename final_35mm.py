import requests
import json
import os

def final_35mm_harvest():
    url = "https://tw.canon/media/image/2024/06/05/26359549f6b940428d0fc61657b98947_RF35mm-f1.4L-VCM-Front.png"
    id = "rf-35mm-f-1-4-l-vcm"
    json_path = "frontend/src/data/products.json"
    target_file = f"frontend/public/images/products/canon/{id}.jpg"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "wb") as f:
            f.write(resp.content)
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for p in data:
            if p.get("id") == id:
                p["image_url"] = f"/images/products/canon/{id}.jpg"
                break
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("SUCCESS")
    except Exception as e:
        print(f"FAIL: {e}")

if __name__ == "__main__":
    final_35mm_harvest()
