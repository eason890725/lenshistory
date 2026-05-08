import os
from PIL import Image, ImageOps

def deploy_batch3_fixed():
    target_dir = "/mnt/c/personl/camera/lenshistory/frontend/public/images/products/sony"
    base_dir = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    mapping = [
        ("sony_a7siii_strict_png_1778205985406.png", "sony-a7s-iii.jpg"),
        ("sony_a9ii_strict_png_1778206030596.png", "sony-a9-ii.jpg"),
        ("sony_a7iv_strict_png_1778206077663.png", "sony-a7-iv.jpg"),
        ("sony_a7c_strict_png_1778206200358.png", "sony-a7c.jpg"),
        ("sony_a6600_strict_png_1778206629994.png", "sony-a6600.jpg"),
        ("sony_fe_400_gm_strict_png_1778206690086.png", "sony-fe-400mm-f2-8-gm-oss.jpg"),
        ("sony_fe_600_gm_strict_png_1778206754045.png", "sony-fe-600mm-f4-gm-oss.jpg"),
        ("sony_fe_200_600_g_strict_png_1778206814921.png", "sony-fe-200-600mm-f5-6-6-3-g-oss.jpg"),
        ("sony_fe_90_macro_g_strict_png_1778206876420.png", "sony-fe-90mm-f2-8-macro-g-oss.jpg"),
        ("sony_fe_24_105_g_strict_png_1778206921803.png", "sony-fe-24-105mm-f4-g-oss.jpg")
    ]

    for src_name, dst_name in mapping:
        src_path = os.path.join(base_dir, src_name)
        dst_path = os.path.join(target_dir, dst_name)
        
        if os.path.exists(src_path):
            try:
                img = Image.open(src_path).convert("RGBA")
                datas = img.getdata()
                newData = []
                for item in datas:
                    if item[0] > 230 and item[1] > 230 and item[2] > 230:
                        newData.append((0, 0, 0, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                
                background = Image.new("RGB", img.size, (0, 0, 0))
                background.paste(img, mask=img.split()[3])
                
                final_img = ImageOps.pad(background, (450, 450), color=(0, 0, 0))
                final_img.save(dst_path, "JPEG", quality=90)
                
                print(f"DEPLOYED & RESIZED: {dst_name} to 450x450")
            except Exception as e:
                print(f"ERROR processing {src_name}: {e}")
        else:
            print(f"MISSING: {src_path}")

if __name__ == "__main__":
    deploy_batch3_fixed()
