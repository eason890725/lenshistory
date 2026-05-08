import json
import os
from PIL import Image

def finalize_sony_visuals():
    target_dir = "frontend/public/images/products/sony"
    base_dir = "C:/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    if not os.path.exists(target_dir): os.makedirs(target_dir)
    
    mapping = {
        "sony_a1_ii_1778145624862.png": "sony-a1-ii.jpg",
        "sony_a9_iii_1778145655971.png": "sony-a9-iii.jpg",
        "sony_a7r_v_1778145673318.png": "sony-a7r-v.jpg",
        "sony_a7_v_1778145705334.png": "sony-a7-v.jpg",
        "sony_a7c_ii_1778145815318.png": "sony-a7c-ii.jpg",
        "sony_fe_28_70mm_f2_gm_1778145847037.png": "sony-fe-28-70mm-f2-gm.jpg",
        "sony_fe_24_70mm_gm_ii_1778145871789.png": "sony-fe-24-70mm-f2-8-gm-ii.jpg",
        "sony_fe_70_200mm_gm_ii_1778145889813.png": "sony-fe-70-200mm-f2-8-gm-oss-ii.jpg",
        "sony_fe_50mm_f1_2_gm_1778145907699.png": "sony-fe-50mm-f1-2-gm.jpg",
        "sony_fe_85mm_gm_ii_1778145928655.png": "sony-fe-85mm-gm-ii.jpg"
    }

    def process_to_black(src, dst):
        try:
            img = Image.open(src).convert("RGBA")
            datas = img.getdata()
            newData = []
            for item in datas:
                # 官網白底通常非常純淨 (R,G,B > 220)
                if item[0] > 220 and item[1] > 220 and item[2] > 220:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            background = Image.new("RGB", img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3])
            background.save(dst, "JPEG", quality=95)
            print(f"SUCCESS: {dst}")
        except Exception as e:
            print(f"ERROR: {e}")

    for src_name, dst_name in mapping.items():
        src_path = os.path.join(base_dir, src_name)
        dst_path = os.path.join(target_dir, dst_name)
        if os.path.exists(src_path):
            process_to_black(src_path, dst_path)
        else:
            print(f"MISSING: {src_path}")

if __name__ == "__main__":
    finalize_sony_visuals()
