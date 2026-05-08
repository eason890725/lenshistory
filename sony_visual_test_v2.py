import os
from PIL import Image

def test_blackout_sample_fixed():
    src_path = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265/sony_a7s3_test_v68_1778146587897.png"
    dst_path = "/mnt/c/Users/eason/.gemini/antigravity/brain/c02609d0-36ed-440a-8e76-b5302abbe265/sony_a7s3_v68_final_sample.jpg"
    
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
            background.save(dst_path, "JPEG", quality=95)
            print(f"SUCCESS: Sample processed to {dst_path}")
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print(f"Source image not found at {src_path}")

if __name__ == "__main__":
    test_blackout_sample_fixed()
