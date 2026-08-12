---
name: visual-artifact
description: Transform agreed material into a self-contained visual HTML artifact with structured explanations, diagrams, code, and presentation interactions. Use when the user or another skill requests a visual explanation, an interactive single-file HTML document, a visual specification, or a browser-readable explanation of technical material.
---

# Visual Artifact

Produce one browser-readable HTML file from material that is already available in the conversation or caller context.

## Step 1: Normalize the material

Read [`references/authoring-rules.md`](references/authoring-rules.md) in full. Build the internal render brief from the supplied material.

Finish when the brief has a title, summary, language, output path, ordered content inventory, and a status for every claim that is not verified.

## Step 2: Select the visual vocabulary

Read [`references/core-components.md`](references/core-components.md) in full on every run. Read [`references/spec-components.md`](references/spec-components.md) in full when the material includes user stories, acceptance criteria, public interfaces, or wireframes.

Map each meaningful relationship to the smallest component that makes it easier to understand.

Finish when every content item has one component or an explicit prose treatment, every selected component exists in the applicable loaded catalog, and each visualization exposes a relationship not already conveyed by adjacent prose.

## Step 3: Resolve the output

Use a caller-supplied path when present. Otherwise write to `docs/artifacts/<date>-<slug>.html` under the project root, where the date comes from `date +%F` and the slug is lowercase English kebab-case. For a new artifact whose target exists, append `-2`, `-3`, and the next available integer. Modify an existing artifact only when the caller explicitly requests an update to that path.

Finish when the absolute target path is known, its parent directory exists, and the create target is new.

## Step 4: Compose the artifact

Copy [`assets/template.html`](assets/template.html) to the resolved target. Replace every `ARTIFACT:` placeholder and author sections with catalog markup.

Finish when all placeholders are replaced, title and summary text are nonempty, every brief item is expressed, and every added fact is supported or state-marked.

## Step 5: Validate the structure

```bash
python3 <skill-directory>/scripts/validate_artifact.py <artifact-path>
```

Fix every reported error.

Finish when the validator exits zero.

## Step 6: Verify in a browser

Open the artifact in a desktop browser with network access so CDN modules can load. Wait for network idle. Inspect the full document and exercise every table-of-contents link, disclosure, wireframe screen control, and state control. Check browser errors and verify that every Mermaid diagram and code block rendered. Confirm that each diagram container stays within `85dvh` and keeps its scrollbars hidden. Confirm that natural-size content can be drag-panned along each overflowing axis without clipping or shrinking. Confirm that code blocks are formatted and highlighted, then confirm that text, diagrams, tables, and controls fit within their desktop containers.

Finish when the desktop artifact has clean browser diagnostics, visible renderer output, working table-of-contents, disclosure, wireframe, drag-scroll, and state controls, coherent layout, and fully visible content. Report browser verification as blocked when tooling is unavailable.

## Step 7: Deliver

Report the artifact path, one sentence per section, every `proposed`, `assumption`, and `unknown` item, the structural validation result, and the browser verification result.

Finish when the report accounts for every section and every non-verified claim in the delivered artifact.
