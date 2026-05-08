import os
import shutil
from PIL import Image, ImageOps

def deploy_batch2():
    target_dir = "frontend/public/images/products/sony"
    base_dir = "C:/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    mapping = [
        ("sony_a7cii_strict_1778205334218.png", "sony-a7c-ii.jpg"),
        ("sony_a7cr_strict_1778205355742.png", "sony-a7cr.jpg"),
        ("sony_zve1_strict_1778205424280.png", "sony-zv-e1.jpg"),
        ("sony_zve10ii_strict_1778205788394.png", "sony-zv-e10-ii.jpg"),
        ("sony_a6700_strict_1778205456991.png", "sony-a6700.jpg"),
        ("sony_fe_16_35_gm2_strict_1778205525013.png", "sony-fe-16-35mm-f2-8-gm-ii.jpg"),
        ("sony_fe_85_gm2_strict_1778205563233.png", "sony-fe-85mm-f1-4-gm-ii.jpg"),
        ("sony_fe_14_gm_strict_1778205656889.png", "sony-fe-14mm-f1-8-gm.jpg"),
        ("sony_fe_24_gm_strict_1778205684615.png", "sony-fe-24mm-f1-4-gm.jpg"),
        ("sony_fe_135_gm_strict_1778205725071.png", "sony-fe-135mm-f1-8-gm.jpg")
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
                
                # 執行精確的 450x450 等比例縮放與填補
                final_img = ImageOps.pad(background, (450, 450), color=(0, 0, 0))
                final_img.save(dst_path, "JPEG", quality=90)
                
                print(f"DEPLOYED & RESIZED: {dst_path}")
            except Exception as e:
                print(f"ERROR processing {src_name}: {e}")
        else:
            print(f"MISSING: {src_path}")

if __name__ == "__main__":
    deploy_batch2()
