import json

def fix_canon_mark_aliases():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0
    for item in products:
        if item.get('brand') == 'Canon' and item.get('gearType') == 'CAMERA_BODY':
            aliases = set(item.get('aliases', []))
            model = item.get('modelName', '')
            
            # 針對 R 系列的 Mark II / Mark III 補全
            if 'II' in model and 'Mark' not in str(aliases):
                base = model.replace('II', '')
                full_mark = f"EOS {base} Mark II"
                aliases.add(full_mark)
                aliases.add(full_mark.lower())
                aliases.add(f"{base} Mark II")
                aliases.add(f"{base} Mark II".lower())
                fixed_count += 1
            
            if 'III' in model and 'Mark' not in str(aliases):
                base = model.replace('III', '')
                full_mark = f"EOS {base} Mark III"
                aliases.add(full_mark)
                aliases.add(full_mark.lower())
                aliases.add(f"{base} Mark III")
                aliases.add(f"{base} Mark III".lower())
                fixed_count += 1
            
            # 確保原始官方名稱 (簡稱前) 也在裡面
            if model == 'R6II': aliases.add("EOS R6 Mark II")
            if model == 'R5II': aliases.add("EOS R5 Mark II")
            if model == 'R6': aliases.add("EOS R6")
            if model == 'R5': aliases.add("EOS R5")
            
            item['aliases'] = sorted(list(aliases))

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"CANON_MARK_FIX_COMPLETE: Fixed {fixed_count} Canon entries.")

if __name__ == "__main__":
    fix_canon_mark_aliases()
