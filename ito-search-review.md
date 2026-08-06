# ito-search 審查結果

審查對象：`.claude/skills/ito-search/SKILL.md`、`.claude/skills/ito-search/agents/openai.yaml`
對照基準：使用者原始需求六條、`ito-write-agent-docs/references/WRITING-PRINCIPLES.md`、`ito-write-agent-docs/references/SKILL-MECHANICS.md`

## 結論

骨架對，六條需求都有對應的段落，打包方式也符合 repo 規範。但有 4 個問題會讓它實際跑起來出錯或跑法不穩，建議修完再用。

---

## 一、需求對照

| # | 需求 | 落點 | 狀態 |
|---|---|---|---|
| 1 | `--codebase` 先派 agent 看程式碼，再依結果搜尋 | Step 2 | 有做，順序正確（明講要等結果回來再改寫問題） |
| 2 | 依複雜度拆面向，最多三個 | Step 1 + Step 3 | 有做 |
| 3 | 一個 sub agent 只查一個問題、只用一種工具 | Step 3 | 有做 |
| 4 | 支援 exa、deepwiki、context7、gh，agent 自選，找不到就 fallback | Step 3 | 有寫，但 fallback 條件錯（見 P3） |
| 5 | 主 agent 整理，先結論再論述，能一句話不用兩句，偏好列點 | Step 4 | 有做 |
| 6 | 附幾個權威來源，不要全列 | Step 4 | 有做 |

---

## 二、必修（4 個）

### P1 — 沒說怎麼派 sub agent

Step 2 和 Step 3 只寫 `dispatch one sub-agent`，沒說用哪個工具派、派哪一種 agent。

為什麼是問題：這個 harness 有多種 agent，能用的工具不一樣。`Explore` 是唯讀搜尋用的，`general-purpose` 才有全部工具。沒指定的話，每次跑可能派到不同種，行為不穩。而且 `gh` 要 Bash 才能跑，派到沒有 Bash 的 agent 就直接失敗。

怎麼修：Step 2 和 Step 3 各自明講用 Agent 工具派、指定 agent 種類。

### P2 — 看程式碼的 agent 被限制只能用一種工具

Step 2 第 18 行：`Require it to use one inspection tool only`。

為什麼是問題：這條是從需求 3 誤套過來的。需求 3 講的是「搜尋」agent 一個工具，避免它亂撒網。但看程式碼本來就要 Glob 找檔案、Grep 找關鍵字、Read 讀內容一起用。限一種等於叫它半殘著查，回來的結果會不完整，後面的搜尋問題就改寫錯方向。

怎麼修：拿掉這條限制。要求它回傳帶檔案路徑和行號的結果就夠了（這句原本就有，留著）。

### P3 — fallback 條件寫錯

Step 3 第 31 行：`When all four are unavailable, use the harness's general search capability.`

為什麼是問題：四個工具全掛才 fallback，是錯的判斷點。真實情況是「這一題最適合的工具剛好沒有」。例如問某套件的 API，最適合 context7，但 context7 沒裝、exa 有 — 照現在的寫法不算 fallback 條件成立，agent 會卡住或硬用 exa 卻沒有規則告訴它可以這樣做。

怎麼修：改成逐題判斷。這題選的工具不在，就從剩下可用的裡面挑次適合的；一個都沒有，才用 harness 自帶的 search。

### P4 — 「查有哪些工具可用」沒講怎麼查

Step 3 第 31 行：`Discover which tools and capabilities are available in the current harness.` 只有指令，沒有方法。

為什麼是問題：在這個 harness 裡，MCP 工具是 deferred 的 — 一開始只看得到名字，要先用 ToolSearch 把 schema 載進來才能呼叫。sub agent 如果不知道這件事，很可能直接回報「找不到 exa」，然後整條 fallback 被誤觸發。`gh` 則要跑 `gh --version` 才知道裝了沒（這台機器有，2.97.0）。

