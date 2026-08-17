---
name: visual-artifact-v2
description: Transform agreed material into a single-file, network-backed visual HTML artifact by choosing the smallest useful components from a relationship-driven decision tree. Use when the user or another skill requests a visual explanation, an interactive HTML document, a visual specification, or a browser-readable explanation of technical material.
---

# Visual Artifact V2

Produce one browser-readable HTML file from material that is already available in the conversation or caller context.

## Step 1: Normalize the material

Read [`references/authoring-rules.md`](references/authoring-rules.md) in full. Build the internal render brief from the supplied material.

Finish when the brief has a title, summary, language, output path, ordered content inventory, and a status for every claim that is not verified.

## Step 2: Select components

Read [`references/components.md`](references/components.md) in full on every run. For each content item, follow this decision tree. A section may combine leaves when each component reveals a different relationship.

```text
What must the reader understand?
|
+-- Context, scope, or claim status
|   +-- One definition or constraint ................ Prose or note
|   +-- Verified, proposed, assumed, or unknown claim  Evidence note
|   +-- Included work versus excluded work ........... Goals and out of scope
|   +-- Optional supporting detail ................... Disclosure
|
+-- Exact values, mappings, or alternatives
|   +-- Repeated fields or exact mappings ............ Data table
|   +-- Exactly two versions or options .............. Comparison
|   +-- Options judged by shared criteria ............ Decision matrix
|   +-- One outcome varying along two axes ........... Rule matrix
|
+-- Progress, state, or quantity
|   +-- Ordered stages without branching ............. Timeline
|   +-- A few categorical conditions ................. Status summary
|   +-- Two to four important quantities ............. Metric summary
|   +-- Values changing across categories or time .... Mermaid xy chart
|
+-- Behavior or control flow
|   +-- Compact algorithm where code-like order matters  Pseudocode code block
|   +-- Branching decisions and outcomes ............... Mermaid flowchart
|   +-- Transitions between named states ............... Mermaid state diagram
|   +-- Messages exchanged by actors over time ........ Mermaid sequence diagram
|
+-- Structure or ownership
|   +-- Runtime callers and callees ................... Call-tree code block
|   +-- UI hierarchy, state, and module boundaries ... Component-tree code block
|   +-- File responsibility or broad refactor shape .. Shallow file-tree code block
|   +-- Types or entities connected by relationships . Mermaid class or ER diagram
|
+-- Source or change to an existing shape
|   +-- Exact before/after lines or an existing patch  Diff
|   +-- Conceptual before/after with no line delta .... Comparison
|   +-- Mostly new content, or omission hides ownership
|       or order, or the reader needs a copyable shape  Full code block
|
+-- Public behavior or interface
    +-- Observable behavior with acceptance criteria . User story
    |   +-- Transitions between named states .......... Add a Mermaid state diagram
    |   +-- One input judged by ordered conditions .... Add a Mermaid flowchart
    |   +-- Messages exchanged by actors over time ... Add a Mermaid sequence diagram
    |   +-- Outcome varies by state, role, or context . Add a rule matrix
    |   +-- Independent rules with no shared path ..... Keep the criteria grid alone
    +-- Endpoint or exported symbol contract ......... API and symbol ledger
    +-- Screens, navigation, or UI states ............. Wireframe
```

When several leaves fit, choose the smallest set that answers the current question. Keep only the necessary nodes, calls, files, props, states, boundaries, rows, and criteria. Do not add a visualization that restates adjacent prose.

The available components are:

- **Explain and qualify:** prose, evidence note, goals and out of scope, disclosure.
- **Compare and decide:** data table, comparison, decision matrix, rule matrix.
- **Orient and summarize:** timeline, status summary, metric summary, Mermaid xy chart.
- **Show behavior:** pseudocode, Mermaid flowchart, state diagram, sequence diagram.
- **Show structure:** call tree, component tree, shallow file tree, Mermaid class diagram, ER diagram.
- **Show source and change:** code block, Diff.
- **Specify product behavior:** user story, API and symbol ledger, wireframe.

Finish when every content item has a component or an explicit prose treatment, every selected component exists in the loaded catalog, and each visualization exposes a relationship that adjacent prose does not.

## Step 3: Resolve the output

Use a caller-supplied path when present. Otherwise write to `docs/artifacts/<date>-<slug>.html` under the project root, where the date comes from `date +%F` and the slug is lowercase English kebab-case. For a new artifact whose target exists, append `-2`, `-3`, and the next available integer. Modify an existing artifact only when the caller explicitly requests an update to that path.

Resolve the working path, the file that Steps 4 through 6 operate on. For a create, the working path is the target itself. For an update, the working path is a staging sibling in the same directory as the target, named `<name>.staging.html`, and the existing target stays untouched until Step 7 replaces it.

Finish when the absolute target path is known, its parent directory exists, the create target is new, and an update's staging path is resolved beside the target.

## Step 4: Compose the artifact

Copy [`assets/template.html`](assets/template.html) to the working path. Replace every `ARTIFACT:` placeholder and author sections with catalog markup.

Finish when all placeholders are replaced, title and summary text are nonempty, every brief item is expressed, and every added fact is supported or state-marked.

## Step 5: Validate the structure

```bash
python3 -B <skill-directory>/scripts/validate_artifact.py <working-path>
```

When the artifact contains both `<section id="overview">` and `<section id="open-items">`, also run the additional profile validator:

```bash
python3 -B <skill-directory>/scripts/validate_visual_spec.py <working-path>
```

Fix every reported error. When repeated fixes still fail validation, stop fixing: keep the working file and carry its path and the failure to Step 7.

Finish when every applicable validator exits zero, or when a validation failure is recorded for Step 7.

## Step 6: Verify in a browser

Open the working path in a desktop browser with network access so CDN modules can load. Wait for network idle. Inspect the full document and exercise every table-of-contents link, disclosure, wireframe screen control, and state control. Check browser errors and verify that every Mermaid diagram, Diff, and code block rendered. Confirm that each diagram container stays within `85dvh` and keeps its scrollbars hidden. Confirm that natural-size content can be drag-panned along each overflowing axis without clipping or shrinking. Confirm that code blocks are formatted and highlighted, Diff fallback content is hidden only after successful rendering, and text, diagrams, tables, and controls fit within their desktop containers.

Finish when the desktop artifact has clean browser diagnostics, visible renderer output, working table-of-contents, disclosure, wireframe, drag-scroll, and state controls, coherent layout, and fully visible content. Report browser verification as blocked when tooling is unavailable or a CDN module cannot load. A blocked Diff renderer must leave its static source fallback readable.

## Step 7: Deliver

For an update whose structural validation passed, replace the target now: move the staging file onto the target path with a same-directory rename. Structural validation alone gates the replacement. For an update whose structural validation failed, keep the original target untouched and report the staging path together with the validation failure.

Report the artifact path, one sentence per section, every `proposed`, `assumption`, and `unknown` item, the structural validation result, and the browser verification result.

Finish when the report accounts for every section and every non-verified claim in the reported file, and an update ends with either a replaced target or an untouched target plus a reported staging path.
