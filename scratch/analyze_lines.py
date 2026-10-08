import os
from PIL import Image

def analyze_image(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    
    # 找到所有的非黑像素
    non_black_pixels = []
    for y in range(h):
        for x in range(w):
            if sum(img.getpixel((x, y))) > 20:
                non_black_pixels.append((x, y))
                
    if not non_black_pixels:
        print(f"{os.path.basename(path)}: All black!")
        return

    min_x = min(p[0] for p in non_black_pixels)
    max_x = max(p[0] for p in non_black_pixels)
    min_y = min(p[1] for p in non_black_pixels)
    max_y = max(p[1] for p in non_black_pixels)
    
    print(f"{os.path.basename(path)}: Bounding box is ({min_x}, {min_y}, {max_x}, {max_y})")
    
    # Check what's at min_y
    top_line_colors = set(img.getpixel((x, min_y)) for x in range(min_x, max_x+1))
    print(f"Top line unique colors: {list(top_line_colors)[:5]} (Total {len(top_line_colors)})")

analyze_image("frontend/public/images/products/sony/sony-a1-ii.jpg")
