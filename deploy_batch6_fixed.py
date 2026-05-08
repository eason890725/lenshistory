import os
from PIL import Image, ImageOps

def deploy_batch6_fixed():
    target_dir = "/mnt/c/personl/camera/lenshistory/frontend/public/images/products/sony"
    base_dir = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    mapping = [
        ("sony_a6500_strict_final_1778218905228.png", "sony-a6500.jpg"),
        ("sony_a6300_strict_final_1778219630402.png", "sony-a6300.jpg"),
        ("sony_a6000_strict_final_1778220323830.png", "sony-a6000.jpg"),
        ("sony_rx100_vii_strict_final_1778220396641.png", "sony-cyber-shot-rx100-vii.jpg"),
        ("sony_rx10_iv_strict_final_body_1778220451777.png", "sony-cyber-shot-rx10-iv.jpg"),
        ("sony_fe_24_70_f28_gm_strict_final_1778220511408.png", "sony-fe-24-70mm-f2-8-gm.jpg"),
        ("sony_fe_70_200_f28_gm_strict_final_body_1778220555642.png", "sony-fe-70-200mm-f2-8-gm-oss.jpg"),
        ("sony_fe_16_35_f28_gm_strict_final_body_1778220605928.png", "sony-fe-16-35mm-f2-8-gm.jpg"),
        ("sony_fe_85_f14_gm_strict_final_body_1778220652674.png", "sony-fe-85mm-f1-4-gm.jpg"),
        ("sony_fe_50_f18_strict_final_body_1778220710314.png", "sony-fe-50mm-f1-8.jpg")
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
    deploy_batch6_fixed()
