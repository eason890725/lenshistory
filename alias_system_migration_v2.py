import json
import re

def migrate_to_alias_system_v2():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    migrated_count = 0

    for item in products:
        if item.get('gearType') == 'CAMERA_BODY':
            migrated_count += 1
            brand = item.get('brand', '')
            # 如果已經有 aliases 且包含官方名稱，我們基於原始狀態處理
            # 這裡假設我們需要重新生成以確保完整性
            
            # 獲取目前的 modelName (可能是簡稱) 和 aliases
            current_model = item.get('modelName', '')
            aliases = item.get('aliases', [])
            
            # 嘗試找回官方全名 (通常在 aliases 中或者是長的那一個)
            official_name = current_model
            if aliases:
                official_name = max(aliases, key=len)
            
            # 預設別名集合
            new_aliases = {official_name, current_model}
            
            # 針對品牌進行變體生成
            if brand == 'Sony':
                # Sony Alpha 7 IV -> A7M4, A74, etc.
                s = official_name.replace("Sony ", "").replace("Alpha ", "")
                new_aliases.add(f"Sony a{s}")
                new_aliases.add(f"a{s}")
                
            elif brand == 'Canon':
                # EOS R6 Mark II -> R6II, R6M2
                if "Mark" in official_name:
                    m_num = "II" if "Mark II" in official_name else "III" if "Mark III" in official_name else "IV" if "Mark IV" in official_name else ""
                    base = official_name.replace("EOS ", "").replace(f" Mark {m_num}", "")
                    new_aliases.add(f"{base}{m_num}")
                    new_aliases.add(f"{base} Mark {m_num}")
                    new_aliases.add(f"EOS {base} {m_num}")
                
            elif brand == 'Nikon':
                new_aliases.add(official_name.replace("Z ", "Z"))
                
            elif brand == 'Fujifilm':
                new_aliases.add(official_name.replace("X-", "X"))

            # 通用處理：轉小寫、去空格
            final_aliases = set()
            for a in new_aliases:
                final_aliases.add(a)
                final_aliases.add(a.lower())
                final_aliases.add(a.replace(" ", ""))
                final_aliases.add(a.replace(" ", "").lower())
            
            item['aliases'] = sorted(list(final_aliases))

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"ALIAS_MIGRATION_V2_COMPLETE: Refined {migrated_count} bodies.")

if __name__ == "__main__":
    migrate_to_alias_system_v2()
