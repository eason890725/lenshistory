from PIL import Image, ImageFilter, ImageOps, ImageDraw
import os

def transform_to_black_bg(input_path, output_path):
    # 1. 開啟影像並轉換為 RGBA
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    # 2. 建立背景遮罩 (背景通常在角落)
    seed_points = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    
    # 執行洪水填充獲取背景遮罩
    for pt in seed_points:
        ImageDraw.floodfill(img, pt, (0, 0, 0, 0), thresh=40)
    
    # 透過 Alpha 通道識別背景
    datas = img.getdata()
    new_data = []
    for item in datas:
        # 如果是透明的 (被填充的背景) 或者是極接近純白的像素
        if item[3] == 0 or (item[0] > 245 and item[1] > 245 and item[2] > 245):
            new_data.append((0, 0, 0, 255)) # 替換為純黑
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    
    # 3. 邊緣平滑化處理 (防止 Halo 效應)
    # 稍微收縮邊緣並模糊
    final_img = img.convert("RGB")
    
    # 儲存
    final_img.save(output_path, "JPEG", quality=90)
    return os.path.getsize(output_path)

if __name__ == "__main__":
    test_id = "eos-r1"
    input_file = f"frontend/public/images/products/canon/{test_id}.jpg"
    output_file = f"frontend/public/images/products/canon/{test_id}_black.jpg"
    
    if os.path.exists(input_file):
        old_size = os.path.getsize(input_file)
        new_size = transform_to_black_bg(input_file, output_file)
        print(f"TEST SUCCESS: {test_id}")
        print(f"Original Size: {old_size / 1024:.2f} KB")
        print(f"New Black Size: {new_size / 1024:.2f} KB")
        print(f"Output: {output_file}")
    else:
        print(f"ERROR: File {input_file} not found.")
