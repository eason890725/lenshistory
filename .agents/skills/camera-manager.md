# Camera Manager Skill
# 此 Skill 用於管理 LensHistory 的器材資料庫 (products.json)

RULES:
1. 【物理備份】：在執行任何修改前，必須先執行 `cp frontend/src/data/products.json frontend/src/data/products.json.bak`。
2. 【絕對增量】：所有新產品只能追加 (Append) 到 `products.json` 陣列的末尾，嚴禁刪除或修改既有資料。
3. 【數量防呆】：修改後必須立即執行 `wsl bash -c "python3 -c 'import json; print(len(json.load(open(\"frontend/src/data/products.json\"))))'"`。
   - 若數量 < 修改前數量，代表發生覆寫錯誤。
   - 必須立即執行 `mv frontend/src/data/products.json.bak frontend/src/data/products.json` 還原資料並向使用者回報。
4. 【嚴禁偽造】：嚴禁為了前端排版、測試或湊數而自動生成假資料 (Mock Data)。資料庫內僅允許存在真實產品。若畫面空白，請保持空白並回報。
5. 【自動存檔】：任務成功且通過防呆檢查後，自動執行：
   - `git add .`
   - `git commit -m "Auto-update: 新增相機產品 [數量: {count}]"`
6. 【視覺驗證】：任務結束前必須啟動瀏覽器訪問 `http://localhost:3000`，親眼確認列表渲染正常、詳細頁無 `undefined` 並附上截圖。
7. 【價格校驗】：所有產品必須包含有效價格（Launch Price 必須 > 0）。若是 2024-2026 年新器材，必須與最新市場建議售價 (MSRP) 進行核實，格式必須統一為台幣 (NTD)。
8. 【狀態持久化】：所有列表篩選組件必須實作 URL 參數同步（URL Parameter Sync）。當篩選條件變更時，必須同步更新網址列；頁面載入時必須從 URL 恢復篩選狀態，以確保導覽「返回」時狀態不遺失。
9. 【原生鏡頭深度提取】：針對 Canon (L-series), Nikon (S-Line), Fujifilm (WR/LM) 等頂級原生鏡頭，必須額外抓取：光學結構（幾群幾枚）、特殊鏡片（UD/ED/非球面）、鍍膜技術（ASC/Nano/Arneo）以及對焦馬達類型（VCM/USM/LM）。
10. 【大一統格式鎖定】：所有品牌鏡頭必須強制顯示以下四大區塊：
    - 影像核心：焦距、光圈範圍、馬達、放大倍率、最近對焦。
    - 光學性能：組數、特殊鏡片、鍍膜、濾鏡口徑。
    - 功能特性：防手震、光圈環、自定義按鈕、防塵防滴。
    - 物理與市場：尺寸、重量、系列、年份、價格。
    缺失欄位必須顯示「--」，且所有單位必須統一樣式（mm, g, m）。資料庫同步時需自動校正 Canon 14mm 等特殊鏡頭的濾鏡口徑標註。

ACTIVATION_KEYWORDS:
- "新增相機"
- "修改產品"
- "添加鏡頭"
- "更新器材庫"
