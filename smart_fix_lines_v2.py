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
        
    # Ignore sparse noise rows/cols to find true bounding box for width calculation
    y_counts = {y: sum(1 for p in non_black if p[1] == y) for y in range(h)}
    x_counts = {x: sum(1 for p in non_black if p[0] == x) for x in range(w)}
    
    valid_y = [y for y, c in y_counts.items() if c > 15]
    valid_x = [x for x, c in x_counts.items() if c > 15]
    
    if not valid_y or not valid_x:
        return False
        
    min_x, max_x = min(valid_x), max(valid_x)
    min_y, max_y = min(valid_y), max(valid_y)
    
    # scan for solid lines to crop out
    true_min_y = min_y
    for y in range(min_y, max_y):
        if y_counts.get(y, 0) > (max_x - min_x) * 0.75: 
            true_min_y = y + 1
        else:
            break
            
    true_max_y = max_y
    for y in range(max_y, min_y, -1):
        if y_counts.get(y, 0) > (max_x - min_x) * 0.75:
            true_max_y = y - 1
        else:
            break
            
    if true_min_y >= true_max_y:
        true_min_y = min_y
        true_max_y = max_y
        
    clean_pixels = [p for p in non_black if true_min_y <= p[1] <= true_max_y and min_x <= p[0] <= max_x]
    if not clean_pixels:
        return False
        
    true_min_x = min(p[0] for p in clean_pixels)
    true_max_x = max(p[0] for p in clean_pixels)
    
    bbox = (true_min_x, true_min_y, true_max_x + 1, true_max_y + 1)
    cropped = img.crop(bbox)
    
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
        "frontend/public/images/products/fujifilm",
        "frontend/public/images/products/canon",
        "frontend/public/images/products/nikon"
    ]
    count = 0
    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".jpg") and not f.endswith("_TEST.jpg"):
                path = os.path.join(d, f)
                if smart_crop_and_pad(path):
                    count += 1
    print(f"Total fixed: {count}")

if __name__ == "__main__":
    process_all()
