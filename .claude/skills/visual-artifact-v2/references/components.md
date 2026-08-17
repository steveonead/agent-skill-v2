# Component Catalog

Copy a complete snippet and replace its content. Use template-defined classes. Reserve literal colors for Mermaid `linkStyle` declarations that follow the semantic color table.

## Contents

### Explain and qualify

- [Prose and evidence](#prose-and-evidence)
- [Goals and out of scope](#goals-and-out-of-scope)
- [Disclosure](#disclosure)

### Compare and decide

- [Tables](#tables)
- [Comparison](#comparison)
- [Decision matrix](#decision-matrix)
- [Rule matrix](#rule-matrix)

### Orient and summarize

- [Timeline](#timeline)
- [Status summary](#status-summary)
- [Metric summary](#metric-summary)

### Show behavior, structure, source, and change

- [Diagrams](#diagrams)
- [Code](#code)
- [Diff](#diff)

### Specify product behavior

- [User stories](#user-stories)
- [API and symbol ledger](#api-and-symbol-ledger)
- [Wireframes](#wireframes)

## Prose and evidence

Use `<h3>` for a subsection inside a section. Use a generic note for scope or one constraint:

```html
<div class="note">
  <span class="label">範圍</span>
  <p>這份文件只描述已登入使用者的流程。</p>
</div>
```

Use one evidence state for claims whose status matters:

```html
<div class="note verified">
  <span class="label">已驗證</span>
  <div>
    <p>目前的 route 已檢查 workspace membership。</p>
    <p class="evidence-meta"><code>src/routes/workspace.ts</code> · <code>loadWorkspace</code></p>
  </div>
</div>

<div class="note proposed">
  <span class="label">提案</span>
  <p>新增明確的 forbidden error。</p>
</div>

<div class="note assumption">
  <span class="label">假設</span>
  <p>操作者已經選定目前 workspace。</p>
</div>

<div class="note unknown">
  <span class="label">待確認</span>
  <p>尚未決定過期資料的保留時間。</p>
</div>
```

Add `.evidence-meta` only when a real source is available.

## Goals and out of scope

```html
<div class="split">
  <div class="panel goals">
    <div class="panel-head"><span class="sign">✓</span>Goals</div>
    <ul><li>使用者能辨識目前 workspace</li></ul>
  </div>
  <div class="panel nongoals">
    <div class="panel-head"><span class="sign">✕</span>Out of Scope</div>
    <ul><li>不處理跨 workspace 搬移</li></ul>
  </div>
</div>
```

Keep the panel order as goals then out of scope.

## Tables

```html
<div class="tw">
  <table>
    <thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead>
    <tbody><tr><td><code>email</code></td><td><code>string</code></td><td>必填</td></tr></tbody>
  </table>
</div>
```

Keep each row comparable to the others.

## Comparison

```html
<div class="comparison">
  <article class="comparison-item before">
    <div class="comparison-head">Before</div>
    <h3>分散判斷</h3>
    <p>每個 route 各自處理 workspace fallback。</p>
  </article>
  <article class="comparison-item after">
    <div class="comparison-head">After</div>
    <h3>集中解析</h3>
    <p>共用 resolver 回傳明確結果。</p>
  </article>
</div>
```

Use exactly two items. Put shared criteria in the same order on both sides.

## Timeline

Number the stages in reading order:

```html
<ol class="timeline">
  <li><span class="timeline-step">01</span><div><h3>蒐集</h3><p>確認輸入與來源。</p></div></li>
  <li><span class="timeline-step">02</span><div><h3>轉換</h3><p>建立可視化結構。</p></div></li>
  <li><span class="timeline-step">03</span><div><h3>驗證</h3><p>檢查內容與呈現。</p></div></li>
</ol>
```

## Decision matrix

```html
<div class="tw decision-matrix">
  <table>
    <thead><tr><th>方案</th><th>一致性</th><th>維護成本</th><th>結論</th></tr></thead>
    <tbody>
      <tr class="recommended"><td>共用 resolver</td><td>高</td><td>低</td><td><span class="status ok">採用</span></td></tr>
      <tr><td>各 route 判斷</td><td>低</td><td>高</td><td><span class="status muted-status">不採用</span></td></tr>
    </tbody>
  </table>
</div>
```

Use one `recommended` row when the material records a recommendation.

## Rule matrix

Use a rule matrix when one outcome varies along two axes, such as a field group against a lifecycle state. Put the subject in the row header and the context in the column header:

```html
<div class="rule-matrix">
  <table>
    <thead>
      <tr><th>欄位群</th><th>draft 草稿</th><th>active 上刊中</th><th>paused 暫停</th></tr>
    </thead>
    <tbody>
      <tr>
        <th>走期、總預算、每日預算</th>
        <td class="allow">可改</td>
        <td class="hold" data-ac="AC-02">唯讀，須先暫停<span class="cell-ac">AC-02</span></td>
        <td data-ac="AC-03">可改，只驗本次變更欄位<span class="cell-ac">AC-03</span></td>
      </tr>
      <tr>
        <th>廣告品類、格式、計價方式</th>
        <td class="allow">可改</td>
        <td class="deny" data-ac="AC-04">永久唯讀，須複製新項目<span class="cell-ac">AC-04</span></td>
        <td class="deny" data-ac="AC-04">永久唯讀，須複製新項目<span class="cell-ac">AC-04</span></td>
      </tr>
    </tbody>
  </table>
</div>
<ul class="matrix-notes">
  <li class="note-line"><span class="ac-id">AC-05</span><span>draft 按儲存時只驗證名稱。</span></li>
</ul>
```

Every cell states its outcome in the reader's words. Use `allow` for an unrestricted cell, `hold` for a restriction the reader can lift, and `deny` for a permanent one. Leave a cell unclassed when it carries a condition rather than a verdict.

Add `.cell-ac` and `data-ac` inside a story to name the acceptance criterion a cell carries. Put a rule that belongs to the same subject but fits no cell in a `.matrix-notes` list after the table.

## Status summary

```html
<div class="status-summary">
  <div class="status-item"><span class="status ok">完成</span><strong>資料契約</strong><p>輸入與錯誤結果已定案。</p></div>
  <div class="status-item"><span class="status warn">待決</span><strong>保留期限</strong><p>需要產品決策。</p></div>
  <div class="status-item"><span class="status bad">風險</span><strong>舊資料</strong><p>遷移策略尚未驗證。</p></div>
</div>
```

Use `ok`, `warn`, `bad`, or `info` on `.status`. Keep every item in the same categorical frame.

## Metric summary

```html
<div class="metrics">
  <div class="metric"><strong class="metric-value">4</strong><span class="metric-label">公開 endpoints</span><span class="metric-detail">2 read · 2 write</span></div>
  <div class="metric"><strong class="metric-value">3</strong><span class="metric-label">待決問題</span><span class="metric-detail">均需產品確認</span></div>
</div>
```

Use two to four metrics. Every number needs a label and enough context to be read correctly.

## Diagrams

Wrap every Mermaid source block in `.diagram` and follow it immediately with one `.diagram-cap` paragraph.

```html
<div class="diagram"><pre class="mermaid">flowchart TD
A[使用者送出] --> B{驗證通過?}
B -->|是| C[建立帳號]
B -->|否| D[顯示錯誤]
linkStyle default stroke:#337ECC,stroke-width:2px
linkStyle 2 stroke:#9E4A46,stroke-width:2px</pre></div>
<p class="diagram-cap">從送出到建立帳號的判斷順序。紅線是被拒絕的路徑。</p>
```

Edge color carries one meaning throughout the artifact:

| Color | Meaning | Value |
| --- | --- | --- |
| Blue | Successful or primary path | `#337ECC` |
| Red | Blocked or rejected path | `#9E4A46` |
| Amber | Empty or missing-data path | `#8A6524` |

Count `linkStyle` indexes from zero in edge definition order. Name every non-blue path in the caption.

The renderer supports `flowchart` or `graph` with a direction, `stateDiagram-v2`, `sequenceDiagram`, `classDiagram`, `erDiagram`, and `xychart-beta`. Put the diagram header alone on the first line. Put every node and edge on its own line. Use plain node labels. Give every `erDiagram` entity an attribute block with `PK` and `FK` markers. Prefer `TD` for Chinese flowcharts.

## Code

Put the language on the `<pre>` and escape HTML-significant characters:

```html
<pre data-lang="ts"><code>export function createUser(input: CreateUserInput): Promise&lt;User&gt;</code></pre>
```

Use a real Shiki language ID such as `ts`, `tsx`, `json`, `sql`, `bash`, or `python`. Use `text` for pseudocode and indented trees that do not follow a programming-language grammar.

Use a compact text shape inside the same code component when the decision tree selects pseudocode, a call tree, a component tree, or a shallow file tree. Keep only the steps or nodes needed to answer the current question. An indented tree names ownership or hierarchy. Pseudocode names order and branching without inventing executable syntax.

Use a full code block when most of the content is new, omitted context would hide ownership or order, or the reader needs a copyable target shape.

## Diff

Use Diff when exact lines changed or the material already supplies a unified patch. Use before/after sources by default:

```html
<div class="diff-view" data-diff data-diff-style="split" data-file-name="src/value.ts">
  <div class="diff-fallback">
    <div>
      <span class="label">Before</span>
      <pre data-diff-before data-diff-source data-lang="ts"><code>export const value = 1;</code></pre>
    </div>
    <div>
      <span class="label">After</span>
      <pre data-diff-after data-diff-source data-lang="ts"><code>export const value = 2;</code></pre>
    </div>
  </div>
  <div data-diff-host></div>
</div>
```

Use an existing unified patch without converting it back to two files:

```html
<div class="diff-view" data-diff data-diff-style="split">
  <div class="diff-fallback">
    <pre data-diff-patch data-diff-source data-lang="diff"><code>--- a/src/value.ts
+++ b/src/value.ts
@@ -1 +1 @@
-export const value = 1;
+export const value = 2;</code></pre>
  </div>
  <div data-diff-host></div>
</div>
```

Use `split` unless the material calls for `unified`. Set a real filename and a Shiki language ID on before/after sources. A Diff has exactly one source form: one `data-diff-before` plus one `data-diff-after`, or one `data-diff-patch`. Keep the fallback intact. The template hides it only after every file renders successfully.

## Disclosure

Use disclosure for optional supporting detail:

```html
<details class="disclosure">
  <summary>查看推導依據<span class="chev"></span></summary>
  <div class="disclosure-body"><p>Resolver 將缺少的 context 分成明確結果。</p></div>
</details>
```

Keep essential conclusions in the section body.

## User stories

Put one `<article class="story">` per observable behavior inside a `.stories` container. Keep the header, lede, picture, and criteria grid in this order.

```html
<div class="stories">
  <article class="story">
    <div class="story-head">
      <span class="story-id">US-01</span>
      <h3 class="story-title">登入取得工作區</h3>
      <span class="story-count">2 條驗收條件</span>
    </div>
    <p class="story-lede">
      登入成功才拿得到 token。<b>帳密錯誤一律回同一則訊息</b>，不透露帳號是否存在。
    </p>
    <div class="diagram"><pre class="mermaid">flowchart TD
S1[在登入頁] -->|AC-01| R1[取得 token 進工作區]
S1 -->|AC-02| R2[顯示一般錯誤]
linkStyle default stroke:#337ECC,stroke-width:2px
linkStyle 1 stroke:#9E4A46,stroke-width:2px</pre></div>
    <p class="diagram-cap">藍線是成功登入，紅線是被拒絕的路徑。</p>
    <div class="ac-grid">
      <div class="ac-head"><span>條件</span><span>前提</span><span>動作</span><span class="then">預期</span></div>
      <div class="ac" data-ac="AC-01">
        <span class="ac-id">AC-01</span>
        <div class="beat given">在登入頁，帳號啟用中</div>
        <div class="beat when">送出正確帳密</div>
        <div class="beat then">取得 token，進入工作區</div>
      </div>
      <div class="ac" data-ac="AC-02">
        <span class="ac-id">AC-02</span>
        <div class="beat given">在登入頁</div>
        <div class="beat when">送出錯誤帳密</div>
        <div class="beat then">顯示一般錯誤，不透露帳號狀態</div>
      </div>
    </div>
  </article>
</div>
```

The `.story-lede` states the rule that shapes the criteria, in one or two sentences, with `<b>` on the part a reader must remember. Write what this story constrains. One role sentence repeated across every story that shares an actor carries no information.

Use the `AC-NN` identifier alone on a Mermaid edge, so an edge label stays narrow and each sentence appears in one visual form.

The `.ac-grid` lists every criterion of the story, headed by one `.ac-head` row. Give each `.ac` a `data-ac` attribute matching its `.ac-id`. The `.story-count` integer equals the number of `.ac` rows.

The template lights a criterion and its picture together when the reader clicks either one, keyed on `data-ac`. Reuse one `AC-NN` on several edges or cells when the criterion governs all of them.

### Choosing the story picture

Choose the optional story picture through the User story branch in [`SKILL.md` Step 2](../SKILL.md#step-2-select-components). Keep the criteria grid as the complete list. A picture whose nodes only restate individual criteria adds no relationship and should be omitted.

Put every criterion that fits the chosen picture on the picture. Name the criteria left out in the `.diagram-cap` so the reader knows the grid is the complete list. Every `AC-NN` on the picture also appears in the `.ac-grid`.

## API and symbol ledger

Use one `<details>` row per endpoint or exported symbol. Group related rows with `.group-label` when the material covers more than one area.

```html
<div class="group-label">Authentication</div>
<div class="ledger">
  <details>
    <summary>
      <span class="verb post">POST</span>
      <span class="path">/api/users</span>
      <span class="auth">需要登入</span>
      <span class="chev"></span>
    </summary>
    <div class="acc-body">
      <p>建立使用者，email 重複時回 409。</p>
      <h4>Parameters</h4>
      <div class="tw"><table>
        <thead><tr><th>參數</th><th>位置</th><th>型別</th><th>必填</th><th>說明</th></tr></thead>
        <tbody><tr><td><code>email</code></td><td>body</td><td><code>string</code></td><td>是</td><td>使用者信箱</td></tr></tbody>
      </table></div>
      <h4>Response 201</h4>
      <pre data-lang="json"><code>{ "id": "usr_123", "email": "user@example.com" }</code></pre>
    </div>
  </details>
</div>
```

Start each `.acc-body` with one behavior and failure paragraph. Add a `Parameters` table when the item accepts parameters, with one row per parameter and all five columns filled. Add one `Response NNN` heading and payload block for every status that returns a body.

Use `verb get` for GET, `verb post` for POST, PUT, PATCH, and DELETE, and `verb fn` for public functions, types, classes, hooks, and components. A code symbol row uses its symbol name as `.path`, its layer in `.auth`, a file path, and a `Signature` code block. Add a parameter table when the signature omits flags, defaults, or constraints.

## Wireframes

A flow groups screens that the reader can click through.

```html
<div data-flow data-start="list">
  <article data-screen="list" data-screen-title="使用者列表">
    <div data-state-panel="default" data-state-label="有資料">
      <div class="browser">
        <div class="browser-bar"><span class="dots"><i></i><i></i><i></i></span><span class="url">https://app.example.com/users</span></div>
        <div class="screen-body">
          <div class="topbar"><strong>使用者</strong><button class="btn line" data-goto="form">新增使用者</button></div>
        </div>
      </div>
    </div>
    <div data-state-panel="empty" data-state-label="空狀態">
      <div class="browser"><div class="screen-body"><div class="msg warn">還沒有任何使用者</div></div></div>
    </div>
  </article>
  <article data-screen="form" data-screen-title="新增使用者">
    <div class="browser">
      <div class="browser-bar"><span class="dots"><i></i><i></i><i></i></span><span class="url">https://app.example.com/users/new</span></div>
      <div class="screen-body">
        <div class="pane">
          <p class="pane-title">新增使用者</p>
          <div class="field">Email</div>
          <button class="btn solid" data-goto="done">送出</button>
          <button class="btn quiet" data-goto="list">取消</button>
        </div>
      </div>
    </div>
  </article>
  <article data-screen="done" data-screen-title="完成">
    <div class="browser"><div class="screen-body"><div class="msg ok">帳號已建立</div><button class="btn line" data-goto="list">回列表</button></div></div>
  </article>
</div>
```

Give every screen a unique `data-screen`, a nonempty `data-screen-title`, and a path from `data-start`. Give every state panel a unique `data-state-panel` and a nonempty `data-state-label`.

Use `.pane` for a centered form column, `.pane-title` for its heading, `.field` for an input placeholder, `.topbar` for a page heading and action, and `.msg` with `ok`, `bad`, `warn`, or `info` for messages. Use `.btn solid` for the primary action, `.btn line` for a secondary action, and `.btn quiet` for cancel or back.

Put text-only rules in an ordered `.notes` list after the flow.
