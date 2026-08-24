---
name: artifact-visualizer
description: Render an ordered list of visual claims into one disposable single-file HTML reference built on a shared component gallery. Use as the renderer that diff, pull request, plan, spec, and explanation skills call, and when a request asks to see code, algorithms, changes, structures, interfaces, states, sequences, flows, metrics, or UI layouts as a browsable page.
---

# Visual artifact renderer

The caller owns what the reader must learn. This skill owns the picture.

## Caller contract

The caller supplies:

- `audience` and `language`, which set the level and wording of prose and labels.
- An ordered list of visuals, each carrying:
  - `claim`: the one sentence the reader must be able to restate after seeing the visual.
  - `source`: `path:line`, or the command whose output is the evidence.
  - `relationship`: what must be visibly related, such as before against after, order, two axes crossed, containment, cause and gate, or status per item.
  - `content`: the concrete labels, values, nodes, and rows the visual must carry.
  - `boundaries`: what stays out, such as raw diff text or a node ceiling.
  - An optional component suggestion, which is guidance rather than a constraint.
- Optional document-level items: `title`, a short `lead` paragraph, section grouping, output path, and a closing link.

This skill owns component choice, layout, emphasis, interaction, and verification. Render each claim once, in the given order, with its required relationship visible and its content inside its boundaries. When a claim resists faithful rendering inside its boundaries, leave the claim intact and name it and the reason in the report.

Report the absolute file path, how the file was opened, the verification performed, and every claim that stayed unrendered.

When someone invokes this skill with raw information and no visual list, derive the list in the shape above first, then continue through the same contract.

## Principles

- The smallest view that makes the claim clear beats the complete one.
- One claim per visual, with one short paragraph beside it that carries what the visual cannot express.
- An edge that connects two things teaches more than a box that holds them.
- One component is often enough, several is common, all of them is unlikely.

## Component judgment

| Component | Use when | Prefer something else when |
| --- | --- | --- |
| `renderDiagram` | Order, branching, or state transition is the claim, the shape holds roughly 3 to 7 nodes, and each node label is a behavior in the reader's words. | A node would hold SQL, a call expression, or a line of source. A step-by-step transcript of code belongs in `createPseudocode`. |
| `createPseudocode` | Decision logic, guards, and ordered steps read better free of implementation noise. | The exact syntax is the evidence, which `renderCode` shows. |
| `createTree` | Nesting and ownership carry the claim: runtime frames as `call-stack`, UI ownership as `component-tree`, repository layout as `file-tree`. | Edges cross the hierarchy or run backward, which `renderDiagram` shows. |
| `createSignatureList` | Types, signatures, and responsibilities grouped by their owner are the claim. | A function body is the evidence. |
| `renderCode` | The surrounding source context is itself the evidence. | The claim is about logic or shape rather than syntax. |
| `renderDiff` | The patch text is the evidence, at the smallest span that proves the claim. | The claim is one added condition inside a long function. A signature list, pseudocode, or a before and after pair carries it with far less reading. |
| `createFileChangeList` | The files themselves are the subject, such as where one change landed across a package. | The list opens the document as an inventory. A few stat cards or a short grouped list gives that overview. |
| `createStatCards` | A few headline numbers answer the claim on their own. | Each number needs a status, a note, or a second axis. |
| `createChecklist` | Tasks, acceptance criteria, or findings each carry a status. | The status depends on two axes, which `createMatrix` crosses. |
| `createMatrix` | Both axes already mean something to the reader, and the answer lives in the cell. | The reader meets either axis for the first time here, or a second matrix appears, which usually means the real subject is a process or a topology. |
| `createCallout` | One risk, decision, or caveat needs attention beside a visual, at most one per visual. | A second callout would join it in the same section. Fold the rest into prose or a checklist. |
| Mockup primitives | Spatial layout and on-screen relationships are the claim. | Ownership or nesting is the claim, which `createTree` shows. |

Design a custom component when no catalog entry expresses the claim's relationship, or when a custom one materially reduces reader effort. Read [`references/DESIGN-SYSTEM.md`](references/DESIGN-SYSTEM.md) in full first, and build from its tokens, typography, and panel anatomy.

## Build the artifact

Write a JSON spec, then run `node assets/build.mjs <spec.json> <out.html>`. The header of [`assets/build.mjs`](assets/build.mjs) documents the spec schema, and [`references/GALLERY.md`](references/GALLERY.md) holds what each component's `data` must contain, plus the document design and construction rules. The builder owns the template, the hosts, and the escaping.

- Write to the caller's output path, which may name a file or a directory, and default to `docs/ito-temp/artifacts/`. Inside a directory, name the file `NNN-<slug>.html`, with `NNN` one past the largest numeric prefix already there, starting at `001`, and a lowercase kebab-case slug.
- Map each caller visual to one spec visual: its `source` goes on the source line, and its `copy` is the short paragraph beside the visual. A caller risk worth a callout goes in that visual's `callout` field.
- Reach for the `html` component together with the spec's `css` and `js` fields when a custom component carries the claim, after reading `references/DESIGN-SYSTEM.md` in full.
- Ground every visual in local sources. Give each visual its source line, and mark an interpretation as an inference in the artifact's language.
- Redact credentials and secret-looking values everywhere.
- Write prose, labels, controls, and messages in the caller's language. Keep quoted evidence, code, and diffs in their source language.
- Open the finished file in a browser. Fall back to a local static server when browser restrictions block modules or cross-origin requests.

## Verify the rendering

Run `node assets/check.mjs <out.html>` once. It sets the viewport to 1440 by 900, opens the file, waits for the CDN renderers to settle, evaluates [`assets/verify.js`](assets/verify.js), and prints the probe JSON. Fix every problem it names, then rerun it once.

Screenshot only the visuals the probe lists under `suspects`, with `agent-browser screenshot --full <png>`, and look at each capture. Before capturing a scrolled position, set `document.documentElement.style.scrollBehavior = 'auto'` and call `scrollTo(0, y)` with the `y` the probe reports for that visual. Judge the rest against the list under Verification in [`references/GALLERY.md`](references/GALLERY.md).

When `agent-browser` is missing, `check.mjs` prints the commands instead, and the report states that rendering is unverified.
