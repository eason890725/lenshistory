import sys
import os
from PIL import Image, ImageDraw

def process_screenshot(src_path, target_path):
    try:
        img = Image.open(src_path).convert("RGB")
        w, h = img.size
        
        # 1. Edge crop (15%)
        img = img.crop((int(w*0.15), int(h*0.15), int(w*0.85), int(h*0.85)))
        w, h = img.size
        
        # 2. Advanced Background Removal
        gray = img.convert("L")
        mask = Image.new("L", (w, h), 255) # Start with everything as "Camera"
        
        # Flood fill from edges to identify "Background"
        # We fill with 0 (Black = Background)
        # We check perimeter points
        for x in [0, w-1]:
            for y in range(0, h, 20):
                ImageDraw.floodfill(mask, (x, y), 0, thresh=50)
        for y in [0, h-1]:
            for x in range(0, w, 20):
                ImageDraw.floodfill(mask, (x, y), 0, thresh=50)
                
        # Additionally, any pixel that is very bright is DEFINITELY background
        # (This handles disconnected white areas)
        datas = list(gray.getdata())
        mask_data = list(mask.getdata())
        new_mask_data = []
        for g, m in zip(datas, mask_data):
            if g > 235: # Pure white-ish
                new_mask_data.append(0)
            else:
                new_mask_data.append(m)
        mask.putdata(new_mask_data)
        
        cam_bbox = mask.getbbox()
        if not cam_bbox:
            print(f"Error: Could not isolate camera in {src_path}")
            return False
            
        tight_cam = img.crop(cam_bbox)
        
        # 3. Final Canvas
        target_size = 450
        padding = 10
        available_size = target_size - padding * 2
        
        tw, th = tight_cam.size
        scale = min(available_size / tw, available_size / th)
        new_w = int(tw * scale)
        new_h = int(th * scale)
        
        resized = tight_cam.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        final_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
        paste_x = (target_size - new_w) // 2
        paste_y = (target_size - new_h) // 2
        final_img.paste(resized, (paste_x, paste_y))
        
        final_img.save(target_path, "JPEG", quality=95)
        print(f"PROFESSIONAL FIX v2: {target_path} - BBox: {cam_bbox}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ultimate_screenshot_processor.py <src> <target>")
    else:
        process_screenshot(sys.argv[1], sys.argv[2])
