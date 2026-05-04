import pandas as pd
import json
import os
import re

def clean_unit(val, unit):
    if not val or str(val) == 'nan': return "--"
    s = str(val).strip()
    # 如果已經包含單位，就不再重複處理 (例如 f/1.4 -> 1.4)
    s = s.replace(unit, '').strip()
    return s

def run_import():
    excel_file = 'sony lens.xlsx'
    old_backup_file = 'frontend/src/data/products.json.pre_sony.bak'
    output_path = 'frontend/src/data/products.json'
    
    xl = pd.ExcelFile(excel_file)
    excel_products = []
    
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        # 尋找關鍵欄位
        name_col = next((c for c in df.columns if '鏡頭' in str(c)), None)
        if not name_col: continue
            
        for index, row in df.iterrows():
            model_name = str(row.get(name_col, '')).replace('\n', ' ').strip()
            if not model_name or model_name == 'nan' or '鏡頭' in model_name or model_name == 'Lens Model':
                continue
            
            # 1. 基礎資訊
            brand = str(row.get('廠牌', 'Sony')).strip()
            if brand == 'nan' or brand == 'Brand': brand = 'Sony'
            
            # 2. 規格校正 (去重單位)
            aperture = clean_unit(row.get('最大\n光圈', ''), 'f/')
            filter_size = clean_unit(row.get('濾鏡\n口徑', ''), 'mm')
            weight = clean_unit(row.get('重量', ''), 'g')
            length = clean_unit(row.get('長度', ''), 'mm')
            width = clean_unit(row.get('寬度', ''), 'mm')
            magnification = clean_unit(row.get('放大\n倍率', ''), 'x')
            
            # 3. 焦段處理
            focal_length = str(row.get('焦段', ''))
            f_min = f_max = 0
            match = re.findall(r'\d+', focal_length)
            if len(match) >= 2: f_min, f_max = int(match[0]), int(match[1])
            elif match: f_min = f_max = int(match[0])

            # 4. 特性校正 (轉為 Boolean)
            def is_true(v): return "有" in str(v) or "Yes" in str(v)

            excel_products.append({
                "id": 9000 + len(excel_products),
                "brand": brand,
                "modelName": model_name,
                "gearType": "LENS",
                "releaseYear": int(row.get('發表\n年份', 2024)) if str(row.get('發表\n年份', '')).isdigit() else 2024,
                "launchPrice": int(re.sub(r'[^\d]', '', str(row.get('上市價\n$NTD', '0')))) if re.sub(r'[^\d]', '', str(row.get('上市價\n$NTD', ''))) else 0,
                "focalLengthMinMm": f_min,
                "focalLengthMaxMm": f_max,
                "apertureMax": aperture,
                "filterSizeMm": filter_size,
                "weightGrams": weight,
                "lengthMm": length,
                "widthMm": width,
                "maxMagnification": magnification,
                "hasOIS": is_true(row.get('防\n手震', '')),
                "hasWeatherSeal": is_true(row.get('防\n塵滴', '')),
                "hasApertureRing": is_true(row.get('光圈\n環', '')),
                "hasCustomButton": is_true(row.get('自訂\n按鍵', '')),
                "series": str(row.get('系列', '')).replace('\n', '').strip() if str(row.get('系列', '')) != 'nan' else ""
            })

    # 5. 合併原始資料 (確保機身也在)
    with open(old_backup_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    merged_dict = {item['modelName']: item for item in old_data}
    for item in excel_products:
        merged_dict[item['modelName']] = item
        
    final_list = list(merged_dict.values())
    
    # 6. 生成 Slug
    seen_slugs = {}
    for item in final_list:
        base_slug = re.sub(r'[^\w\s-]', '', item['modelName'].lower()).replace(' ', '-')
        slug = base_slug
        c = 1
        while slug in seen_slugs:
            slug = f"{base_slug}-{c}"
            c += 1
        seen_slugs[slug] = True
        item['slug'] = slug
        item['id'] = str(item.get('id', slug))

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Imported {len(excel_products)} items with precise mapping.")

if __name__ == "__main__":
    run_import()
