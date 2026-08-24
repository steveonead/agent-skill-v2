# Component gallery and document design

`assets/build.mjs` emits every component from a JSON spec, and its header documents the spec schema. `assets/template.html` holds a working invocation of every component under `demo-<name>` and `data-<name>` ids, plus `#html-mockup` for the mockup primitives, for the rare case the spec cannot express something.

## Document design

Fixed across every artifact:

- The template's document shell: sticky table of contents, single-column main flow, and the visual anatomy of hierarchical number, short title, optional concise context, source line, and optional interaction-status label.
- The table of contents behaves as an accordion so the whole list fits one viewport without a scrollbar of its own. Sections always show, only the section being read expands its visuals, and a visual whose callout carries a warning or negative tone gets a risk marker.
- When the caller asks for an accent change, remap only `--artifact-accent`, `--artifact-positive`, `--artifact-warning`, and `--artifact-negative`, and only to named Vitesse tokens.

Decided per artifact:

- Group visuals that share a subject, and title each group by what it settles.
- Default to static presentation. Enable tree collapse when a hierarchy needs disclosure, and add another vanilla JavaScript interaction when a state, order, filter, or causal relationship requires it. Mark every interactive visual with nearby localized status text such as `Interactive` or `可互動`.

## Component catalog

The spec's `component` values map to the builders below: `statCards`, `fileChanges`, `signatures`, `pseudocode`, `tree`, `code`, `diff`, `diagram`, `checklist`, `matrix`, `callout`, and `html`. `build.mjs` owns the host markup, panel and caption wrappers, embedded data blocks, escaping, the bootstrap order, the interaction-status labels, and the `buildToc()` call, so a visual carries only its `component`, `options`, and `data`.

### pseudocode (createPseudocode)

Each line is `{ indent, segments, note? }` and each segment `{ type, text }` with type in `plain | keyword | function | value | operator | symbol | comment`.

### tree (createTree)

One nested-tree anatomy, three vocabularies chosen by `options.variant`:

- `call-stack`: nodes `{ frame, location?, detail?, children?, active?, badges? }`.
- `component-tree`: nodes `{ component, props?, responsibility?, children?, active?, badges? }`.
- `file-tree`: nodes `{ name, kind, path?, note?, children?, active?, badges? }`.

`options.collapsible: true` adds toggle buttons. Mark the node under discussion with `active`.

### signatures (createSignatureList)

Data is `{ lang?, groups: [{ owner, summary?, items: [{ declaration, lang?, fields?: [{ label, value }] }] }] }`. Declarations are Shiki-highlighted.

### code (renderCode)

Shiki-highlighted source from `{ source, lang? }`.

### diff (renderDiff)

Changes and patches through Pierre, from `{ oldFile, newFile }` with each file `{ name, contents }`. The template post-processes Pierre's shadow root to mute whitespace-only highlight spans and to unquote git's octal-escaped non-ASCII file names.

### diagram (renderDiagram)

Diagram source rendered through Beautiful Mermaid. The template fits each diagram to its panel width, holding labels between a 16px floor and a 20px ceiling, so the whole shape is visible without panning and a small diagram is not blown up into a poster. Height is uncapped: the page scroll carries a tall diagram. A diagram whose labels reach the floor before it fits overflows horizontally and becomes grab-scrollable, the one diagram case that carries an interaction-status label. The fit is width-bound, so a chain drawn `LR` reads larger than the same chain drawn `TD`.

### checklist (createChecklist)

Items are `{ state, stateLabel, label, note? }`. `state` in `pass | pending | fail` picks the color, and `stateLabel` is the displayed localized text.

### matrix (createMatrix)

Rows are `{ label, cells }` and cells `{ value, tone?, note? }` with tone in `positive | warning | negative`. `corner` labels the header cell above the row labels.

### statCards (createStatCards)

Items are `{ label, value, tone?, note? }` with tone in `positive | warning | negative`.

### callout (createCallout)

Data is `{ tone, title?, body }` with tone in `note | positive | warning | negative`.

### fileChanges (createFileChangeList)

Files are `{ path, change, changeLabel, additions?, deletions?, note? }`. `change` in `added | modified | removed | renamed` picks the color, and `changeLabel` is the displayed localized text.

### Mockup primitives, through `html`

Low-fidelity UI structure assembled from the template's `.mockup-*` classes and delivered as an `html` fragment. The template's `#html-mockup` article exercises the full set.

## Construction rules

- Override any template message string through the spec's `messages`, written in the artifact's language.
- Keep the HTML self-contained apart from the pinned CDN requests, runnable directly in the browser without a build step.
- A custom `html` fragment is trusted and inserted verbatim, so route real source text through a builder's `data` and keep the fragment to the structure a custom component needs.
- A renderer failure replaces only its mount point with the localized error component and leaves the rest of the document usable.

## Verification

`node assets/check.mjs <out.html>` proves what a browser can prove and names the visuals worth a screenshot. Judgment stays here.

Inspect each captured suspect for the crowding, overlap, and truncation the DOM cannot expose. One probe run and a few targeted captures carry the whole loop, so reach for a wider sweep only when a capture shows something the probe missed. The probe recognizes an interactive visual only by a tree toggle or a scroll track, so a custom interaction carries its own status text through the spec's `interactive` field.

Judge these yourself:

- The output path and next numeric prefix are correct.
- Every visual carries its caller-supplied claim, in the caller's order, with the required relationship visible and the content inside its boundaries.
- Each custom component reuses the tokens, typography, and anatomy in `DESIGN-SYSTEM.md`.
- Every source line is present, every inference is labeled, and secrets are redacted.
