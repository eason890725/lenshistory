import json
import os
import shutil
from PIL import Image

def finalize_fujifilm_visuals():
    target_dir = "frontend/public/images/products/fujifilm"
    artifact_dir = "C:/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265/artifacts"
    
    # 映射表: 暫存檔名 -> 目標檔名
    mapping = {
        "fujifilm_x_e5_1778136905538.png": "fujifilm-x-e5.jpg",
        "fujifilm_x100vi_1778136974653.png": "fujifilm-x100vi.jpg",
        "fujifilm_x_m5_1778137033453.png": "fujifilm-x-m5.jpg",
        "fujifilm_gfx_50s_ii_1778141849888.png": "fujifilm-gfx-50s-ii.jpg",
        "fujifilm_xf_100_400mm_f4_5_5_6_r_lm_ois_wr_1778141916707.png": "fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr.jpg"
    }

    def process_to_black(src, dst):
        try:
            img = Image.open(src).convert("RGBA")
            datas = img.getdata()
            newData = []
            for item in datas:
                # 高強度白轉黑門檻 (R,G,B > 200 視為背景)
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            
            background = Image.new("RGB", img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3])
            background.save(dst, "JPEG", quality=95)
            print(f"Processed and saved: {dst}")
        except Exception as e:
            print(f"Error processing {src}: {e}")

    for src_name, dst_name in mapping.items():
        src_path = os.path.join(artifact_dir, src_name)
        dst_path = os.path.join(target_dir, dst_name)
        if os.path.exists(src_path):
            process_to_black(src_path, dst_path)
        else:
            print(f"Artifact not found: {src_path}")

    print("Fujifilm Final Visual Deployment Complete.")

if __name__ == "__main__":
    finalize_fujifilm_visuals()
