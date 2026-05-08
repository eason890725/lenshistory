import os
from PIL import Image

def convert_and_blackout_sony():
    target_dir = "frontend/public/images/products/sony"
    files = [
        "sony-a1-ii.png", "sony-a9-iii.png", "sony-a7r-v.png", "sony-a7-v.png", "sony-a7c-ii.png",
        "sony-fe-28-70mm-f2-gm.png", "sony-fe-24-70mm-f2-8-gm-ii.png", "sony-fe-70-200mm-f2-8-gm-oss-ii.png",
        "sony-fe-50mm-f1-2-gm.png", "sony-fe-85mm-gm-ii.png"
    ]

    for f in files:
        src_path = os.path.join(target_dir, f)
        dst_path = src_path.replace(".png", ".jpg")
        
        if os.path.exists(src_path):
            try:
                img = Image.open(src_path).convert("RGBA")
                datas = img.getdata()
                newData = []
                for item in datas:
                    if item[0] > 220 and item[1] > 220 and item[2] > 220:
                        newData.append((0, 0, 0, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                background = Image.new("RGB", img.size, (0, 0, 0))
                background.paste(img, mask=img.split()[3])
                background.save(dst_path, "JPEG", quality=95)
                print(f"SUCCESS: {dst_path}")
                os.remove(src_path)
            except Exception as e:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    convert_and_blackout_sony()
