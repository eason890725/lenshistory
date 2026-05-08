import requests
import json
import os

def download_and_sync_r1():
    url = "https://sg.canon/media/image/2024/07/17/2d53bdd971e049838f89515bf8976992_PR-Image-EOS-R1-with-RF24-70mm-f2.8L-IS-USM.png"
    target_path = "frontend/public/images/products/canon/canon-eos-r1.jpg"
    json_path = "frontend/src/data/products.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"DEBUG: Downloading from {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # 儲存圖片
        with open(target_path, "wb") as f:
            f.write(response.content)
        
        file_size = os.path.getsize(target_path)
        print(f"DEBUG: Download successful. File size: {file_size} bytes.")
        
        if file_size == 0:
            print("ERROR: Downloaded file is empty.")
            return

        # 更新 JSON
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
        
        updated = False
        for p in products:
            if p.get("id") == "eos-r1":
                p["image_url"] = "/images/products/canon/canon-eos-r1.jpg"
                updated = True
                break
        
        if updated:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            print("DEBUG: products.json updated successfully.")
        else:
            print("ERROR: Product 'eos-r1' not found in JSON.")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    download_and_sync_r1()
