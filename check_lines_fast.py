import os
from PIL import Image

files = [
    'frontend/public/images/products/sony/sony-a1-ii.jpg',
    'frontend/public/images/products/sony/sony-a7r-v.jpg',
    'frontend/public/images/products/sony/sony-fe-24-70mm-f2-8-gm-ii.jpg',
    'frontend/public/images/products/sony/sony-zv-e10-ii.jpg',
    'frontend/public/images/products/fujifilm/fujifilm-gfx-50s-ii.jpg'
]

for f in files:
    try:
        img = Image.open(f).convert('RGB')
        w, h = img.size
        datas = img.getdata()
        
        y_counts = {}
        for i, item in enumerate(datas):
            if sum(item) > 20:
                y = i // w
                y_counts[y] = y_counts.get(y, 0) + 1
                
        lines = [y for y, c in y_counts.items() if c > 350]
        print(f"{os.path.basename(f)}: lines at {lines[:3]} ... {lines[-3:] if len(lines) > 3 else ''}")
    except Exception as e:
        print(f"Error on {f}: {e}")
