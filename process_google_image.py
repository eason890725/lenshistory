import sys
import os
from PIL import Image, ImageOps

def process_image(src_path, target_path):
    try:
        img = Image.open(src_path).convert("RGB")
        
        # 1. Basic auto-crop to remove white background if present
        # We find the bounding box of non-white pixels
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = Image.new(img.mode, img.size)
        import PIL.ImageChops as ImageChops
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        
        if bbox:
            img = img.crop(bbox)
        
        # 2. Resize to fit 410x410 (with 20px padding)
        target_size = 450
        padding = 20
        available_size = target_size - padding * 2
        
        w, h = img.size
        scale = min(available_size / w, available_size / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 3. Create black canvas and paste
        final_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
        paste_x = (target_size - new_w) // 2
        paste_y = (target_size - new_h) // 2
        final_img.paste(img, (paste_x, paste_y))
        
        final_img.save(target_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"Error processing {src_path}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process_google_image.py <src> <target>")
    else:
        process_image(sys.argv[1], sys.argv[2])
