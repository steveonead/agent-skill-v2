---
name: artifact-visualizer
description: Turn supplied or caller-structured information into a disposable single-file HTML reference using a fixed visual component system. Use for grounded explanations of algorithms, code, diffs, call stacks, component or file structures, interfaces, states, sequences, flows, and UI layouts.
---

# Visual artifact

Create a temporary HTML reference whose visuals carry the explanation. Build every artifact with the template's fixed component system.

## Honor the caller's information architecture

Treat a caller-supplied structure as authoritative. Accept an ordered set of sections where each section names its component type, content, and source. A section may also specify explanation, interaction, and emphasis. Preserve the supplied order and component choices. Add only the labels and short connective copy needed to assemble a coherent document.

When a direct user request or an older caller omits that structure, identify the subject, audience, and single job of the document. Then derive the ordered sections and choose components from the fixed catalog. Start with the visual or conclusion that best performs the document's job.

Use a single-column main flow. Place side-by-side content only when direct comparison depends on alignment and both panes fit at their natural heights.

## Deliver one disposable HTML file

- Write to the caller-supplied path, or to `docs/ito-temp/artifacts/NNN-<slug>.html` by default.
- For the default path, scan numeric filename prefixes in that directory, increment the largest value, start at `001`, and format the slug as lowercase kebab-case. Continue naturally past `999`.
- Author explanation, navigation, controls, errors, and inference labels in the user's current language. Preserve quoted evidence, code, and diffs in their source language.
- Open the finished file in a browser. Try the file directly, then use a local static server when browser restrictions block modules, WebAssembly, or cross-origin requests.
- Treat the result as a network-dependent desktop document. Optimize for a 1440 by 900 viewport and the template's fixed document shell.

## Ground every component

Inspect the caller-named or directly relevant local sources needed to verify labels, values, paths, code, diffs, relationships, and states. Keep that inspection within the requested subject.

Inventory the material claims, relationships, sequences, states, code, and changes before building. Every material item must appear in a visual, appear in its adjacent explanation when the visual cannot carry it, or be omitted because another visual already communicates it.

Use real labels, paths, values, and examples. Place a short path, URL, or data name in each visual's source line. Label interpretations as inferences in the artifact's language, using plain wording such as `只是猜測` or `僅供參考` in Chinese. Redact credentials and secret-looking values from prose, diagrams, diffs, code, data blocks, and attributes.

## Select from the fixed component catalog

Use [`assets/template.html`](assets/template.html) as the implementation source for these components:

| Information shape | Component |
| --- | --- |
| Algorithm, branch, guard, or ordered decision logic | `ArtifactUI.createPseudocode` |
| Runtime frames and calls | `ArtifactUI.createTree` with the `call-stack` variant |
| UI ownership and component nesting | `ArtifactUI.createTree` with the `component-tree` variant |
| Repository or package layout | `ArtifactUI.createTree` with the `file-tree` variant |
| Types, function signatures, ownership, and responsibilities | `ArtifactUI.createSignatureList` |
| Source whose surrounding context matters | `ArtifactUI.renderCode` |
| Source changes and patches | `ArtifactUI.renderDiff` |
| State, sequence, or directional flow with meaningful graph topology | `ArtifactUI.renderDiagram` |
| UI structure and spatial relationships | The template's HTML mockup primitives |

Use the common nested-tree anatomy for all tree variants. Let each preset determine its kind label and metadata fields. Put structural change evidence in Pierre Diffs. Use trees and pseudocode to show one current structure.

Use Mermaid for state, sequence, and flow diagrams when graph topology carries the meaning. Keep each diagram at a readable natural scale inside the template's two-axis overflow viewport. Use the fixed HTML components for call stacks, component trees, file trees, pseudocode, signatures, source code, and UI layouts.

Each visual consists of a hierarchical number, short title, up to three explanatory sentences, source line, optional interaction-status label, and its component. Code-like components also use the template's caption bar for kind, name, language, path, or status metadata.

Default to static components. Enable tree collapse only when the caller asks for it or the hierarchy needs disclosure. Mermaid retains pan and overflow navigation. Add another vanilla JavaScript interaction only when the caller specifies a state, order, filter, or causal relationship that requires it. Mark every interactive visual with localized status text such as `Interactive` or `可互動`.

## Preserve the fixed design system

Start from the template and retain its document shell, hierarchical table of contents, component markup, CSS, `ArtifactUI` namespace, pinned dependencies, renderer helpers, typography, and Vitesse Light theme across the document, code, diffs, diagrams, and custom components.

The caller may explicitly remap only `--artifact-accent`, `--artifact-positive`, `--artifact-warning`, and `--artifact-negative` to the template's named Vitesse Light palette tokens. Keep the background, surfaces, text, borders, code panels, type, spacing, radii, and component anatomy fixed.

Use Noto Serif TC for Chinese prose and diagram labels. Use Maple Mono with a Noto Serif TC fallback for code, diffs, pseudocode, trees, signatures, and preformatted content. Keep rendered text at 16px or larger, diff line height at 28px, and prose and labels at `text-wrap: pretty`. Preserve code and diff whitespace. Use Shiki's `vitesse-light` theme and the template-owned light Pierre theme.

## Build safely from the template

Replace the template's document language, title, visible demo content, localized labels and messages, navigation and ARIA labels, and sample data with the artifact's real content. Remove unused `data-demo` sections, component instances, data blocks, and demo invocations. Retain the shared CSS, page shell, table-of-contents builder, `ArtifactUI` methods, and renderer infrastructure.

Embed dynamic component data in `script[type="application/json"]` blocks. Serialize JSON with `<`, `>`, `&`, U+2028, and U+2029 escaped for an HTML script context, then read it with `ArtifactUI.readData`. Insert source material through text-safe DOM APIs or renderer inputs. Treat renderer-produced markup as trusted only at the renderer boundary.

Keep the HTML self-contained apart from the pinned CDN requests. Run the file directly in the browser without a build or installation step.

Run Pierre Diffs on the main thread with focused excerpts. Keep code and diff excerpts below roughly 150 lines when a smaller grounded excerpt supports the same claim.

Keep renderer failures local. Replace only the failed mount point with the localized error component and leave the rest of the document usable.

## Verify the artifact

Check the written file before opening it:

- The output path and next numeric prefix are correct.
- Unused demo sections, sample data, demo invocations, controls, and placeholders are gone.
- Every component follows the template anatomy and supports a claim in scope.
- Every source line is present, every inference is labeled, and secrets are redacted.
- JSON data is safe for its script context, DOM insertion is text-safe, and executable contexts contain no untrusted strings.
- The sticky table of contents reflects the final section and visual hierarchy, numbering matches the headings, and every anchor resolves.
- Chinese text, monospace content, minimum sizes, diff line height, wrapping, and whitespace match the fixed typography.
- The main flow is single-column, and aligned comparisons leave vertical scrolling to the page.
- Mermaid diagrams retain natural scale, two-axis overflow, scrollbars, wheel or trackpad navigation, and grab-to-scroll behavior inside the fixed viewport bounds.
- Every interactive visual has nearby localized interaction-status text.

When browser capability is available, inspect the artifact at 1440 by 900. Confirm that the table of contents tracks the current section, anchors and tree disclosure work, every renderer completes or displays its local error state, the console contains no implementation errors, and no text, control, visual, diff, or code block overlaps or overflows incoherently. Capture a screenshot, inspect it, fix defects, and repeat the affected checks.

When browser capability is unavailable, perform the structural checks and report that visual rendering and interaction remain unverified. Finish by reporting the absolute file path, how it was opened, verification performed, and any renderer that displayed its error state.
