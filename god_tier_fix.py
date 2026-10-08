import os
from PIL import Image

def god_tier_fix(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    datas = img.getdata()
    mask_data = []
    
    for item in datas:
        r, g, b = item[0], item[1], item[2]
        
        is_bg = False
        
        # 1. Pure black background
        if r < 20 and g < 20 and b < 20:
            is_bg = True
            
        # 2. Sony / Fujifilm annoying horizontal lines
        # These are usually a bright blueish-grey.
        elif b > r + 10 and b >= g and g >= r and b > 100:
            is_bg = True
            
        # 3. Pure grey/white lines
        elif abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15 and r > 150:
            is_bg = True
            
        if is_bg:
            mask_data.append((0, 0, 0, 0))
        else:
            mask_data.append((255, 255, 255, 255))
            
    mask = Image.new("RGBA", img.size)
    mask.putdata(mask_data)
    
    bbox = mask.getbbox()
    if not bbox:
        return False
        
    # Crop the ORIGINAL image using the pristine bounding box
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
        "frontend/public/images/products/fujifilm"
    ]
    count = 0
    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".jpg") and not f.endswith("_TEST.jpg") and not f.endswith("_DEBUG.jpg"):
                path = os.path.join(d, f)
                try:
                    if god_tier_fix(path):
                        count += 1
                except Exception as e:
                    pass
    print(f"Total flawless fixed: {count}")

if __name__ == "__main__":
    process_all()
