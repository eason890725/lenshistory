import sys
import os
import requests
from PIL import Image, ImageOps

def optimize_product_image(src_path, target_path):
    """
    Implements Rule 16: Auto-Crop (Threshold > 240) and 450x450 Black Canvas Reconstruction.
    """
    try:
        # Load image and convert to RGB
        img = Image.open(src_path).convert("RGB")
        
        # 1. Auto-Crop: Detect and remove white padding (Threshold > 240)
        # We also remove black padding just in case.
        gray = img.convert("L")
        
        # Create mask: Pixels that are NOT white (>240) AND NOT pure black (<5)
        # We want to isolate the product body.
        # However, if the product is on a pure white background, we just need to remove white.
        # If it's on a pure black background, we just need to remove black.
        
        # Strategy: Find pixels that are different from the corner color
        corner_color = gray.getpixel((0, 0))
        if corner_color > 240: # White background
            mask = gray.point(lambda p: 255 if p < 240 else 0)
        elif corner_color < 15: # Black background
            mask = gray.point(lambda p: 255 if p > 15 else 0)
        else: # Mixed or grey
            mask = gray.point(lambda p: 255 if abs(p - corner_color) > 30 else 0)
            
        bbox = mask.getbbox()
        if not bbox:
            print(f"Warning: Could not detect product in {src_path}. Using full image.")
            bbox = (0, 0, img.width, img.height)
            
        product = img.crop(bbox)
        
        # 2. Canvas Reconstruction: Center on 450x450 black canvas
        target_size = 450
        padding = 20
        max_dim = target_size - (padding * 2)
        
        pw, ph = product.size
        scale = min(max_dim / pw, max_dim / ph)
        new_w, new_h = int(pw * scale), int(ph * scale)
        
        resized_product = product.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Create black canvas
        canvas = Image.new("RGB", (target_size, target_size), (0, 0, 0))
        
        # Paste centered
        offset_x = (target_size - new_w) // 2
        offset_y = (target_size - new_h) // 2
        canvas.paste(resized_product, (offset_x, offset_y))
        
        # Save as JPEG (or PNG if transparency is needed, but user requested RGB 0,0,0 canvas)
        canvas.save(target_path, "JPEG", quality=95)
        print(f"SUCCESS: Optimized {target_path} (Original: {pw}x{ph} -> Crop: {bbox})")
        return True
    except Exception as e:
        print(f"ERROR optimizing {src_path}: {e}")
        return False

def download_image(url, local_path):
    """
    Rule 15: Download binary stream using requests.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            print(f"Failed to download {url}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"Download Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        optimize_product_image(sys.argv[1], sys.argv[2])
