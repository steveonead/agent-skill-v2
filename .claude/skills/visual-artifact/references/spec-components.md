# Specification Component Pack

Core catalog rules still apply.

## Contents

- [User stories](#user-stories)
- [API and symbol ledger](#api-and-symbol-ledger)
- [Wireframes](#wireframes)

## User stories

Put one `<article class="story">` per observable behavior inside a `.stories` container. Keep the header, role statement, diagram, and collapsed text criteria in this order.

```html
<div class="stories">
  <article class="story">
    <div class="story-head">
      <span class="story-id">US-01</span>
      <h3 class="story-title">登入取得工作區</h3>
      <span class="story-count">2 條驗收條件</span>
    </div>
    <dl class="story-role">
      <dt>身為</dt><dd>AOE</dd>
      <dt>想要</dt><dd>用 email 與密碼登入</dd>
      <dt>以便</dt><dd>進到工作區操作資料</dd>
    </dl>
    <div class="diagram"><pre class="mermaid">flowchart TD
S1[在登入頁] -->|AC-01| R1[取得 token 進工作區]
S1 -->|AC-02| R2[顯示一般錯誤]
linkStyle default stroke:#337ECC,stroke-width:2px
linkStyle 1 stroke:#9E4A46,stroke-width:2px</pre></div>
    <p class="diagram-cap">藍線是成功登入，紅線是被拒絕的路徑。</p>
    <details class="ac-text">
      <summary>文字版驗收條件<span class="chev"></span></summary>
      <div class="ac-list">
        <div class="ac">
          <span class="ac-id">AC-01</span>
          <div class="beat given">在登入頁，帳號啟用中</div>
          <div class="beat when">送出正確帳密</div>
          <div class="beat then">取得 token，進入工作區</div>
        </div>
        <div class="ac">
          <span class="ac-id">AC-02</span>
          <div class="beat given">在登入頁</div>
          <div class="beat when">送出錯誤帳密</div>
          <div class="beat then">顯示一般錯誤，不透露帳號狀態</div>
        </div>
      </div>
    </details>
  </article>
</div>
```

Every acceptance criterion appears once as a labeled edge whose label is its `AC-NN` ID. A node names a state or outcome; keep the detailed action in the matching `.ac` row. The `.story-count` integer, diagram criterion IDs, and `.ac` rows must match.

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

A flow groups screens that the reader can click through. Every `data-goto` stays inside its nearest `data-flow`.

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

Every flow has a valid `data-start`. Every screen has a unique `data-screen` and a nonempty `data-screen-title`. Every `data-goto` names a screen in the same flow. Every screen is reachable from the start screen. Every state panel has a unique `data-state-panel` and nonempty `data-state-label` within its screen.

Use `.pane` for a centered form column, `.pane-title` for its heading, `.field` for an input placeholder, `.topbar` for a page heading and action, and `.msg` with `ok`, `bad`, `warn`, or `info` for messages. Use `.btn solid` for the primary action, `.btn line` for a secondary action, and `.btn quiet` for cancel or back.

Put text-only rules in an ordered `.notes` list after the flow.
