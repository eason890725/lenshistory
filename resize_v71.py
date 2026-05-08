import os
from PIL import Image, ImageOps

def resize_to_standard():
    target_files = [
        "frontend/public/images/products/fujifilm/fujifilm-gfx-50s-ii.jpg",
        "frontend/public/images/products/fujifilm/fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr.jpg",
        "frontend/public/images/products/sony/sony-a1-ii.jpg",
        "frontend/public/images/products/sony/sony-a7-iv.jpg",
        "frontend/public/images/products/sony/sony-a7r-v.jpg",
        "frontend/public/images/products/sony/sony-a9-iii.jpg",
        "frontend/public/images/products/sony/sony-fe-24-70mm-f2-8-gm-ii.jpg",
        "frontend/public/images/products/sony/sony-fe-35mm-f1-4-gm.jpg",
        "frontend/public/images/products/sony/sony-fe-50mm-f1-2-gm.jpg",
        "frontend/public/images/products/sony/sony-fe-70-200mm-f2-8-gm-oss-ii.jpg"
    ]

    for f_path in target_files:
        if os.path.exists(f_path):
            try:
                img = Image.open(f_path)
                # 使用 ImageOps.pad 進行等比例縮放，並將不足部分填補為純黑色，確保輸出嚴格為 450x450
                standardized_img = ImageOps.pad(img, (450, 450), color=(0, 0, 0))
                standardized_img.save(f_path, "JPEG", quality=90)
                print(f"RESIZED: {f_path} to 450x450")
            except Exception as e:
                print(f"ERROR processing {f_path}: {e}")
        else:
            print(f"MISSING: {f_path}")

if __name__ == "__main__":
    resize_to_standard()
