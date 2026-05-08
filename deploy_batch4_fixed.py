import os
from PIL import Image, ImageOps

def deploy_batch4_fixed():
    target_dir = "/mnt/c/personl/camera/lenshistory/frontend/public/images/products/sony"
    base_dir = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    mapping = [
        # Priority Fix
        ("sony_fe_28_70_gm_isolated_1778212107483.png", "sony-fe-28-70mm-f2-gm.jpg"),
        # Batch 4
        ("sony_fe_50_f14_gm_strict_1778211745889.png", "sony-fe-50mm-f1-4-gm.jpg"),
        ("sony_fe_12_24_gm_strict_1778211758051.png", "sony-fe-12-24mm-f2-8-gm.jpg"),
        ("sony_fe_100_400_gm_strict_1778211771113.png", "sony-fe-100-400mm-f4-5-5-6-gm-oss.jpg"),
        ("sony_fe_pz_16_35_f4_g_strict_1778211792490.png", "sony-fe-pz-16-35mm-f4-g.jpg"),
        ("sony_fe_70_200_f4_macro_g_oss_ii_strict_1778211803909.png", "sony-fe-70-200mm-f4-macro-g-oss-ii.jpg"),
        ("sony_fe_20_f18_g_strict_1778211816371.png", "sony-fe-20mm-f1-8-g.jpg"),
        ("sony_fe_35_f18_strict_1778211831893.png", "sony-fe-35mm-f1-8.jpg"),
        ("sony_fe_85_f18_strict_1778211851398.png", "sony-fe-85mm-f1-8.jpg"),
        ("sony_fe_55_f18_za_strict_1778211871438.png", "sony-sonnar-t-fe-55mm-f1-8-za.jpg"),
        ("sony_e_16_55_f28_g_strict_1778211883025.png", "sony-e-16-55mm-f2-8-g.jpg")
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
                    # 門檻值 230，確保官網純淨白底能完美被剔除
                    if item[0] > 230 and item[1] > 230 and item[2] > 230:
                        newData.append((0, 0, 0, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                
                background = Image.new("RGB", img.size, (0, 0, 0))
                background.paste(img, mask=img.split()[3])
                
                # 嚴格 450x450 填補
                final_img = ImageOps.pad(background, (450, 450), color=(0, 0, 0))
                final_img.save(dst_path, "JPEG", quality=90)
                
                print(f"DEPLOYED & RESIZED: {dst_name} to 450x450")
            except Exception as e:
                print(f"ERROR processing {src_name}: {e}")
        else:
            print(f"MISSING: {src_path}")

if __name__ == "__main__":
    deploy_batch4_fixed()
