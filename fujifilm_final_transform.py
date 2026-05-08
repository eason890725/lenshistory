import os
from PIL import Image

def convert_and_blackout():
    target_dir = "frontend/public/images/products/fujifilm"
    files = [
        "fujifilm-x-e5.png",
        "fujifilm-x100vi.png",
        "fujifilm-x-m5.png",
        "fujifilm-gfx-50s-ii.png",
        "fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr.png"
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
                    if item[0] > 200 and item[1] > 200 and item[2] > 200:
                        newData.append((0, 0, 0, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                
                background = Image.new("RGB", img.size, (0, 0, 0))
                background.paste(img, mask=img.split()[3])
                background.save(dst_path, "JPEG", quality=95)
                print(f"SUCCESS: {dst_path}")
                # 刪除原始 png
                os.remove(src_path)
            except Exception as e:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    convert_and_blackout()
