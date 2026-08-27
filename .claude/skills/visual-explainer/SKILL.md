---
name: visual-explainer
description: Create a disposable HTML visual explainer when the user or another workflow asks to visualize technical or structured information such as a diff, PR, spec, plan, architecture, or process.
---

# Visual explainer

Explain the subject to someone new to it with literal visual structure and concise prose.

Work from context supplied by the requester or an upstream workflow, without requiring a handoff schema or visual brief. The context supplier owns research, source interpretation, and substantive claims. This skill owns the visual narrative, information density, component choices, prose editing, HTML production, and verification. It may clarify and rearrange supplied content, but it must preserve the meaning, evidence status, and conclusions of substantive claims.

Honor any supplied reading target and main-path or appendix boundary. Use them to control density and disclosure, not to omit a central relationship or alter a substantive claim.

## Compose the explanation

Start with the one idea the reader must retain. Show the overall mental model before details, then reveal one primary idea per section. Prefer literal structure over decoration. Use a metaphor only when one metaphor can clarify the whole explanation without hiding important mechanics.

Before drafting, inventory the central relationships the reader must see. Consider comparison, sequence, state, hierarchy, dependency, quantity, evidence, impact, and uncertainty. Give the opening mental model and each behavior-changing core mechanism a relationship-bearing view when time, causality, or structure carries the meaning. Record a reason when prose is more precise for a central relationship.

A relationship-bearing view uses position, connection, alignment, size, or state styling to encode meaning. A border, card, badge, metric strip, ordinary table, or boxed paragraph does not become a visualization merely by containing prose. A visual should replace prose it makes redundant. Its caption should tell the reader what to notice rather than restate the content.

Choose components in two passes. First select a pattern by the relationship the reader must understand, not by the source label. A PR and a spec may both need a flow, comparison, hierarchy, or uncertainty view. Then select the presentation by the reader's task, content density, known renderer limits, and available width. Apply capacity limits before drafting. Changing orientation or renderer does not change the pattern.

Use [references/components.md](references/components.md) to apply the presentation pass, select established patterns and their variants, decide when a custom component is justified, and compose common diff, PR, spec, and plan explainers.

Follow [references/design-system.md](references/design-system.md) for every artifact.

## Preserve meaning

Keep facts, inferences, and unknowns distinct when the source does, and never present an inference as confirmed. Omit peripheral gaps or label them as unknown. Stop for clarification only when the central conclusion cannot be supported from the available context.

Edit wording for clarity without dropping the reason a change, rule, or risk matters. Keep one idea per text block, but allow several short sentences or paragraphs when they read better than one dense sentence. Let text wrap naturally. Use an explicit line break only when the break communicates structure.

When rearranging existing content, preserve substantive factual claims, numbers, nearby citations, and conclusions. Sentence and paragraph breaks may change without changing their meaning. Update headings, introductions, counts, and references such as `the first two items` whenever moved content makes them stale.

Use code and diagrams as evidence, not decoration. When exact syntax proves a breaking contract, counter-intuitive control flow, shared invariant, or concurrency behavior, include the smallest focused code or diff excerpt that proves the claim. Escape all source text before inserting it into HTML.

## Produce the artifact

Start from [assets/template.html](assets/template.html). Replace its language, title, placeholder content, and any starter component whose encoded relationship does not match the relationship inventory. Use the requested language, or the source or conversation language when none is specified. Create one HTML file with a light page palette. Keep custom CSS and JavaScript inline. Load only the libraries and font pinned in the template, following the boundaries in [references/libraries.md](references/libraries.md).

Use a supplied destination when present. Otherwise write to a writable temporary directory and return the exact path. Treat every artifact as disposable. The main explanation must remain understandable without interaction. If a library fails, leave readable HTML or escaped source in its place instead of a blank region.

## Verify the artifact

Run [scripts/validate_artifact.py](scripts/validate_artifact.py) on the completed HTML. When Python is unavailable, check the same static properties directly: a concrete document language, replaced starter content, font sizes that use `--fs-*` tokens of at least 16px, no inline font declarations, and visible readable fallbacks for each optional diagram or code renderer.

When a rendering capability is available, render at a 1440 x 900 baseline viewport and capture one full-page screenshot to an absolute path in a dedicated writable temporary directory. Check the console and external requests, including that each optional-library request has a corresponding render target. When rendering is unavailable, complete the static and semantic checks and report that rendering was not verified.

Perform one semantic scan of the whole page. The opening silhouette must reveal the mental model before its labels are read. Each central relationship must have a relationship-bearing view or a recorded prose rationale. Consecutive core sections made only of boxed prose fail this check. Confirm that visuals replace redundant prose and that supporting detail remains subordinate to the main path.

Spend at most one fix pass per verification cycle on failed static checks, a blank page, failed dependency without readable fallback, missing relationship view, overlapping text, or clipped primary content. Repeat the full verification after a material content correction. Report any blocking defect that remains after the correction pass. Remove verification files before finishing unless the requester asks to keep them.
