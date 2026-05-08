from PIL import Image, ImageDraw
import json
import os

def transform_to_black_bg(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        seed_points = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        for pt in seed_points:
            ImageDraw.floodfill(img, pt, (0, 0, 0, 0), thresh=40)
        
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[3] == 0 or (item[0] > 245 and item[1] > 245 and item[2] > 245):
                new_data.append((0, 0, 0, 255))
            else:
                new_data.append(item)
        img.putdata(new_data)
        final_img = img.convert("RGB")
        final_img.save(output_path, "JPEG", quality=90)
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def batch_process():
    target_dir = "frontend/public/images/products/canon"
    json_path = "frontend/src/data/products.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 遍歷資料夾下所有圖檔
    files = [f for f in os.listdir(target_dir) if f.endswith(('.jpg', '.png')) and not f.endswith('_black.jpg')]
    
    count = 0
    for filename in files:
        file_id = os.path.splitext(filename)[0]
        # 跳過 canon- 前綴 (我們之前更名過，但為了相容性)
        if file_id.startswith("canon-"):
            new_id = file_id.replace("canon-", "")
        else:
            new_id = file_id
            
        input_path = os.path.join(target_dir, filename)
        # 統一輸出為 .jpg
        output_filename = f"{new_id}.jpg"
        output_path = os.path.join(target_dir, output_filename)
        
        print(f"Processing {filename} -> {output_filename}...")
        if transform_to_black_bg(input_path, output_path):
            count += 1
            # 更新 JSON 中的路徑
            for p in products:
                if p.get("id") == new_id:
                    p["image_url"] = f"/images/products/canon/{output_filename}"
                    break
            
            # 如果原檔是 .png 且我們另存為 .jpg，則刪除原 .png
            if input_path.endswith(".png"):
                os.remove(input_path)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Processed {count} images and synchronized database.")

if __name__ == "__main__":
    batch_process()
