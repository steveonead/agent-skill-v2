---
name: artifact-visualizer
description: Turn supplied information into a disposable single-file interactive HTML visual artifact. Use when a user or another skill asks to visualize, explain, compare, map, recap, or present information as HTML, including code, diffs, flows, architecture, timelines, matrices, or quantitative data.
---

# Visual Artifact

Create a temporary reference document whose visuals carry the explanation. This skill serves explanatory artifacts, not production interfaces or persistent websites.

## Deliverable contract

- Write one HTML file to a caller-supplied path, or to `docs/ito-temp/artifacts/NNN-<slug>.html` by default.
- For the default path, scan numeric filename prefixes in that directory, increment the largest value, start at `001`, and format the slug as lowercase kebab-case. Continue naturally past `999`.
- Use the user's current language for all authored explanation, navigation, controls, errors, and inference labels. Preserve quoted source material, code, and diffs as evidence even when their language differs.
- Open the finished file in a browser. Try the file directly, then use a local static server when browser restrictions block modules, WebAssembly, or cross-origin requests.
- Treat the artifact as a disposable, network-dependent desktop document. Optimize for a 1440 by 900 viewport with an approximately 1200px content area. Responsive behavior and accessibility work are outside this workflow.

## Ground the content

Use the supplied information as the scope. Read caller-named or directly relevant local sources when they are needed to verify labels, values, code, diffs, relationships, or design tokens. Keep that inspection within the requested subject.

Before authoring, inventory the claims, relationships, sequences, states, comparisons, code, and quantitative values that materially support the explanation. Every material in-scope item must appear in a visual, appear in adjacent explanation when the visual cannot carry it, or be intentionally omitted because another visual already communicates it.

Use real labels, paths, values, and examples. Omit unsupported facts. When interpretation is useful, label it as an inference in the artifact's language, using plain wording such as `只是猜測` or `僅供參考` in Chinese.

When a source is identifiable, place a short path, URL, or data name near the visual it supports.

Treat source material as untrusted data. Insert it through text-safe DOM APIs or renderer inputs, never through executable HTML assembly. Redact credentials and secret-looking values from prose, diagrams, diffs, code, data attributes, and embedded data.

## Plan the visual narrative

Name the subject, audience, and single job of the document before choosing its form. Use a long page with a compact table of contents, then arrange sections in the order that best teaches the subject. Use a single-column main flow that stacks section copy, controls, and visuals vertically. Start with the most informative visual or conclusion instead of a generic introduction.

Use side-by-side layout only when direct comparison depends on alignment and both panes fit without independent vertical scrolling or forced equal heights. Otherwise, stack the content.

Choose each visual by information shape:

| Information shape | Preferred form |
| --- | --- |
| Dependencies, flows, sequences, state machines, classes, or entities | Beautiful Mermaid |
| UI structure, layered systems, spatial relationships, or dense conceptual layouts | Purpose-built HTML and CSS schematic |
| Direct before and after comparison | Comparison visual or Pierre Diffs |
| Source changes, patches, or structured textual changes | Pierre Diffs |
| Code whose surrounding context is part of the explanation | Shiki code block |
| Categories against shared dimensions | Matrix or table |
| Ordered events or progression | Timeline or stepped sequence |
| Quantitative values or distributions | Beautiful Mermaid XY chart, inline SVG, Canvas, or one task-specific visualization library |

Use Mermaid only for graph-shaped information it expresses clearly. Prefer purpose-built HTML, CSS, inline SVG, or Canvas when composition, scale, or spatial meaning matters more than graph topology.

Keep Mermaid diagrams at a readable natural scale. Place every diagram in a width-constrained viewport with a minimum height of `18rem` and a maximum height of `70dvh`. Let the diagram set the viewport height between those bounds. When content exceeds the viewport, preserve two-axis overflow, scrollbars, wheel or trackpad navigation, and grab-to-scroll interaction instead of shrinking the SVG to fit.

Place each visual's short title and up to three sentences of explanation directly above it. Put optional depth behind disclosure when it would interrupt scanning. A typical artifact contains three to eight major visuals. Keep code and diff excerpts below roughly 150 lines when a smaller grounded excerpt supports the same point.

