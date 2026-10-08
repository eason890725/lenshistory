import os
from PIL import Image, ImageOps

def smart_crop_and_pad(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    non_black = []
    for y in range(h):
        for x in range(w):
            if sum(img.getpixel((x, y))) > 20: 
                non_black.append((x, y))
                
    if not non_black:
        return False
        
    min_x = min(p[0] for p in non_black)
    max_x = max(p[0] for p in non_black)
    min_y = min(p[1] for p in non_black)
    max_y = max(p[1] for p in non_black)
    
    print(f"Original bbox: x:{min_x}-{max_x}, y:{min_y}-{max_y}")
    
    true_min_y = min_y
    for y in range(min_y, max_y):
        pixels_in_row = sum(1 for p in non_black if p[1] == y)
        if pixels_in_row > (max_x - min_x) * 0.8: 
            true_min_y = y + 1
        else:
            break
            
    true_max_y = max_y
    for y in range(max_y, min_y, -1):
        pixels_in_row = sum(1 for p in non_black if p[1] == y)
        if pixels_in_row > (max_x - min_x) * 0.8:
            true_max_y = y - 1
        else:
            break
            
    print(f"True Y bounds: {true_min_y} - {true_max_y}")
        
    if true_min_y >= true_max_y:
        print("Y bounds inverted, skipping")
        true_min_y = min_y
        true_max_y = max_y
        
    clean_pixels = [p for p in non_black if true_min_y <= p[1] <= true_max_y]
    if not clean_pixels:
        print("No clean pixels")
        return False
        
    true_min_x = min(p[0] for p in clean_pixels)
    true_max_x = max(p[0] for p in clean_pixels)
    print(f"True X bounds: {true_min_x} - {true_max_x}")
    
    bbox = (true_min_x, true_min_y, true_max_x + 1, true_max_y + 1)
    cropped = img.crop(bbox)
    
    # 檢查裁切後還有沒有線
    cw, ch = cropped.size
    print(f"Cropped size: {cw}x{ch}")
    
    # 存檔
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
    
    final_img.save("frontend/public/images/products/sony/sony-a9-iii_TEST.jpg", "JPEG", quality=95)
    return True

smart_crop_and_pad("frontend/public/images/products/sony/sony-a9-iii.jpg")
