# Component Catalog

## Hard rules

- Color comes only from the CSS variables the template defines on `:root`: `--brand`, `--brand-deep`, `--brand-soft`, `--brand-bg`, `--paper`, `--surface`, `--sunken`, `--ink`, `--ink-2`, `--ink-3`, `--line`, `--line-2`, `--green`, `--green-bg`, `--amber`, `--amber-bg`, `--red`, `--red-bg`. Reach them through the catalog's class names. A literal color (`#fff`, `rgb(...)`) or a utility framework class (`bg-white`, `text-slate-500`, `card`, `badge`, `alert`) resolves to nothing, because the page loads no CSS framework.
- Authored sections are markup only: the template's script and CSS provide all behavior.
- The page renders one light theme.

## Prose blocks

Use `<h3>` for subsections inside a section. The section headings and the table of contents already exist in the template.

Note, for scope statements and constraints:

```html
<div class="note">
  <span class="label">範圍</span>
  <p>這個 feature 只影響已登入的使用者。</p>
</div>
```

Add `proposal` for anything that extends beyond the current code:

```html
<div class="note proposal">
  <span class="label">提案</span>
  <p>新增 endpoint 時，缺少範圍限制的查詢應在資料存取層主動拒絕。</p>
</div>
```

Goals and Out of Scope:

```html
<div class="split">
  <div class="panel goals">
    <div class="panel-head"><span class="sign">✓</span>Goals</div>
    <ul>
      <li>使用者可以在 30 秒內完成註冊</li>
    </ul>
  </div>
  <div class="panel nongoals">
    <div class="panel-head"><span class="sign">✕</span>Out of Scope</div>
    <ul>
      <li>不處理企業 SSO</li>
    </ul>
  </div>
</div>
```

The second panel keeps the class `nongoals` and the heading text `Out of Scope`.

Data table:

```html
<div class="tw">
  <table>
    <thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead>
    <tbody>
      <tr><td><code>email</code></td><td><code>string</code></td><td>必填，需通過格式驗證</td></tr>
    </tbody>
  </table>
</div>
```

## Diagrams (beautiful-mermaid)

Wrap every diagram in `.diagram`, and follow it with one line of `.diagram-cap` saying what the diagram shows.

```html
<div class="diagram"><pre class="mermaid">flowchart TD
A[使用者送出表單] --> B{驗證通過?}
B -->|是| C[建立帳號]
B -->|否| D[顯示錯誤]
linkStyle default stroke:#337ECC,stroke-width:2px
linkStyle 1 stroke:#9E4A46,stroke-width:2px</pre></div>
<p class="diagram-cap">從送出到建立帳號的判斷順序。<span style="color:var(--red)">紅線</span>是被擋下來的路徑。</p>
```

Edge color carries meaning, and the same three colors apply to every diagram in the spec:

| Color | Meaning | Value |
| --- | --- | --- |
| Blue | The path that succeeds | `#337ECC` |
| Red | The path that gets blocked or rejected | `#9E4A46` |
| Amber | An empty or missing-data state | `#8A6524` |

`linkStyle` indexes edges in definition order starting at 0. Recount after adding or removing an edge. Name the colored paths in the `.diagram-cap` so the reader knows what a red line means.

Syntax rules for this renderer, stricter than official mermaid:

- Supported types: `flowchart` / `graph` (TD, TB, LR, BT, RL), `stateDiagram-v2`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `xychart-beta`. Any other type (gantt, pie, mindmap, journey) throws, and the page shows an inline error box instead of the diagram.
- The header keyword stands alone on the first line. Semicolon-joined one-liners like `graph TD; A-->B` throw. Put every node and edge on its own line.
- Node labels are plain text. A `<br/>` inside a label renders literally, so split the idea into two nodes instead.
- Give every `erDiagram` entity its attribute block with `PK` and `FK` markers. An entity without one renders the words `(no attributes)`.

Prefer `TD` over `LR`. A left-to-right chain of Chinese labels reaches roughly 2000px wide and forces the reader to drag.

## Code blocks (shiki)

The language goes in `data-lang` on the `<pre>`:

```html
<pre data-lang="ts"><code>export function createUser(input: CreateUserInput): Promise&lt;User&gt;</code></pre>
```

Escape `<` as `&lt;`. Use a real language id (`ts`, `tsx`, `json`, `sql`, `bash`, `python`).

## User stories

One `<article class="story">` per story, all of them inside the template's `.stories` container. A story has four parts in this order: the header, the role statement, the diagram, and the collapsed text version.

