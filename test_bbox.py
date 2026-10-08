import os
from PIL import Image

def test_bright_bbox(src_path):
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    datas = img.getdata()
    mask_data = []
    
    # We want to find the camera. The camera has dark pixels.
    # The white lines are bright (R>150, G>150, B>150).
    for item in datas:
        # If it's pure black (background), ignore it
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            mask_data.append((0, 0, 0, 0))
        # If it's bright (the white lines), ignore it
        elif item[0] > 150 and item[1] > 150 and item[2] > 150:
            mask_data.append((0, 0, 0, 0))
        # Otherwise, it's the camera (dark/mid-tones)
        else:
            mask_data.append((255, 255, 255, 255))
            
    mask = Image.new("RGBA", img.size)
    mask.putdata(mask_data)
    
    bbox = mask.getbbox()
    if bbox:
        print(f"Found camera bbox: {bbox}")
        # Crop the ORIGINAL image
        cropped = img.crop(bbox)
        
        target_size = 450
        padding = 20
        available_size = target_size - padding * 2
        
        scale = min(available_size / cropped.width, available_size / cropped.height)
        new_w = int(cropped.width * scale)
        new_h = int(cropped.height * scale)
        
        resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        final_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
        paste_x = (target_size - new_w) // 2
        paste_y = (target_size - new_h) // 2
        final_img.paste(resized, (paste_x, paste_y))
        
        final_img.save("frontend/public/images/products/sony/sony-a9-iii_TEST_BBOX.jpg", "JPEG", quality=95)
    else:
        print("No bbox found")

test_bright_bbox("frontend/public/images/products/sony/sony-a9-iii.jpg")
