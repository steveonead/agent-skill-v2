---
name: artifact-visualizer
description: Render supplied or caller-structured information into a disposable single-file HTML reference built on a shared visual component gallery. Use for grounded explanations of algorithms, code, diffs, pull requests, plans, specs, call stacks, file or component structures, interfaces, states, sequences, flows, metrics, and UI layouts, and as the renderer other visualization skills call.
---

# Visual artifact

Render the caller's information as one disposable HTML file whose visuals carry the explanation. You own the design: choose the components, order, and layout that explain the material best.

## Caller input

A caller may hand over ordered sections, each carrying content, a source, and an optional component hint. Treat sections as material and intent: keep the content and its grounding, respect the ordering intent, and follow a hint unless another component explains that content better. When no structure is supplied, derive the sections yourself from the subject, audience, and the document's single job.

## Output contract

- Write to the caller-supplied path, or to `docs/ito-temp/artifacts/NNN-<slug>.html` by default: increment the largest numeric prefix in that directory, start at `001`, lowercase kebab-case slug.
- Ground every visual: inspect the relevant local sources, use real labels, paths, and values, give each visual a source line, and label interpretations as inferences in the artifact's language. Redact credentials and secret-looking values everywhere.
- Author prose, labels, controls, and messages in the user's current language. Keep quoted evidence, code, and diffs in their source language.
- Open the finished file in a browser. Fall back to a local static server when browser restrictions block modules or cross-origin requests.

## Route information to components

Start from `assets/template.html` and its `ArtifactUI` catalog. This table is guidance, not law: pick whatever explains the shape best.

| Information shape | Component |
| --- | --- |
| Algorithm, branch, or ordered decision logic | `createPseudocode` |
| Runtime frames and calls | `createTree` (`call-stack`) |
| UI ownership and component nesting | `createTree` (`component-tree`) |
| Repository or package layout | `createTree` (`file-tree`) |
| Types, signatures, and responsibilities | `createSignatureList` |
| Source whose surrounding context matters | `renderCode` |
| Source changes and patches | `renderDiff` |
| Per-file change overview | `createFileChangeList` |
| Change, run, or review metrics | `createStatCards` |
| Tasks, acceptance criteria, or findings with status | `createChecklist` |
| Risk, decision, or caveat that needs attention | `createCallout` |
| State, sequence, or flow with graph topology | `renderDiagram` |
| UI structure and spatial relationships | Mockup primitives |

For a shape with no good fit, such as a timeline or a comparison matrix, design your own component from the tokens and anatomy in [`references/DESIGN-SYSTEM.md`](references/DESIGN-SYSTEM.md).

Before building, read [`references/GALLERY.md`](references/GALLERY.md) in full: component APIs and examples, document design rules, construction safety, and the detailed verification checklist.

## Verify

- Confirm every renderer completes or shows its localized error state.
- With browser capability, inspect at 1440 by 900, capture a screenshot, and fix overlaps, overflow, and console errors. Without it, report that visual rendering is unverified.
- Confirm source lines, inference labels, and secret redaction survived into the final file.

Finish by reporting the absolute file path, how it was opened, and the verification performed.
