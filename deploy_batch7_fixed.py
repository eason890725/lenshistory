import os
from PIL import Image, ImageOps

def deploy_batch7_fixed():
    target_dir = "/mnt/c/personl/camera/lenshistory/frontend/public/images/products/sony"
    base_dir = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    mapping = [
        ("sony_fe_35_f28_za_strict_final_1778221137143.png", "sony-sonnar-t-fe-35mm-f2-8-za.jpg"),
        ("sony_fe_16_35_f4_za_strict_final_1778221202740.png", "sony-vario-tessar-t-fe-16-35mm-f4-za-oss.jpg"),
        ("sony_fe_24_70_f4_za_strict_final_1778221241755.png", "sony-vario-tessar-t-fe-24-70mm-f4-za-oss.jpg"),
        ("sony_fe_35_f14_za_strict_final_1778221287003.png", "sony-distagon-t-fe-35mm-f1-4-za.jpg"),
        ("sony_fe_28_f2_strict_final_1778221321088.png", "sony-fe-28mm-f2.jpg"),
        ("sony_fe_50_f28_macro_strict_final_1778221380872.png", "sony-fe-50mm-f2-8-macro.jpg"),
        ("sony_e_10_20_g_strict_final_1778221458611.png", "sony-e-pz-10-20mm-f4-g.jpg"),
        ("sony_e_15_g_strict_final_1778221515372.png", "sony-e-15mm-f1-4-g.jpg"),
        ("sony_e_35_f18_strict_final_1778221547486.png", "sony-e-35mm-f1-8-oss.jpg"),
        ("sony_e_50_f18_strict_final_1778221602642.png", "sony-e-50mm-f1-8-oss.jpg")
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
    deploy_batch7_fixed()
