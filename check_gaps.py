import os
from PIL import Image

def check_gaps():
    dirs = ["frontend/public/images/products/sony", "frontend/public/images/products/fujifilm"]
    results = []
    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if not f.endswith(".jpg"): continue
            img = Image.open(os.path.join(d, f)).convert("RGB")
            w, h = img.size
            datas = list(img.getdata())
            y_counts = {}
            for i, p in enumerate(datas):
                if sum(p) > 20:
                    y = i // w
                    y_counts[y] = y_counts.get(y, 0) + 1
            if not y_counts: continue
            valid_y = sorted(y_counts.keys())
            min_y = valid_y[0]
            # Find the gap after the line
            # Line is roughly where y_counts > 250
            line_end = min_y
            for y in range(min_y, min_y + 20):
                if y_counts.get(y, 0) > 250:
                    line_end = y
                else:
                    break
            # Camera start
            cam_start = line_end + 1
            for y in range(line_end + 1, line_end + 50):
                if y_counts.get(y, 0) > 0 and y_counts.get(y, 0) < 400:
                    cam_start = y
                    break
            gap = cam_start - line_end
            results.append((f, gap, line_end - min_y + 1))
    
    results.sort(key=lambda x: x[1])
    for r in results[:20]:
        print(f"{r[0]}: gap={r[1]}, line_height={r[2]}")

if __name__ == "__main__":
    check_gaps()
