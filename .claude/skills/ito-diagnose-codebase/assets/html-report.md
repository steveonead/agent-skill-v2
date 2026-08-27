# HTML report format

The architectural review is rendered as a single HTML file in the OS temp directory. Write every user-visible string in Traditional Chinese (zh-TW), while keeping code identifiers and canonical `codebase-design` terms in English. Tailwind and Mermaid both come from CDNs. Use Mermaid for graph-shaped diagrams. Use hand-built divs and inline SVG for editorial visuals such as mass diagrams and cross-sections. Use both across the report.

## Scaffold

```html
<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="utf-8" />
    <title>{{repo name}} 架構診斷</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Show the repo name, a date formatted for zh-TW such as `2026 年 8 月 25 日`, and this compact legend: `實線方框 = module`, `虛線 = seam`, `紅色箭頭 = 洩漏`, `粗深色方框 = deep module`. Start with the candidates immediately after the header.

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms from `codebase-design` without ceremony.

Each candidate is one `<article>`. Use these visible section labels: `檔案`, `問題`, `方案`, `改善`, `之前`, `之後`, `建議程度`, and `架構決策紀錄衝突`.

- **Title**: short, names the deepening in Traditional Chinese (e.g. "收攏 Order 接單流程").
- **Badge row**: recommendation strength (`強烈建議` = emerald, `值得探索` = amber, `推測性建議` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files**: monospaced list, `font-mono text-sm`.
- **Before / After diagram**: the centrepiece. Two columns, side by side. See patterns below.
- **Problem**: one sentence. What hurts.
- **Solution**: one sentence. What changes.
- **Wins**: short Traditional Chinese bullets, e.g. "測試只通過一個 interface", "Pricing 不再跨 seam 洩漏", "刪除 4 個 shallow module".
- **ADR callout** (if applicable): one line in an amber-tinted box.

Use diagrams and short labels instead of explanatory paragraphs. Redraw any diagram that needs a paragraph to be understood.

## Diagram patterns

Pick the pattern that fits each candidate, and vary the patterns across the report.

### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a Tailwind-styled card. Style with classDef to colour leakage edges red and the deep module dark. Sequence diagrams work well when the before state has six round-trips and the after state has one.

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals, since Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module: one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. Serif optional for headings (`font-serif` works well with stone/slate).
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams, so they read as schematic, not as UI.
- The only scripts are the Tailwind CDN and the Mermaid ESM import. The report is otherwise static: no app code, no interactivity beyond Mermaid's own rendering.

## Top recommendation section

One larger card labelled `首要建議`. Candidate name, one sentence on why, anchor link to its card.

## Tone

Write concise Traditional Chinese. Keep architectural nouns and verbs from `codebase-design` in English.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

Use **module** instead of component, service, or unit. Use **interface** instead of API or signature. Use **seam** instead of boundary. Use layer and wrapper only for their literal meanings, not as substitutes for module.

**Traditional Chinese phrasings that fit the style:**

- "Order 接單 module 過淺，interface 幾乎和 implementation 一樣複雜。"
- "Pricing 跨越 seam 洩漏。"
- "深化方向：一個 interface，一個測試入口。"
- "兩個 adapter 讓 seam 成立，正式環境使用 HTTP，測試使用記憶體內實作。"

**Wins bullets** name the gain in glossary terms: *"locality：錯誤集中在一個 module"*, *"leverage：一個 interface，N 個呼叫端"*, *"interface 縮小，implementation 吸收原有轉接層"*. Replace generic claims such as *"更好維護"* or *"程式碼更乾淨"* with a glossary term and a concrete mechanism.

Cut hedging, throat-clearing, and phrases such as "it's worth noting that". If a sentence could be a bullet, make it a bullet. Cut any bullet that contains no concrete information.
