# 交接：垂直切片 × 前後端分離 → 契約先行落地

## 下一步該做什麼

延續本文件的研究結論，規劃「契約先行（contract-first）」在目前團隊（前後端分離、想導入 vertical slice）的具體落地細節，至少要決定：

1. 契約工具選型（見下方「決策要點」的三選項比較表），要選 OpenAPI、Pact，還是 tRPC 型別，取決於目前後端語言、是否為 monorepo（前後端放同一個程式碼庫）。
2. 拆票流程怎麼調整：契約什麼時候定案、由誰先寫、前端票跟後端票何時才能各自開始平行做。
3. 如果團隊要用 AI 代理人（例如 Claude Code）輔助實作，要不要引入專門防止 AI 亂改契約的工具（見下方 Specmatic / micro-contracts / ContractSpec）。

這份文件本身不含程式碼變更，只是研究結論 + 已拍板的決策方向，下一個 session 可以直接從「怎麼落地」開始，不用重新查證。

## 已拍板的決策

使用者已明確同意採用「**契約先行**」的方式，來處理「團隊仍維持前後端分離、但要導入 vertical slice（垂直切片，指一個功能從畫面到資料庫串成一小片、可獨立驗證）」這個問題。

核心原則：**不是先切好一片垂直切片再機械式拆成一張前端票、一張後端票**，而是先講好一份契約（前後端約定好的資料格式跟規則，通常寫成一份 API 規格檔案），或先做一個很薄但真的跑得通的端對端骨架（walking skeleton）定出介面，之後前後端才各自平行把細節做完。

## 研究結論全文

以下是 `/ito-search` 用三個平行查證任務（vertical slice 定義與原因、前後端分離團隊怎麼落實、契約在中間扮演的角色）得出的完整結論，已在對話中呈現給使用者，使用者已閱讀並同意結論裡的契約先行方向。

### 結論摘要

- Vertical slice 本身不是要拆掉前後端分工，是要讓一次工作範圍（不管是一個人還是一個 AI 代理人）能做完一件完整、可驗證的事，不要照「畫面」「後端」「資料庫」這種技術層切票。
- 實務常見做法是「先做骨架、後端先行、契約橋接」：先把最薄的端對端流程串起來或先定資料契約，讓後端先做，再自動產生給前端用的契約，前端對著契約做畫面。
- 契約（API 規格）是把 vertical slice 和前後端分離團隊接起來的關鍵，契約要在正式拆工之前先講好。
- 2025 到 2026 年出現一批專門給 AI 代理人用的契約工具（Specmatic、micro-contracts、ContractSpec），作用是機制上擋住 AI 亂改契約或憑空生欄位。

### 一、什麼是 AI 輔助開發下的垂直切片，為什麼要這樣切？

- Jimmy Bogard 2018 年提出的原始定義：把程式碼依「一個需求做一件事」組織，不依 controller/service/repository 這種技術層組織。核心規則：切片內部盡量黏在一起，切片之間盡量鬆開。（來源：https://www.jimmybogard.com/vertical-slice-architecture/）
- Devin（AI 寫程式代理人公司）官方文件把任務分成「窄而深」跟「寬而淺」，窄而深（範圍小、可獨立驗證）的任務給 AI 做成功率高很多。（來源：https://docs.devin.ai/use-cases/best-practices）
- Anthropic 官方 Claude Code 文件：Claude 的 context window（一次能記住的工作範圍）會隨對話變長而塞滿、表現變差，建議一次工作範圍縮小到約一次程式碼審查（PR）大小。（來源：https://code.claude.com/docs/en/best-practices）
- 業界文章（Magnum Code、alexop.dev，2026 年）明確指出，把功能拆成「前端任務」「後端任務」「測試任務」三張票分給不同 AI 代理人做，是有害做法，因為每個代理人看不到別層在做什麼，容易讓欄位、格式對不起來。

### 二、前後端分離團隊具體怎麼落實垂直切片？

