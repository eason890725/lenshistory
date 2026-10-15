# Design — LensHistory

LensHistory 的設計系統。每次改頁面都先讀這份；要新增規則時改這份，不要在單一頁面另起爐灶。
Token 的實際值在 `frontend/src/app/tokens.css`（Tailwind v4 `@theme`，會自動產生 `bg-paper`、`text-ink`、`font-display` 等 class）。

## Genre
editorial — 器材型錄 / 檔案館。

## Macrostructure family
- 首頁：Catalogue。小標題 + 一句說明 + 文字連結，接「依品牌」細線清單與「近年發表」商品格。沒有大 hero、沒有 CTA 按鈕。
- 資料庫：Catalogue。左側篩選欄（手機改成全螢幕面板）+ 等大商品格（F6，1:1，桌機 4 欄、手機 2 欄）。
- 詳細頁：左大圖展示盤，右側名稱與三格關鍵數字；下方 F3 規格表（兩欄、每列細線、等寬數字）。
- 比較頁：F3 規格表橫向展開，第一欄固定。

## Theme（Specimen，強調色沿用品牌紅）
- `--color-paper`   oklch(96% 0.018 80)
- `--color-paper-2` oklch(93% 0.020 80)
- `--color-plate`   oklch(93% 0.020 80) — 產品圖展示盤
- `--color-rule`    oklch(82% 0.014 75)
- `--color-rule-2`  oklch(64% 0.012 70)
- `--color-muted`   oklch(47% 0.012 65)
- `--color-ink-2`   oklch(28% 0.014 60)
- `--color-ink`     oklch(18% 0.014 60)
- `--color-accent`  oklch(50% 0.19 27) — 唯一強調色，每個畫面用量 < 5%
- `--color-focus`   同 accent

## Typography
- Display：Chiron Sung HK 700（中英文標題、型號名稱），roman，不用斜體
- Body：Geist 400，中文退回 PingFang TC / 微軟正黑體
- Mono：Geist Mono（標籤、規格數字、頁尾版權說明）；所有數字欄位加 `.tnum`
- 標題 `--text-display` = clamp(2.25rem, 4vw + 1rem, 4rem)

## 產品圖
- 一律白底（或透明），1000×1000 WebP，產品置中、四邊留 8%。用 `frontend/scripts/prepare_product_image.py` 處理。
- 顯示時放在 `.plate` 裡，圖片 `mix-blend-mode: multiply`，白底會融進展示盤的紙色。
- 不用網頁截圖、不用黑底圖。沒有圖就顯示「尚無圖片」，不放假圖。

## 規格欄位寫法
- 統一格式由 `frontend/scripts/normalize_products.py` 改寫（例如 "0.28m"、"0.25x"、"14 elements in 11 groups"、"Ø76 x 96 mm"、"10fps (Mech) / 30fps (Elec)"）。
- `npm run validate` 會擋下不符格式的值、未知的卡口名稱與片幅名稱。
- 新增資料後先跑 normalize，再跑 validate。
- `launchPrice` 是台灣新台幣**首發**建議售價：來自台灣分公司／總代理公告或台灣媒體的上市報導。現價、促銷價、外幣換算價都不收。
  例外：上市 6 個月內的新品，可以用台灣官方商店目前標示的建議售價（2026-10 起的規則）。
- `weightGrams`：機身含電池與記憶卡，鏡頭用官方值。外接電池的電影機（RED、Blackmagic 盒式機、Z CAM）用官方公布的機身淨重（body only）。
- `sensorFormat` 只能用 Full Frame、APS-C、Medium Format、Four Thirds、1-inch、1/1.7-inch、1/2.3-inch；卡口名稱見 `scripts/validate-products.mjs` 的 MOUNTS。

## Spacing
命名的 4pt 系列，定義在 `tokens.css` 的 `--space-*`。頁面左右留白 `--page-gutter`，最大寬度 `--page-max`。

## Motion
- 只有 hover 時圖片放大 1.02、連結底線變粗、顏色漸變；160–240ms，`--ease-out`。
- 沒有捲動進場動畫。`prefers-reduced-motion` 時全部關閉。

## Microinteractions
- 比較勾選：卡片左上角方框，點了即時生效，不跳提示。
- 已選器材 ≥ 1 時，底部固定一條比較列（C4）。
- 焦點框立即出現，不做淡入。

## CTA voice
- 主要動作：實心方角按鈕（ink 或 accent 底），文字一行不換行。
- 次要動作：文字連結加 1px 底線，hover 變 2px、變紅（`.link-type`）。

## Nav / Footer
- Nav：N6 報頭 — 置中字標、下方一行收錄統計（等寬字）、連結列、單細線。
- Footer：Ft4 版權說明 — 一段等寬小字，說明資料來源與留白原則。

## What pages MUST share
字標、報頭、配色、字型、按鈕形狀（方角）、展示盤處理、規格表樣式。

## What pages MAY differ on
頁面骨架（上面各頁的 macrostructure）、商品格欄數。
