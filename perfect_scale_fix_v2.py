import os
from PIL import Image, ImageDraw

def perfect_scale_fix(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    datas = img.getdata()
    all_pixels = [(i % w, i // w) for i, item in enumerate(datas) if sum(item) > 10]
    if not all_pixels: return False
    
    box_min_x = min(p[0] for p in all_pixels)
    box_max_x = max(p[0] for p in all_pixels)
    box_min_y = min(p[1] for p in all_pixels)
    box_max_y = max(p[1] for p in all_pixels)
    
    draw = ImageDraw.Draw(img)
    
    # Erase the 20-pixel border around the letterbox
    # This securely deletes the white lines (top/bottom) and grey blocks (left/right)
    draw.rectangle([0, box_min_y, w, box_min_y + 20], fill=(0, 0, 0)) # Top
    draw.rectangle([0, box_max_y - 20, w, box_max_y], fill=(0, 0, 0)) # Bottom
    draw.rectangle([box_min_x, 0, box_min_x + 20, h], fill=(0, 0, 0)) # Left
    draw.rectangle([box_max_x - 20, 0, box_max_x, h], fill=(0, 0, 0)) # Right
    
    new_datas = img.getdata()
    cam_pixels = [(i % w, i // w) for i, item in enumerate(new_datas) if sum(item) > 20]
    if not cam_pixels: return False
    
    cam_min_x = min(p[0] for p in cam_pixels)
    cam_max_x = max(p[0] for p in cam_pixels)
    cam_min_y = min(p[1] for p in cam_pixels)
    cam_max_y = max(p[1] for p in cam_pixels)
    
    cam_width = cam_max_x - cam_min_x
    cam_height = cam_max_y - cam_min_y
    
    target_size = 450
    padding = 20
    available_size = target_size - padding * 2
    
    scale_x = available_size / cam_width if cam_width > 0 else 1.0
    scale_y = available_size / cam_height if cam_height > 0 else 1.0
    scale = min(scale_x, scale_y)
    
    # Crop the letterbox tightly around the camera's X bounds, but keep the original Y bounds
    # This preserves the camera's original vertical centering and its black bottom!
    clean_box = img.crop((cam_min_x, box_min_y + 21, cam_max_x + 1, box_max_y - 21))
    
    new_w = int(clean_box.width * scale)
    new_h = int(clean_box.height * scale)
    
    resized = clean_box.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
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
                    if perfect_scale_fix(path):
                        count += 1
                except Exception as e:
                    pass
    print(f"Total flawless fixed: {count}")

if __name__ == "__main__":
    process_all()
