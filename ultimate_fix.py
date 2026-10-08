import os
from PIL import Image, ImageDraw, ImageOps

def ultimate_fix(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    datas = img.getdata()
    y_counts = {}
    
    for i, item in enumerate(datas):
        if sum(item) > 20:
            y = i // w
            y_counts[y] = y_counts.get(y, 0) + 1
            
    if not y_counts: return False
    
    valid_y = sorted([y for y in y_counts])
    
    # Identify the top noise block and bottom noise block
    # Noise blocks are usually continuous rows at the very top/bottom.
    # The camera is separated from the noise block by a gap of 0 pixels,
    # OR if it's not separated, the noise block is only a few pixels tall.
    
    # Let's find the largest contiguous block of Y values. That is the camera!
    # A block is a sequence of consecutive Y values (difference is 1).
    blocks = []
    current_block = [valid_y[0]]
    
    for i in range(1, len(valid_y)):
        if valid_y[i] == valid_y[i-1] + 1:
            current_block.append(valid_y[i])
        else:
            blocks.append(current_block)
            current_block = [valid_y[i]]
    blocks.append(current_block)
    
    # The camera is the block with the most rows (largest height)
    camera_block = max(blocks, key=len)
    
    true_min_y = camera_block[0]
    true_max_y = camera_block[-1]
    
    # Now get the X bounds for the camera_block
    camera_pixels = []
    for i, item in enumerate(datas):
        if sum(item) > 20:
            y = i // w
            if true_min_y <= y <= true_max_y:
                x = i % w
                camera_pixels.append((x, y))
                
    if not camera_pixels: return False
    
    true_min_x = min(p[0] for p in camera_pixels)
    true_max_x = max(p[0] for p in camera_pixels)
    
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
        "frontend/public/images/products/fujifilm"
    ]
    count = 0
    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".jpg") and not f.endswith("_TEST.jpg"):
                path = os.path.join(d, f)
                try:
                    if ultimate_fix(path):
                        count += 1
                except Exception as e:
                    pass
    print(f"Total fixed: {count}")

if __name__ == "__main__":
    process_all()
