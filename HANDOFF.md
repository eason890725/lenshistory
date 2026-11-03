# 交接檔（雲端 ↔ 本機）

雲端 session 學到的規則、來源與待辦都寫在這裡。本機記憶不會同步，回本機接手時先讀這份。

## 資料流程
- 資料：`frontend/src/data/products.json`。改完跑 `node frontend/scripts/validate-products.mjs`，必須 0 errors。
- 圖片：官方圖下載後用 `python frontend/scripts/prepare_product_image.py <輸入> frontend/public/images/products/<品牌>/<id>.webp`，再填 `image_url`。
- 補欄：填寫 agent 輸出 `{id:{fields:{欄位:{value,source,quote}}}}`；另一個獨立查核 agent（預設立場是有錯）回 `{"checked":[[id,欄位]],"failures":[[id,欄位,原因]]}`。
  只合併 checked、沒有 failed、而且原本是空的欄位。false 是有效值，不能當空值丟掉。
- 資料 commit 驗證過就直接 push；改程式、刪資料、改既有值要先跟使用者講。commit 訊息用繁體中文。

## 規則
- 台灣時間 20:00–09:00 不跑 agent，也不排會在這段時間觸發的任務。
- 一次最多 10 個 subagent；大型 workflow 前先看 5 小時額度。
- agent 不准用瀏覽器工具、web.archive.org、curl／PowerShell 連網、不准開子 agent；遇到 403／429／機器人防護就跳過。
- false 或 "None" 只在來源明寫時填；圖片只收官方、優先黑色版本；logSupport "None" 要有完整 Picture Profile 清單；
  只有自動對焦鏡頭的 hasCustomButton 不填 false。

## 寫法慣例
- afTargets 英文單數，順序 Human, Animal, Bird, Insect, Horse, Car, Motorcycle, Bicycle, Train, Airplane, Helicopter, Drone；
  只有臉眼寫 "Human (Face/Eye)"；小型機只有臉部偵測寫 "Face"；Olympus 寵物 "Face, Animal (Dog, Cat)"，Pentax／Ricoh "Face, Animal (Pet)"。
  中文由 `frontend/src/lib/gear.ts` 的 AF_TARGET_ZH 翻譯，出現新詞要加。
- afRange "EV -4 to 20"；有低光源 AF 寫 "EV -4 to 19 (without low-light AF: -2 to 19)"。沒 EVF 的 evfResolution 留空。

## 來源
- Sony 用 helpguide.sony.net；sony.jp 是 Shift_JIS，WebFetch 會亂碼。
- 403：panasonic.com、canon-europe.com、usa.canon.com。
- 429：Shopify 系鏡頭店（7artisans.store、store.sirui、ttartisan.store、brightinstar、astrhori、lensbaby.com）。
- imaging-resource 的 robots.txt 擋 anthropic-ai，不准批次抓。
- Fujifilm 鍍膜查 dl.fujifilm-x.com 說明書 PDF；Leica 規格表 JS 載入讀不到。
- Fujifilm、Leica、Hasselblad、Nikon 1、舊 Panasonic 官方沒有 AF 測距範圍，別再派。

## 待辦（雲端 session 會持續更新這一段）
- G9、GH5S afTargets 目前是 "Face/Eye"；韌體公告其實有動物辨識，使用者若要「Human, Animal」就改回去。

## 進度紀錄
- 2026-11-03 雲端接手：1996 筆、0 errors；缺圖 175、缺月份 20。
