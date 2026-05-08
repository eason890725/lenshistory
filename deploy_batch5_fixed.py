import os
from PIL import Image, ImageOps

def deploy_batch5_fixed():
    target_dir = "/mnt/c/personl/camera/lenshistory/frontend/public/images/products/sony"
    base_dir = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    mapping = [
        ("sony_a6400_strict_final_1778213064186.png", "sony-a6400.jpg"),
        ("sony_a6100_strict_final_1778212927194.png", "sony-a6100.jpg"),
        ("sony_zv_e10_strict_1778213256887.png", "sony-zv-e10.jpg"),
        ("sony_zv_1_ii_strict_final_1778213373392.png", "sony-zv-1-ii.jpg"),
        ("sony_zv_1f_strict_final_1778213478087.png", "sony-zv-1f.jpg"),
        ("sony_fe_24_240_strict_final_1778213605868.png", "sony-fe-24-240mm-f3-5-6-3-oss.jpg"),
        ("sony_fe_70_300_g_strict_final_1778213633893.png", "sony-fe-70-300mm-f4-5-5-6-g-oss.jpg"),
        ("sony_fe_40_g_strict_final_1778213653961.png", "sony-fe-40mm-f2-5-g.jpg"),
        ("sony_fe_50_g_strict_final_1778213664845.png", "sony-fe-50mm-f2-5-g.jpg"),
        ("sony_fe_24_g_strict_final_1778213712073.png", "sony-fe-24mm-f2-8-g.jpg")
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
    deploy_batch5_fixed()
