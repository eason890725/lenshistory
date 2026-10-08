import os
from PIL import Image, ImageDraw

def test_floodfill_center(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # 掃描並 floodfill
    # 我們可以針對前 150 行和後 150 行，從左到右掃描。
    # 如果遇到非黑的連續長條（長度 > w * 0.7），就找上面隨便一點 floodfill 掉！
    # 但這個太複雜了，其實我們可以直接用 Y 投影：
    
    # 計算 Y 投影 (大於 20 亮度的像素數量)
    y_counts = {y: sum(1 for x in range(w) if sum(img.getpixel((x, y))) > 20) for y in range(h)}
    
    # 找出非常寬的行 (大於 w * 0.7 = 315)
    wide_rows = [y for y, count in y_counts.items() if count > 300]
    
    if wide_rows:
        draw = ImageDraw.Draw(img)
        for y in wide_rows:
            # 找到這行第一個不是黑色的點，然後 floodfill 掉
            for x in range(w):
                if sum(img.getpixel((x, y))) > 20:
                    ImageDraw.floodfill(img, (x, y), (0, 0, 0), thresh=40)
                    break
                    
        print(f"Removed artifacts on rows: {wide_rows}")
        
    img.save("frontend/public/images/products/sony/sony-a9-iii_TEST_FF2.jpg", "JPEG", quality=95)

test_floodfill_center("frontend/public/images/products/sony/sony-a9-iii.jpg")
