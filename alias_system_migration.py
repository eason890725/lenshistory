import json
import re

def migrate_to_alias_system():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    migrated_count = 0
    alias_map = {}

    for item in products:
        if item.get('gearType') == 'CAMERA_BODY':
            migrated_count += 1
            full_name = item.get('modelName', '')
            brand = item.get('brand', '')
            
            # 建立別名清單
            aliases = [full_name]
            
            # 預設簡稱轉化邏輯
            short_name = full_name
            
            if brand == 'Sony':
                # Alpha 7C II -> A7C2
                short_name = re.sub(r'Alpha\s*7', 'A7', short_name)
                short_name = re.sub(r'Alpha\s*6', 'A6', short_name)
                short_name = re.sub(r'Alpha\s*1', 'A1', short_name)
                short_name = re.sub(r'Alpha\s*9', 'A9', short_name)
                short_name = short_name.replace(' II', '2').replace(' III', '3').replace(' IV', '4').replace(' V', '5')
                aliases.append(full_name.replace("Alpha ", "a"))
                aliases.append(short_name.lower())
                
            elif brand == 'Canon':
                # EOS R6 Mark II -> R6II
                short_name = short_name.replace('EOS ', '')
                short_name = re.sub(r'Mark\s*II', 'II', short_name)
                short_name = re.sub(r'Mark\s*III', 'III', short_name)
                aliases.append(full_name)
                aliases.append(short_name.lower())
                
            elif brand == 'Nikon':
                # Z 8 -> Z8
                short_name = short_name.replace('Z ', 'Z')
                aliases.append(full_name)
                aliases.append(short_name.lower())
                
            elif brand == 'Fujifilm':
                # X-T5 -> XT5, X-H2S -> XH2S
                short_name = short_name.replace('X-', 'X')
                aliases.append(full_name)
                aliases.append(short_name.lower())

            # 去空格簡稱處理 (如 A7C2)
            short_name = short_name.replace(' ', '')
            aliases.append(short_name)
            
            # 寫回 JSON
            item['modelName'] = short_name # 顯示名稱改為簡稱
            item['aliases'] = list(set(aliases)) # 去重
            alias_map[short_name] = item['aliases']

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"ALIAS_MIGRATION_COMPLETE: Migrated {migrated_count} bodies.")
    return alias_map

if __name__ == "__main__":
    migrate_to_alias_system()
