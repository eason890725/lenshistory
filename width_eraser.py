import os
from PIL import Image, ImageDraw

def width_eraser_fix(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # 1. 計算每一行的非黑像素數量
    y_counts = {}
    datas = img.getdata()
    for i, item in enumerate(datas):
        if sum(item) > 20:
            y = i // w
            y_counts[y] = y_counts.get(y, 0) + 1
            
    if not y_counts: return False
    
    valid_y = sorted(list(y_counts.keys()))
    min_y = valid_y[0]
    max_y = valid_y[-1]
    
    # 2. 從上方開始刪除超級寬的行 (大於 250 像素)
    # 只要一碰到 < 250 的行，就代表碰到相機主體了，馬上停止！
    top_erase_end = min_y - 1
    for y in range(min_y, min_y + 50):
        if y not in y_counts: continue
        if y_counts[y] > 250:
            top_erase_end = y
        else:
            break
            
    # 從下方開始刪除超級寬的行
    bottom_erase_start = max_y + 1
    for y in range(max_y, max_y - 50, -1):
        if y not in y_counts: continue
        if y_counts[y] > 250:
            bottom_erase_start = y
        else:
            break
            
    # 3. 塗黑這些干擾行
    draw = ImageDraw.Draw(img)
    if top_erase_end >= min_y:
        draw.rectangle([0, 0, w, top_erase_end], fill=(0, 0, 0))
    if bottom_erase_start <= max_y:
        draw.rectangle([0, bottom_erase_start, w, h], fill=(0, 0, 0))
        
    # 4. 重新計算 Bounding Box
    new_datas = img.getdata()
    clean_pixels = []
    for i, item in enumerate(new_datas):
        if sum(item) > 20:
            clean_pixels.append((i % w, i // w))
            
    if not clean_pixels: return False
    
    true_min_x = min(p[0] for p in clean_pixels)
    true_max_x = max(p[0] for p in clean_pixels)
    true_min_y = min(p[1] for p in clean_pixels)
    true_max_y = max(p[1] for p in clean_pixels)
    
    bbox = (true_min_x, true_min_y, true_max_x + 1, true_max_y + 1)
    cropped = img.crop(bbox)
    
    # 5. 縮放並置中
    target_size = 450
    padding = 20
    available_size = target_size - padding * 2
    
    scale = min(available_size / cropped.width, available_size / cropped.height)
    new_w = int(cropped.width * scale)
    new_h = int(cropped.height * scale)
    
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
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
                try:
                    if width_eraser_fix(path):
                        count += 1
                except Exception as e:
                    pass
    print(f"Total flawless fixed: {count}")

if __name__ == "__main__":
    process_all()
