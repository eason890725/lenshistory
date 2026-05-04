import pandas as pd
import json
import os
import re

def precise_fix_and_import():
    excel_file = 'sony lens.xlsx'
    old_backup_file = 'frontend/src/data/products.json.pre_sony.bak'
    output_path = 'frontend/src/data/products.json'
    
    # 1. 讀取 Excel (跳過可能存在的次表頭列)
    xl = pd.ExcelFile(excel_file)
    all_excel_items = []
    
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        
        # 尋找「廠牌」欄位
        brand_col = '廠牌'
        name_col = next((c for c in df.columns if '鏡頭' in str(c)), None)
        
        if not name_col:
            continue
            
        for index, row in df.iterrows():
            brand_val = str(row.get(brand_col, 'Sony')).strip()
            model_name = str(row.get(name_col, '')).replace('\n', ' ').strip()
            
            # 過濾次表頭或無效行
            if brand_val == 'Brand' or not model_name or model_name == 'nan' or '鏡頭' in model_name:
                continue
            
            # 廠牌安全檢查：如果抓到的是無意義字串，強制設為 Sony
            if brand_val in ['nan', '', 'DG DN', 'Series'] or re.match(r'^\d+$', brand_val):
                brand_val = 'Sony'

            # 提取焦段與價格 (保持之前成功的邏輯)
            price_raw = str(row.get('上市價\n$NTD', '0'))
            price = int(re.sub(r'[^\d]', '', price_raw)) if re.sub(r'[^\d]', '', price_raw) else 0
            year_raw = row.get('發表\n年份', 2024)
            try: year = int(year_raw)
            except: year = 2024

            all_excel_items.append({
                "id": 8000 + len(all_excel_items),
                "brand": brand_val,
                "modelName": model_name,
                "gearType": "LENS",
                "releaseYear": year,
                "launchPrice": price,
                "apertureMax": str(row.get('最大\n光圈', '')).replace('\n', '').strip(),
                "filterSizeMm": str(row.get('濾鏡\n口徑', '')).replace('\n', '').strip(),
                "series": str(row.get('系列', '')).replace('\n', '').strip()
            })

    # 2. 讀取原始手動資料 (備份檔) 並去重合併
    with open(old_backup_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    # 建立合併字典
    merged_dict = {item['modelName']: item for item in old_data}
    
    # 強制用 Excel 的「正確廠牌」覆蓋
    for item in all_excel_items:
        merged_dict[item['modelName']] = item
        
    final_list = list(merged_dict.values())
    
    # 3. 對帳
    sony_in_json = len([p for p in final_list if p['brand'] == 'Sony'])
    excel_total_rows = len(all_excel_items)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"EXCEL_TOTAL_RECORDS:{excel_total_rows}")
    print(f"SONY_ITEMS_IN_JSON:{sony_in_json}")
    print(f"FINAL_TOTAL_JSON:{len(final_list)}")
    
    # 選取 5 筆隨機樣本
    import random
    sample = random.sample(final_list, min(5, len(final_list)))
    print("--- SAMPLES ---")
    for s in sample:
        print(f"[{s['brand']}] {s['modelName']} ({s.get('apertureMax', 'N/A')})")

if __name__ == "__main__":
    precise_fix_and_import()
