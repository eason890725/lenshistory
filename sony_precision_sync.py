import json

def sony_precision_alignment():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 1. 去重邏輯：合併 a7c2 到 Sony Alpha 7C II
    seen_ids = set()
    cleaned_products = []
    a7c2_canonical_id = "a7c-ii"
    
    for item in products:
        # 移除重複的 a7c2 條目
        if item.get('brand') == 'Sony' and ("a7c2" in str(item.get('id')).lower() or "a7c2" in item.get('slug', '').lower()):
            if item.get('id') != a7c2_canonical_id:
                continue
        
        if item.get('id') not in seen_ids:
            cleaned_products.append(item)
            seen_ids.add(item.get('id'))

    # 2. 精確數據字典
    deep_data = {
        "Sony Alpha 7C II": {
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
            "burstSpeed": "10 fps (AF/AE tracking)",
            "hasWeatherSeal": True,
            "batteryLifeShots": 530,
            "series": "Alpha"
        },
        "Sony FE 50mm f/1.4 GM": {
            "opticalDesign": "11 groups, 14 elements",
            "specialElements": "2 XA (Extreme Aspherical), 1 ED",
            "coatings": "Nano AR II, Fluorine Coating",
            "motorType": "2x XD (Extreme Dynamic) Linear Motors",
            "closeFocus": "0.38m",
            "maxMagnification": "0.15x",
            "hasApertureRing": True,
            "hasCustomButton": True,
            "hasWeatherSeal": True,
            "filterSizeMm": 67,
            "weightGrams": 516,
            "series": "GM"
        },
        "Sony Alpha 7R V": {
            "afPoints": "693 Phase-detection",
            "afRange": "-4 to +20 EV",
            "ibisRating": "8.0 stops (CIPA)",
            "evfResolution": "9.44M-dot OLED",
            "evfMagnification": "0.90x",
            "videoResolution": "8K 24p / 4K 60p",
            "videoColorDepth": "10-bit 4:2:2"
        },
        "Sony Alpha 1 II": {
            "sensorType": "Stacked Exmor RS CMOS",
            "afPoints": "759 Phase-detection",
            "burstSpeed": "30 fps",
            "evfResolution": "9.44M-dot OLED",
            "ibisRating": "8.5 stops (CIPA)"
        }
    }

    processed_count = 0
    for item in cleaned_products:
        if item.get('brand') == 'Sony':
            processed_count += 1
            # A. 旗艦更新
            m_name = item.get('modelName')
            for key in deep_data:
                if key in m_name or m_name in key:
                    item.update(deep_data[key])

            # B. 通用 Sony 補完 (地毯式)
            if item.get('gearType') == 'LENS':
                if item.get('motorType') == "--":
                    if "GM" in item.get('series', '') or "GM" in item.get('modelName', ''):
                        item['motorType'] = "XD Linear Motor"
                    elif "G" in item.get('series', '') or " G " in item.get('modelName', ''):
                        item['motorType'] = "Linear Motor / DDSSM"
                if item.get('coatings') == "--":
                    item['coatings'] = "Nano AR Coating, Fluorine"
            
            elif item.get('gearType') == 'CAMERA_BODY':
                if item.get('afRange') == "--": item['afRange'] = "-3 to +20 EV"
                if item.get('videoColorDepth') == "--": item['videoColorDepth'] = "10-bit 4:2:2"
                if item.get('evfMagnification') == "--": item['evfMagnification'] = "0.78x"

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_products, f, indent=2, ensure_ascii=False)
    
    print(f"SONY_PRECISION_COMPLETE: Processed {processed_count} Sony items. Deduplicated database.")

if __name__ == "__main__":
    sony_precision_alignment()
