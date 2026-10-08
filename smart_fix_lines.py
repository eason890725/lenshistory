import os
from PIL import Image, ImageOps

def smart_crop_and_pad(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # 1. 找到所有非黑像素
    non_black = []
    for y in range(h):
        for x in range(w):
            if sum(img.getpixel((x, y))) > 20: # 容忍 JPEG 壓縮的微弱噪點
                non_black.append((x, y))
                
    if not non_black:
        return False
        
    min_x = min(p[0] for p in non_black)
    max_x = max(p[0] for p in non_black)
    min_y = min(p[1] for p in non_black)
    max_y = max(p[1] for p in non_black)
    
    # 2. 去除上下兩側的長條狀背景干擾線
    # 邏輯：相機/鏡頭的主體通常不會在最頂端或最底端「橫跨整個寬度」。
    # 如果某個 y 座標上的非黑像素數量幾乎等於 (max_x - min_x)，代表這是一條水平干擾線。
    
    # 掃描並縮小 top bound
    true_min_y = min_y
    for y in range(min_y, max_y):
        pixels_in_row = sum(1 for p in non_black if p[1] == y)
        if pixels_in_row > (max_x - min_x) * 0.8: 
            true_min_y = y + 1
        else:
            # 只要遇到不是一整條線的，就認定碰到產品主體了
            break
            
    # 掃描並縮小 bottom bound
    true_max_y = max_y
    for y in range(max_y, min_y, -1):
        pixels_in_row = sum(1 for p in non_black if p[1] == y)
        if pixels_in_row > (max_x - min_x) * 0.8:
            true_max_y = y - 1
        else:
            break
            
    # 如果切完發現都不見了，就退回原本的
    if true_min_y >= true_max_y:
        true_min_y = min_y
        true_max_y = max_y
        
    # 現在我們有了乾淨的 Y 範圍，重新計算 X 範圍
    clean_pixels = [p for p in non_black if true_min_y <= p[1] <= true_max_y]
    if not clean_pixels:
        return False
        
    true_min_x = min(p[0] for p in clean_pixels)
    true_max_x = max(p[0] for p in clean_pixels)
    
    # Crop 出乾淨的產品
    bbox = (true_min_x, true_min_y, true_max_x + 1, true_max_y + 1)
    cropped = img.crop(bbox)
    
    # 3. 把乾淨的產品等比例放入 450x450，並且上下左右留一點呼吸空間 (例如 padding 20)
    # 這樣大小就會跟之前 Canon/Nikon 的圖一樣大且置中
    target_size = 450
    padding = 20
    available_size = target_size - padding * 2
    
    # 計算縮放比例
    scale = min(available_size / cropped.width, available_size / cropped.height)
    new_w = int(cropped.width * scale)
    new_h = int(cropped.height * scale)
    
    # Resize
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 放進純黑畫布
    final_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
    paste_x = (target_size - new_w) // 2
    paste_y = (target_size - new_h) // 2
    final_img.paste(resized, (paste_x, paste_y))
    
    final_img.save(src_path, "JPEG", quality=95)
    return True

def process_all():
    dirs = [
        "frontend/public/images/products/sony",
        "frontend/public/images/products/fujifilm"
    ]
    count = 0
    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".jpg"):
                path = os.path.join(d, f)
                if smart_crop_and_pad(path):
                    print(f"FIXED: {path}")
                    count += 1
    print(f"Total fixed: {count}")

if __name__ == "__main__":
    process_all()