```html
<article class="story">
  <div class="story-head">
    <span class="story-id">US-01</span>
    <h3 class="story-title">登入取得工作區</h3>
    <span class="story-count">2 條驗收條件</span>
  </div>
  <dl class="story-role">
    <dt>身為</dt><dd>OneAD 的 AOE</dd>
    <dt>想要</dt><dd>用 email 與密碼登入</dd>
    <dt>以便</dt><dd>進到工作區操作廣告資料</dd>
  </dl>
  <div class="diagram"><pre class="mermaid">flowchart TD
S1[在登入頁] -->|AC-01 送出正確帳密| R1[取得 token 進工作區]
S1 -->|AC-02 送出錯誤帳密| R2[電子郵件或密碼錯誤]
linkStyle default stroke:#337ECC,stroke-width:2px
linkStyle 1 stroke:#9E4A46,stroke-width:2px</pre></div>
  <details class="ac-text">
    <summary>文字版驗收條件<span class="chev"></span></summary>
    <div class="ac-list">
      <div class="ac-legend"><span></span><span>前提</span><span></span><span>動作</span><span></span><span>結果</span></div>
      <div class="ac">
        <span class="ac-id">AC-01</span>
        <div class="beat given">在登入頁，帳號啟用中</div><div class="arrow"></div>
        <div class="beat when">送出正確的 email 與密碼</div><div class="arrow"></div>
        <div class="beat then">取得 token，進入工作區</div>
      </div>
      <div class="ac">
        <span class="ac-id">AC-02</span>
        <div class="beat given">在登入頁</div><div class="arrow"></div>
        <div class="beat when">送出錯誤的 email 或密碼</div><div class="arrow"></div>
        <div class="beat then">顯示錯誤訊息，不透露帳號是否存在</div>
      </div>
    </div>
  </details>
</article>
```

Rules that keep the diagram and the text in step:

- Every acceptance criterion appears as one labelled edge. The label starts with its `AC-NN` id, then the action, so a reader who finds a line knows which criterion it is.
- A node is a state or an outcome. The action lives on the edge.
- `.story-count` states how many criteria the story has.

The three beat classes each take one kind of content: `given` is the state that already holds, `when` is the single thing the user does, and `then` is what gets verified.

## API ledger

Every endpoint and exported symbol is one `<details>` row inside `.ledger`. Group rows under `.group-label` headings when the feature has more than one area.

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
      <p>建立新使用者，email 重複時回 409。</p>
      <h4>Parameters</h4>
      <div class="tw">
        <table>
          <thead><tr><th>參數</th><th>位置</th><th>型別</th><th>必填</th><th>說明</th></tr></thead>
          <tbody>
            <tr><td><code>email</code></td><td>body</td><td><code>string</code></td><td>是</td><td>使用者信箱</td></tr>
          </tbody>
        </table>
      </div>
      <h4>Response 201</h4>
      <pre data-lang="json"><code>{ "id": "usr_123", "email": "user@example.com" }</code></pre>
    </div>
  </details>
</div>
```

Required contents of `.acc-body`, applied to each row on its own:

- One description paragraph comes first, saying what the row does and how it fails.
- A row that takes parameters follows that paragraph with `<h4>Parameters</h4>` and the parameter table, one table row per parameter, with all five columns filled.
- A row that returns a body follows with `<h4>Response NNN</h4>` and a `data-lang` code block holding a real example payload, one such pair for each status code that returns a body.
- The description paragraph carries behavior, and the table carries the field list.

A public function, type, class, hook, or component uses the same row with `verb fn`, the symbol name as the path, and its layer as the `auth` slot:

```html
<details>
  <summary>
    <span class="verb fn">FUNC</span>
    <span class="path">createUser</span>
    <span class="auth">backend</span>
    <span class="chev"></span>
  </summary>
  <div class="acc-body">
    <p>建立使用者並寄出驗證信，email 重複時丟 <code>DuplicateEmailError</code>。</p>
    <h4>檔案</h4>
    <p><code>src/services/user.ts</code></p>
    <h4>Signature</h4>
    <pre data-lang="ts"><code>export async function createUser(
  input: CreateUserInput,
): Promise&lt;User&gt;</code></pre>
  </div>
