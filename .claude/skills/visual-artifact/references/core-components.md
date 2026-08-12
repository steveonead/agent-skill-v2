# Core Component Catalog

Copy a complete snippet and replace its content. Use template-defined classes. Reserve literal colors for Mermaid `linkStyle` declarations that follow the semantic color table.

## Contents

- [Prose and evidence](#prose-and-evidence)
- [Goals and out of scope](#goals-and-out-of-scope)
- [Tables](#tables)
- [Comparison](#comparison)
- [Timeline](#timeline)
- [Decision matrix](#decision-matrix)
- [Status summary](#status-summary)
- [Metric summary](#metric-summary)
- [Diagrams](#diagrams)
- [Code](#code)
- [Disclosure](#disclosure)

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

Use `verified`, `proposed`, `assumption`, and `unknown` only with their defined meanings. Add `.evidence-meta` only when a real source is available.

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

Keep the second panel class and heading as `nongoals` and `Out of Scope`.

## Tables

```html
<div class="tw">
  <table>
    <thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead>
    <tbody><tr><td><code>email</code></td><td><code>string</code></td><td>必填</td></tr></tbody>
  </table>
</div>
```

Use tables for repeated fields and exact mappings. Keep each row comparable to the others.

## Comparison

Use comparison for two alternatives, versions, or before and after states:

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

Use timeline for a linear sequence without branching:

```html
<ol class="timeline">
  <li><span class="timeline-step">01</span><div><h3>蒐集</h3><p>確認輸入與來源。</p></div></li>
  <li><span class="timeline-step">02</span><div><h3>轉換</h3><p>建立可視化結構。</p></div></li>
  <li><span class="timeline-step">03</span><div><h3>驗證</h3><p>檢查內容與呈現。</p></div></li>
</ol>
```

Use Mermaid instead when a step branches or loops.

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

Use one `recommended` row when the material records a recommendation. Mark a winner only when the material records it.

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

Use two to four metrics. Every number needs a label and enough context to prevent a misleading interpretation.

## Diagrams

Use Mermaid for flow, state, sequence, class, entity relationship, or quantitative chart relationships. Wrap every source block in `.diagram` and follow it immediately with one `.diagram-cap` paragraph.

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

Use a real Shiki language ID such as `ts`, `tsx`, `json`, `sql`, `bash`, or `python`.

## Disclosure

Use disclosure for optional supporting detail:

```html
<details class="disclosure">
  <summary>查看推導依據<span class="chev"></span></summary>
  <div class="disclosure-body"><p>Resolver 將缺少的 context 分成明確結果。</p></div>
</details>
```

Keep essential conclusions outside a disclosure.
