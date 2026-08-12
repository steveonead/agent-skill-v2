---
name: ito-visual-spec
description: Generate a single-file visual HTML spec with feature explanation, user stories, API interface, and interactive wireframe sections.
argument-hint: "要幫哪個 feature 產 spec？可以附 GitHub issue 編號或連結當輸入來源。"
disable-model-invocation: true
---

# Visual HTML Spec

Produce one single-file HTML spec the team reviews in a browser. Skip this workflow for a change one paragraph can describe.

## Step 1: Collect and verify the material

When the invocation arguments name a GitHub issue, read it with `gh issue view <number> --comments`.

Ground every technical claim in the codebase: trace each file path, symbol, endpoint, and data structure the spec will mention to its definition, and read enough surrounding code to state its real shape. Mark anything that extends beyond the current code as proposed.

Finish when every identifier the spec will name is traced to a real definition or marked as proposed.

## Step 2: Load the component catalog

Read [`references/components.md`](references/components.md) in full. Copy each block from a catalog snippet and adapt its content.

Finish when the catalog has been read in full.

## Step 3: Create the spec file

Copy [`assets/template.html`](assets/template.html) to `docs/specs/<date>-<feature-slug>.html` in the project root, where `<date>` comes from `date +%F` and the slug is lowercase hyphenated English.

Finish when the copy exists at the target path.

## Step 4: Fill the sections

Write prose in Traditional Chinese (zh-TW). Keep code, identifiers, and API names in English.

Replace every `<!-- SPEC:... -->` placeholder:

- **Feature**: what the feature does and why, goals and out of scope, and the main flow as a mermaid diagram.
- **User Stories**: one story per behavior a user can observe, each carrying its role statement, a `flowchart TD` whose edges are its acceptance criteria, and the text version of those criteria. When the feature changes nothing a user can observe, delete this section together with its table-of-contents link.
- **API Interface**: one ledger row per endpoint and one per public function or type. Use whichever kinds the feature actually has.
- **Wireframe**: screens, navigation, and per-screen states, expressed only through the catalog's `data-` attributes.

Finish when no `SPEC:` placeholder remains, every `data-goto` value matches a `data-screen` in the same flow, every screen is reachable from the start screen, every mermaid block follows the catalog's syntax rules, every acceptance criterion appears as one edge whose label begins with its `AC-NN` id, every endpoint row that takes parameters carries an `<h4>Parameters</h4>` and a parameter table with one row per parameter, and every endpoint row that returns a body carries an `<h4>Response NNN</h4>` and a `data-lang` code block for each status code it returns with a body.

## Step 5: Deliver

Finish when the delivered report states the file path, a one-line summary per section, and every item the spec marks as proposed.
