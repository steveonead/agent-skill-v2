# Visual design system

Build a new component from these tokens and structures so it reads as part of the same document as the catalog components. Read the rule here, then copy the closest existing component's markup and CSS as the starting point.

## Color tokens

Use the `--artifact-*` tokens. They already resolve to the Vitesse Light palette, so a new component inherits any accent remap the caller requested.

| Token | Use |
| --- | --- |
| `--artifact-bg` | Page ground behind every surface |
| `--artifact-surface` | Prose panels, table of contents, navigation |
| `--artifact-ink` | Body text on a surface |
| `--artifact-muted` | Labels, captions, secondary text on a surface |
| `--artifact-border` | Surface outlines and dividers |
| `--artifact-accent` | Numbering, kind labels, the current table-of-contents entry |
| `--artifact-positive` | Added, passing, or resolved state |
| `--artifact-warning` | Pending, degraded, or inferred state |
| `--artifact-negative` | Removed, failing, or error state |
| `--artifact-code` | Ground inside a code panel |
| `--artifact-code-raised` | Caption bars, group bands, and hierarchy inside a code panel |
| `--artifact-code-border` | Code panel outline and its internal dividers |
| `--artifact-code-ink` | Primary text inside a code panel |
| `--artifact-code-muted` | Labels, bullets, and annotations inside a code panel |

Reach for a raw `--vitesse-*` token when a semantic token carries the wrong meaning: use the syntax hues (`--vitesse-blue`, `--vitesse-cyan`, `--vitesse-function`, `--vitesse-orange`, `--vitesse-string`, `--vitesse-pink`, `--vitesse-yellow`) to tint a category label so it matches the code it describes. Keep each hue bound to one meaning across the document.

## Typography

All text is Maple Mono, with Maple Mono CN carrying CJK glyphs and browser-synthesized CJK bold. `--font-sans` and `--font-mono` both resolve to that stack. Keep using `--font-sans` for prose and `--font-mono` for declarations, paths, trees, and anything whose alignment carries meaning, so the roles stay legible and a future face change stays a token edit.

Body text is 16px at line height 1.625, and monospace content in a panel is 16px at 26px line height. A component title inside a panel may reach 17px to 18px, and heading weight tops out at 700. Give any element holding `white-space: pre` content its own `overflow-x: auto` so a long line scrolls inside the component instead of widening the page.

## Panel anatomy

A component that shows evidence lives in a `.code-panel`: a 6px radius, a one pixel `--artifact-code-border` outline, `--artifact-code` ground, and `overflow: hidden`. The visual's number, title, explanation, and source line belong to the `.visual-header` above it, outside the panel.

When the component carries metadata about the whole panel, open it with a `.code-caption` bar: 46px minimum height, `--artifact-code-raised` ground, a bottom border, `.panel-kind` in accent for the kind, `.caption-name` in ink for the name, and `.caption-meta` in muted at the right edge for language, path, or status.

Inside the panel, build depth with ground and spacing before reaching for another border. One nested outline inside an outlined panel reads as a doubled frame. Use `--artifact-code-raised` for a band or a rail that groups rows, `--artifact-code-border` for a divider that separates peers of the panel's own weight, and `--vitesse-border-soft` for a divider between rows within a group.

## Grouping and labels

When items share an owner, a file, or a phase, name that shared value once as a group heading rather than repeating it on every row. Give the heading a mono name and, when a one-sentence summary earns its place, set it in sans and muted on the same baseline. Let the heading disappear when the group has no shared value, and keep the rows aligned as if it were there.

Per-item metadata is a short label and value pair rendered under the item, with the label in a muted or tinted hue and the value in the panel's ink. Accept those pairs as caller-supplied `label` and `value` strings so the component carries no built-in vocabulary and needs no translation.

## Building the component

Mount the component into an empty host element addressed by id. Build its nodes with the `element` helper, which takes a tag, a class, and text, and reserve `innerHTML` for the output of a pinned renderer. Wrap the render in a try and catch so a failure calls `showRendererError` and replaces only that mount point.

Add the component's failure message to `rendererMessages` and any interface string it prints to `uiMessages`, both in the artifact's language.
