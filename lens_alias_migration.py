import json
import re

def migrate_lens_to_alias_system():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    migrated_count = 0

    for item in products:
        if item.get('gearType') == 'LENS':
            migrated_count += 1
            full_name = item.get('modelName', '')
            brand = item.get('brand', '')
            series = item.get('series', '')
            
            # 建立別名清單 (保留原始官方全名)
            aliases = {full_name}
            
            # 預設簡稱轉化邏輯
            short_name = full_name
            
            # 1. 提取焦段 (例如 24-70 -> 2470, 50 -> 50)
            focal = ""
            f_match = re.search(r'(\d+)-(\d+)', full_name)
            if f_match:
                focal = f"{f_match.group(1)}{f_match.group(2)}"
            else:
                f_match_prime = re.search(r'(\d+)mm', full_name)
                if f_match_prime:
                    focal = f_match_prime.group(1)

            # 2. 提取代數 (II -> 2, III -> 3)
            version = ""
            if " II" in full_name: version = "2"
            elif " III" in full_name: version = "3"

            # 3. 品牌與系列專屬轉化
            if brand == 'Sony':
                # FE 24-70mm F2.8 GM II -> 2470GM2
                if "GM" in full_name:
                    short_name = f"{focal}GM{version}"
                elif " G" in full_name:
                    short_name = f"{focal}G{version}"
                aliases.add(full_name.replace("FE ", ""))
                aliases.add(full_name.replace("E ", ""))

            elif brand == 'Canon':
                # RF 50mm F1.2 L USM -> 50L
                if " L " in full_name or full_name.endswith(" L"):
                    short_name = f"{focal}L{version}"
                aliases.add(full_name.replace("RF ", "").replace("EF ", ""))

            elif brand == 'Nikon':
                # Z 24-70mm f/2.8 S -> 2470S
                if " S" in full_name:
                    short_name = f"{focal}S{version}"
                aliases.add(full_name.replace("Z ", ""))

            elif brand == 'Fujifilm':
                # XF 33mm F1.4 R LM WR -> 33WR
                if "WR" in full_name:
                    short_name = f"{focal}WR"
                aliases.add(full_name.replace("XF ", "").replace("GF ", ""))

            # 通用別名添加
            aliases.add(short_name)
            aliases.add(short_name.lower())
            
            # 寫回 JSON
            item['modelName'] = short_name # 顯示名稱改為簡稱
            item['aliases'] = sorted(list(aliases))

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"LENS_ALIAS_MIGRATION_COMPLETE: Migrated {migrated_count} lenses.")

if __name__ == "__main__":
    migrate_lens_to_alias_system()
