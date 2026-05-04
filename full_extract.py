import pandas as pd
import json
import os
import re

def full_extract():
    excel_file = 'sony lens.xlsx'
    old_backup_file = 'frontend/src/data/products.json.pre_sony.bak'
    output_path = 'frontend/src/data/products.json'
    
    # 1. 讀取所有分頁
    xl = pd.ExcelFile(excel_file)
    print(f"Detected Sheets: {xl.sheet_names}")
    
    excel_products = []
    total_excel_rows = 0
    
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        total_excel_rows += len(df)
        
        # 尋找關鍵欄位 (適配不同分頁可能的名稱差異)
        name_col = next((c for c in df.columns if '鏡頭' in str(c)), None)
        if not name_col:
            continue
            
        for index, row in df.iterrows():
            model_name = str(row.get(name_col, '')).replace('\n', ' ').strip()
            if not model_name or model_name == 'nan' or '鏡頭' in model_name:
                continue
            
            # 數據清洗與映射
            price_raw = str(row.get('上市價\n$NTD', '0'))
            price = int(re.sub(r'[^\d]', '', price_raw)) if re.sub(r'[^\d]', '', price_raw) else 0
            
            year_raw = row.get('發表\n年份', 2024)
            try: year = int(year_raw)
            except: year = 2024
                
            # 提取焦段
            focal_length = str(row.get('焦段', ''))
            f_min = f_max = 0
            match = re.findall(r'\d+', focal_length)
            if len(match) >= 2:
                f_min, f_max = int(match[0]), int(match[1])
            elif match:
                f_min = f_max = int(match[0])

            excel_products.append({
                "id": 7000 + len(excel_products),
                "brand": "Sony",
                "modelName": model_name,
                "gearType": "LENS",
                "releaseYear": year,
                "launchPrice": price,
                "focalLengthMinMm": f_min,
                "focalLengthMaxMm": f_max,
                "apertureMax": str(row.get('最大\n光圈', '')).replace('\n', '').strip(),
                "filterSizeMm": str(row.get('濾鏡\n口徑', '')).replace('\n', '').strip(),
                "hasOIS": "有" in str(row.get('防\n手震', '')),
                "hasWeatherSeal": "有" in str(row.get('防\n塵滴', '')),
                "series": str(row.get('系列', '')).replace('\n', '').strip()
            })

    # 2. 讀取原始手動資料 (備份檔)
    with open(old_backup_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    # 3. 智能合併 (以名稱為 Key 去重)
    merged_dict = {item['modelName']: item for item in old_data}
    for item in excel_products:
        merged_dict[item['modelName']] = item
        
    final_list = list(merged_dict.values())
    
    # 4. 寫入 JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"TOTAL_EXCEL_ROWS:{total_excel_rows}")
    print(f"EXCEL_PRODUCTS_EXTRACTED:{len(excel_products)}")
    print(f"ORIGINAL_ITEMS:{len(old_data)}")
    print(f"FINAL_TOTAL:{len(final_list)}")
    print(f"LAST_10_ITEMS:" + "|".join([p['modelName'] for p in final_list[-10:]]))

if __name__ == "__main__":
    full_extract()