</details>
```

On a code symbol row, `<h4>Signature</h4>` stands in for the parameter table when the argument types state everything a caller needs. Give the symbol an `<h4>Parameters</h4>` table as well when its arguments carry required flags, defaults, or constraints that the signature leaves out.

Verb class by kind:

| Kind | Class |
| --- | --- |
| GET | `verb get` |
| POST, PUT, PATCH, DELETE | `verb post` |
| Code symbol | `verb fn` |

## Wireframe

### Flow container and screens

A flow is a group of screens the reader clicks through. The template script builds the screen tab bar, shows one screen at a time, and starts at `data-start`.

```html
<div data-flow data-start="list">
  <article data-screen="list" data-screen-title="使用者列表">
    <div class="browser">
      <div class="browser-bar">
        <span class="dots"><i></i><i></i><i></i></span>
        <span class="url">https://app.example.com/users</span>
      </div>
      <div class="screen-body">
        <div class="topbar"><strong>使用者</strong><button class="btn line" data-goto="form">新增使用者</button></div>
      </div>
    </div>
  </article>

  <article data-screen="form" data-screen-title="註冊表單">
    <div class="browser">
      <div class="browser-bar">
        <span class="dots"><i></i><i></i><i></i></span>
        <span class="url">https://app.example.com/users/new</span>
      </div>
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
    <div class="browser">
      <div class="browser-bar">
        <span class="dots"><i></i><i></i><i></i></span>
        <span class="url">https://app.example.com/users</span>
      </div>
      <div class="screen-body">
        <div class="pane">
          <div class="msg ok">帳號已建立</div>
          <button class="btn line" data-goto="list">回列表</button>
        </div>
      </div>
    </div>
  </article>
</div>
```

Rules the template enforces at load time:

- Every `data-goto` value matches a `data-screen` in the same flow. An unmatched value gets a dashed red outline and a console error.
- Every screen carries a `data-screen-title`, which becomes its tab label.

Multiple independent flows are fine, one `data-flow` block each.

Building blocks inside `.screen-body`:

| Element | Markup | Use |
| --- | --- | --- |
| Centered form column | `<div class="pane">` | Login, single-purpose forms |
| Form heading | `<p class="pane-title">` | Title above a pane |
| Input placeholder | `<div class="field">文字</div>` | Any text field |
| Primary action | `<button class="btn solid">` | The one action the screen exists for |
| Secondary action | `<button class="btn line">` | Alternatives of equal weight |
| Text action | `<button class="btn quiet">` | Cancel, back, forgot password |
| Page header row | `<div class="topbar">` | Screen title plus one control |
| Message | `<div class="msg ok">` | `ok`, `bad`, `warn`, `info` |

### Screen states

Panels inside a screen show its UX states. The template script builds the state switcher and shows the first panel, so put the default state first.

```html
<article data-screen="list" data-screen-title="使用者列表">
  <div data-state-panel="default" data-state-label="有資料">
    <div class="browser">…</div>
  </div>
  <div data-state-panel="empty" data-state-label="空狀態">
    <div class="browser">
      <div class="screen-body"><div class="msg warn">還沒有任何使用者</div></div>
    </div>
  </div>
  <div data-state-panel="error" data-state-label="錯誤">
    <div class="browser">
      <div class="screen-body"><div class="msg bad">載入失敗，請重試</div></div>
    </div>
  </div>
</article>
```

### Annotations

Numbered notes below a mockup, for rules the picture cannot show:

```html
<ol class="notes">
  <li>按下後立即停用按鈕，避免重複送出</li>
</ol>
```

## Common mistakes

| Wrong | Right |
| --- | --- |
| `class="card bg-base-200"` or `class="bg-white text-gray-700"` | A catalog class such as `class="panel"`, which reaches the CSS variables |
| `<pre class="mermaid">` on its own | Wrap it in `<div class="diagram">` |
| `<pre><code class="language-json">` | `<pre data-lang="json"><code>` |
| `<pre class="mermaid">graph TD; A-->B</pre>` | Header line `graph TD` alone, edges on their own lines |
| `pie title 佔比` in a mermaid block | Unsupported type, use a data table instead |
| `flowchart LR` for a user story | `flowchart TD`, so the diagram fits the column width |
| An acceptance criterion table with no diagram | A diagram whose edge labels carry every `AC-NN` |
| An edge label reading only `送出正確帳密` | `AC-01 送出正確帳密` |
| `erDiagram` entities with no attribute block | Attributes with `PK` and `FK` markers |
| `data-goto="signup"` with `data-screen="form"` | Make the two values identical |
| Writing an `onclick` or a `<script>` for interaction | Use `data-goto` and `data-state-panel`, the template script does the rest |
| An `.acc-body` reading `<p>body：<code>name</code>、<code>channelId</code> 必填。</p>` | A description paragraph, then `<h4>Parameters</h4>` and a table row per parameter |
| Unescaped `<` in a code block | Write `&lt;` |
