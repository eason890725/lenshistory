import os
from PIL import Image

def overhaul_blackout():
    dirs = [
        "frontend/public/images/products/fujifilm",
        "frontend/public/images/products/sony"
    ]

    for d in dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".png"):
                src_path = os.path.join(d, f)
                dst_path = src_path.replace(".png", ".jpg")
                
                try:
                    img = Image.open(src_path).convert("RGBA")
                    datas = img.getdata()
                    newData = []
                    for item in datas:
                        # 門檻值 220
                        if item[0] > 220 and item[1] > 220 and item[2] > 220:
                            newData.append((0, 0, 0, 0))
                        else:
                            newData.append(item)
                    img.putdata(newData)
                    
                    background = Image.new("RGB", img.size, (0, 0, 0))
                    background.paste(img, mask=img.split()[3])
                    background.save(dst_path, "JPEG", quality=95)
                    print(f"OVERHAULED: {dst_path}")
                    os.remove(src_path)
                except Exception as e:
                    print(f"FAILED {src_path}: {e}")

if __name__ == "__main__":
    overhaul_blackout()