怎麼修：把查法寫進去，並且要求派工的 prompt 裡就告訴 sub agent 它被指派的工具叫什麼名字、怎麼載。

---

## 三、該補（5 個）

### P5 — 搜尋失敗後沒有下一步

Step 3 完成條件寫 `has returned or has a recorded failure`。記下失敗之後呢？要不要換工具重試？沒寫。現在會變成失敗就算過，主 agent 拿著缺一塊的證據去寫結論。

建議：明講失敗一次就換次適合的可用工具重派一次，再失敗才記為缺口，並在最後的答案裡講出來。

### P6 — sub agent 的 prompt 要求，寫得像在講主 agent

Step 3 第 33 行用 `Each sub-agent must focus on ... distinguish evidence from inference, and return source titles and direct URLs`。

這是在描述 sub agent 應該有的行為，但沒有明講「這些要原封不動寫進派給它的 prompt」。sub agent 讀不到這份 skill，主 agent 不轉述它就不會照做。

建議：改成「派工 prompt 必須包含：指派的問題、指派的工具、區分證據與推論、回傳來源標題與直接連結」。

### P7 — 「最多三個」寫了兩次

Step 1（第 12、14 行）和 Step 3（第 33 行）各寫一次。違反 repo 自己的單一真相來源原則，之後改數字容易漏改一邊。留在 Step 1 就好。

### P8 — 平行化寫得太軟

Step 3 第 33 行 `Run independent searches in parallel when the harness supports it.` 這個條件式讓 agent 有理由不做。

建議：直接寫「在同一則訊息裡一次派出所有搜尋 agent」。

### P9 — Step 1 的完成條件有一半是空的

第 14 行：`the presence of --codebase is recorded`。記在哪？沒說。agent 做不做這件事，行為都一樣，等於一句廢話。刪掉，或改成「有 `--codebase` 就進 Step 2」。

---

## 四、可考慮（3 個）

### P10 — 簡單問題也一定要派 sub agent

Step 3 是「一個問題派一個 agent」，沒有例外。所以問一個小事實也會多繞一層 sub agent，慢又費 token。

原始需求沒禁止主 agent 自己查，可以加一句：只有一個問題、而且主 agent 手上就有那個工具時，自己查完直接進 Step 4。這算設計取捨，看你要不要一致性優先。

### P11 — argument-hint 語言跟隔壁不一致

`ito-grill` 的 argument-hint 是中文（`給我一個模糊的計畫或想法，我幫你釐清`），這支是英文。同一組 skill 的提示語建議統一。

### P12 — description 講的是內部做法，不是使用者拿到什麼

現在是 `Research a question with focused sub-agents, optional codebase context, and authoritative sources.`。「sub-agents」是實作細節。user-invoked skill 的 description 是給人看的，講價值比講機制好。

---

## 五、做對的部分

- 打包完全符合 `SKILL-MECHANICS.md`：資料夾名與 frontmatter `name`一致、`disable-model-invocation: true` 搭配 `agents/openai.yaml` 的 `policy.allow_implicit_invocation: false`、description 是一行人看的摘要。
- 寫作符合 `WRITING-PRINCIPLES.md`：沒有破折號、沒有分號、每個 step 都有完成條件、用正面敘述而不是禁止句。
- Step 2 明確要求等程式碼結果回來才改寫問題，沒有讓它跟搜尋平行跑。這點很重要，做對了。
- Step 4 的輸出順序（結論 → 列點 → Key sources）完全對到需求 5 和 6。
- 四個工具各自的適用時機寫得清楚，agent 有足夠資訊自選。

---

## 六、修改順序建議

1. P2（拿掉看程式碼的單一工具限制）— 一行刪除，影響最大
2. P3（fallback 改逐題判斷）— 一句改寫
3. P1（明講派 agent 的方式）— Step 2、Step 3 各加一句
4. P4（工具偵測方法）— 併進 P1 那句一起寫
5. P5 到 P9 一起整理 Step 3 和 Step 1
6. P10 到 P12 看個人偏好
