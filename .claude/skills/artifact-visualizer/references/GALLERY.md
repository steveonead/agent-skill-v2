# Component gallery and document design

`assets/template.html` is the authoritative implementation. Its `data-demo` sections are the canonical examples: each component below names the demo host and JSON data block that show a working invocation.

## Document design

Fixed across every artifact:

- The template's document shell: sticky table of contents, single-column main flow, and the visual anatomy of hierarchical number, short title, up to three explanatory sentences, source line, and optional interaction-status label.
- The table of contents behaves as an accordion so the whole list fits one viewport without a scrollbar of its own: sections always show, and only the section being read expands its visuals. It builds itself from `data-toc-section`, `data-toc-visual`, `[data-section-title]`, and `[data-visual-title]`, assigns every number, and marks a visual whose callout carries a warning or negative tone. Call `buildToc()` last, after awaiting every async builder, so the risk markers see the finished callouts.
- Maple Mono CN is the only family, carrying both Latin and CJK glyphs, and rendered text stays at 16px or larger. `DESIGN-SYSTEM.md` holds the sizes and measures a new component must match.
- Links in the reading column are underlined and accent-colored, so a reader tells one from body text before clicking.
- The Vitesse Light palette through the `--artifact-*` tokens, Shiki's `vitesse-light` theme, and the template-owned light Pierre theme. A caller may remap only `--artifact-accent`, `--artifact-positive`, `--artifact-warning`, and `--artifact-negative` to named Vitesse tokens.

Yours to decide:

- How many components, and in what order. Start with the visual or conclusion that best performs the document's job.
- Section grouping, emphasis, and the short connective copy between visuals.
- Side-by-side placement, the one exception to the single-column flow, when direct comparison depends on alignment and both panes fit at their natural heights.
- Interactivity. Default to static. Enable tree collapse when a hierarchy needs disclosure, and add another vanilla JavaScript interaction only when a state, order, filter, or causal relationship requires it. Mark every interactive visual with nearby localized status text such as `Interactive` or `可互動`.

## Component catalog

Read data with `ArtifactUI.readData(id)` from a `script[type="application/json"]` block, then call the builder with a host id or element. `createSignatureList`, `renderDiagram`, `renderDiff`, and `renderCode` are async: await all of them before calling `buildToc()`.

### createPseudocode(host, { lines })

Decision logic, guards, and ordered steps, free of implementation noise. Each line is `{ indent, segments, note? }` and each segment `{ type, text }` with type in `plain | keyword | function | value | operator | symbol | comment`. Example: `demo-pseudocode` with `data-pseudocode`.

### createTree(host, { roots }, { variant, collapsible? })

One nested-tree anatomy, three vocabularies:

- `call-stack`: nodes `{ frame, location?, detail?, children?, active?, badges? }`. Example: `demo-call-stack` with `data-call-stack`.
- `component-tree`: nodes `{ component, props?, responsibility?, children?, active?, badges? }`. Example: `demo-component-tree` with `data-component-tree`.
- `file-tree`: nodes `{ name, kind, path?, note?, children?, active?, badges? }`. Example: `demo-file-tree` with `data-file-tree`.

`collapsible: true` adds toggle buttons. Mark the node under discussion with `active`.

### createSignatureList(host, data)

Interfaces and responsibilities grouped by owner. Data is `{ lang?, groups: [{ owner, summary?, items: [{ declaration, lang?, fields?: [{ label, value }] }] }] }`. Declarations are Shiki-highlighted. Example: `demo-signatures` with `data-signatures`.

### renderCode(host, source, { lang })

Source whose surrounding context matters, Shiki-highlighted. Example: `demo-code` with `data-code`.

### renderDiff(host, oldFile, newFile)

Changes and patches through Pierre. Each file is `{ name, contents }`. Pierre runs on the main thread, so keep the excerpt to the smallest span that still grounds the claim, roughly 150 lines at the outside. The template post-processes Pierre's shadow root to mute whitespace-only highlight spans and to unquote git's octal-escaped non-ASCII file names, so keep `watchDiffShadowRoot` alongside the renderer. Example: `demo-diff` with `data-diff`.

### renderDiagram(host, source)

