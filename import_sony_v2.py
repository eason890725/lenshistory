import pandas as pd
import json
import os
import re

def run_import():
    excel_file = 'sony lens.xlsx'
    output_path = 'frontend/src/data/products.json'
    
    df = pd.read_excel(excel_file)
    
    products = []
    for index, row in df.iterrows():
        # 清理換行符號
        model_name = str(row.get('鏡頭\n(更新時間：2026.02.25)', '')).replace('\n', ' ').strip()
        if not model_name or model_name == 'nan':
            continue
            
        # 處理價格 (移除逗號並轉為數字)
        price_raw = str(row.get('上市價\n$NTD', '0'))
        price = re.sub(r'[^\d]', '', price_raw)
        price = int(price) if price else 0
        
        # 處理年份
        year_raw = row.get('發表\n年份', 2024)
        try:
            year = int(year_raw)
        except:
            year = 2024
            
        # 提取焦段資訊
        focal_length = str(row.get('焦段', ''))
        f_min = 0
        f_max = 0
        if '-' in focal_length:
            match = re.findall(r'\d+', focal_length)
            if len(match) >= 2:
                f_min = int(match[0])
                f_max = int(match[1])
        else:
            match = re.findall(r'\d+', focal_length)
            if match:
                f_min = f_max = int(match[0])

        item = {
            "id": 6000 + index,
            "brand": "Sony",
            "modelName": model_name,
            "gearType": "LENS",
            "releaseYear": year,
            "launchPrice": price,
            "focalLengthMinMm": f_min,
            "focalLengthMaxMm": f_max,
            "apertureMax": str(row.get('最大\n光圈', '')).replace('\n', ''),
            "filterSizeMm": str(row.get('濾鏡\n口徑', '')).replace('\n', ''),
            "weightGrams": str(row.get('重量', '')).replace('\n', ''),
            "hasOIS": "有" in str(row.get('防\n手震', '')),
            "hasWeatherSeal": "有" in str(row.get('防\n塵滴', '')),
            "hasApertureRing": "有" in str(row.get('光圈\n環', '')),
            "series": str(row.get('系列', '')).replace('\n', '')
        }
        products.append(item)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Imported {len(products)} real Sony lenses.")
    for p in products[:5]:
        print(f"- {p['modelName']}")

if __name__ == "__main__":
    run_import()
