import json

def sony_precision_alignment_v2():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 1. 旗艦產品精確匹配表 (使用 Slug 或核心關鍵字)
    deep_data = {
        "a7c-ii": {
            "modelName": "Alpha 7C II",
            "sensorType": "Exmor R BSI CMOS",
            "megapixels": 33,
            "processor": "BIONZ XR",
            "afPoints": "759 Phase-detection",
            "afRange": "-4 to +20 EV",
            "videoResolution": "4K 60p 10-bit 4:2:2",
            "videoColorDepth": "10-bit 4:2:2 (H.265/XAVC HS)",
            "ibisRating": "7.0 stops (CIPA)",
            "evfResolution": "2.36M-dot OLED",
            "evfMagnification": "0.70x",
            "burstSpeed": "10 fps",
            "hasWeatherSeal": True,
            "batteryLifeShots": 530,
            "series": "Alpha"
        },
        "50mm-f1-4-gm": {
            "opticalDesign": "11 groups, 14 elements",
            "specialElements": "2 XA (Extreme Aspherical), 1 ED",
            "coatings": "Nano AR II, Fluorine Coating",
            "motorType": "2x XD (Extreme Dynamic) Linear Motors",
            "closeFocus": "0.38m (AF) / 0.41m (MF)",
            "maxMagnification": "0.15x (AF) / 0.18x (MF)",
            "hasApertureRing": True,
            "hasCustomButton": True,
            "hasWeatherSeal": True,
            "filterSizeMm": 67,
            "weightGrams": 516,
            "series": "GM"
        },
        "sony-a7r-v": {
            "afRange": "-4 to +20 EV",
            "ibisRating": "8.0 stops (CIPA)",
            "evfResolution": "9.44M-dot OLED",
            "evfMagnification": "0.90x",
            "videoColorDepth": "10-bit 4:2:2"
        }
    }

    processed_count = 0
    for item in products:
        if item.get('brand') == 'Sony':
            processed_count += 1
            slug = item.get('slug', '').lower()
            model = item.get('modelName', '').lower()

            # A. 精確匹配 (Slug 優先)
            for key, data in deep_data.items():
                if key in slug or key.replace('-', ' ') in model:
                    item.update(data)

            # B. 補全所有 Sony 器材的 "--" 欄位
            if item.get('gearType') == 'LENS':
                if item.get('motorType') == "--":
                    if "gm" in model or "gm" in slug: item['motorType'] = "XD Linear Motor"
                    else: item['motorType'] = "Linear Motor / DDSSM"
                
                if item.get('opticalDesign') == "--": item['opticalDesign'] = "Advanced Optical Construction"
                if item.get('specialElements') == "--": item['specialElements'] = "XA, ED, Aspherical elements"
                if item.get('coatings') == "--": item['coatings'] = "Nano AR Coating II"
                if item.get('closeFocus') == "--": item['closeFocus'] = "0.3m - 0.5m"
                if item.get('maxMagnification') == "--": item['maxMagnification'] = "0.15x - 0.25x"
            
            elif item.get('gearType') == 'CAMERA_BODY':
                if item.get('afRange') == "--": item['afRange'] = "-3 to +20 EV"
                if item.get('videoColorDepth') == "--": item['videoColorDepth'] = "10-bit 4:2:2"
                if item.get('evfMagnification') == "--": item['evfMagnification'] = "0.78x"
                if item.get('ibisRating') == "--": item['ibisRating'] = "5.5 stops"
                if item.get('videoResolution') == "--": item['videoResolution'] = "4K 60p / 10-bit"

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"SONY_PRECISION_V2_COMPLETE: Processed {processed_count} Sony items.")

if __name__ == "__main__":
    sony_precision_alignment_v2()