States, sequences, and flows with meaningful graph topology, through Beautiful Mermaid. The template fits each diagram to its panel width, holding labels between a 16px floor and a 20px ceiling, so the whole shape is visible without panning and a small diagram is not blown up into a poster. Height is uncapped: the page scroll carries a tall diagram. A diagram whose labels reach the floor before it fits overflows horizontally and becomes grab-scrollable, the one diagram case that carries an interaction-status label. Example: `demo-sequence`, `demo-flowchart`, and `demo-state` with `data-sequence`, `data-flowchart`, and `data-state`.

Prefer `LR` over `TD` for a chain with little branching: the fit is width-bound, so a horizontal chain reads larger.

### createChecklist(host, { items })

Tasks, acceptance criteria, and findings with per-item status. Items are `{ state, stateLabel, label, note? }`. `state` in `pass | pending | fail` picks the color, `stateLabel` is the displayed localized text. Host is a `.checklist-host` inside a code panel. Example: `demo-checklist` with `data-checklist`.

### createMatrix(host, { columns, rows, corner? })

Two axes crossed, where the answer lives in the cell: state combinations against their consequences, or affected callers against what each must do. Rows are `{ label, cells }` and cells `{ value, tone?, note? }` with tone in `positive | warning | negative`. `corner` labels the header cell above the row labels. Host is a `.matrix-host` inside a code panel. Example: `demo-matrix` with `data-matrix`.

Two matrices is the practical ceiling for one document. When a third crossing appears, at least one of them is usually a process or a topology, so check whether `renderDiagram` or `createPseudocode` states it better.

### createStatCards(host, { items })

Headline metrics for a change, run, or review. Items are `{ label, value, tone?, note? }` with tone in `positive | warning | negative`. Host is a plain `.stat-grid` element, each card its own surface. Example: `demo-stat-cards` with `data-stat-cards`.

### createCallout(host, { tone, title?, body })

One risk, decision, or caveat per callout. Tone in `note | positive | warning | negative`. Host is an `.artifact-surface` element. Example: `demo-callout` with `data-callout`.

### createFileChangeList(host, { files })

Per-file change overview for a diff or pull request. Files are `{ path, change, changeLabel, additions?, deletions?, note? }`. `change` in `added | modified | removed | renamed` picks the color, `changeLabel` is the displayed localized text. Host is a `.filechange-list` inside a code panel. Example: `demo-file-changes` with `data-file-changes`.

### Mockup primitives

Low-fidelity UI structure and spatial relationships, assembled from the template's `.mockup-*` classes. Example: the `#html-mockup` demo article, which exercises the full set.


## Construction rules

- Replace the template's document language, title, demo content, `rendererMessages` and `uiMessages` strings, and sample data with the artifact's real content. Remove unused `data-demo` sections, data blocks, and demo invocations. Keep the shared CSS, page shell, table-of-contents builder, `ArtifactUI` methods, and renderer infrastructure.
- Serialize embedded JSON with `<`, `>`, `&`, U+2028, and U+2029 escaped for an HTML script context. Insert source material through text-safe DOM APIs or renderer inputs. Treat renderer-produced markup as trusted only at the renderer boundary.
- Keep the HTML self-contained apart from the pinned CDN requests, runnable directly in the browser without a build step.
- Keep renderer failures local: a failure replaces only its mount point with the localized error component and leaves the rest of the document usable.

## Verification

Open the artifact at 1440 by 900, let every renderer settle, then evaluate the contents of `assets/verify.js` in the page. It returns `{ ok, problems, visuals, suspects }`: `problems` names each defect it proved, in plain language, and `suspects` names the visuals worth a screenshot, each with the absolute page position to scroll to. Fix what it reports and evaluate it again until `ok` is true.

Then screenshot each suspect and inspect it for the crowding, overlap, and truncation the DOM cannot expose. One evaluation and a few targeted captures carry the whole loop, so reach for a wider sweep only when a capture shows something the probe missed. The probe proves structure, not judgment, and it recognizes an interactive visual only by a tree toggle or a scroll track, so a custom interaction still needs its status text placed by hand.

Judge these yourself:

- The output path and next numeric prefix are correct.
- Every component supports a claim in scope, and each custom component reuses the tokens, typography, and anatomy in `DESIGN-SYSTEM.md`.
- Every source line is present, every inference is labeled, and secrets are redacted.
- DOM insertion is text-safe, and executable contexts contain no untrusted strings.
