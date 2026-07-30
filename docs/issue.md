## 錢花在哪

三塊，由大到小。

1. **兩個 review subagent 約 17 萬 token**（Standards 95,975 + Spec 74,645）。這是 skill 第 4 步規定的。
2. **檔案被整份重貼回對話**。lint hook 每次改動檔案，系統就把整份檔案塞回來，發生五六次，最大一次一千多行。這不是 skill 造成的。
3. **前期探索讀太寬**。我整段拉了 435 行的路由檔和 420 行的測試檔，實際上只需要其中幾十行。

時間主要花在 `pnpm test` 全跑三次，每次兩分鐘，其中 664 個 backend 測試跟這次改動完全無關。

## 對 /ito-implement-v2 的建議

### 1. Review 規模要跟 diff 大小掛鉤

現在不管改 20 行還是 2000 行，都固定派兩個 subagent，而且把 `code-review.md` 開頭加各自的 section 全文貼進去，貼了兩遍。

建議加一句門檻：diff 小於某個規模（例如 300 行或 5 個檔案）時，自己對著 diff 走一遍 checklist 就好，不派 agent。或者派一個 agent 回兩份 verdict，就像這個 repo 既有的 `ito-task-reviewer` 那樣。

### 2. 規則檔被讀了三遍

第 1 步要我讀完 `BEST-PRACTICE-MAP.md` 和它指到的所有規則集。第 4 步又要我把同一批規則交給兩個 agent，他們各自再讀一次。同樣的檔案讀三遍。

建議：第 1 步讀完之後，把「這次適用哪幾條、各自約束什麼」寫成一段摘要，第 4 步只把那段摘要傳給 agent，不要叫他們自己重讀。

### 3. 全套測試不該全跑

第 4 步寫「Run the full test suite once, using the repository's own command」。這個 repo 的 `AGENTS.md` 明講了：只跑受影響的 spec，跨 package 全跑要背景執行。兩份指令打架，我照 skill 跑了三次全套。

建議改成：跑覆蓋這次改動的那些 package，不是整個 monorepo。或者明說「repo 自己的測試策略優先」。

### 4. 加一步「先確認 lint 允不允許」

我這次撞牆兩次，都很貴。

- 想用 `parentElement` 縮測試範圍，被 `testing-library/no-node-access` 擋掉。
- 想用 `useEffect` 回報驗證狀態，觸發 `react/set-state-in-effect`，跟隔壁檔案已經在用的 render-phase 寫法互斥。

第二次讓我把整個元件重寫了一遍。

建議在第 3 步加一句：要用一個這個 codebase 還沒出現過的寫法之前，先跑一次該檔案的 lint，別等到收尾才發現。

### 5. 每個 slice 綠燈的定義要包含「沒弄壞別人」

現在第 3 步的 done 條件只說自己的測試由紅轉綠、typecheck 過。我到 slice 6 才發現我加的「未設定」跟預算摘要卡的「未設定」撞名，弄掉一條既有測試。那時候已經寫了五個 slice。

建議 done 條件加上：跑一次 `vitest related` 或該模組的既有測試。早三個 slice 發現，就不用回頭補。

### 6. 明講「窄讀」

skill 完全沒提怎麼讀檔案。建議在第 1 步加一句：知道要看哪一段就只讀那一段，不要整檔拉。這是我這次最能自己省下來的部分。

### 7. Refactor 排在最後，代價可能很高

第 4 步要求「with the findings in hand and the whole diff visible」才重構。立意是對的，但這次 review 指出的結構問題讓我把一個已經寫了三遍的檔案再寫一遍。

這條我沒有更好的替代方案，只是提醒：如果第 2 步的 seam 討論能順帶談一下元件邊界，有些結構問題可以更早定案。
