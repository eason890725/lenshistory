import os
from PIL import Image

def precision_fix_v4(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # 1. Identify the letterbox area (the area not being pure black padding)
    datas = list(img.getdata())
    # Use sum > 10 to catch even very dark camera bodies
    active_pixels = [i for i, p in enumerate(datas) if sum(p) > 10]
    if not active_pixels: return False
    
    box_min_y = min(active_pixels) // w
    box_max_y = max(active_pixels) // w
    box_min_x = min(i % w for i in active_pixels)
    box_max_x = max(i % w for i in active_pixels)
    
    # 2. Extract the letterbox
    letterbox = img.crop((box_min_x, box_min_y, box_max_x + 1, box_max_y + 1))
    lw, lh = letterbox.size
    ldatas = list(letterbox.getdata())
    
    # 3. Create a mask to find the camera inside the letterbox
    # We want to EXCLUDE only the blueish-grey background lines.
    # We want to INCLUDE everything else, including pure black camera bodies.
    mask_pixels = []
    for p in ldatas:
        r, g, b = p
        # Noise line color condition: Blueish and bright-ish
        if b > r + 8 and b > 40:
            mask_pixels.append(0) # Exclude
        else:
            mask_pixels.append(255) # Include
            
    mask = Image.new("L", letterbox.size)
    mask.putdata(mask_pixels)
    
    # Get the bbox of included pixels (the camera + gaps)
    cam_bbox = mask.getbbox()
    if not cam_bbox: return False
    
    # 4. Crop to the tight camera bbox
    tight_cam = letterbox.crop(cam_bbox)
    
    # 5. Scale to fit 410x410
    target_size = 450
    padding = 20
    available_size = target_size - padding * 2 # 410
    
    tw, th = tight_cam.size
    scale = min(available_size / tw, available_size / th)
    
    new_w = int(tw * scale)
    new_h = int(th * scale)
    
    resized = tight_cam.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 6. Paste centered onto black canvas
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
                if precision_fix_v4(os.path.join(d, f)):
                    count += 1
    print(f"Total processed: {count}")

if __name__ == "__main__":
    process_all()