- 較舊的敏捷建議（Marcel Britsch，2019）：預設不要把一個功能拆成「前端故事」「後端故事」兩張獨立票，真要拆也要留在同一張母票下同步做。（來源：https://thedigitalbusinessanalyst.co.uk/frontend-vs-backend-user-stories-95bf583946ab）
- Team Topologies：建議乾脆用跨職能的「串流對齊團隊」取代前後端分家，一個團隊端對端做完一片垂直切片。
- 走鋼索骨架（walking skeleton）模式：先做一個很薄但真的跑得通的端對端流程，畫面到資料庫都串起來，自然定出 API 介面跟資料庫結構，介面定案後前後端才平行加厚細節。（來源：https://henko.net/blog/break-down-silos-with-a-walking-skeleton/）
- AI 代理人時代具體案例（Funding Societies，2025）：先定資料契約，一個代理人由下往上做（資料庫先做，再做 API），自動產生給前端用的契約（型別定義），另一個代理人對著契約做畫面。整體仍算同一片垂直切片，只是內部有清楚先後順序，靠自動產生的契約當橋樑。

### 三、契約在中間扮演什麼角色？

契約先行把「前後端兜不攏」的風險從執行期搬到設計期。前端對著規格產生的假伺服器先做，後端照規格實作真邏輯，兩邊不用互等。

| 契約類型 | 誰先寫 | 比較適合的情境 |
|---|---|---|
| OpenAPI / GraphQL schema-first | 後端或架構師先寫 | 跨語言、跨 repo 的團隊 |
| Pact（消費者驅動契約測試） | 前端（使用方）先寫期待的介面 | 微服務、各服務發版時間不同步 |
| tRPC 共用型別 | 前後端共用同一份 TypeScript 型別，無獨立契約檔 | 同一個 monorepo、同語言 |

- Apollo GraphQL 官方教學流程：後端團隊先跟前端團隊開會，把畫面稿標出需要哪些資料，一起寫一條範例查詢，正式簽好契約後前後端才分頭平行做。（來源：https://www.apollographql.com/tutorials/voyage-part1/03-agreeing-on-a-schema）
- Pact 讓前端先寫下自己期待的介面當契約，後端只要通過驗證就能自由重構內部邏輯。EPAM 案例：導入後 API 相關正式環境事故從每月 3-4 次降到 0，整合測試時間從 2 小時以上降到 15 分鐘。（來源：https://docs.pact.io/consumer）
- 2025-2026 專門給 AI 代理人設計的契約工具：
  - Specmatic MCP（給 Claude 等代理人用）：https://github.com/specmatic/labs/blob/main/coding-agents/README.md
  - micro-contracts（OpenAPI 當單一事實來源，防止人和 AI 繞過契約）：https://github.com/foo-ogawa/micro-contracts
  - ContractSpec（把 API/資料/錯誤/UI 狀態/測試都綁到同一份契約，防止 AI 跨層漂移）：https://github.com/Pluviobyte/ContractSpec

### 沒查到的部分（證據缺口）

- 沒有找到真的有公司「先切好一片垂直切片，再正式拆成一張前端票一張後端票」當標準流程並公開寫成案例文件的證據，最接近的做法是走鋼索骨架，或乾脆換成跨職能團隊。
- 沒有找到直接比較「先切垂直再拆前後端」跟「契約先行平行做」對 AI 代理人生產力影響的量化研究。

## 相關檔案

- 這份研究是純對話輸出，沒有落到程式碼或既有規格文件，本文件是唯一書面記錄。
- 目前 repo 有未提交變更：`.claude/skills/ito-write-agent-docs/` 底下三個檔案（SKILL.md、agents/openai.yaml、references/SKILL-MECHANICS.md）是修改中，另外 `.claude/skills/ito-implement/` 和 `.claude/skills/ito-to-prd/` 是新增未追蹤的目錄。這些跟本次垂直切片研究無關，下一個 session 若要處理它們需另外確認範圍。

## Suggested Skills

- 若下一步要把契約先行落地成正式的規格或計畫文件，可用 `/ito-to-prd` 把決策方向轉成產品需求文件（PRD）。
- 若下一步要直接動手改拆票流程或建立契約範本檔案，可用 `/ito-implement` 進場實作。
