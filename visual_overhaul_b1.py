import json
import os
from PIL import Image

def process_batch1_visuals():
    target_fuji = "frontend/public/images/products/fujifilm"
    target_sony = "frontend/public/images/products/sony"
    base_dir = "C:/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    # 映射表: 暫存檔名 -> 目標檔名 (格式: [(src, dst_dir, dst_name), ...])
    mapping = [
        ("fujifilm_xf_100_400_1778203399840.png", target_fuji, "fujifilm-xf-100-400mm-f4-5-5-6-r-lm-ois-wr.jpg"),
        ("fujifilm_gfx_50sii_1778203431085.png", target_fuji, "fujifilm-gfx-50s-ii.jpg"),
        ("sony_a1ii_1778203459491.png", target_sony, "sony-a1-ii.jpg"),
        ("sony_a9iii_1778203479033.png", target_sony, "sony-a9-iii.jpg"),
        ("sony_a7rv_1778203505924.png", target_sony, "sony-a7r-v.jpg"),
        ("sony_a7v_final_1778203537606.png", target_sony, "sony-a7-v.jpg"),
        ("sony_fe_24_70_gm_ii_1778203557822.png", target_sony, "sony-fe-24-70mm-f2-8-gm-ii.jpg"),
        ("sony_fe_70_200_gm_ii_final_1778203588828.png", target_sony, "sony-fe-70-200mm-f2-8-gm-oss-ii.jpg"),
        ("sony_fe_35_gm_1778203611605.png", target_sony, "sony-fe-35mm-f1-4-gm.jpg"),
        ("sony_fe_50_gm_1778203632764.png", target_sony, "sony-fe-50mm-f1-2-gm.jpg")
    ]

    def process_to_black(src, dst):
        try:
            img = Image.open(src).convert("RGBA")
            datas = img.getdata()
            newData = []
            for item in datas:
                # 高強度白轉黑 (R,G,B > 220)
                if item[0] > 220 and item[1] > 220 and item[2] > 220:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            background = Image.new("RGB", img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3])
            background.save(dst, "JPEG", quality=95)
            print(f"DEPLOYED: {dst}")
        except Exception as e:
            print(f"ERROR processing {src}: {e}")

    for src_name, dst_dir, dst_name in mapping:
        src_path = os.path.join(base_dir, src_name)
        dst_path = os.path.join(dst_dir, dst_name)
        if os.path.exists(src_path):
            process_to_black(src_path, dst_path)
        else:
            print(f"MISSING: {src_path}")

if __name__ == "__main__":
    process_batch1_visuals()
