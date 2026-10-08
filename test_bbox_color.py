import os
from PIL import Image

def test_bbox_color(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    datas = img.getdata()
    mask_data = []
    
    for item in datas:
        r, g, b = item[0], item[1], item[2]
        
        is_bg = False
        
        # Pure black / dark shadows
        if r < 20 and g < 20 and b < 20:
            is_bg = True
            
        # Sony/Fuji background lines (blueish grey)
        # 1. B is the largest component
        # 2. It's relatively bright (B > 100)
        # 3. G is in between B and R
        elif b > r + 10 and b >= g and g >= r and b > 100:
            is_bg = True
            
        # Also purely grey backgrounds (like R=200, G=200, B=200)
        elif abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15 and r > 150:
            is_bg = True
            
        if is_bg:
            mask_data.append((0, 0, 0, 0))
        else:
            mask_data.append((255, 255, 255, 255))
            
    mask = Image.new("RGBA", img.size)
    mask.putdata(mask_data)
    
    bbox = mask.getbbox()
    print(f"{os.path.basename(src_path)} bbox: {bbox}")
    
    if bbox:
        # Save a debug image showing what we kept
        debug = img.copy()
        debug.putdata([item if m[3] == 255 else (255, 0, 0) for item, m in zip(datas, mask_data)])
        debug.save(src_path.replace(".jpg", "_DEBUG.jpg"), "JPEG")

test_bbox_color("frontend/public/images/products/sony/sony-zv-e10-ii.jpg")
test_bbox_color("frontend/public/images/products/sony/sony-a1-ii.jpg")
test_bbox_color("frontend/public/images/products/fujifilm/fujifilm-gfx-50s-ii.jpg")
