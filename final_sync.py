import pandas as pd
import json
import os
import re

def clean_val(val):
    if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
        return None
    return str(val).replace("\n", " ").strip()

def is_true(v):
    if pd.isna(v): return False
    s = str(v).lower().strip()
    return s in ['ip', 'v', 'o', 'ois', '有', 'yes', 'true']

def clean_aperture(v):
    s = str(v).lower().replace('f/', '').strip()
    if '-' in s:
        parts = s.split('-')
        if len(parts) == 2 and parts[0].strip() == parts[1].strip():
            return parts[0].strip()
    return s

def to_float(v):
    if pd.isna(v): return 0.0
    s = str(v).lower().replace('x', '').replace('g', '').replace('mm', '').strip()
    try:
        return float(re.findall(r"[-+]?\d*\.\d+|\d+", s)[0])
    except:
        return 0.0

def run_final_sync():
    excel_file = 'sony lens.xlsx'
    output_path = 'frontend/src/data/products.json'
    
    xl = pd.ExcelFile(excel_file)
    all_data = []
    
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        name_col = next((c for c in df.columns if '鏡頭' in str(c)), None)
        if not name_col: continue
        
        for _, row in df.iterrows():
            name = str(row.get(name_col, '')).replace('\n', ' ').strip()
            if not name or name == 'nan' or '鏡頭' in name or name == 'Lens Model':
                continue
                
            item = {
                "brand": clean_val(row.get('廠牌', 'Sony')) or "Sony",
                "modelName": name,
                "gearType": "LENS",
                "series": clean_val(row.get('系列', '')),
                "releaseYear": int(row.get('發表\n年份', 2024)) if str(row.get('發表\n年份', '')).isdigit() else 2024,
                "launchPrice": int(re.sub(r'[^\d]', '', str(row.get('上市價\n$NTD', '0')))) if re.sub(r'[^\d]', '', str(row.get('上市價\n$NTD', ''))) else 0,
                "apertureMax": clean_aperture(row.get('最大\n光圈', '')),
                "filterSizeMm": to_float(row.get('濾鏡\n口徑', '')),
                "weightGrams": to_float(row.get('重量', '')),
                "lengthMm": to_float(row.get('長度', '')),
                "widthMm": to_float(row.get('寬度', '')),
                "maxMagnification": to_float(row.get('放大\n倍率', '')),
                "hasOIS": is_true(row.get('防\n手震', '')),
                "hasWeatherSeal": is_true(row.get('防\n塵滴', '')),
                "hasApertureRing": is_true(row.get('光圈\n環', '')),
                "hasCustomButton": is_true(row.get('自訂\n按鍵', '')),
            }
            
            match = re.findall(r'\d+', str(row.get('焦段', '')))
            item["focalLengthMinMm"] = int(match[0]) if len(match) > 0 else 0
            item["focalLengthMaxMm"] = int(match[-1]) if len(match) > 0 else 0
            
            all_data.append(item)

    with open('frontend/src/data/products.json.pre_sony.bak', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    final_dict = {i['modelName']: i for i in old_data if i.get('gearType') == 'CAMERA_BODY'}
    for i in all_data:
        final_dict[i['modelName']] = i
        
    final_list = list(final_dict.values())
    seen = {}
    for i in final_list:
        slug = re.sub(r'[^\w\s-]', '', i['modelName'].lower()).replace(' ', '-')
        base = slug
        c = 1
        while slug in seen:
            slug = f"{base}-{c}"
            c += 1
        seen[slug] = True
        i['slug'] = slug
        i['id'] = slug

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
    print(f"Final Sync Done. Total items: {len(final_list)}")

if __name__ == "__main__":
    run_final_sync()
