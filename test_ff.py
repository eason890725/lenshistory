import os
from PIL import Image, ImageDraw

def test_floodfill(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # Find top non-black pixel row on x=0 and x=w-1
    # Actually, let's just find any non-black pixel on x=0 and x=w-1 and flood fill them!
    # Because the only things that touch the absolute edges (x=0, x=w-1) in these 450x450 padded images
    # are the unwanted horizontal background lines!
    # A properly padded camera should NOT touch x=0 or x=w-1.
    
    draw = ImageDraw.Draw(img)
    
    count = 0
    # Left edge
    for y in range(h):
        if sum(img.getpixel((0, y))) > 20:
            ImageDraw.floodfill(img, (0, y), (0, 0, 0), thresh=40)
            count += 1
            
    # Right edge
    for y in range(h):
        if sum(img.getpixel((w-1, y))) > 20:
            ImageDraw.floodfill(img, (w-1, y), (0, 0, 0), thresh=40)
            count += 1
            
    if count > 0:
        print(f"Floodfilled {count} edge artifacts.")
        
    img.save("frontend/public/images/products/sony/sony-a9-iii_TEST_FF.jpg", "JPEG", quality=95)

test_floodfill("frontend/public/images/products/sony/sony-a9-iii.jpg")
