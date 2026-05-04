# Camera Manager Skill
# 此 Skill 用於管理 LensHistory 的器材資料庫 (products.json)

RULES:
1. 【物理備份】：在執行任何修改前，必須先執行 `cp frontend/src/data/products.json frontend/src/data/products.json.bak`。
2. 【絕對增量】：所有新產品只能追加 (Append) 到 `products.json` 陣列的末尾，嚴禁刪除或修改既有資料。
3. 【數量防呆】：修改後必須立即執行 `wsl bash -c "python3 -c 'import json; print(len(json.load(open(\"frontend/src/data/products.json\"))))'"`。
   - 若數量 < 修改前數量，代表發生覆寫錯誤。
   - 必須立即執行 `mv frontend/src/data/products.json.bak frontend/src/data/products.json` 還原資料並向使用者回報。
4. 【自動存檔】：任務成功且通過防呆檢查後，自動執行：
   - `git add .`
   - `git commit -m "Auto-update: 新增相機產品 [數量: {count}]"`

ACTIVATION_KEYWORDS:
- "新增相機"
- "修改產品"
- "添加鏡頭"
- "更新器材庫"
