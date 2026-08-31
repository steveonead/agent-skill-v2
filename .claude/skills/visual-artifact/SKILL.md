---
name: visual-artifact
description: Transform agreed material into a single-file, network-backed visual HTML artifact with structured explanations, diagrams, code, and presentation interactions. Use when the user or another skill requests a visual explanation, an interactive single-file HTML document, a visual specification, or a browser-readable explanation of technical material.
user-invocable: false
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

Resolve the working path, the file that Steps 4 through 6 operate on. For a create, the working path is the target itself. For an update, the working path is a staging sibling in the same directory as the target, named `<name>.staging.html`, and the existing target stays untouched until Step 7 replaces it.

Finish when the absolute target path is known, its parent directory exists, the create target is new, and an update's staging path is resolved beside the target.

## Step 4: Compose the artifact

Copy [`assets/template.html`](assets/template.html) to the working path. Replace every `ARTIFACT:` placeholder and author sections with catalog markup.

Finish when all placeholders are replaced, title and summary text are nonempty, every brief item is expressed, and every added fact is supported or state-marked.

## Step 5: Validate the structure

```bash
python3 <skill-directory>/scripts/validate_artifact.py <working-path>
```

When the material includes the spec skeleton's `overview` and `open-items` sections, also run the spec validator:

```bash
python3 <skill-directory>/scripts/validate_visual_spec.py <working-path>
```

Fix every reported error. When repeated fixes still fail validation, stop fixing: keep the working file and carry its path and the failure to Step 7.

Finish when every applicable validator exits zero, or when a validation failure is recorded for Step 7.

## Step 6: Verify in a browser

Open the working path in a desktop browser with network access so CDN modules can load. Wait for network idle. Inspect the full document and exercise every table-of-contents link, disclosure, wireframe screen control, and state control. Check browser errors and verify that every Mermaid diagram and code block rendered. Confirm that each diagram container stays within `85dvh` and keeps its scrollbars hidden. Confirm that natural-size content can be drag-panned along each overflowing axis without clipping or shrinking. Confirm that code blocks are formatted and highlighted, then confirm that text, diagrams, tables, and controls fit within their desktop containers.

Finish when the desktop artifact has clean browser diagnostics, visible renderer output, working table-of-contents, disclosure, wireframe, drag-scroll, and state controls, coherent layout, and fully visible content, or when browser verification is reported as blocked with its reason. Report browser verification as blocked when tooling is unavailable or CDN modules cannot load (network, CDN outage, or CSP).

## Step 7: Deliver

For an update whose structural validation passed, replace the target now: move the staging file onto the target path with a same-directory rename. Structural validation alone gates the replacement. For an update whose structural validation failed, keep the original target untouched and report the staging path together with the validation failure.

Report the artifact path, one sentence per section, every `proposed`, `assumption`, and `unknown` item, the structural validation result, and the browser verification result.

Finish when the report accounts for every section and every non-verified claim in the reported file, and an update ends with either a replaced target or an untouched target plus a reported staging path.
