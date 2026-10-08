import os
from PIL import Image, ImageDraw

def ultimate_fix_v5(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # 1. Identify the letterbox area
    datas = list(img.getdata())
    active_pixels = [i for i, p in enumerate(datas) if sum(p) > 20]
    if not active_pixels: return False
    
    box_min_y = min(active_pixels) // w
    box_max_y = max(active_pixels) // w
    box_min_x = min(i % w for i in active_pixels)
    box_max_x = max(i % w for i in active_pixels)
    
    # 2. Row by row analysis inside the letterbox to find where the lines end
    def is_line_color(p):
        r, g, b = p
        return b > r + 8 and b > 40
    
    # Find the first row that isn't a line
    true_min_y = box_min_y
    for y in range(box_min_y, box_max_y + 1):
        # Check a few pixels in the middle of the row
        is_line = True
        for x in range(w // 4, 3 * w // 4):
            if not is_line_color(img.getpixel((x, y))):
                is_line = False
                break
        if not is_line:
            true_min_y = y
            break
            
    # Find the last row that isn't a line
    true_max_y = box_max_y
    for y in range(box_max_y, box_min_y - 1, -1):
        is_line = True
        for x in range(w // 4, 3 * w // 4):
            if not is_line_color(img.getpixel((x, y))):
                is_line = False
                break
        if not is_line:
            true_max_y = y
            break
            
    # 3. Same for X (left/right grey blocks)
    true_min_x = box_min_x
    for x in range(box_min_x, box_max_x + 1):
        is_line = True
        for y in range(true_min_y, true_max_y + 1):
            if not is_line_color(img.getpixel((x, y))):
                is_line = False
                break
        if not is_line:
            true_min_x = x
            break
            
    true_max_x = box_max_x
    for x in range(box_max_x, box_min_x - 1, -1):
        is_line = True
        for y in range(true_min_y, true_max_y + 1):
            if not is_line_color(img.getpixel((x, y))):
                is_line = False
                break
        if not is_line:
            true_max_x = x
            break

    # 4. Crop to this area
    # Add a tiny 1-pixel safety margin to ensure no line pixels remain
    crop_rect = (true_min_x + 1, true_min_y + 1, true_max_x - 1, true_max_y - 1)
    if crop_rect[2] <= crop_rect[0] or crop_rect[3] <= crop_rect[1]:
        return False
        
    tight_cam = img.crop(crop_rect)
    
    # 5. Scale to fit 410x410
    target_size = 450
    padding = 20
    available_size = target_size - padding * 2
    
    tw, th = tight_cam.size
    scale = min(available_size / tw, available_size / th)
    
    new_w = int(tw * scale)
    new_h = int(th * scale)
    
    resized = tight_cam.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 6. Paste centered
    final_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
    paste_x = (target_size - new_w) // 2
    paste_y = (target_size - new_h) // 2
    final_img.paste(resized, (paste_x, paste_y))
    
    final_img.save(src_path, "JPEG", quality=95)
    return True

def process_all():
    dirs = ["frontend/public/images/products/sony", "frontend/public/images/products/fujifilm"]
    count = 0
    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".jpg"):
                if ultimate_fix_v5(os.path.join(d, f)):
                    count += 1
    print(f"Total processed: {count}")

if __name__ == "__main__":
    process_all()
