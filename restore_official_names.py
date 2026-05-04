import json

def restore_official_names():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    restored_count = 0

    for item in products:
        current_display = item.get('modelName', '')
        aliases = item.get('aliases', [])
        brand = item.get('brand', '')
        
        # 如果 aliases 為空，跳過 (這不應該發生)
        if not aliases:
            continue
            
        # --- 1. 確定官方全名 ---
        # 邏輯：從 aliases 中找尋最長、且通常包含品牌關鍵字的字串
        brand_keyword = brand if isinstance(brand, str) else ""
        potential_official = [a for a in aliases if brand_keyword in a]
        
        if potential_official:
            official_name = max(potential_official, key=len)
        else:
            official_name = max(aliases, key=len)
            
        # 特殊修正：Alpha 9 III 等
        if "A93" in current_display or "A9 III" in str(aliases):
            official_name = "Sony Alpha 9 III"
        elif "A12" in current_display or "A1 II" in str(aliases):
            official_name = "Sony Alpha 1 II"

        # --- 2. 更新別名清單 ---
        # 將目前的簡稱加入別名
        new_aliases = set(aliases)
        new_aliases.add(current_display)
        
        # 從別名中移除被選為顯示名稱的項目
        if official_name in new_aliases:
            new_aliases.remove(official_name)
            
        # --- 3. 寫回資料 ---
        item['modelName'] = official_name
        item['aliases'] = sorted(list(new_aliases))
        restored_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"RESTORE_OFFICIAL_NAMES_COMPLETE: Restored {restored_count} products.")

if __name__ == "__main__":
    restore_official_names()