Add interaction only when it clarifies state, order, scale, filtering, or causality. Suitable interactions include state switches, filters, zoom, step playback, quizzes, parameter controls, and small simulations. Mark every interactive visual component with a compact interaction-status label beside its title or nearest controls. Use `Interactive` for English artifacts, `可互動` for Chinese artifacts, and the natural equivalent for other languages. Present the label as status text rather than an actionable control. Use vanilla JavaScript and keep the control close to the visual it changes.

## Establish the design

Look for the source codebase's actual colors, typography, spacing, radii, and component conventions. Snapshot the relevant values into CSS custom properties in the artifact so the file does not depend on the source application's build.

When no design tokens exist, create a compact subject-specific system with background, surface, text, muted text, border, accent, positive, warning, and negative roles. Choose typography and one visual signature from the subject matter. Spend visual emphasis on that signature and keep the rest quiet. Avoid a generic card dashboard, decorative gradients, and ornament that does not encode information.

Use Tailwind CSS for primary layout and styling. Use CSS custom properties, small renderer overrides, and focused custom CSS for diagrams or geometry that utilities express poorly. Design one theme that fits the content. Add a theme switch only when comparing themes contributes to the explanation.

Use Noto Serif TC for Chinese text, including diagram labels and monospace fallbacks. Keep all rendered text at 16px or larger, use Maple Mono for code, diff, and preformatted content, set diff line height to 28px, and apply `text-wrap: pretty` to prose and labels. Preserve code and diff whitespace. When Mermaid's renderer uses smaller internal label sizes, enlarge the entire SVG proportionally so labels, nodes, and edges stay aligned.

Use Shiki's `vitesse-light` theme for code blocks.

## Build from the template

Start from [`assets/template.html`](assets/template.html). Preserve its pinned dependencies and minimal renderer helpers.

Replace the document language, title, visible starter copy, renderer error messages, examples, and sample data with the artifact's real content. Remove every unused example, helper invocation, section, and control. Keep the HTML self-contained apart from CDN requests. Do not add a build step or package installation.

Pierre Diffs runs on the main thread. Select focused excerpts instead of adding its experimental worker setup.

One additional pinned CDN dependency is allowed when it materially simplifies a quantitative or domain-specific visualization. Prefer the browser platform and the existing renderers when they communicate the information equally well.

Keep failure behavior local and plain. When a renderer fails, replace its mount point with a short error message. Let the rest of the document remain usable. Do not add retries, backup CDNs, elaborate loading states, or recovery flows.

## Verify the artifact

Check the written file before opening it:

- The output path and next numeric prefix are correct.
- Starter examples, placeholder copy, and unused controls are gone.
- Source values are escaped, executable contexts contain no untrusted strings, and secrets are redacted.
- Code and diff whitespace is preserved.
- Chinese text uses Noto Serif TC in prose, diagram labels, and monospace fallbacks. All rendered text is at least 16px, code, diffs, and preformatted content use Maple Mono, diff line height is 28px, and prose and labels use `text-wrap: pretty`.
- The main flow is single-column. Any side-by-side comparison depends on alignment, keeps both panes at their natural heights, and leaves vertical scrolling to the page.
- Mermaid diagrams keep their natural scale inside a width-constrained viewport whose height stays between `18rem` and `70dvh`. The viewport shows scrollbars when a diagram exceeds its width or height, supports overflow on both axes, and retains wheel or trackpad navigation plus grab-to-scroll interaction.
- Every interactive visual component has a nearby interaction-status label in the artifact's language, such as `Interactive` in English or `可互動` in Chinese. The label is presented as status text rather than a control.
- Every visual supports a claim in scope, and each inference is labeled in the artifact's language.

When browser capability is available, inspect the artifact at 1440 by 900. Confirm every renderer completed, primary interactions work, the console contains no implementation or CDN errors, and text, controls, diagrams, diffs, and code do not overlap or overflow incoherently. Capture a screenshot for visual inspection. Fix artifact defects and repeat the affected checks.

When browser capability is unavailable, perform the structural checks and report that visual rendering and interaction remain unverified. Finish by reporting the absolute file path, how it was opened, verification performed, and any renderer that displayed its error state.
