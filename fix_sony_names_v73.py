import json
import re

def clean_sony_names():
    db_path = "frontend/src/data/products.json"
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_count = 0
    for item in data:
        if item.get("brand", "").lower() == "sony":
            original_name = item.get("modelName", "")
            
            # 移除常見的冗餘前綴與組合
            new_name = original_name
            # 替換 "Sony SONYAlpha Alpha " -> "Sony Alpha "
            new_name = re.sub(r"Sony\s*SONYAlpha\s*Alpha\s*", "Sony Alpha ", new_name, flags=re.IGNORECASE)
            # 替換 "Sony SONYAlpha " -> "Sony Alpha "
            new_name = re.sub(r"Sony\s*SONYAlpha\s*", "Sony Alpha ", new_name, flags=re.IGNORECASE)
            # 替換 "Alpha Alpha " -> "Alpha "
            new_name = re.sub(r"Alpha\s*Alpha\s*", "Alpha ", new_name, flags=re.IGNORECASE)
            # 替換 "Sony Alpha Sony " -> "Sony Alpha "
            new_name = re.sub(r"Sony\s*Alpha\s*Sony\s*", "Sony Alpha ", new_name, flags=re.IGNORECASE)
            # 替換 "Sony Sony " -> "Sony "
            new_name = re.sub(r"Sony\s*Sony\s*", "Sony ", new_name, flags=re.IGNORECASE)

            # 針對 R 系列的空白處理 (Alpha 7 R V -> Alpha 7R V)
            new_name = re.sub(r"Alpha\s*(\d)\s*R", r"Alpha \1R", new_name)
            
            # 針對 A9II 的空白處理 (Alpha 9II -> Alpha 9 II)
            new_name = re.sub(r"Alpha\s*(\d)(I+)", r"Alpha \1 \2", new_name)

            if new_name != original_name:
                print(f"CLEANED: '{original_name}' -> '{new_name}'")
                item["modelName"] = new_name
                cleaned_count += 1

    if cleaned_count > 0:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully cleaned {cleaned_count} Sony model names.")
    else:
        print("No redundant names found.")

if __name__ == "__main__":
    clean_sony_names()
