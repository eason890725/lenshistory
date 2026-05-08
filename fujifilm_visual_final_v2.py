import json
import os
from PIL import Image

def finalize_fujifilm_visuals_v2():
    target_dir = "frontend/public/images/products/fujifilm"
    base_dir = "C:/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
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
                # 門檻值調整為 220
                if item[0] > 220 and item[1] > 220 and item[2] > 220:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            background = Image.new("RGB", img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3])
            background.save(dst, "JPEG", quality=95)
            print(f"SUCCESS: Processed {dst}")
        except Exception as e:
            print(f"ERROR processing {src}: {e}")

    for src_name, dst_name in mapping.items():
        src_path = os.path.join(base_dir, src_name)
        dst_path = os.path.join(target_dir, dst_name)
        if os.path.exists(src_path):
            process_to_black(src_path, dst_path)
        else:
            print(f"MISSING: {src_path}")

if __name__ == "__main__":
    finalize_fujifilm_visuals_v2()
