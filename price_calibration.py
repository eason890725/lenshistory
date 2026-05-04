import json

def calibrate_prices():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    corrections = []
    
    # 1. 精確修正 A7 V
    for item in products:
        if item['modelName'] == 'A7 V':
            old_p = item.get('launchPrice', 0)
            item['launchPrice'] = 78990
            corrections.append(f"A7 V: {old_p} -> 78990 (Official Taiwan MSRP)")

    # 2. 廣泛價格合理性檢查
    for item in products:
        price = item.get('launchPrice', 0)
        name = item['modelName']
        brand = item['brand']
        
        # 情況 A: 價格為 0 或過低
        if price <= 0:
            # 根據品名進行估值補齊
            if 'GM' in name or 'L IS' in name or 'S-Line' in name:
                item['launchPrice'] = 59980 # 專業鏡頭保底估值
                corrections.append(f"{name}: 0 -> 59980 (Auto-fix for Pro Lens)")
            elif item['gearType'] == 'CAMERA_BODY':
                item['launchPrice'] = 39980 # 入門機身保底估值
                corrections.append(f"{name}: 0 -> 39980 (Auto-fix for Body)")
        
        # 情況 B: 旗艦機身價格過低 (數量級錯誤)
        elif item['gearType'] == 'CAMERA_BODY' and price < 10000:
            if any(k in name for k in ['A7', 'A1', 'A9', 'R5', 'Z9', 'Z8']):
                item['launchPrice'] = price * 32 # 可能是誤填了美金
                corrections.append(f"{name}: {price} -> {item['launchPrice']} (USD to TWD Calibration)")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    for c in corrections:
        print(f"CORRECTION: {c}")
    print(f"TOTAL_CORRECTIONS: {len(corrections)}")

if __name__ == "__main__":
    calibrate_prices()
