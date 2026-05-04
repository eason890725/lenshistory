import json
import re

def canon_naming_audit_v10_1():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0

    for item in products:
        if item.get('brand') != 'Canon':
            continue
            
        old_name = item.get('modelName', '')
        gear_type = item.get('gearType', '')
        
        # 1. 基礎清理
        name = old_name.replace("canon", "Canon").strip()
        
        if gear_type == 'LENS':
            # 鏡頭類別：移除 "EOS" 字樣
            name = name.replace("EOS ", "").replace("eos ", "")
            # 修正常見關鍵字大小寫
            name = name.replace("rf", "RF").replace("ef", "EF")
            name = name.replace(" f", " F").replace("is", "IS").replace("usm", "USM").replace("stm", "STM")
            # 處理 L 鏡頭標記 (f2.8l -> F2.8 L)
            name = re.sub(r'([fF]\d+\.\d+)([lL])', r'\1 L', name)
            # 修正 15-35mm 這種模式
            name = re.sub(r'(\d+-\d+mm)', lambda m: m.group(1).lower(), name) # 保持 mm 為小寫
        
        elif gear_type == 'CAMERA_BODY':
            # 機身類別：確保有 "EOS"
            if "EOS" not in name.upper():
                name = name.replace("Canon ", "Canon EOS ")
            name = name.replace("mark", "Mark").replace("eos", "EOS")
        
        # 移除重複品牌與多餘空格
        name = re.sub(r'^(Canon\s+)+', 'Canon ', name)
        name = re.sub(r'\s+', ' ', name).strip()
        
        if name != old_name:
            item['modelName'] = name
            fixed_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"CANON_NAMING_AUDIT_V10_1_COMPLETE: Re-formatted {fixed_count} Canon products.")

if __name__ == "__main__":
    canon_naming_audit_v10_1()
