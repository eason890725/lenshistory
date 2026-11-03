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
- 403：panasonic.com、canon-europe.com、usa.canon.com、B&H、mobile01、cool3c、respond.tw、tamron.com.tw、insta360.com、canon.com.au。
- 503／空白：laowacine、zyoptics、venuslens、irixlens、mkgrip、yongnuo.com.cn、arch.casio；blazarlens 有機器人驗證；7artisans.com 規格是圖片。
- 可用：Adorama 規格表、DPReview 規格頁（舊機欄位少）、PChome 搜尋 API、Panasonic 台灣官方商城、sony.jp 英文說明書 PDF、helpguide.sony.net。
- 429：Shopify 系鏡頭店（7artisans.store、store.sirui、ttartisan.store、brightinstar、astrhori、lensbaby.com）。
- sony.com／electronics.sony.com 抓不到；pro.sony 403；PetaPixel 403；vazen.cn、wap.dzofilm.com 不在網路白名單。
- imaging-resource 的 robots.txt 擋 anthropic-ai，不准批次抓。
- Fujifilm 鍍膜查 dl.fujifilm-x.com 說明書 PDF；Leica 規格表 JS 載入讀不到。
- Fujifilm、Leica、Hasselblad、Nikon 1、舊 Panasonic 官方沒有 AF 測距範圍，別再派。

## 待辦（雲端 session 會持續更新這一段）
- G9、GH5S afTargets 目前是 "Face/Eye"；韌體公告其實有動物辨識，使用者若要「Human, Animal」就改回去。
- **Sony a7、a7R、a6000 的 videoColorDepth 仍是錯的 "10-bit 4:2:2"**：使用者要求找正確資料。sony.jp 規格頁、DPReview 評測、
  helpguide（ilc/13xx 都 404）都沒寫取樣／位元；可試舊版英文說明書 PDF 或 Sony 2013–2014 新聞稿（sony.com 雲端抓不到）。
  其他 14 台已改成 "8-bit 4:2:2 (HDMI)"（sony.jp HDMI 映像出力）。
- 副廠鏡頭卡口已補 6 個（使用者同意）。未補（官方頁沒光學規格可比對）：YN35 F2 DF +Z、YN50 F1.8S DA +Z +X、YN50 DF +Z、YN85 DF +RF。
  YN85 F1.8 DF DSM 官方重量 405g，資料庫 346g，待確認。
- 4 支 Yongnuo 新鏡頭找不到正式發表日沒收：YN42.5 F1.7M II、YN85 F1.8R DF DSM II、YN33 F1.4 DA DSM WL Pro、YN35 F1.8S DA DSM WL。
  7Artisans AF 10mm F4、Meike 58mm F1.2、YN16mm、YN50 F1.8S II 已收但 releaseMonth 空著（只有預告／開賣報導）。
- Sirui、Laowa、Tokina 的漏收稽核在雲端做不了（網站擋或空白）。
- **台灣價格**：雲端連不到 Mobile01、cool3c（403），WebSearch 額度用完，剩約 470 筆。本機有網路時優先做。
  已查過但沒收：Zeiss Otus ML 50（77,980）、Lumix S1（79,990）、RX100 VA（26,980）、HERO5 Black（15,500）只看到搜尋摘要，需開 Mobile01 原文核對。
- **圖片**：剩約 170 筆缺圖。官方多半只有 <500px 小圖（Kodak、Casio、舊 Sony／Nikon 卡片機）或多色合照、黑底橫幅（Cooke、Cosina）。
- **鏡頭規格**：hasOIS／hasWeatherSeal／maxMagnification 等，副廠官網多半不寫、規格是圖片；B&H 在雲端 403。Adorama 規格表明寫 "Image Stabilization: No" 可用。
- AstrHori 28mm Periprobe：資料庫規格像 2024-06 的 360° 版，與 2023-11 版混在一起，要確認是哪一版再填月份。
- Sony a7R III／IV 的原機條目若改色深，a7R IIIA／IVA 新條目已是 8-bit 4:2:0。

## 使用者決定（2026-11-03）
- 收 Sigma sd Quattro／sd Quattro H（MOUNTS 已加 'Sigma SA'）。
- Panasonic 2026-08 的「A」型號改款鏡頭（S-R70200A、H-ES12060A、H-XA025A、H-HS043A，只加氟鍍膜）暫不分開收；之後若有官方產品頁再議。
- afRange 統一：最佳值在前，括號寫 "(without low-light AF: …)" 或 "(without Starlight View: …)"。
- 收錄範圍擴到 Sony E 卡口起點（2010 NEX）。小改款／SE 版（a7R IIIA、FX3A、Z 28mm SE 等）分開收。

## 進度紀錄
- 2026-11-03 雲端接手：1996 筆、0 errors；缺圖 175、缺月份 20。
- 圖片：剩下缺圖的多半官方只有 <500px 小圖（Kodak、Casio、舊 Sony／Nikon 卡片機）、多色合照或黑底橫幅（Cooke、Cosina）；prepare_product_image.py 會拒收小圖。
- 雲端 2026-11-03 成果：新增 27 筆（Sony NEX／E 鏡、Nikon Z 120-300 TC、SE 鏡、sd Quattro、GH4R 等），補圖 6、規格約 180 欄、台灣價格 11、月份 11。
- 雲端 WebSearch 額度（整個 session 200 次）很快用完，之後只能 WebFetch。
- 月份查核退回：預購上架、Amazon 開賣、單一地區發表都不算正式發表月份。7Artisans 7.5/25/35 F2 應為 2017-06、M75 為 2019-08、AstrHori Periprobe 2023-12（officialUrl 指到直桿版，要再查）。
