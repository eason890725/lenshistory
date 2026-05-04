import json
import os

def smart_merge():
    old_file = 'frontend/src/data/products.json.pre_sony.bak'
    new_file = 'frontend/src/data/products.json'
    
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    old_count = len(old_data)
    new_count = len(new_data)
    
    # 建立名稱映射，方便去重 (以 Excel 的新資料為優先)
    merged_dict = {item['modelName']: item for item in old_data}
    
    duplicate_count = 0
    for item in new_data:
        if item['modelName'] in merged_dict:
            duplicate_count += 1
        merged_dict[item['modelName']] = item
    
    final_list = list(merged_dict.values())
    final_count = len(final_list)
    
    # 防遺失檢查：原始 + 新增 - 重複 == 總數
    # 邏輯：原本有的 + 新加進去且不重複的 == 最終總數
    expected_count = old_count + new_count - duplicate_count
    
    if final_count != expected_count:
        print(f"ERROR: Count mismatch! Expected {expected_count}, got {final_count}")
        return
    
    # 寫入檔案
    with open(new_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Recovered {old_count} old items.")
    print(f"Merged with {new_count} new items (Found {duplicate_count} duplicates).")
    print(f"Final total: {final_count}")
    print(f"LAST_3_ITEMS:" + "|".join([p['modelName'] for p in final_list[-3:]]))

if __name__ == "__main__":
    smart_merge()
